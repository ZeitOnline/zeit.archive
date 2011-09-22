# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import datetime
import grokcore.component
import zeit.cms.interfaces
import zeit.cms.repository.folder
import zeit.cms.workflow.interfaces
import zeit.cms.workflow.interfaces
import zeit.content.cp.blocks.cpextra
import zeit.content.cp.centerpage
import zeit.edit.interfaces
import zope.component
import zope.i18n.locales


german = zope.i18n.locales.locales.getLocale('de', 'DE')
MONTH_NAMES = german.dates.calendars[u'gregorian'].getMonthNames()
del german


def create_cpextra(where, what):
    factory = zope.component.getAdapter(
        where, zeit.edit.interfaces.IElementFactory, name='cpextra')
    block = factory()
    block.cpextra = what


@grokcore.component.subscribe(
    zeit.cms.interfaces.ICMSContent,
    zeit.cms.workflow.interfaces.IBeforePublishEvent)
def create_breadcrumb_index_on_publish(context, event):
    metadata = zeit.cms.content.interfaces.ICommonMetadata(context, None)
    if metadata is None or context.__name__ == 'index':
        # Ignore index as a rough measure to ignore the publishing of the
        # breadcrumb index itself.
        return
    month_container = context.__parent__
    try:
        month = datetime.datetime.strptime(
            month_container.__name__, '%Y-%m').month
    except ValueError:
        # Not a month container
        return
    ressort_month_container = None
    if metadata.sub_ressort:
        # The following parent/parent even works, when the month container is a
        # child of the repository. ressort_contain will be the ZODB root then.
        ressort_container = month_container.__parent__.__parent__
        if zeit.cms.interfaces.ICMSContent.providedBy(ressort_container):
            # Be extra sure we're still in the repository
            try:
                ressort_month_container = ressort_container[
                    month_container.__name__]
            except KeyError:
                # Doesn't exist. Create it
                ressort_container[month_container.__name__] = (
                    zeit.cms.repository.folder.Folder())
                ressort_month_container = ressort_container[
                    month_container.__name__]
        sub_ressort_container = month_container.__parent__
        sub_ressort_month_container = month_container
    else:
        ressort_container = month_container.__parent__
        ressort_month_container = month_container
        sub_ressort_container = None
        sub_ressort_month_container = None
    if (metadata.ressort and
        metadata.ressort.lower() == ressort_container.__name__):
        create_breadcrumb_index(
            ressort_month_container, month, metadata, set_sub_ressort=False)
    if (sub_ressort_month_container is not None and
        metadata.sub_ressort and
        metadata.sub_ressort.lower() == sub_ressort_container.__name__):
        create_breadcrumb_index(
            sub_ressort_month_container, month, metadata, set_sub_ressort=True)


def create_breadcrumb_index(
    month_container, month, metadata, set_sub_ressort=True):
    index = month_container.get('index')
    if index is not None:
        index = month_container['index']
        # There is an index; but it might not be published! (#9252)
        info = zeit.cms.workflow.interfaces.IPublishInfo(index, None)
        if info and info.published:
            # All right, we're done.
            return
        # Either it's the wrong type or it is not published. Delete and
        # re-create the index
        del month_container['index']
    index = zeit.content.cp.centerpage.CenterPage()
    create_cpextra(index['lead'], 'solr-month')
    create_cpextra(index['informatives'], 'dpa-news')
    create_cpextra(index['informatives'], 'dwds-ticker')
    create_cpextra(index['informatives'], 'blindblock')
    # Adding to container implicitly creates mostread and mostcommmented

    index.ressort = metadata.ressort
    if set_sub_ressort:
        index.sub_ressort = metadata.sub_ressort
        ressort_name = metadata.sub_ressort or metadata.ressort
    else:
        ressort_name = metadata.ressort
    index.year = metadata.year
    month_name = MONTH_NAMES[month-1]

    index.title = index.teaserTitle = (
        u'Artikel und Nachrichten im %s %s aus dem Ressort %s | ZEIT ONLINE' %(
        month_name, index.year, ressort_name))
    index.teaserText = (
        u'Lesen Sie alle Artikel und Nachrichten vom %s %s'
        u' aus dem Ressort %s auf ZEIT ONLINE' % (
        month_name, index.year, ressort_name))

    month_container['index'] = index

    publish = zeit.cms.workflow.interfaces.IPublish(month_container['index'])
    publish.publish()

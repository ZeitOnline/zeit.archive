# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import zeit.cms.repository.folder
import datetime
import grokcore.component
import zeit.cms.interfaces
import zeit.cms.workflow.interfaces
import zeit.cms.workflow.interfaces
import zeit.content.cp.blocks.cpextra
import zeit.content.cp.centerpage
import zeit.content.cp.interfaces
import zope.component
import zope.i18n.locales


german = zope.i18n.locales.locales.getLocale('de', 'DE')
MONTH_NAMES = german.dates.calendars[u'gregorian'].getMonthNames()
del german


def create_block(where, what):
    factory = zope.component.getAdapter(
        where, zeit.content.cp.interfaces.IElementFactory, name=what)
    return factory()


@grokcore.component.subscribe(
    zeit.cms.interfaces.ICMSContent,
    zeit.cms.workflow.interfaces.IBeforePublishEvent)
def create_breadcrumb_index_on_publish(context, event):
    metadata = zeit.cms.content.interfaces.ICommonMetadata(context, None)
    if metadata is None:
        return
    month_container = context.__parent__
    ressort_month_container = None
    if metadata.sub_ressort:
        try:
            ressort_container = month_container.__parent__.__parent__
        except AttribueError:
            pass
        else:
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
    create_breadcrumb_index(month_container, metadata)
    if ressort_month_container is not None:
        create_breadcrumb_index(
            ressort_month_container, metadata, set_sub_ressort=False)

def create_breadcrumb_index(
    month_container, metadata, set_sub_ressort=True):
    if 'index' in month_container:
        return
    try:
        month = datetime.datetime.strptime(
            month_container.__name__, '%Y-%m').month
    except ValueError:
        # Not a month container
        return

    index = zeit.content.cp.centerpage.CenterPage()
    create_block(index['lead'], 'solr-month')
    create_block(index['informatives'], 'dpa-news')
    create_block(index['informatives'], 'dwds-ticker')
    create_block(index['informatives'], 'blindblock')
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

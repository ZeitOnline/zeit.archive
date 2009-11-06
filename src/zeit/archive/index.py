from __future__ import with_statement
import zeit.archive.interfaces
import zeit.cms.checkout.interfaces
import zeit.cms.repository.interfaces
import zeit.content.article.interfaces
import zeit.workflow
import zope.component
import zope.interface



def rebuildVolume(id):
    valid_status = ['OK', 'imported', 'importedVHB']
    index_year = zeit.content.cp.centerpage.CenterPage()
    index_year.type = u'archive-print-year'
    start_container = zeit.cms.interfaces.ICMSContent(id)
    stack = [start_container]
    while stack:
        content = stack.pop(0)
        if zeit.cms.repository.interfaces.ICollection.providedBy(content):
            stack.extend(content.values())
            if 'index' in content:
                del content['index']
            if content.__parent__.__name__ == 'repository':
                index_year.year = content.__name__
                year_coll = content
                continue
            index_volume = zeit.content.cp.centerpage.CenterPage()
            index_volume.type = u'archive-print-volume'
            index_volume.year = content.__parent__.__name__
            index_volume.volume = content.__name__
            for resource in content.values():
                article = zeit.content.article.interfaces.IArticle(resource, None)
                if article is None:
                    continue
                pubinfo = zeit.cms.workflow.interfaces.IPublishInfo(article)
                published = pubinfo.published
                status = zeit.workflow.interfaces.IOldCMSStatus(article).status
                if (published == False) and (status not in valid_status):
                    continue
                archive_index = zeit.archive.interfaces.IArchiveIndex(article)
                archive_volume = zeit.archive.interfaces.IArchiveVolume(article)
                archive_year = zeit.archive.interfaces.IArchiveYear(article)
                if archive_volume.name is None:
                    continue
                archive_index._createTeaser(archive_volume, index_volume)
                if article.page == 1:
                    archive_index._createTeaser(archive_year, index_year)
                elif 'index' not in archive_year.index_coll:
                    archive_index._createTeaser(
                        archive_year, index_year, dummy=True)
            content['index'] = index_volume
    year_coll['index'] = index_year


@zope.component.adapter(
    zeit.content.article.interfaces.IArticle,
    zeit.cms.workflow.interfaces.IBeforePublishEvent)
def addContext(context, event):
    index = zeit.archive.interfaces.IArchiveIndex(context)
    index.addTeaser()


@zope.component.adapter(
    zeit.content.article.interfaces.IArticle,
    zeit.cms.repository.interfaces.IBeforeObjectRemovedEvent)
def removeContextWhenRemoved(context, event):
    index = zeit.archive.interfaces.IArchiveIndex(context)
    index.removeTeaser()


@zope.component.adapter(
    zeit.content.article.interfaces.IArticle,
    zeit.cms.workflow.interfaces.IBeforeRetractEvent)
def removeContextWhenRetract(context, event):
    index = zeit.archive.interfaces.IArchiveIndex(context)
    index.removeTeaser()




class ArchiveIndex(object):

    zope.component.adapts(zeit.content.article.interfaces.IArticle)
    zope.interface.implements(zeit.archive.interfaces.IArchiveIndex)

    def __init__(self, context):
        self.context = context
        if not zeit.cms.repository.interfaces.ICollection.providedBy(context):
            self.teaser = context
            self.volume = zeit.archive.interfaces.IArchiveVolume(context)
            self.year = zeit.archive.interfaces.IArchiveYear(context)

    def addTeaser(self):
        if self.volume.name is None:
            return
        self._addTeaserTo(self.volume)
        if self.teaser.page == 1:
            self._addTeaserTo(self.year)
        elif 'index' not in self.year.index_coll:
            self._addTeaserTo(self.year, dummy=True)

    def removeTeaser(self):
        if self.volume.name is None:
            return
        self._removeTeaser(self.volume)
        if self.teaser.page == 1:
            self._removeTeaser(self.year)

    def _addTeaserTo(self, archiv, dummy=False):
        index = archiv.index
        if index is None:
            index = zeit.content.cp.centerpage.CenterPage()
            index.type = archiv.type
            index.year = archiv.year
            if archiv.volume is not None:
                index.volume = archiv.volume
            self._createTeaser(archiv, index, dummy)
            archiv.create(index)
        else:
            with zeit.cms.checkout.helper.checked_out(
                index, events=False) as co:
                self._createTeaser(archiv, co)

    def _createTeaser(self, archiv, index, dummy=False):
        lead = index['lead']
        if archiv.name in lead:
            block = lead[archiv.name]
        else:
            factory = zope.component.getAdapter(
                lead, zeit.content.cp.interfaces.IElementFactory, name='teaser')
            block = factory()
            layout = zeit.content.cp.layout.get_layout(archiv.type)
            block.layout = layout
            block.__name__ = archiv.name
            block.title = archiv.name
        if dummy == False:
            block.insert(0, zeit.cms.interfaces.ICMSContent(self.teaser))

    def _removeTeaser(self, archiv):
        index = archiv.index
        if index is None:
            return
        with zeit.cms.checkout.helper.checked_out(index) as co:
            lead = co['lead']
            if archiv.name not in lead:
                return
            block = lead[archiv.name]
            block.remove(zeit.cms.interfaces.ICMSContent(self.teaser))
            if len(block) == 0:
                del lead[block.__name__]


class ArchiveBase(object):

    archive_name = 'index'

    @property
    def index(self):
        index = self.index_coll.get(self.archive_name)
        if zeit.content.cp.interfaces.ICenterPage.providedBy(index):
            return index

    def create(self, index):
        self.index_coll[self.archive_name] = index

class ArchiveVolume(ArchiveBase):

    zope.component.adapts(zeit.content.article.interfaces.IArticle)
    zope.interface.implements(zeit.archive.interfaces.IArchiveVolume)

    type = u'archive-print-volume'

    def __init__(self, teaser):
        self.teaser = teaser
        self.index_coll = teaser.__parent__
        self.volume = teaser.__parent__.__name__
        self.year = teaser.__parent__.__parent__.__name__
        meta = zeit.cms.content.interfaces.ICommonMetadata(self.teaser, None)
        if meta is not None:
            self.name = meta.printRessort


class ArchiveYear(ArchiveBase):

    zope.component.adapts(zeit.content.article.interfaces.IArticle)
    zope.interface.implements(zeit.archive.interfaces.IArchiveYear)

    type = u'archive-print-year'
    volume = None

    def __init__(self, teaser):
        self.teaser = teaser
        self.index_coll = teaser.__parent__.__parent__
        self.year = teaser.__parent__.__parent__.__name__
        self.name = teaser.__parent__.__name__

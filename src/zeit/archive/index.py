from __future__ import with_statement
import zeit.archive.interfaces
import zeit.cms.checkout.interfaces
import zeit.cms.repository.interfaces
import zeit.content.article.interfaces
import zeit.workflow
import zope.component
import zope.interface



def rebuildVolume(id):
    start_container = zeit.cms.interfaces.ICMSContent(id)
    stack = [start_container]
    while stack:
        content = stack.pop(0)
        publish = zeit.cms.workflow.interfaces.IPublishInfo(content)
        status = zeit.workflow.interfaces.IOldCMSStatus(content).status
        valid_status = ['OK', 'imported', 'importedVHB']
        if zeit.cms.repository.interfaces.ICollection.providedBy(content):
            if 'index_new_archive' in content:
                del content['index_new_archive']
            stack.extend(content.values())
        elif publish.published or (status in valid_status):
            index = zeit.archive.interfaces.IArchiveIndex(content, None)
            if index is not None:
                index.teaser = content
                index.cp = zeit.content.cp.centerpage.CenterPage()
                index.addTeaser()


@zope.component.adapter(
    zeit.content.article.interfaces.IArticle,
    zeit.cms.workflow.interfaces.IBeforePublishEvent)
def addContext(context, event):
    index = zeit.archive.interfaces.IArchiveIndex(context)
    index.addTeaser()


@zope.component.adapter(
    zeit.content.article.interfaces.IArticle,
    zeit.cms.repository.interfaces.IBeforeObjectRemovedEvent)
def removeContext(context, event):
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
            #self.volume_coll = self.teaser.__parent__
            #self.year_coll = self.teaser.__parent__.__parent__

    def addTeaser(self):
        if self.volume.name is None:
            return
        self._addTeaserTo(self.volume)
        if self.teaser.page == 1:
            self._addTeaserTo(self.year)

    def removeTeaser(self):
        if self.volume.name is None:
            return
        self._removeTeaser(self.volume)
        if self.teaser.page == 1:
            self._removeTeaser(self.year)

    def _addTeaserTo(self, archiv):
        if 'index_new_archive' in archiv.index_coll:
            index = archiv.index_coll['index_new_archive']
            with zeit.cms.checkout.helper.checked_out(index, events=False) as co:
                archiv.index = co
                self._createTeaser(archiv)
        else:
            index = zeit.content.cp.centerpage.CenterPage()
            index.type = archiv.type
            index.year = archiv.year
            if archiv.volume is not None:
                index.volume = archiv.volume
            archiv.index = index
            self._createTeaser(archiv)
            archiv.index_coll['index_new_archive'] = archiv.index

    def _createTeaser(self, archiv):
        lead = archiv.index['lead']
        if archiv.name not in lead:
            factory = zope.component.getAdapter(
                lead, zeit.content.cp.interfaces.IElementFactory, name='teaser')
            block = factory()
            layout = zeit.content.cp.layout.get_layout(archiv.type)
            block.layout = layout
            block.__name__ = archiv.name
            block.title = archiv.name
        else:
            block = lead[archiv.name]
        block.insert(0, zeit.cms.interfaces.ICMSContent(self.teaser))

    def _removeTeaser(self, archiv):
        index = archiv.index_coll['index_new_archive']
        with zeit.cms.checkout.helper.checked_out(index) as co:
            lead = co['lead']
            if archiv.name not in lead:
                return
            block = lead[archiv.name]
            block.remove(zeit.cms.interfaces.ICMSContent(self.teaser))
            if len(block) == 0:
                del lead[block.__name__]

    def _clearIndex(self):
        del self.index_coll['index_new_archive']


class ArchiveVolume(object):

    zope.component.adapts(zeit.content.article.interfaces.IArticle)
    zope.interface.implements(zeit.archive.interfaces.IArchiveVolume)

    def __init__(self, teaser):
        self.teaser = teaser
        self.type = 'archive-print-volume'
        self.index_coll = teaser.__parent__
        self.volume = teaser.__parent__.__name__
        self.year = teaser.__parent__.__parent__.__name__
        meta = zeit.cms.content.interfaces.ICommonMetadata(self.teaser, None)
        if meta is not None:
            self.name = meta.printRessort


class ArchiveYear(object):

    zope.component.adapts(zeit.content.article.interfaces.IArticle)
    zope.interface.implements(zeit.archive.interfaces.IArchiveYear)

    def __init__(self, teaser):
        self.teaser = teaser
        self.type = 'archive-print-year'
        self.index_coll = teaser.__parent__.__parent__
        self.volume = None
        self.year = teaser.__parent__.__parent__.__name__
        self.name = teaser.__parent__.__name__


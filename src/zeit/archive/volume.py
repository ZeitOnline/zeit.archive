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
            self.volume_coll = self.teaser.__parent__
            self.year_coll = self.teaser.__parent__.__parent__

    def addTeaser(self):
        self._addTeaserTo(self.volume_coll, self._createVolumeTeaser)
        if self.teaser.page == 1:
            self._addTeaserTo(self.year_coll, self._createYearTeaser)

    def removeTeaser(self):
        self._removeVolumeTeaser()
        if self.teaser.page == 1:
            self._removeYearTeaser()

    def _addTeaserTo(self, index_coll, createTeaser):
        if 'index_new_archive' in index_coll:
            index = index_coll['index_new_archive']
            with zeit.cms.checkout.helper.checked_out(index) as co:
                createTeaser(co)
        else:
            index = zeit.content.cp.centerpage.CenterPage()
            index.type = 'archive-print'
            index.volume = index_coll.__name__
            index.year = index_coll.__parent__.__name__
            createTeaser(index)
            index_coll['index_new_archive'] = index

    def _createVolumeTeaser(self, index):
        meta = zeit.cms.content.interfaces.ICommonMetadata(self.teaser, None)
        if meta is None:
            return
        ressort = meta.printRessort
        if ressort is None:
            return
        lead = index['lead']
        if ressort not in lead:
            factory = zope.component.getAdapter(
                lead, zeit.content.cp.interfaces.IElementFactory, name='teaser')
            block = factory()
            layout = zeit.content.cp.layout.get_layout('archive-print')
            block.layout = layout
            block.__name__ = ressort
            block.title = ressort
        else:
            block = lead[ressort]
        block.insert(0, zeit.cms.interfaces.ICMSContent(self.teaser))

    def _createYearTeaser(self, index):
        volume = self.volume_coll.__name__
        if volume is None:
            return
        lead = index['lead']
        if volume not in lead:
            factory = zope.component.getAdapter(
                lead, zeit.content.cp.interfaces.IElementFactory, name='teaser')
            block = factory()
            layout = zeit.content.cp.layout.get_layout('archive-print')
            block.layout = layout
            block.__name__ = volume
            block.title = volume
        else:
            block = lead[volume]
        block.insert(0, zeit.cms.interfaces.ICMSContent(self.teaser))

    def _removeVolumeTeaser(self):
        meta = zeit.cms.content.interfaces.ICommonMetadata(self.teaser, None)
        if meta is None:
            return
        ressort = meta.printRessort
        if ressort is None:
            return
        index = self.volume_coll['index_new_archive']
        with zeit.cms.checkout.helper.checked_out(index) as co:
            lead = co['lead']
            if ressort not in lead:
                return
            block = lead[ressort]
            block.remove(zeit.cms.interfaces.ICMSContent(self.teaser))
            if len(block) == 0:
                del lead[block.__name__]

    def _removeYearTeaser(self):
        volume = self.volume_coll.__name__
        if volume is None:
            return
        index = self.year_coll['index_new_archive']
        with zeit.cms.checkout.helper.checked_out(index) as co:
            lead = co['lead']
            if volume not in lead:
                return
            block = lead[volume]
            block.remove(zeit.cms.interfaces.ICMSContent(self.teaser))
            if len(block) == 0:
                del lead[block.__name__]

    def _clearIndex(self, ndex_coll):
        del index_coll['index_new_archive']

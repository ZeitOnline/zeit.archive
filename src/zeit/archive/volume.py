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
        if zeit.cms.repository.interfaces.ICollection.providedBy(content):
            if 'index_new_archive' in content:
                del content['index_new_archive']
            stack.extend(content.values())
        elif publish.published:
            volume = zeit.archive.interfaces.IArchiveVolume(content, None)
            if volume is not None:
                volume.teaser = content
                volume.cp = zeit.content.cp.centerpage.CenterPage()
                volume.addTeaser()


@zope.component.adapter(
    zeit.content.article.interfaces.IArticle,
    zeit.cms.workflow.interfaces.IBeforePublishEvent)
def addContext(context, event):
    volume = zeit.archive.interfaces.IArchiveVolume(context)
    volume.addTeaser()


@zope.component.adapter(
    zeit.content.article.interfaces.IArticle,
    zeit.cms.repository.interfaces.IBeforeObjectRemovedEvent)
def removeContext(context, event):
    volume = zeit.archive.interfaces.IArchiveVolume(context)
    volume.removeTeaser()


class ArchiveVolume(object):

    zope.component.adapts(zeit.content.article.interfaces.IArticle)
    zope.interface.implements(zeit.archive.interfaces.IArchiveVolume)

    def __init__(self, context):
        self.context = context
        if not zeit.cms.repository.interfaces.ICollection.providedBy(context):
            self.teaser = context
            self.volume_coll = self.teaser.__parent__

    def addTeaser(self, position=0):
        if 'index_new_archive' in self.volume_coll:
            volume_index = self.volume_coll['index_new_archive']
            with zeit.cms.checkout.helper.checked_out(volume_index) as co:
                self.volume = co
                self._createTeaser()
        else:
            self.volume = zeit.content.cp.centerpage.CenterPage()
            self.volume.type = 'archive-print'
            self.volume.volume = self.volume_coll.__name__
            self.volume.year = self.volume_coll.__parent__.__name__
            self._createTeaser()
            self.volume_coll['index_new_archive'] = self.volume

    def removeTeaser(self):
        meta = zeit.cms.content.interfaces.ICommonMetadata(self.teaser, None)
        if meta is None:
            return
        ressort = meta.printRessort
        if ressort is None:
            return
        volume_index = self.volume_coll['index_new_archive']
        with zeit.cms.checkout.helper.checked_out(volume_index) as co:
            lead = co['lead']
            block = lead[ressort]
            block.remove(zeit.cms.interfaces.ICMSContent(self.teaser))
            if len(block) == 0:
                del lead[block.__name__]

    def _createTeaser(self):
        meta = zeit.cms.content.interfaces.ICommonMetadata(self.teaser, None)
        if meta is None:
            return
        ressort = meta.printRessort
        if ressort is None:
            return
        lead = self.volume['lead']
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

    def _clearVolume(self):
        del self.volume_coll['index_new_archive']

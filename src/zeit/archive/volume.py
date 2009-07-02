from __future__ import with_statement
import zeit.archive.interfaces
import zeit.cms.checkout.interfaces
import zeit.cms.repository.interfaces
import zeit.workflow
import zope.interface
import zope.component



def rebuildVolume(id):
    start_container = zeit.cms.interfaces.ICMSContent(id)
    stack = [start_container]
    while stack:
        content = stack.pop(0)
        publish = zeit.cms.workflow.interfaces.IPublishInfo(content)
        if zeit.cms.repository.interfaces.ICollection.providedBy(content):
            if 'index' in content:
                del content['index']
            stack.extend(content.values())
        elif publish.published:
            volume = zeit.archive.interfaces.IArchiveVolume(content, None)
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
            self.parent = self.teaser.__parent__

    def addTeaser(self, position=0):
        if 'index' in self.parent:
            index = self.parent['index']
            with zeit.cms.checkout.helper.checked_out(index) as co:
                self.cp = co
                self._createTeaser()
        else:
            self.cp = zeit.content.cp.centerpage.CenterPage()
            self._createTeaser()
            self.parent['index'] = self.cp

    def removeTeaser(self):
        index = self.parent['index']
        with zeit.cms.checkout.helper.checked_out(index) as co:
            ressort = getattr(self.teaser, 'ressort', None)
            block = co['lead'][ressort]
            block.remove(zeit.cms.interfaces.ICMSContent(self.teaser))

    def _createTeaser(self):
        ressort = getattr(self.teaser, 'ressort', None)
        if ressort is None:
            return
        lead = self.cp['lead']
        if ressort not in lead:
            factory = zope.component.getAdapter(
                lead, zeit.content.cp.interfaces.IElementFactory, name='teaser')
            block = factory()
            block.__name__ = ressort
            block.title = ressort
        else:
            block = lead[ressort]
        block.insert(0, zeit.cms.interfaces.ICMSContent(self.teaser))

    def _clearVolume(self):
        del self.parent['index']

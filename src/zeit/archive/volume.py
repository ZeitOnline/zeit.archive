from __future__ import with_statement
import zeit.archive.interfaces
import zeit.cms.checkout.interfaces
import zope.interface


class ArchiveVolume(object):

    zope.component.adapts(zeit.cms.interfaces.ICMSContent)
    zope.interface.implements(zeit.archive.interfaces.IArchiveVolume)

    def __init__(self, context):
        self.context = context

    #TODO def rebuild(self):

    def addTeaser(self, position=0):
        if 'index' in self.context.__parent__:
            self.cp = self.context.__parent__['index']
            with zeit.cms.checkout.helper.checked_out(self.cp) as co:
                self._createTeaser()
        else:
            self.cp = zeit.content.cp.centerpage.CenterPage()
            self._createTeaser()
            self.context.__parent__['index'] = self.cp

    #TODO def removeTeaser(self):

    def _createTeaser(self):
        ressort = getattr(self.context, 'ressort', None)
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
        block.insert(0, zeit.cms.interfaces.ICMSContent(self.context))

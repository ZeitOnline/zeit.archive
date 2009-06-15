import zeit.archive.interfaces
import zope.interface


class ArchiveVolume(object):

    zope.component.adapts(zeit.cms.interfaces.ICMSContent)
    zope.interface.implements(zeit.archive.interfaces.IArchiveVolume)

    def __init__(self, context):
        self.context = context
        cp = zeit.content.cp.centerpage.CenterPage()
        self.lead = cp['lead']

    #TODO def rebuild(self):

    def addTeaser(self, position=0):
        ressort = getattr(self.context, 'ressort', None)
        if ressort is None:
            return
        factory = zope.component.getAdapter(
            self.lead, zeit.content.cp.interfaces.IElementFactory, name='teaser')
        if ressort not in self.lead:
            block = factory()
            block.__name__ = ressort
            block.title = ressort
        else:
            block = self.lead[ressort]
        block.insert(0, zeit.cms.interfaces.ICMSContent(self.context))
 
    #TODO def removeTeaser(self):

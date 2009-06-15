import zeit.archive.interfaces
import zope.interface


class ArchiveVolume(object):

    zope.component.adapts(zeit.cms.interfaces.ICMSContent)
    zope.interface.implements(zeit.archive.interfaces.IArchiveVolume)

    def __init__(self, context):
        self.context = context
        self.cp = zeit.content.cp.centerpage.CenterPage()

    #TODO def rebuild(self):

    def addTeaser(self, position=0):
        ressort = getattr(self.context, 'ressort', None)
        if ressort is None:
            return
        lead = self.cp['lead']
        factory = zope.component.getAdapter(
            lead, zeit.content.cp.interfaces.IElementFactory, name='teaser')
        if ressort not in lead:
            block = factory()
            block.__name__ = ressort
            block.title = ressort
        else:
            block = lead[ressort]
        block.insert(0, zeit.cms.interfaces.ICMSContent(self.context))
        self.context.__parent__['index'] = self.cp
 
    #TODO def removeTeaser(self):

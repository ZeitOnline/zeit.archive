Prepare for functional tests.

>>> import zope.app.component.hooks
>>> old_site = zope.app.component.hooks.getSite()
>>> zope.app.component.hooks.setSite(getRootFolder())


#TODO Check if an archive volume already exists.

Create a sample archive volume.
>>> import zeit.cms.interfaces
>>> article = zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/online/2007/01/Somalia')

>>> import zeit.archive.volume
>>> volume = zeit.archive.interfaces.IArchiveVolume(article)

>>> volume.addTeaser()

>>> import lxml.etree
>>> print lxml.etree.tostring(volume.lead.xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="leader" cp:__name__="International" title="International">
    <block href="http://xml.zeit.de/online/2007/01/Somalia" year="2007" issue="1">
...


Cleanup.
>>> zope.app.component.hooks.setSite(old_site)

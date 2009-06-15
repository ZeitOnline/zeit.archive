Prepare for functional tests.

>>> import zope.app.component.hooks
>>> old_site = zope.app.component.hooks.getSite()
>>> zope.app.component.hooks.setSite(getRootFolder())


Archive volume should not exist yet.

>>> import zeit.cms.interfaces
>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/online/2007/01/index')
>>> index
<zeit.cms.repository.unknown.PersistentUnknownResource object at 0xb03feec>


Create a new archive volume containing a single teaser.

>>> import zeit.archive.volume
>>> article = zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/online/2007/01/Somalia')
>>> volume = zeit.archive.interfaces.IArchiveVolume(article)
>>> volume.addTeaser()


Archive volume should exist now.

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/online/2007/01/index')
>>> index
<zeit.content.cp.centerpage.CenterPage object at 0x...>


Check content.

>>> import lxml.etree
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="leader" cp:__name__="International" title="International">
    <block href="http://xml.zeit.de/online/2007/01/Somalia" year="2007" issue="1">
      <supertitle py:pytype="str">Somalia</supertitle>
...
    </block>
  </container>
</region>
<BLANKLINE>


Cleanup.
>>> zope.app.component.hooks.setSite(old_site)

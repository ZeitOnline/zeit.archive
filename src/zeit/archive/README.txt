Prepare for functional tests.

>>> import zope.app.component.hooks
>>> old_site = zope.app.component.hooks.getSite()
>>> zope.app.component.hooks.setSite(getRootFolder())


Archive volume should not exist yet.

>>> import zeit.cms.interfaces
>>> zeit.cms.interfaces.ICMSContent('http://xml.zeit.de/2007/01/index')
Traceback (most recent call last):
...
TypeError: ('Could not adapt', 'http://xml.zeit.de/2007/01/index', <InterfaceClass zeit.cms.interfaces.ICMSContent>)


Create a new archive volume containing a single teaser.

>>> import zeit.archive.volume
>>> principal = zeit.cms.testing.create_interaction()
>>> article = zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/Miami')
>>> volume = zeit.archive.interfaces.IArchiveVolume(article)
>>> volume.addTeaser()


Archive volume should exist now.

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index')
>>> index
<zeit.content.cp.centerpage.CenterPage object at 0x...>


Check content.

>>> import lxml.etree
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="leader" cp:__name__="Reisen" title="Reisen">
    <block href="http://xml.zeit.de/2007/01/Miami" publication-date="" expires="" year="2007" issue="1">
      <supertitle py:pytype="str">Florida</supertitle>
...
    </block>
  </container>
</region>
<BLANKLINE>


Add a teaser to an existing volume in the same ressort.

>>> article2 = zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/Momente-Uhl')
>>> volume = zeit.archive.interfaces.IArchiveVolume(article2)
>>> volume.addTeaser()

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="leader" cp:__name__="Reisen" title="Reisen">
    <block href="http://xml.zeit.de/2007/01/Momente-Uhl" publication-date="" expires="" year="2006" issue="1">
...
    </block>
    <block href="http://xml.zeit.de/2007/01/Miami" publication-date="" expires="" year="2007" issue="1">
      <supertitle py:pytype="str">Florida</supertitle>
...
    </block>
  </container>
</region>
<BLANKLINE>


Add a teaser to an existing volume in a different ressort.

>>> article3 = zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/Martenstein')
>>> volume = zeit.archive.interfaces.IArchiveVolume(article3)
>>> volume.addTeaser()

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="leader" cp:__name__="Reisen" title="Reisen">
    <block href="http://xml.zeit.de/2007/01/Momente-Uhl" publication-date="" expires="" year="2006" issue="1">
...
    </block>
    <block href="http://xml.zeit.de/2007/01/Miami" publication-date="" expires="" year="2007" issue="1">
      <supertitle py:pytype="str">Florida</supertitle>
...
    </block>
  </container>
  <container cp:type="teaser" module="buttons" cp:__name__="Leben" title="Leben">
    <block href="http://xml.zeit.de/2007/01/Martenstein" publication-date="" expires="" year="2007" issue="1">
...
  </container>
</region>
<BLANKLINE>


Remove a teaser from the volume.

>>> volume = zeit.archive.interfaces.IArchiveVolume(article2)
>>> volume.removeTeaser()

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="leader" cp:__name__="Reisen" title="Reisen">
    <block href="http://xml.zeit.de/2007/01/Miami" publication-date="" expires="" year="2007" issue="1">
      <supertitle py:pytype="str">Florida</supertitle>
...
    </block>
  </container>
  <container cp:type="teaser" module="buttons" cp:__name__="Leben" title="Leben">
...
  </container>
</region>
<BLANKLINE>


Rebuild a whole volume from scratch.
We need to assign the published attribute to articles we want to appear in
the resultset since our testarticles do not have set this attribute by default.

>>> article4 = zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/Macher')
>>> zeit.cms.workflow.interfaces.IPublishInfo(article4).published = True

>>> volume = zeit.archive.interfaces.IArchiveVolume(
...     zeit.cms.interfaces.ICMSContent(
...         'http://xml.zeit.de/2007/01/'))
>>> volume.rebuildVolume()

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="leader" cp:__name__="Wirtschaft" title="Wirtschaft">
    <block href="http://xml.zeit.de/2007/01/Macher" publication-date="" expires="" year="2007" issue="1">
      <supertitle py:pytype="str">Entwicklungshilfe</supertitle>
...
    </block>
  </container>
</region>
<BLANKLINE>


Cleanup.
>>> zope.app.component.hooks.setSite(old_site)

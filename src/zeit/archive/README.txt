Prepare for functional tests.

>>> import zope.app.component.hooks
>>> old_site = zope.app.component.hooks.getSite()
>>> zope.app.component.hooks.setSite(getRootFolder())


Archive volume should not exist yet.

>>> import zeit.cms.interfaces
>>> zeit.cms.interfaces.ICMSContent('http://xml.zeit.de/2007/01/index_new_archive')
Traceback (most recent call last):
...
TypeError: ('Could not adapt', 'http://xml.zeit.de/2007/01/index_new_archive', <InterfaceClass zeit.cms.interfaces.ICMSContent>)


Create a new archive volume containing a single teaser.

>>> import zeit.archive.volume
>>> principal = zeit.cms.testing.create_interaction()
>>> article = zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/Miami')
>>> with zeit.cms.checkout.helper.checked_out(article) as checked_out:
...     zeit.cms.content.interfaces.ICommonMetadata(
...         checked_out).printRessort = u'Reisen'
>>> volume = zeit.archive.interfaces.IArchiveVolume(article)
>>> volume.addTeaser()


Archive volume should exist now.

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index_new_archive')
>>> index
<zeit.content.cp.centerpage.CenterPage object at 0x...>


Check content.

>>> import lxml.etree
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print" cp:__name__="Reisen" title="Reisen">
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
>>> with zeit.cms.checkout.helper.checked_out(article2) as checked_out:
...     zeit.cms.content.interfaces.ICommonMetadata(
...         checked_out).printRessort = u'Reisen'
>>> volume = zeit.archive.interfaces.IArchiveVolume(article2)
>>> volume.addTeaser()

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index_new_archive')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print" cp:__name__="Reisen" title="Reisen">
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


A teaser without a print ressort specified will not be added.

>>> article3 = zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/Martenstein')
>>> volume = zeit.archive.interfaces.IArchiveVolume(article3)
>>> volume.addTeaser()
>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index_new_archive')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print" cp:__name__="Reisen" title="Reisen">
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

>>> with zeit.cms.checkout.helper.checked_out(article3) as checked_out:
...     zeit.cms.content.interfaces.ICommonMetadata(
...         checked_out).printRessort = u'Leben'
>>> volume = zeit.archive.interfaces.IArchiveVolume(article3)
>>> volume.addTeaser()

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index_new_archive')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print" cp:__name__="Reisen" title="Reisen">
    <block href="http://xml.zeit.de/2007/01/Momente-Uhl" publication-date="" expires="" year="2006" issue="1">
...
    </block>
    <block href="http://xml.zeit.de/2007/01/Miami" publication-date="" expires="" year="2007" issue="1">
      <supertitle py:pytype="str">Florida</supertitle>
...
    </block>
  </container>
  <container cp:type="teaser" module="archive-print" cp:__name__="Leben" title="Leben">
    <block href="http://xml.zeit.de/2007/01/Martenstein" publication-date="" expires="" year="2007" issue="1">
...
  </container>
</region>
<BLANKLINE>


Remove a teaser from the volume.

>>> volume = zeit.archive.interfaces.IArchiveVolume(article2)
>>> volume.removeTeaser()

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index_new_archive')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print" cp:__name__="Reisen" title="Reisen">
    <block href="http://xml.zeit.de/2007/01/Miami" publication-date="" expires="" year="2007" issue="1">
      <supertitle py:pytype="str">Florida</supertitle>
...
    </block>
  </container>
  <container cp:type="teaser" module="archive-print" cp:__name__="Leben" title="Leben">
...
  </container>
</region>
<BLANKLINE>


Adapting only works with articles.
#FIXME Additional content types may follow.

>>> folder = zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/')
>>> volume = zeit.archive.interfaces.IArchiveVolume(folder)
Traceback (most recent call last):
...
TypeError: ('Could not adapt', ...)


Rebuild a whole volume from scratch.
We need to assign the published attribute to articles we want to appear in
the resultset since our testarticles do not have set this attribute by default.

>>> article4 = zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/Macher')
>>> with zeit.cms.checkout.helper.checked_out(article4) as checked_out:
...     zeit.cms.content.interfaces.ICommonMetadata(
...         checked_out).printRessort = u'Wirtschaft'
>>> zeit.cms.workflow.interfaces.IPublishInfo(article4).published = True
>>> article5 = zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/02/Vita')
>>> with zeit.cms.checkout.helper.checked_out(article5) as checked_out:
...     zeit.cms.content.interfaces.ICommonMetadata(
...         checked_out).printRessort = u'Feuilleton'
>>> zeit.cms.workflow.interfaces.IPublishInfo(article5).published = True
>>> zeit.archive.volume.rebuildVolume('http://xml.zeit.de/2007/')

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index_new_archive')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print" cp:__name__="Wirtschaft" title="Wirtschaft">
    <block href="http://xml.zeit.de/2007/01/Macher" publication-date="" expires="" year="2007" issue="1">
      <supertitle py:pytype="str">Entwicklungshilfe</supertitle>
...
    </block>
  </container>
</region>
<BLANKLINE>

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/02/index_new_archive')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print" cp:__name__="Feuilleton" title="Feuilleton">
    <block href="http://xml.zeit.de/2007/02/Vita" publication-date="" expires="" year="2007" issue="2">
...
    </block>
  </container>
</region>
<BLANKLINE>


Publish an article to test our event handler.

>>> workflow = zeit.workflow.interfaces.IContentWorkflow(article)
>>> publish = zeit.cms.workflow.interfaces.IPublish(article)
>>> workflow.published
False
>>> workflow.urgent = True
>>> workflow.can_publish()
True
>>> publish.publish()
>>> import lovely.remotetask.interfaces
>>> tasks = zope.component.getUtility(
...     lovely.remotetask.interfaces.ITaskService, 'general')
>>> tasks.process()
>>> workflow.published
True

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index_new_archive')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print" cp:__name__="Wirtschaft" title="Wirtschaft">
    <block href="http://xml.zeit.de/2007/01/Macher" publication-date="" expires="" year="2007" issue="1">
      <supertitle py:pytype="str">Entwicklungshilfe</supertitle>
...
    </block>
  </container>
  <container cp:type="teaser" module="archive-print" cp:__name__="Reisen" title="Reisen">
    <block href="http://xml.zeit.de/2007/01/Miami" publication-date="" expires="" year="2007" issue="1">
      <supertitle py:pytype="str">Florida</supertitle>
...
    </block>
  </container>
</region>
<BLANKLINE>


Delete an article to test our event handler.

>>> repository = zope.component.getUtility(zeit.cms.repository.interfaces.IRepository)
>>> del repository['2007']['01']['Macher']
>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index_new_archive')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print" cp:__name__="Reisen" title="Reisen">
    <block href="http://xml.zeit.de/2007/01/Miami" publication-date="" expires="" year="2007" issue="1">
      <supertitle py:pytype="str">Florida</supertitle>
...
    </block>
  </container>
</region>
<BLANKLINE>


Check attribute values.

>>> print lxml.etree.tostring(index.xml, pretty_print=True)
<centerpage ...>
  <head>
    <attribute py:pytype="str" ns="http://namespaces.zeit.de/CMS/document" name="date-last-modified">...</attribute>
    <attribute py:pytype="str" ns="http://namespaces.zeit.de/CMS/document" name="last_modified_by">zope.user</attribute>
    <attribute py:pytype="str" ns="http://namespaces.zeit.de/CMS/meta" name="type">centerpage-2009</attribute>
    <attribute py:pytype="str" ns="http://namespaces.zeit.de/CMS/document" name="uuid">{urn:uuid:5b15e4ec-be2d-461d-b717-cba15096e44e}</attribute>
    <attribute py:pytype="str" ns="http://namespaces.zeit.de/CMS/document" name="volume">01</attribute>
    <attribute py:pytype="str" ns="http://namespaces.zeit.de/CMS/document" name="year">2007</attribute>
  </head>
...
</centerpage>
<BLANKLINE>



Cleanup.
>>> zope.app.component.hooks.setSite(old_site)

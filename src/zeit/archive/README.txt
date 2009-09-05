Prepare for functional tests.

>>> import zeit.cms.testing
>>> zeit.cms.testing.set_site()


Archive volume should not exist yet.

>>> import zeit.cms.interfaces
>>> zeit.cms.interfaces.ICMSContent('http://xml.zeit.de/2007/01/index')
Traceback (most recent call last):
...
TypeError: ('Could not adapt', 'http://xml.zeit.de/2007/01/index', <InterfaceClass zeit.cms.interfaces.ICMSContent>)


Archive year should not exist as well.

>>> zeit.cms.interfaces.ICMSContent('http://xml.zeit.de/2007/index')
Traceback (most recent call last):
...
TypeError: ('Could not adapt', 'http://xml.zeit.de/2007/index', <InterfaceClass zeit.cms.interfaces.ICMSContent>)


Create a new archive volume containing a single teaser.

>>> import zeit.archive.index
>>> principal = zeit.cms.testing.create_interaction()
>>> article = zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/Miami')
>>> with zeit.cms.checkout.helper.checked_out(article) as checked_out:
...     zeit.cms.content.interfaces.ICommonMetadata(
...         checked_out).printRessort = u'Reisen'
>>> archive_index = zeit.archive.interfaces.IArchiveIndex(article)
>>> archive_index.addTeaser()


Archive volume should exist now.

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index')
>>> index
<zeit.content.cp.centerpage.CenterPage object at 0x...>


Check content.

>>> import lxml.etree
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print-volume" cp:__name__="Reisen" title="Reisen">
    <block href="http://xml.zeit.de/2007/01/Miami" ...
      <supertitle py:pytype="str">Florida</supertitle>
...
    </block>
  </container>
</region>
<BLANKLINE>


Archive year contains only articles from page 1, so there is only a container.

>>> zeit.cms.interfaces.ICMSContent('http://xml.zeit.de/2007/index')
<zeit.content.cp.centerpage.CenterPage object at 0x...>

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/index')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print-year" cp:__name__="01" title="01"/>
</region>
<BLANKLINE>


Adding the same teaser again will not affect the volume.

>>> with zeit.cms.checkout.helper.checked_out(article) as checked_out:
...     zeit.cms.content.interfaces.ICommonMetadata(
...         checked_out).page = 1
>>> archive_index.addTeaser()


Archive year should now contain a teaser.

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/index')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print-year" cp:__name__="01" title="01">
    <block href="http://xml.zeit.de/2007/01/Miami" ...
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
...     zeit.cms.content.interfaces.ICommonMetadata(
...         checked_out).page = 1
>>> archive_index = zeit.archive.interfaces.IArchiveIndex(article2)
>>> archive_index.addTeaser()

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print-volume" cp:__name__="Reisen" title="Reisen">
    <block href="http://xml.zeit.de/2007/01/Momente-Uhl" ...
...
    </block>
    <block href="http://xml.zeit.de/2007/01/Miami" ...
      <supertitle py:pytype="str">Florida</supertitle>
...
    </block>
  </container>
</region>
<BLANKLINE>


>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/index')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print-year" cp:__name__="01" title="01">
    <block href="http://xml.zeit.de/2007/01/Momente-Uhl" ...
...
    </block>
    <block href="http://xml.zeit.de/2007/01/Miami" ...
      <supertitle py:pytype="str">Florida</supertitle>
...
    </block>
  </container>
</region>
<BLANKLINE>


A teaser without a print ressort specified will not be added.

>>> article3 = zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/Martenstein')
>>> archive_index = zeit.archive.interfaces.IArchiveIndex(article3)
>>> archive_index.addTeaser()
>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print-volume" cp:__name__="Reisen" title="Reisen">
    <block href="http://xml.zeit.de/2007/01/Momente-Uhl" ...
...
    </block>
    <block href="http://xml.zeit.de/2007/01/Miami" ...
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
>>> archive_index = zeit.archive.interfaces.IArchiveIndex(article3)
>>> archive_index.addTeaser()

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print-volume" cp:__name__="Reisen" title="Reisen">
    <block href="http://xml.zeit.de/2007/01/Momente-Uhl"...
    <block href="http://xml.zeit.de/2007/01/Miami"...
      <supertitle py:pytype="str">Florida</supertitle>...
  <container cp:type="teaser" module="archive-print-volume" cp:__name__="Leben" title="Leben">
    <block href="http://xml.zeit.de/2007/01/Martenstein"...


Remove a teaser from the archive.

>>> archive_index = zeit.archive.interfaces.IArchiveIndex(article2)
>>> archive_index.removeTeaser()

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print-volume" cp:__name__="Reisen" title="Reisen">
    <block href="http://xml.zeit.de/2007/01/Miami"...
      <supertitle py:pytype="str">Florida</supertitle>...
  <container cp:type="teaser" module="archive-print-volume" cp:__name__="Leben" title="Leben">
...

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/index')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print-year" cp:__name__="01" title="01">
    <block href="http://xml.zeit.de/2007/01/Miami" ...
      <supertitle py:pytype="str">Florida</supertitle>
...
    </block>
  </container>
</region>
<BLANKLINE>


Adapting only works with articles.
#FIXME Additional content types may follow.

>>> folder = zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/')
>>> archive_index = zeit.archive.interfaces.IArchiveIndex(folder)
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
...     zeit.cms.content.interfaces.ICommonMetadata(
...         checked_out).page = u'1'
>>> zeit.cms.workflow.interfaces.IPublishInfo(article4).published = True
>>> article5 = zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/02/Vita')
>>> with zeit.cms.checkout.helper.checked_out(article5) as checked_out:
...     zeit.cms.content.interfaces.ICommonMetadata(
...         checked_out).printRessort = u'Feuilleton'
...     zeit.cms.content.interfaces.ICommonMetadata(
...         checked_out).page = u'1'
>>> zeit.cms.workflow.interfaces.IPublishInfo(article5).published = True
>>> zeit.archive.index.rebuildVolume('http://xml.zeit.de/2007/')

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print-volume" cp:__name__="Wirtschaft" title="Wirtschaft">
    <block href="http://xml.zeit.de/2007/01/Macher"...
      <supertitle py:pytype="str">Entwicklungshilfe</supertitle>...

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/02/index')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print-volume" cp:__name__="Feuilleton" title="Feuilleton">
    <block href="http://xml.zeit.de/2007/02/Vita"...

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/index')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print-year" cp:__name__="01" title="01">
    <block href="http://xml.zeit.de/2007/01/Miami"...
    </block>
    <block href="http://xml.zeit.de/2007/01/Macher"...
    </block>
  </container>
  <container cp:type="teaser" module="archive-print-year" cp:__name__="02" title="02">
    <block href="http://xml.zeit.de/2007/02/Vita"...
    </block>
  </container>
</region>


Clean up to test our event handler.

>>> import lovely.remotetask.interfaces
>>> import zope.component
>>> repository = zope.component.getUtility(
...     zeit.cms.repository.interfaces.IRepository)
>>> del repository['2007']['01']['index']
>>> print zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index', None)
None

>>> del repository['2007']['index']
>>> print zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/index', None)
None


Publish an unpublished article.

>>> workflow = zeit.workflow.interfaces.IContentWorkflow(article)
>>> publish = zeit.cms.workflow.interfaces.IPublish(article)
>>> workflow.published
False
>>> workflow.urgent = True
>>> workflow.can_publish()
True
>>> p = publish.publish()
>>> tasks = zope.component.getUtility(
...     lovely.remotetask.interfaces.ITaskService, 'general')
>>> tasks.process()
>>> workflow.published
True


Publish an already published article.

>>> workflow = zeit.workflow.interfaces.IContentWorkflow(article4)
>>> publish = zeit.cms.workflow.interfaces.IPublish(article4)
>>> workflow.published
True
>>> workflow.urgent = True
>>> workflow.can_publish()
True
>>> p = publish.publish()
>>> tasks = zope.component.getUtility(
...     lovely.remotetask.interfaces.ITaskService, 'general')
>>> tasks.process()
>>> workflow.published
True

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print-volume" cp:__name__="Reisen" title="Reisen">
    <block href="http://xml.zeit.de/2007/01/Miami"...
      <supertitle py:pytype="str">Florida</supertitle>...
  <container cp:type="teaser" module="archive-print-volume" cp:__name__="Wirtschaft" title="Wirtschaft">
    <block href="http://xml.zeit.de/2007/01/Macher"...
      <supertitle py:pytype="str">Entwicklungshilfe</supertitle>...

>>> with zeit.cms.checkout.helper.checked_out(article4) as checked_out:
...     zeit.cms.content.interfaces.ICommonMetadata(
...         checked_out).printRessort = u'Wirtschaft'
...     zeit.cms.content.interfaces.ICommonMetadata(
...         checked_out).page = u'1'

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/index')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print-year" cp:__name__="01" title="01">
    <block href="http://xml.zeit.de/2007/01/Macher"...
      <supertitle py:pytype="str">Entwicklungshilfe</supertitle>...
    <block href="http://xml.zeit.de/2007/01/Miami"...
      <supertitle py:pytype="str">Florida</supertitle>...


Delete an article to test our event handler.

>>> repository = zope.component.getUtility(
...     zeit.cms.repository.interfaces.IRepository)
>>> del repository['2007']['01']['Macher']
>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index')
>>> print lxml.etree.tostring(index['lead'].xml, pretty_print=True)
<region ...>
  <container cp:type="teaser" module="archive-print-volume" cp:__name__="Reisen" title="Reisen">
    <block href="http://xml.zeit.de/2007/01/Miami"...
      <supertitle py:pytype="str">Florida</supertitle>...


Check attribute values.

>>> print lxml.etree.tostring(index.xml, pretty_print=True)
<centerpage ... type="archive-print-volume">
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

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/index')
>>> print lxml.etree.tostring(index.xml, pretty_print=True)
<centerpage ... type="archive-print-year">
  <head>
    <attribute py:pytype="str" ns="http://namespaces.zeit.de/CMS/document" name="date-last-modified">...</attribute>
    <attribute py:pytype="str" ns="http://namespaces.zeit.de/CMS/document" name="last_modified_by">zope.user</attribute>
    <attribute py:pytype="str" ns="http://namespaces.zeit.de/CMS/meta" name="type">centerpage-2009</attribute>
    <attribute py:pytype="str" ns="http://namespaces.zeit.de/CMS/document" name="uuid">{urn:uuid:5b15e4ec-be2d-461d-b717-cba15096e44e}</attribute>
    <attribute py:pytype="str" ns="http://namespaces.zeit.de/CMS/document" name="year">2007</attribute>
  </head>
...
</centerpage>
<BLANKLINE>


When the archive CP isn't a CP but some other object it will just be
overwritten:

>>> import zeit.cms.repository.file
>>> repository['2007']['01']['index'] = (
...     zeit.cms.repository.file.LocalFile())
>>> article = zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/Martenstein')
>>> workflow = zeit.workflow.interfaces.IContentWorkflow(article)
>>> publish = zeit.cms.workflow.interfaces.IPublish(article)
>>> workflow.published
False
>>> workflow.urgent = True
>>> workflow.can_publish()
True
>>> p = publish.publish()
>>> import lovely.remotetask.interfaces
>>> import zope.component
>>> tasks = zope.component.getUtility(
...     lovely.remotetask.interfaces.ITaskService, 'general')
>>> tasks.process()
>>> workflow.published
True

>>> index =  zeit.cms.interfaces.ICMSContent(
...     'http://xml.zeit.de/2007/01/index')
>>> list(index['lead'])
['Leben']

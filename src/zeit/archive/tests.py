import unittest
import pkg_resources
import zeit.cms.testing
from zope.testing import doctest
import zope.app.testing.functional

ArchiveLayer = zope.app.testing.functional.ZCMLLayer(
    pkg_resources.resource_filename(__name__, 'ftesting.zcml'),
    __name__, 'ArchiveLayer', allow_teardown=True)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(zeit.cms.testing.FunctionalDocFileSuite(
        'README.txt',
        layer=ArchiveLayer,
        optionflags=doctest.ELLIPSIS
        ))

    return suite

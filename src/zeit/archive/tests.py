from zope.testing import doctest
import pkg_resources
import unittest
import zeit.cms.testing
import zeit.content.article.tests
import zeit.content.cp.testing
import zope.app.testing.functional


ArchiveLayer = zope.app.testing.functional.ZCMLLayer(
    pkg_resources.resource_filename(__name__, 'ftesting.zcml'),
    __name__, 'ArchiveLayer', allow_teardown=True)


# Use a rules file which contains only a syntax error so we don't have any
# rules.
cp_config = zeit.content.cp.testing.product_config['zeit.content.cp'].copy()
cp_config['rules-url'] = 'file://%s' % pkg_resources.resource_filename(
            'zeit.content.cp.tests.fixtures', 'syntax_error')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(zeit.cms.testing.FunctionalDocFileSuite(
        'README.txt',
        layer=ArchiveLayer,
        product_config={
            'zeit.content.article': zeit.content.article.tests.product_config,
            'zeit.content.cp': cp_config,
            'zeit.workflow': {'publish-script': 'cat',
                              'retract-script': 'cat',
                              'path-prefix': ''},
        }
    ))

    return suite

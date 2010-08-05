from zope.testing import doctest
import pkg_resources
import unittest
import zeit.cms.testing
import zeit.content.article.tests
import zeit.content.cp.testing
import zope.app.testing.functional


ArchiveZCMLLayer = zeit.cms.testing.ZCMLLayer(
    'ftesting.zcml',
    product_config=(
        zeit.cms.testing.cms_product_config +
        zeit.content.cp.testing.product_config))


class ArchiveLayer(ArchiveZCMLLayer):

    @classmethod
    def setUp(cls):
        # Use a rules file which contains only a syntax error so we don't have
        # any rules.
        cls.config = zope.app.appsetup.product.getProductConfiguration(
            'zeit.content.cp')
        cls.rules_url = cls.config['rules-url']
        cls.config['rules-url'] = 'file://%s' % (
            pkg_resources.resource_filename(
                'zeit.content.cp.tests.fixtures', 'syntax_error'))

    @classmethod
    def tearDown(cls):
        cls.config['rules-url'] = cls.rules_url
        del cls.config



def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(zeit.cms.testing.FunctionalDocFileSuite(
        'README.txt',
        'breadcrumbindex.txt',
        layer=ArchiveLayer,
        product_config={
            'zeit.content.article': zeit.content.article.tests.product_config,
            'zeit.workflow': {'publish-script': 'cat',
                              'retract-script': 'cat',
                              'path-prefix': ''},
        }
    ))

    return suite

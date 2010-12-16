from zope.testing import doctest
import pkg_resources
import unittest
import zeit.cms.testing
import zeit.content.article.testing
import zeit.content.cp.testing
import zeit.edit.testing
import zope.app.testing.functional


ArchiveZCMLLayer = zeit.cms.testing.ZCMLLayer(
    'ftesting.zcml',
    product_config=(
        zeit.cms.testing.cms_product_config +
        zeit.content.article.testing.product_config +
        zeit.content.cp.testing.product_config))


class ArchiveLayer(ArchiveZCMLLayer):

    @classmethod
    def setUp(cls):
        cls.config = zope.app.appsetup.product.getProductConfiguration(
            'zeit.edit')
        cls.rules_url = cls.config['rules-url']
        cls.config['rules-url'] = None

    @classmethod
    def tearDown(cls):
        cls.config['rules-url'] = cls.rules_url
        del cls.config



def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(zeit.cms.testing.FunctionalDocFileSuite(
        'breadcrumbindex.txt',
        layer=ArchiveLayer,
        product_config={
            'zeit.workflow': {'publish-script': 'cat',
                              'retract-script': 'cat',
                              'path-prefix': ''},
        }
    ))

    return suite

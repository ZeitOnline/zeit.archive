import mock
import pkg_resources
import plone.testing
import unittest
import zeit.cms.testing
import zeit.content.article.testing
import zeit.content.cp.testing
import zeit.workflow.testing
import zope.app.appsetup.product


ZCML_LAYER = zeit.cms.testing.ZCMLLayer(
    'ftesting.zcml',
    product_config=(
        zeit.cms.testing.cms_product_config +
        zeit.content.article.testing.product_config +
        zeit.workflow.testing.product_config +
        zeit.content.cp.testing.product_config))


class Layer(plone.testing.Layer):

    defaultBases = (ZCML_LAYER,)

    def setUp(self):
        # Use a rules file which contains only a syntax error so we don't have
        # any rules.
        self.config = zope.app.appsetup.product.getProductConfiguration(
            'zeit.edit')
        self.rules_url = self.config.get('rules-url')
        self.config['rules-url'] = 'file://%s' % (
            pkg_resources.resource_filename(
                'zeit.content.cp.tests.fixtures', 'syntax_error'))

    def tearDown(self):
        if self.rules_url is not None:
            self.config['rules-url'] = self.rules_url
        del self.config

LAYER = Layer()


class BreadcrumbIndexTest(zeit.cms.testing.FunctionalTestCase):

    layer = LAYER

    def setUp(self):
        super(BreadcrumbIndexTest, self).setUp()
        from zeit.cms.repository.folder import Folder
        self.repository['deutschland'] = Folder()
        self.ressort_month = self.repository['deutschland']['2009-11'] = \
            Folder()
        self.repository['deutschland']['integration'] = Folder()
        self.sub_ressort_month = \
            self.repository['deutschland']['integration']['2009-06'] = Folder()

    def get_article(self, **kw):
        article = zeit.content.article.article.Article()
        article.year = 2009
        for key, value in kw.items():
            setattr(article, key, value)
        return article

    def create(self, article):
        from zeit.archive.breadcrumbindex import (
            create_breadcrumb_index_on_publish)
        create_breadcrumb_index_on_publish(article, mock.sentinel.event)

    def test_no_create_on_name_ressort_mismatch_in_sub_ressort_folder(self):
        article = self.get_article(ressort=u'International')
        self.sub_ressort_month['art'] = article
        self.create(article)
        self.assertNotIn('index', self.ressort_month)
        self.assertNotIn('index', self.sub_ressort_month)

    def test_no_create_on_name_ressort_missmatch_in_ressort_folder(self):
        article = self.get_article(ressort=u'International')
        self.ressort_month['art'] = article
        self.create(article)
        self.assertNotIn('index', self.ressort_month)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BreadcrumbIndexTest))
    suite.addTest(zeit.cms.testing.FunctionalDocFileSuite(
        'breadcrumbindex.txt',
        layer=LAYER,
    ))
    return suite

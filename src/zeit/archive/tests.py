# Copyright (c) 2011-2012 gocept gmbh & co. kg
# See also LICENSE.txt

import mock
import pkg_resources
import unittest
import zeit.cms.testing
import zeit.content.article.tests
import zeit.content.cp.testing
import zeit.workflow.testing
import zope.app.testing.functional


ArchiveZCMLLayer = zeit.cms.testing.ZCMLLayer(
    'ftesting.zcml',
    product_config=(
        zeit.cms.testing.cms_product_config +
        zeit.content.article.tests.product_config +
        zeit.workflow.testing.product_config +
        zeit.content.cp.testing.product_config))


class ArchiveLayer(ArchiveZCMLLayer):

    @classmethod
    def setUp(cls):
        # Use a rules file which contains only a syntax error so we don't have
        # any rules.
        cls.config = zope.app.appsetup.product.getProductConfiguration(
            'zeit.content.cp')
        cls.rules_url = cls.config.get('rules-url')
        cls.config['rules-url'] = 'file://%s' % (
            pkg_resources.resource_filename(
                'zeit.content.cp.tests.fixtures', 'syntax_error'))

    @classmethod
    def tearDown(cls):
        if cls.rules_url is not None:
            cls.config['rules-url'] = cls.rules_url
        del cls.config


class BreadcrumbIndexTest(zeit.cms.testing.FunctionalTestCase):

    layer = ArchiveLayer

    def setUp(self):
        super(BreadcrumbIndexTest, self).setUp()
        from zeit.cms.repository.folder import Folder
        self.repository['deutschland'] = Folder()
        self.ressort_month = \
                self.repository['deutschland']['2009-11'] = \
            Folder()
        self.repository['deutschland']['integration'] = Folder()
        self.sub_ressort_month = \
                self.repository['deutschland']['integration']['2009-06'] = \
                Folder()

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

    def test_should_not_create_on_name_ressort_missmatch_in_sub_ressort_folder(self):
        article = self.get_article(ressort=u'International')
        self.sub_ressort_month['art'] = article
        self.create(article)
        self.assertNotIn('index', self.ressort_month)
        self.assertNotIn('index', self.sub_ressort_month)

    def test_should_not_create_on_name_ressort_missmatch_in_ressort_folder(self):
        article = self.get_article(ressort=u'International')
        self.ressort_month['art'] = article
        self.create(article)
        self.assertNotIn('index', self.ressort_month)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BreadcrumbIndexTest))
    suite.addTest(zeit.cms.testing.FunctionalDocFileSuite(
        'breadcrumbindex.txt',
        layer=ArchiveLayer,
    ))

    return suite

# Copyright (c) 2008-2009 gocept gmbh & co. kg
# See also LICENSE.txt

import zope.component
import zope.interface

import zeit.archive.interfaces
import zeit.content.article.interfaces
import zeit.workflow.interfaces


class PublicationDependencies(object):
    """Article dependencies."""

    zope.interface.implements(
        zeit.workflow.interfaces.IPublicationDependencies)
    zope.component.adapts(
        zeit.content.article.interfaces.IArticle)

    def __init__(self, context):
        self.context = context

    def get_dependencies(self):
        indexes = []
        volume_index = zeit.content.cp.interfaces.ICenterPage(
            self.context.__parent__['index'], None)
        if volume_index is not None:
            indexes.append(volume_index)
        year_index = zeit.content.cp.interfaces.ICenterPage(
            self.context.__parent__.__parent__['index'], None)
        if year_index is not None:
            indexes.append(year_index)
        return indexes

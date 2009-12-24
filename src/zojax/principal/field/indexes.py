##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.app.intid.interfaces import IIntIds
from zc.catalog.catalogindex import ValueIndex, SetIndex
from zojax.catalog.utils import Indexable
from zojax.principal.field.interfaces import IPrincipal, IUser, IGroup


def principalId():
    return ValueIndex(
        'value', Indexable('zojax.principal.field.indexes.PrincipalId'))


def principalType():
    return SetIndex(
        'value', Indexable('zojax.principal.field.indexes.PrincipalType'))


def principalTitle():
    return ValueIndex(
        'value', Indexable('zojax.principal.field.indexes.PrincipalTitle'))


class PrincipalId(object):

    def __init__(self, content, default=None):
        self.value = default

        if IPrincipal.providedBy(content):
            self.value = content.id


class PrincipalType(object):

    def __init__(self, content, default=None):
        self.value = default

        if IUser.providedBy(content):
            self.value = ('user',)

        if IGroup.providedBy(content):
            self.value = ('group',)


class PrincipalTitle(object):

    def __init__(self, content, default=None):
        self.value = default

        if IPrincipal.providedBy(content):
            self.value = getattr(content, 'title', u'')

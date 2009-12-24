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
""" principal fields implmentation

$Id$
"""

from zope import schema, interface
from zope.component import getUtility
from zope.schema.interfaces import IFromUnicode
from zope.security.interfaces import IGroup, IPrincipal
from zope.app.security.interfaces import IAuthentication, PrincipalLookupError

from interfaces import IUserField, IGroupField, IPrincipalField, InvalidPrincipal


class PrincipalField(schema.Field):
    interface.implements(IFromUnicode, IPrincipalField)

    def fromUnicode(self, value):
        return unicode(value)


class UserField(PrincipalField):
    interface.implements(IUserField)

    def _validate(self, value):
        super(PrincipalField, self)._validate(value)

        try:
            principal = getUtility(IAuthentication).getPrincipal(value)
        except PrincipalLookupError:
            raise InvalidPrincipal(value)

        if IGroup.providedBy(principal):
            raise InvalidPrincipal(value)


class GroupField(PrincipalField):
    interface.implements(IGroupField)

    def _validate(self, value):
        super(PrincipalField, self)._validate(value)

        try:
            principal = getUtility(IAuthentication).getPrincipal(value)
        except PrincipalLookupError:
            raise InvalidPrincipal(value)

        if not IGroup.providedBy(principal):
            raise InvalidPrincipal(value)

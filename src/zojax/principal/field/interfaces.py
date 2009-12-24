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
""" zojax.principal.field interfaces

$Id$
"""
from zope import schema, interface
from zope.i18nmessageid import MessageFactory
from z3c.form.interfaces import IWidget

_ = MessageFactory('zojax.principal.field')


class InvalidPrincipal(schema.ValidationError):
    __doc__ = _("""The specified id is not valid principal id.""")


class IPrincipalField(interface.Interface):
    """ principal id field """


class IUserField(IPrincipalField):
    """ user principal id field """


class IGroupField(IPrincipalField):
    """ group principal id field """


class IPrincipalWidget(IWidget):
    """ principal widget """


class IPrincipalsWidget(IWidget):
    """ principals widget """


# principal types
class IPrincipal(interface.Interface):
    """ principal """

    id = interface.Attribute('Principal Id')

    title = interface.Attribute('Principal title')


class IUser(IPrincipal):
    """ user principal """


class IGroup(IPrincipal):
    """ group principal """

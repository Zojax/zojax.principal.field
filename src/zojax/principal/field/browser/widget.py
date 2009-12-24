##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
from zope import interface, component
from zope.component import getUtility, getMultiAdapter, queryMultiAdapter
from zope.schema.interfaces import IField, ICollection
from zope.traversing.api import getPath
from zope.session.interfaces import ISession
from zope.app.security.interfaces import IAuthentication

from z3c.form import interfaces, converter
from z3c.form.widget import Widget, FieldWidget
from z3c.form.browser import widget

from zojax.batching.session import SessionBatch
from zojax.catalog.interfaces import ICatalogConfiglet
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.principal.field.interfaces import \
    IUser, IUserField, IGroupField, \
    IPrincipalField, IPrincipalWidget, IPrincipalsWidget
from zojax.principal.field.utils import searchPrincipals

SESSIONKEY = 'zojax.batching'


class BasePrincipalWidget(widget.HTMLInputWidget, Widget):

    pageSize = 20

    def update(self):
        name = self.name
        request = self.request
        context = self.form.context

        self.auth = getUtility(IAuthentication)

        key = u'%s:%s'%(getPath(context), name)
        self.sessionKey = key
        self.selectedName = u'%s-selectedItem'%name

        super(BasePrincipalWidget, self).update()

        tp = []
        if IUserField.providedBy(self.field):
            tp = ('user',)
        elif IGroupField.providedBy(self.field):
            tp = ('group',)
        else:
            tp = ('user', 'group')

        # search text
        data = ISession(request)[SESSIONKEY]
        if '%s-empty-marker'%name not in request and key in data:
            del data[key]

        if u'%s.searchButton'%name in request:
            searching = True
            searchtext = request.get(u'%s.searchText'%name, u'')
            data[key] = (searchtext, True)
            if searchtext:
                try:
                    principals = searchPrincipals(
                        tp, searchableText = searchtext)
                except:
                    principals = []
            else:
                principals = []
        elif u'%s.searchClear'%name in request:
            if key in data:
                del data[key]
            searchtext = u''
            searching = False
            principals = searchPrincipals(tp)
        else:
            searchtext, searching = data.get(key, (u'', False))
            if searchtext:
                try:
                    principals = searchPrincipals(
                        tp, searchableText = searchtext)
                except:
                    principals = []
            else:
                principals = searchPrincipals(tp)

        self.searching = searching
        self.searchtext = searchtext

        self.principals = SessionBatch(
            principals, size=self.pageSize,
            context=context, request=request, prefix=name,
            queryparams = {'%s-empty-marker'%self.name: '1'})

    def getPrincipalInfo(self, principal):
        title = principal.title

        try:
            profile = IPersonalProfile(
                self.auth.getPrincipal(principal.id))
            title = profile.title
        except:
            pass

        info = {'id': principal.id,
                'title': title,
                'user': IUser.providedBy(principal)}
        return info


class PrincipalWidget(BasePrincipalWidget):
    interface.implementsOnly(IPrincipalWidget)

    def getSelected(self):
        auth = getUtility(IAuthentication)

        try:
            return auth.getPrincipal(self.value)
        except:
            pass

    def extract(self, default=interfaces.NOVALUE):
        request = self.request

        value = request.get(self.name, default)
        if value is default:
            value = request.get(self.selectedName, default)

        return value


@component.adapter(IPrincipalField, interfaces.IFormLayer)
@interface.implementer(interfaces.IFieldWidget)
def PrincipalFieldWidget(field, request):
    """IFieldWidget factory for PrincipalWidget."""
    return FieldWidget(field, PrincipalWidget(request))


class PrincipalsWidget(BasePrincipalWidget):
    interface.implementsOnly(IPrincipalsWidget)

    def update(self):
        super(PrincipalsWidget, self).update()

        name = self.name
        request = self.request

        self.auth = getUtility(IAuthentication)

        if not self.value:
            self.value = ()

        sessiondata = ISession(request)[SESSIONKEY]
        key = u'%s:selected'%self.sessionKey

        if '%s-empty-marker'%name not in request and key in sessiondata:
            del sessiondata[key]

        if key in sessiondata:
            self.value = sessiondata[key]

        self.value = list(self.value)

        sessiondata[key] = self.value

        if u'%s.selectPrincipal'%name in request:
            value = self.value
            for pid in request.get(name, ()):
                if pid not in value:
                    try:
                        principal = self.auth.getPrincipal(pid)
                    except:
                        continue

                    value.append(pid)

            self.value = value
            sessiondata[key] = value

        if u'%s.removeSelected'%name in request:
            value = self.value
            for pid in request.get(u'%s.selected'%name, ()):
                if pid in value:
                    value.remove(pid)

            self.value = value
            sessiondata[key] = value

        if u'%s.clearSelected'%name in request:
            sessiondata[key] = []
            self.value = []

        # check if value changed
        dm = getMultiAdapter(
            (self.context, self.field), interfaces.IDataManager)
        try:
            value = list(dm.query())
        except:
            value = []

        if value != self.value:
            self.changed = True
        else:
            self.changed = False

    def getSelected(self):
        principals = []

        if self.value:
            for pid in self.value:
                try:
                    principal = self.auth.getPrincipal(pid)
                except:
                    continue

                profile = IPersonalProfile(principal)

                principals.append(
                    {'id': principal.id,
                     'title': profile.title,
                     })

        return principals

    def extract(self, default=interfaces.NOVALUE):
        request = self.request
        sessiondata = ISession(request)[SESSIONKEY]
        key = u'%s:selected'%self.sessionKey

        if self.name not in request and key not in sessiondata:
            return default

        value = request.get(self.name, default)

        if '%s-empty-marker'%self.name in request:
            if key in sessiondata:
                if value is default:
                    value = []
                for pid in sessiondata[key]:
                    if pid in value:
                        continue
                    value.append(pid)
            elif value:
                sessiondata[key] = value

        if not value and self.field.required:
            return default

        return value


@component.adapter(ICollection, IPrincipalField, interfaces.IFormLayer)
@interface.implementer(interfaces.IFieldWidget)
def PrincipalsFieldWidget(field, value_type, request):
    """IFieldWidget factory for PrincipalWidget."""
    return FieldWidget(field, PrincipalsWidget(request))


class PrincipalsWidgetConverter(converter.BaseDataConverter):
    component.adapts(IField, IPrincipalsWidget)

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return []
        return value

    def toFieldValue(self, value):
        value = [elem.strip() for elem in value]

        if hasattr(self.field, '_type'):
            value = self.field._type(value)

        return value

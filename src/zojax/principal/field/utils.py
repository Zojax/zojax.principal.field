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
from zope.component import getUtility
from zope.component.interfaces import IComponentLookup
from zojax.catalog.interfaces import ICatalogConfiglet


def searchPrincipals(type=(('user', 'group')), **kwargs):
    catalog = getUtility(ICatalogConfiglet).catalog

    return catalog.searchResults(
        sort_on='principalTitle', principalType={'any_of': type},
        noSecurityChecks=True,
        searchContext=IComponentLookup(catalog).__parent__, **kwargs)

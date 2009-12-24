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
import os
import unittest, doctest
from zope import interface
from zope.component import getUtility
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.app.testing import functional
from zope.app.rotterdam import Rotterdam
from zope.app.component.hooks import setSite
from zope.app.security.interfaces import IAuthentication
from zojax.catalog.catalog import Catalog, ICatalog
from zojax.layoutform.interfaces import ILayoutFormLayer


class IDefaultSkin(ILayoutFormLayer, Rotterdam):
    """ skin """


zojaxPrincipalField = functional.ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxPrincipalField', allow_teardown=True)


def FunctionalDocFileSuite(*paths, **kw):
    globs = kw.setdefault('globs', {})
    globs['http'] = functional.HTTPCaller()
    globs['getRootFolder'] = functional.getRootFolder

    kw['package'] = doctest._normalize_module(kw.get('package'))

    kwsetUp = kw.get('setUp')
    def setUp(test):
        functional.FunctionalTestSetup().setUp()

        root = functional.getRootFolder()
        setSite(root)

        root['ids'] = IntIds()
        root.getSiteManager().registerUtility(root['ids'], IIntIds)

        root['catalog'] = Catalog()
        root.getSiteManager().registerUtility(root['catalog'], ICatalog)

        if kwsetUp is not None:
            kwsetUp(test)

    kw['setUp'] = setUp

    kwtearDown = kw.get('tearDown')
    def tearDown(test):
        if kwtearDown is not None:
            kwtearDown(test)
        functional.FunctionalTestSetup().tearDown()
    kw['tearDown'] = tearDown

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old
                             | doctest.ELLIPSIS
                             | doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = zojaxPrincipalField
    return suite


def test_suite():
    return unittest.TestSuite((
            FunctionalDocFileSuite("testbrowser.txt"),))

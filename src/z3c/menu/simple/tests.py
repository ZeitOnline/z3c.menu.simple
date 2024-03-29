##############################################################################
#
# Copyright (c) 2005 Zope Foundation and Contributors.
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
$Id: tests.py 114728 2010-07-14 06:53:53Z icemac $
"""
__docformat__ = 'restructuredtext'

import re
import unittest
import zope.security
import doctest
from zope.app.testing import setup, ztapi


# Strip out u'' literals in doctests, adapted from
# <https://stackoverflow.com/a/56507895>.
class Py23OutputChecker(doctest.OutputChecker, object):
    RE = re.compile(r"(\W|^)[uU]([rR]?[\'\"])", re.UNICODE)

    def remove_u(self, want, got):
        return (re.sub(self.RE, r'\1\2', want),
                re.sub(self.RE, r'\1\2', got))

    def check_output(self, want, got, optionflags):
        want, got = self.remove_u(want, got)
        return super(Py23OutputChecker, self).check_output(
            want, got, optionflags)

    def output_difference(self, example, got, optionflags):
        example.want, got = self.remove_u(example.want, got)
        return super(Py23OutputChecker, self).output_difference(
            example, got, optionflags)


class TestParticipation(object):
    principal = 'foobar'
    interaction = None


def setUp(test):
    root = setup.placefulSetUp(site=True)
    test.globs['root'] = root

    # resource namespace setup
    from zope.traversing.interfaces import ITraversable
    from zope.traversing.namespace import resource
    ztapi.provideAdapter(None, ITraversable, resource, name="resource")
    ztapi.provideView(None, None, ITraversable, "resource", resource)

    from zope.browserpage import metaconfigure
    from zope.contentprovider import tales
    metaconfigure.registerType('provider', tales.TALESProviderExpression)

    zope.security.management.getInteraction().add(TestParticipation())


def tearDown(test):
    setup.placefulTearDown()


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'README.txt',
            setUp=setUp, tearDown=tearDown,
            checker=Py23OutputChecker(),
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
        ),
    ))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

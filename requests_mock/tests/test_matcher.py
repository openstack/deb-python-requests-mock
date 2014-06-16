# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import requests

from requests_mock import adapter
from requests_mock.tests import base


class TestMatcher(base.TestCase):

    def match(self,
              target,
              url,
              matcher_method='GET',
              request_method='GET',
              complete_qs=False):
        matcher = adapter._Matcher(matcher_method, target, [], complete_qs)
        request = requests.Request(request_method, url).prepare()
        return matcher.match(request)

    def assertMatch(self,
                    target,
                    url,
                    matcher_method='GET',
                    request_method='GET',
                    **kwargs):
        self.assertEqual(True,
                         self.match(target,
                                    url,
                                    matcher_method=matcher_method,
                                    request_method=request_method,
                                    **kwargs),
                         'Matcher %s %s failed to match %s %s' %
                         (matcher_method, target, request_method, url))

    def assertMatchBoth(self,
                        target,
                        url,
                        matcher_method='GET',
                        request_method='GET',
                        **kwargs):
        self.assertMatch(target,
                         url,
                         matcher_method=matcher_method,
                         request_method=request_method,
                         **kwargs)
        self.assertMatch(url,
                         target,
                         matcher_method=request_method,
                         request_method=matcher_method,
                         **kwargs)

    def assertNoMatch(self,
                      target,
                      url,
                      matcher_method='GET',
                      request_method='GET',
                      **kwargs):
        self.assertEqual(False,
                         self.match(target,
                                    url,
                                    matcher_method=matcher_method,
                                    request_method=request_method,
                                    **kwargs),
                         'Matcher %s %s unexpectedly matched %s %s' %
                         (matcher_method, target, request_method, url))

    def assertNoMatchBoth(self,
                          target,
                          url,
                          matcher_method='GET',
                          request_method='GET',
                          **kwargs):
        self.assertNoMatch(target,
                           url,
                           matcher_method=matcher_method,
                           request_method=request_method,
                           **kwargs)
        self.assertNoMatch(url,
                           target,
                           matcher_method=request_method,
                           request_method=matcher_method,
                           **kwargs)

    def assertMatchMethodBoth(self, matcher_method, request_method, **kwargs):
        url = 'http://www.test.com'

        self.assertMatchBoth(url,
                             url,
                             request_method=request_method,
                             matcher_method=matcher_method,
                             **kwargs)

    def assertNoMatchMethodBoth(self,
                                matcher_method,
                                request_method,
                                **kwargs):
        url = 'http://www.test.com'

        self.assertNoMatchBoth(url,
                               url,
                               request_method=request_method,
                               matcher_method=matcher_method,
                               **kwargs)

    def test_url_matching(self):
        self.assertMatchBoth('http://www.test.com',
                             'http://www.test.com')
        self.assertMatchBoth('http://www.test.com',
                             'http://www.test.com/')
        self.assertMatchBoth('http://www.test.com/abc',
                             'http://www.test.com/abc')
        self.assertMatchBoth('http://www.test.com:5000/abc',
                             'http://www.test.com:5000/abc')

        self.assertNoMatchBoth('https://www.test.com',
                               'http://www.test.com')
        self.assertNoMatchBoth('http://www.test.com/abc',
                               'http://www.test.com')
        self.assertNoMatchBoth('http://test.com',
                               'http://www.test.com')
        self.assertNoMatchBoth('http://test.com',
                               'http://www.test.com')
        self.assertNoMatchBoth('http://test.com/abc',
                               'http://www.test.com/abc/')
        self.assertNoMatchBoth('http://test.com/abc/',
                               'http://www.test.com/abc')
        self.assertNoMatchBoth('http://test.com:5000/abc/',
                               'http://www.test.com/abc')
        self.assertNoMatchBoth('http://test.com/abc/',
                               'http://www.test.com:5000/abc')

    def test_subset_match(self):
        self.assertMatch('/path', 'http://www.test.com/path')
        self.assertMatch('/path', 'http://www.test.com/path')
        self.assertMatch('//www.test.com/path', 'http://www.test.com/path')
        self.assertMatch('//www.test.com/path', 'https://www.test.com/path')

    def test_query_string(self):
        self.assertMatch('/path?a=1&b=2',
                         'http://www.test.com/path?a=1&b=2')
        self.assertMatch('/path?a=1',
                         'http://www.test.com/path?a=1&b=2',
                         complete_qs=False)
        self.assertNoMatch('/path?a=1',
                           'http://www.test.com/path?a=1&b=2',
                           complete_qs=True)
        self.assertNoMatch('/path?a=1&b=2',
                           'http://www.test.com/path?a=1')

    def test_method_match(self):
        self.assertNoMatchMethodBoth('GET', 'POST')
        self.assertMatchMethodBoth('GET', 'get')
        self.assertMatchMethodBoth('GeT', 'geT')

# coding=utf-8
"""
 Licensed to the Apache Software Foundation (ASF) under one or more
 contributor license agreements.  See the NOTICE file distributed with
 this work for additional information regarding copyright ownership.
 The ASF licenses this file to You under the Apache License, Version 2.0
 (the "License"); you may not use this file except in compliance with
 the License.  You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

"""
import unittest
from dubbo_client import ZookeeperRegistry, DubboClient, DubboClientError, Application, MulticastRegistry


class TestRpclib(unittest.TestCase):

    def test_something(self):
        application_name = 'test_rpclib'
        address = '224.5.6.7:1234'
        service = 'com.unj.dubbotest.provider.DemoService'
        config = Application(application_name)
        registry = MulticastRegistry(address)
        user_provider = DubboClient(service, registry)
        result = user_provider.sayHello('World')
        self.assertEqual(result, 'Hello World')


if __name__ == '__main__':
    testSuite = unittest.TestSuite()
    testSuite.addTest(TestRpclib('test_something'))
    unittest.TextTestRunner().run(testSuite)

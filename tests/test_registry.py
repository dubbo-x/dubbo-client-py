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
from dubbo_client import Application
from dubbo_client import Registry, ZookeeperRegistry, MulticastRegistry

application_config = Application('app_consumer')


class TestRegistry(unittest.TestCase):

    def test_registry(self):
        registry = Registry()
        registry._add_node("com.ofpay.demo.api.UserProvider",
                           "jsonrpc://192.168.2.1:38081/com.ofpay.demo.api.UserProvider2?"
                           "anyhost=true&application=jsonrpcdemo&default.timeout=10000&"
                           "dubbo=2.4.10&environment=product&interface=com.ofpay.demo.api.UserProvider&"
                           "methods=getUser,queryAll,isLimit,queryUser&owner=wenwu&pid=60402&revision=2.0&"
                           "side=provider&timestamp=1429105028153&version=2.0")
        registry._add_node("com.ofpay.demo.api.UserProvider",
                           "jsonrpc://192.168.2.1:38081/com.ofpay.demo.api.UserProvider?"
                           "anyhost=true&application=jsonrpcdemo&default.timeout=10000&"
                           "dubbo=2.4.10&environment=product&interface=com.ofpay.demo.api.UserProvider&"
                           "methods=getUser,queryAll,isLimit,queryUser&owner=wenwu&pid=60402&revision=2.0&"
                           "side=provider&timestamp=1429105028153&version=1.0")
        assert registry._service_providers

    def test_multicast_registry(self):
        address = '224.5.6.7:1234'
        interface = 'dubbo.DubboService'
        registry = MulticastRegistry(address, application_config)
        registry.register(interface)
        registry.subscribe(interface)
        print(registry.get_providers(interface))
        registry.unregister(interface)
        registry.unsubscribe(interface)

    def test_zookeeper_registry(self):
        address = '127.0.0.1:2181'
        interface = 'dubbo.DubboService'
        registry = ZookeeperRegistry(address, application_config)
        registry.subscribe(interface)
        print(registry.get_providers(interface))


if __name__ == '__main__':
    testSuite = unittest.TestSuite()
    # testSuite.addTest(TestRegistry('test_registry'))
    # testSuite.addTest(TestRegistry('test_multicast_registry'))
    testSuite.addTest(TestRegistry('test_zookeeper_registry'))
    unittest.TextTestRunner().run(testSuite)

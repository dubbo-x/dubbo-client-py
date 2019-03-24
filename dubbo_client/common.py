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

from urlparse import urlparse, parse_qsl


class Constants(object):

    DUBBO = 'dubbo'
    PROVIDER = 'provider'
    CONSUMER = 'consumer'
    REGISTER = 'register'
    UNREGISTER = 'unregister'
    SUBSCRIBE = 'subscribe'
    UNSUBSCRIBE = 'unsubscribe'
    CATEGORY_KEY = 'category'
    PROVIDERS_CATEGORY = 'providers'
    CONSUMERS_CATEGORY = 'consumers'
    ROUTES_CATEGORY = 'routers'
    DYNAMIC_ROUTES_CATEGORY = 'dynamicrouters'
    CONFIGURATORS_CATEGORY = 'configurators'
    DYNAMIC_CONFIGURATORS_CATEGORY = 'dynamicconfigurators'
    APP_DYNAMIC_CONFIGURATORS_CATEGORY = 'appdynamicconfigurators'
    DEFAULT_CATEGORY = PROVIDERS_CATEGORY
    DEFAULT_PROTOCOL = 'dubbo'
    SIDE_KEY = 'side'
    PROVIDER_SIDE = 'provider'
    CONSUMER_SIDE = 'consumer'
    DEFAULT_REGISTRY = 'dubbo'
    ANYHOST_KEY = 'anyhost'
    ANYHOST_VALUE = '0.0.0.0'
    LOCALHOST_KEY = 'localhost'
    LOCALHOST_VALUE = '127.0.0.1'
    APPLICATION_KEY = 'application'
    PROTOCOL_KEY = 'protocol'
    DUBBO_PROTOCOL = DUBBO
    METHODS_KEY = 'methods'
    PID_KEY = 'pid'
    TIMESTAMP_KEY = 'timestamp'
    CHECK_KEY = 'check'
    REGISTER_KEY = 'register'
    SUBSCRIBE_KEY = 'subscribe'
    INTERFACE_KEY = 'interface'
    DUBBO_VERSION_KEY = 'dubbo'
    PROVIDER_PROTOCOL = 'provider'
    CONSUMER_PROTOCOL = 'consumer'
    JSONRPC_PROTOCOL = 'jsonrpc'


def simple_urlencode(query):
    query = query.items()
    l = []
    for k, v in query:
        k = str(k)
        v = str(v)
        l.append(k + '=' + v)
    return '&'.join(l)


class ServiceURL(object):
    protocol = 'jsonrpc'
    location = ''  # ip+port
    path = ''  # like /com.qianmi.dubbo.UserProvider
    ip = '127.0.0.1'
    port = '9090'
    version = ''
    group = ''
    disabled = False
    weight = 100
    has_disable_value = False
    has_weight_value = False

    def __init__(self, url):
        result = urlparse(url)
        self.protocol = result[0]
        self.location = result[1]
        self.path = result[2]
        if self.location.find(':') > -1:
            self.ip, self.port = result[1].split(':')
        params = parse_qsl(result[4])
        for key, value in params:
            # url has a default.timeout property, but it can not add in python object
            # so keep the last one
            pos = key.find('.')
            if pos > -1:
                key = key[pos + 1:]
            # print key
            if key == 'disabled':
                value = value.lower() == 'true' if value else False
                self.has_disable_value = True
            elif key == 'weight':
                value = int(value) if value else 100
                self.has_weight_value = True
            self.__dict__[key] = value

    def __repr__(self):
        return str(self.__dict__)

    def init_default_config(self):
        """
        恢复默认设置，dubbo配置是覆盖形式，如果恢复默认值，那么configurators下的配置会被清空
        :return:
        """
        self.disabled = False
        self.weight = 100

    def set_config(self, url_list):
        """
        设置自定义dubbo配置
        :param url_list:
        :return:
        """
        if not url_list:
            return

        param_list = []
        for configuration_url in url_list:
            result = urlparse(configuration_url)
            params = parse_qsl(result[4])
            param_list.extend(params)
        has_disable_value = False
        has_weight_value = False
        for key, value in param_list:
            if key == 'disabled':
                self.disabled = value.lower() == 'true' if value else False
                has_disable_value = True
            if key == 'weight':
                self.weight = int(value) if value else 100
                has_weight_value = True

        if not has_disable_value:
            self.disabled = False
        if not has_weight_value:
            self.weight = 100


class URLBuilder(object):

    def __init__(self):
        self.protocol = ''
        self.host = ''
        self.port = 0
        self.interface = ''
        self.params = dict()

    def set_protocol(self, protocol):
        self.protocol = protocol
        return self

    def set_host(self, host):
        self.host = host
        return self

    def set_port(self, port):
        self.port = port
        return self

    def set_interface(self, interface):
        self.interface = interface
        return self

    def add_param(self, k, v):
        self.params[k] = v
        return self

    def build(self):
        address = self.host if self.port == 0 else '{0}:{1}'.format(self.host, self.port)
        kv = simple_urlencode(self.params)
        url = '{0}://{1}/{2}?{3}'.format(
            self.protocol,
            address,
            self.interface,
            kv
        )
        return url

from api import RestApi


URLS = {'/': (RestApi.index, ['POST', 'GET']),
        '/index': (RestApi.index, ['POST', 'GET']),
        '/BulkCalls': (RestApi.BulkCalls, ['POST', 'GET']),
        '/Call': (RestApi.Call, ['POST', 'GET']),
        '/TestApp': (RestApi.TestApp, ['POST', 'GET']),
        '/TestRequest': (RestApi.TestRequest, ['POST', 'GET']),
        '/TestAttr': (RestApi.TestAttr, ['POST', 'GET']),
        '/TestConfig': (RestApi.TestConfig, ['POST', 'GET']),
       }


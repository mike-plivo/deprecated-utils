from api import RestApi



URLS = {'/': RestApi.index,
        '/index': RestApi.index,
        '/BulkCalls': RestApi.BulkCalls,
        '/Call': RestApi.Call,
        '/TestApp': RestApi.TestApp,
        '/TestRequest': RestApi.TestRequest,
        '/TestAttr': RestApi.TestAttr,
        '/TestConfig': RestApi.TestConfig,
       }


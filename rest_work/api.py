from flask import request

class RestApi(object):
    def TestApp(self):
        '''Test to access flask application object'''
        return str(self.app)

    def TestAttr(self):
        '''Test to get instance attribute'''
        return self.name

    def TestConfig(self):
        '''Test to get config parameter'''
        return self.app.config['FS_INBOUND_ADDRESS']

    def TestRequest(self):
        '''Test HTTP GET/POST'''
        if request.method == 'GET':
            return "GET => " + str(request.args)
        elif request.method == 'POST':
            return "POST => " + str(request.form)

    def Call(self):
        '''Fake Call'''
        return 'Call'

    def BulkCalls(self):
        '''Fake BulkCalls'''
        return "BulkCalls"

    def _NotExposed(self):
        '''This function is not exposed to rest server'''
        return 'NotExposed'

    def index(self):
        result = []
        for func in dir(RestApi):
            if func[0] != '_':
                result.append(func)
        return '<br/>'.join(result)



from gevent.wsgi import WSGIServer
from flask import Flask
from plivo.core.freeswitch.inboundsocket import InboundEventSocket
from config import Config
from api import RestApi



class RestServer(InboundEventSocket, RestApi):
    name = "RestServer"

    def __init__(self, configfile):
        # create flask app
        self.app = Flask(self.name)
        # create and load config
        self.config = Config(configfile)
        # load config into flask app
        self.app.config.from_object(self.config)
        # create rest server
        fs_host, fs_port = self.config['FS_INBOUND_ADDRESS'].split(':', 1)
        fs_port = int(fs_port)
        fs_password = self.config['FS_PASSWORD']
        InboundEventSocket.__init__(self, fs_host, fs_port, fs_password, filter='ALL')
        # TODO self.connect()
        # expose api functions to flask app
        for func in dir(RestApi):
            if func[0] != '_':
                fn = getattr(self, func)
                self.app.add_url_rule('/'+func, func, fn)
                # if index, root path is redirected to index endpoint
                if func == 'index':
                    self.app.add_url('/', func, fn)
        # create wsgi server
        http_host, http_port = self.config['HTTP_ADDRESS'].split(':', 1)
        http_port = int(http_port)
        self.http_server = WSGIServer((http_host, http_port), self.app)

    def start(self):
        # run
        self.app.debug = True
        #self.app.run()
        self.http_server.serve_forever()


if __name__ == '__main__':
    server = RestServer(configfile='./restserver.conf')
    server.start()



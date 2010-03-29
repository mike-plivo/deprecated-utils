import cc.web

def application(environ, start_response):
  status, output = cc.web.dispatch(environ)

  response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
  start_response(status, response_headers)

  return [output]

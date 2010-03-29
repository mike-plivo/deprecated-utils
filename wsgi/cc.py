import cc.actions

def application(environ, start_response):
  req = cc.actions.Process(environ)
  status, output = req.run()

  response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
  start_response(status, response_headers)

  return [output]

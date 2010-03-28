#debug = False
import time

try:
  import json
except ImportError:
  import simplejson as json  



def application(environ, start_response):
  status = '200 OK'

  if environ['PATH_INFO'] == '/' or environ['PATH_INFO'] == '':
    output = 'Hello World!\n'
  elif environ['PATH_INFO'] == '/sleep':
    time.sleep(30.0)
    output = 'Sleep done\n'
  elif environ['PATH_INFO'] == '/selfhangup':
    var = {'action':'selfhangup', 'result':True}
    output = json.dumps(var)
  else:
    output = 'Not found\n'
    status = '404 Not found'

  #if debug:
  #  output += "\n" + "="*15 + "\n".join([ str(k)+': '+str(environ[k]) for k in environ ])

  response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
  start_response(status, response_headers)

  return [output]

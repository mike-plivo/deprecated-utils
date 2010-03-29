import string
import cgi
import cc
import cc.actions as actions

try:
  import json
except ImportError:
  import simplejson as json



CODES = {
    100: 'CONTINUE',
    101: 'SWITCHING PROTOCOLS',
    200: 'OK',
    201: 'CREATED',
    202: 'ACCEPTED',
    203: 'NON-AUTHORITATIVE INFORMATION',
    204: 'NO CONTENT',
    205: 'RESET CONTENT',
    206: 'PARTIAL CONTENT',
    300: 'MULTIPLE CHOICES',
    301: 'MOVED PERMANENTLY',
    302: 'FOUND',
    303: 'SEE OTHER',
    304: 'NOT MODIFIED',
    305: 'USE PROXY',
    306: 'RESERVED',
    307: 'TEMPORARY REDIRECT',
    400: 'BAD REQUEST',
    401: 'UNAUTHORIZED',
    402: 'PAYMENT REQUIRED',
    403: 'FORBIDDEN',
    404: 'NOT FOUND',
    405: 'METHOD NOT ALLOWED',
    406: 'NOT ACCEPTABLE',
    407: 'PROXY AUTHENTICATION REQUIRED',
    408: 'REQUEST TIMEOUT',
    409: 'CONFLICT',
    410: 'GONE',
    411: 'LENGTH REQUIRED',
    412: 'PRECONDITION FAILED',
    413: 'REQUEST ENTITY TOO LARGE',
    414: 'REQUEST-URI TOO LONG',
    415: 'UNSUPPORTED MEDIA TYPE',
    416: 'REQUESTED RANGE NOT SATISFIABLE',
    417: 'EXPECTATION FAILED',
    500: 'INTERNAL SERVER ERROR',
    501: 'NOT IMPLEMENTED',
    502: 'BAD GATEWAY',
    503: 'SERVICE UNAVAILABLE',
}

def code2str(code):
  return '%d %s' % (code, CODES[code])


class Request(object):
  def __init__(self, environ):
    self._environ = environ
    self._params = self._parse_qs()
    self._json = False
    if 'json' in self._params:
      if self._params['json'] in ('1', 'true', 'yes'):
        self._json = True

  @staticmethod
  def format_json(var):
    return json.dumps(var)

  def _parse_qs(self):
    qs = self._environ['QUERY_STRING']
    args = cgi.parse_qs(qs)
    for k in args:
      args[k] = args[k][-1]
    return args

  def has_json(self):
    return self._json

  def get(self, name):
    try:
      return self._params[name]
    except KeyError, err:
      raise KeyError(str(name)) 

  def __getitem__(self, name):
    return self.get(name)

  def __contains__(self, name):
    return name in self._params



class QueryHandler(actions.Actions):
  def __init__(self, environ):
    self._environ = environ
    self._pinfo = environ['PATH_INFO']
    self._pinfo = self._pinfo.strip('/').strip()
    if self._pinfo == '/' or self._pinfo == '':
      self._action = 'do_root'
    else:
      self._action = 'do_' + string.lower(self._pinfo)

  def _has_action(self):
    return self._action in dir(self)

  def _run(self):
    action = getattr(self, self._action, None)
    if not action:
      return (code2str(404), 'Not found')
    else:
      try:
        code, data = action(Request(self._environ))
        return (code2str(code), data)
      except KeyError, err:
        return (code2str(500), "Missing argument %s\n" % str(err))



def dispatch(environ):
    h = QueryHandler(environ)
    return h._run()




import cc

class Actions:
  def do_root(self, request):
    if request.has_json():
      return (200, request.format_json({'version':str(cc.__version__)}))
    return (200, '%s\n' % str(cc.__version__))

  def do_selfhangup(self, request):
    agentid = str(request.get('agentid'))
    if request.has_json():
      return (200, request.format_json({'agentid':agentid}))
    return (200, agentid)

  def do_test(self, request):
    agentid = str(request.get('agentid'))
    hangup = str(request.get('hangup'))
    if request.has_json():
      return (200, request.format_json({'agentid':agentid, 'hangup': 'true'}))
    return (200, agentid+' '+hangup)


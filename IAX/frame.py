# frames
IAX_FULL_FRAME = 1
IAX_MINI_FRAME = 0

# frames type
IAX_TYPE_DTMF = 0x01
IAX_TYPE_VOICE_DATA = 0x02
IAX_TYPE_VOICE = 0x03
IAX_TYPE_CONTROL = 0x04
IAX_TYPE_UNUSED = 0x05
IAX_TYPE_IAX_CONTROL = 0x06
IAX_TYPE_TEXT = 0x07
IAX_TYPE_IMAGE = 0x08
IAX_TYPE_HTML = 0x09

# subclass for voice data
IAX_G7231 = 0x0001
IAX_GSM = 0x0002
IAX_G711U = 0x0004
IAX_G711A = 0x0008
IAX_LPC10 = 0x0080
IAX_G729 = 0x0100
IAX_SPEEX = 0x0200
IAX_ILBC = 0x0400


# subclass for control
IAX_CONTROL_HANGUP = 0x01
IAX_CONTROL_RING = 0x02
IAX_CONTROL_RINGING = 0x03
IAX_CONTROL_ANSWER = 0x04
IAX_CONTROL_BUSY = 0x05
IAX_CONTROL_CONGESTION = 0x08
IAX_CONTROL_PROGRESS = 0x0e


# subclass for iax control
IAX_NEW = 0x01
IAX_PING = 0x02
IAX_PONG = 0x03
IAX_ACK = 0x04
IAX_HANGUP = 0x05
IAX_REJECT = 0x06
IAX_ACCEPT = 0x07
IAX_AUTHREQ = 0x08
IAX_AUTHREP = 0x09
IAX_INVAL = 0x0a
IAX_LAGRQ = 0x0b
IAX_LAGRP = 0x0c
IAX_REGREQ = 0x0d
IAX_REGAUTH = 0x0e
IAX_REGACK = 0x0f
IAX_REGREJ = 0x10
IAX_REGREL = 0x11
IAX_VNAK = 0x12
IAX_DPREQ = 0x13
IAX_DPREP = 0x14
IAX_DIAL = 0x15
IAX_TXREQ = 0x16
IAX_TXCNT = 0x17
IAX_TXACC = 0x18
IAX_TXREADY = 0x19
IAX_TXREL = 0x1a
IAX_TXREJ = 0x1b
IAX_QUELCH = 0x1c
IAX_UNQUELCH = 0x1d
IAX_MWI = 0x20
IAX_UNSUPPORT = 0x21

# check a bit
# value >> pos & 0x1 (return bit value 1 or 0)
# pos from 0 to 31

# to_binary : "".join([ str(8 >> x & 0x1) for x in xrange(31,-1,-1) ])


def to_binary(int32):
  return "".join([ str(int32 >> x & 0x1) for x in xrange(31,-1,-1) ])



class FullFrame:
  def __init__(self):
    self.type = IAX_FULL_FRAME # 1 bit 
    self.source_callno = None # 15 bit unsigned int
    self.retransmitted = 0 # 1 bit, 1 if retransmitted else 0
    self.dest_callno = None # 15 bit unsigned int

    self.timestamp = 0 # 32 bit unsigned int

    self.oseqno = 0 # 8 bit, outbound stream
    self.iseqno = 0 # 8 bit, inbound stream

    self.frame_type = None # 8 bit
    self.subclass_c = 0 # 1 bit, if 1, subclass = subclass**2
    self.subclass = None # 7 bit

    self.data = None

  def serialize(self):
    #struct
    a = 0
    a |= self.type

    pass

  def unserialize(self):
    pass



class MiniFrame:
  def __init__(self):
    self.type = IAX_MINI_FRAME # 1 bit 
    self.source_callno = None # 15 bit unsigned int

    self.timestamp = None # 16 bit unsigned int, only low bits of timestamp
    
    self.data = None

  def serialize(self):
    #struct
    pass

  def unserialize(self):
    pass

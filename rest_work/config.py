"""
Config class for rest server
"""
import sys
import copy
import flask


class Config(flask.Config):
    default_attr = {'FS_INBOUND_ADDRESS':'127.0.0.1:8021',
                   }

    def __init__(self, filename):
        # default options
        self.filename = filename
        self.fd = open(self.filename)
        self._read()
        try:
            self.fd.close()
        except:
            pass

    def reload(self):
        self.fd = open(self.filename)
        self.clear()
        self._read()
        try:
            self.fd.close()
        except:
            pass

    def __getitem__(self, name):
        try:
            return dict.__getitem__(self, name)
        except KeyError:
            return self.default_attr[name]

    def __setitem__(self, name, value):
        dict.__setitem__(self, name, value)
        setattr(self, name, value)

    def get_line(self, line):
        return line.split('=', 1)

    def pretty_dump(self):
        for key, value in self.iteritems():
            print " >> %s = %s" % (key, value)

    def _read(self):
        for k, v in self.default_attr.iteritems():
            self[k] = v
        count = 1
        for line in self.fd:
            line = line.strip()
            if line == '':
                count += 1
            elif line.startswith('#'):
                count += 1
            elif not "=" in line:
                sys.stderr.write("WARNING : wrong format at line %d in '%s'" % (count, line))
                sys.stderr.flush()
                count += 1
            else:
                key, value = self.get_line(line)
                key = key.strip()
                value = value.strip()
                key = key.strip("'")
                value = value.strip("'")
                key = key.strip('"')
                value = value.strip('"')
                self[key] = str(value)
                count += 1


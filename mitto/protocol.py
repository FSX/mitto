import sys
import struct

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from thrift.Thrift import TMessageType, TType
from thrift.protocol.TBinaryProtocol import TBinaryProtocol


class BaseSerialize(object):
    def __init__(self):
        self._buffer = StringIO()

    def getvalue(self):
        data = self._buffer.getvalue()
        self._buffer.flush()
        return data

    def close(self):
        self._buffer.close()

    def message_begin(self, name, type, seqid):
        pass

    def message_end(self):
        pass

    def struct_begin(self, name):
        pass

    def struct_end(self):
        pass

    def field_begin(self, name, type_id):
        pass

    def field_end(self):
        pass

    def field_stop(self):
        pass

    def map_begin(self, ktype, vtype, size):
        pass

    def map_end(self):
        pass

    def list_begin(self, etype, size):
        pass

    def list_end(self):
        pass

    def set_begin(self, etype, size):
        pass

    def set_end(self):
        pass

    def bool(self, value):
        pass

    def byte(self, value):
        pass

    def i16(self, value):
        pass

    def i32(self, value):
        pass

    def i64(self, value):
        pass

    def double(self, value):
        pass

    def string(self, value):
        pass


class BaseUnserialize(object):
    def __init__(self, data=None):
        self._buffer = StringIO(data)

    def getvalue(self):
        data = self._buffer.getvalue()
        self._buffer.flush()
        return data

    def close(self):
        self._buffer.close()

    def skip(self, type):
        pass

    def message_begin(self):
        pass

    def message_end(self):
        pass

    def struct_begin(self):
        pass

    def struct_end(self):
        pass

    def field_begin(self):
        pass

    def field_end(self):
        pass

    def field_stop(self):
        pass

    def map_begin(self):
        pass

    def map_end(self):
        pass

    def list_begin(self):
        pass

    def list_end(self):
        pass

    def set_begin(self):
        pass

    def set_end(self):
        pass

    def bool(self):
        pass

    def byte(self):
        pass

    def i16(self):
        pass

    def i32(self):
        pass

    def i64(self):
        pass

    def double(self):
        pass

    def string(self):
        pass


class BinarySerialize(BaseSerialize):
    def __init__(self, strict=False):
        super(BinarySerialize, self).__init__()
        self.strict = strict

    def message_begin(self, name, type, seqid):
        if self.strict:
            self.byte(TBinaryProtocol.VERSION_1 | type)
            self.string(name)
            self.i32(seqid)
        else:
            self.string(name)
            self.byte(type)
            self.i32(seqid)

    def field_begin(self, name, type, id):
        self.byte(type)
        self.i16(id)

    def field_stop(self):
        self.byte(TType.STOP)

    def map_begin(self, ktype, vtype, size):
        pass

    def map_end(self):
        pass

    def list_begin(self, etype, size):
        pass

    def list_end(self):
        pass

    def set_begin(self, etype, size):
        pass

    def set_end(self):
        pass

    def bool(self, value):
        if bool:
            self._buffer.write('\x01')
        else:
            self._buffer.write('\x00')

    def byte(self, value):
        self._buffer.write(struct.pack('!b', value))

    def i16(self, value):
        self._buffer.write(struct.pack('!h', value))

    def i32(self, value):
        self._buffer.write(struct.pack('!i', value))

    def i64(self, value):
        self._buffer.write(struct.pack('!q', value))

    def double(self, value):
        self._buffer.write(struct.pack('!d', value))

    def string(self, value):
        self._buffer.write(struct.pack('!i', len(value)))
        self._buffer.write(value)


class BinaryUnserialize(BaseUnserialize):
    def __init__(self, data=None, strict=False):
        super(BinaryUnserialize, self).__init__(data)
        self.strict = strict

    def skip(self, type):
        if type == TType.STOP:
            return
        elif type == TType.BOOL:
            self.bool()
        elif type == TType.BYTE:
            self.byte()
        elif type == TType.I16:
            self.i16()
        elif type == TType.I32:
            self.i32()
        elif type == TType.I64:
            self.i64()
        elif type == TType.DOUBLE:
            self.double()
        elif type == TType.STRING:
            self.string()
        elif type == TType.STRUCT:
            name = self.struct_begin()
            while True:
                (name, type, id) = self.field_begin()
                if type == TType.STOP:
                    break
                self.skip(type)
                self.field_end()
            self.struct_end()
        elif type == TType.MAP:
            (ktype, vtype, size) = self.map_begin()
            for i in range(size):
                self.skip(ktype)
                self.skip(vtype)
            self.map_end()
        elif type == TType.SET:
            (etype, size) = self.set_begin()
            for i in range(size):
                self.skip(etype)
            self.set_end()
        elif type == TType.LIST:
            (etype, size) = self.list_begin()
            for i in range(size):
                self.skip(etype)
            self.list_end()

    def message_begin(self):
        sz = self.i32()
        if sz < 0:
            version = sz & TBinaryProtocol.VERSION_MASK
            if version != TBinaryProtocol.VERSION_1:
                raise Exception('Bad version in message_begin: %d' % sz)
            type = sz & TBinaryProtocol.TYPE_MASK
            name = self.string()
            seqid = self.i32()
        else:
            if self.strict:
                raise Exception('No protocol version header')
            name = self._buffer.read(sz)
            type = self.byte()
            seqid = self.i32()

        return (name, type, seqid)

    def field_begin(self):
        type = self.byte()
        if type == TType.STOP:
            return (None, type, 0)
        id = self.i16()
        return (None, type, id)

    def field_stop(self):
        pass

    def map_begin(self):
        pass

    def map_end(self):
        pass

    def list_begin(self):
        pass

    def list_end(self):
        pass

    def set_begin(self):
        pass

    def set_end(self):
        pass

    def bool(self):
        val, = struct.unpack('!b', self._buffer.read(1))
        if val == 0:
            return False
        return True

    def byte(self):
        val, = struct.unpack('!b', self._buffer.read(1))
        return val

    def i16(self):
        val, = struct.unpack('!h', self._buffer.read(2))
        return val

    def i32(self):
        val, = struct.unpack('!i', self._buffer.read(4))
        return val

    def i64(self):
        val, = struct.unpack('!q', self._buffer.read(8))
        return val

    def double(self):
        val, = struct.unpack('!d', self._buffer.read(8))
        return val

    def string(self):
        length, = struct.unpack('!i', self._buffer.read(4))
        return self._buffer.read(length)

import re
import struct
import socket
from time import sleep

from tornado import ioloop
from tornado import iostream

from thrift.Thrift import TMessageType, TType
from thrift.protocol.TBinaryProtocol import TBinaryProtocol


from mitto.protocol import BinarySerialize, BinaryUnserialize


def connected():
    buffer = BinarySerialize()

    buffer.message_begin('add', TMessageType.CALL, 0)
    buffer.struct_begin('add_args')

    buffer.field_begin('num1', TType.I32, 1)
    buffer.i32(2)
    buffer.field_end()

    buffer.field_begin('num2', TType.I32, 2)
    buffer.i32(2)
    buffer.field_end()

    buffer.field_stop()
    buffer.struct_end()
    buffer.message_end()

    stream.write(buffer.getvalue())
    stream.read_until_regex('\x00$', process_msg)


def process_msg(data):

    buffer = BinaryUnserialize(data)
    (fname, mtype, rseqid) = buffer.message_begin()

    if mtype == TMessageType.EXCEPTION:
        pass # TODO Raise an exception

    buffer.struct_begin()

    while True:
        (unused, ftype, fid) = buffer.field_begin()
        if ftype == TType.STOP:
            break
        if fid == 0:
            if ftype == TType.I32:
                result = buffer.i32()
            else:
                buffer.skip(ftype)
        else:
            buffer.skip(ftype)
        buffer.field_end()

    buffer.struct_end()
    buffer.message_end()

    print fname, result

    sleep(2)
    connected()
    # stream.read_until_regex('\x00$', process_msg)


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

    stream = iostream.IOStream(s)
    stream.connect(('localhost', 9090), connected)

    ioloop.IOLoop.instance().start()
except KeyboardInterrupt:
    print 'Exit'

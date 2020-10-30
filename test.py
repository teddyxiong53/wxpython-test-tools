from __future__ import print_function
import wave
import struct

# wf = wave.open('./audio_output/right.wav')
# print(wf.tell())
# wf.setpos(100)
# print(wf.tell())
#
# wf.close()

buffer = struct.pack('ihb', 1,2,3)
print(buffer)
print( struct.unpack('ihb', buffer))

data = [1,2,3]
buffer = struct.pack('!ihb', *data)
print(buffer)

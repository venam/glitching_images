#!/usr/bin/env python

from struct import *
import sys
import os


def wordpad_effect(data, output_file):

	out = open(output_file, 'wb')
	print("reading len: "+ str(len(data)) + " and writing: "+output_file)
	index = 0
	previous_byte = b"\x00"
	while index < len(data):
		component, = unpack("B", data[index:index+1])
		if component == 0x07:
			component = 0x20

		if component == 0x0d:
			if index < len(data):
				next_byte, = unpack("B", data[index+1:index+2])
				if next_byte != 0x0a:
					component |= 0x0a00
		elif component == 0x0a and previous_byte != 0x0d:
			component = ((component << 8) | 0x0d)
			out.write(pack("H", component))
		else:
			out.write(pack("B", component))
		index += 1
		previous_byte = component


wordpad_effect(open('world_map.interleaved.data', 'rb').read(), 'world_map.interleaved.corrupt.data')
wordpad_effect(open('world_map.planar.data', 'rb').read(), 'world_map.planar.corrupt.data')


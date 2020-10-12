#!/usr/bin/env python

from struct import *
import sys
import random

def corrupt_byte_and_save(head, btoc, max_change, output):
	if len(head) < btoc:
		btoc = len(head) - 2
	corrupted, = unpack(">B", head[btoc:btoc+1])
	#print(hex(corrupted))
	r = random.randint(1, max_change)
	operation = random.choice(['add', 'sub'])
	if operation == 'add':
		corrupted = (corrupted + r) & 0xFF
	elif operation == 'sub':
		corrupted = (256 + corrupted - r) & 0xFF
	#print(hex(corrupted))
	output.write(head[0:btoc])
	## because it's immutable
	output.write(pack("B", corrupted))
	output.write(head[btoc+1:])

def corrupt_header(data, output):
	output = open(output, 'wb')
	index = 0
	lenchunk = 0
	parts = []
	while(True):
		hdr, = unpack(">H", data[0:2])
		if hdr == 0xffd8:
			lenchunk = 2
		else:
			# fetch the length of this chunk (LV)
			lenchunk, = unpack(">H", data[2:4])
			# plus the size of the tag (TLV)
			lenchunk+=2
			# the actual content/V is placed after TL
			chunk = data[4:lenchunk]
		if hdr == 0xffda:
			break
		# go to next chunk
		parts.append(data[0:lenchunk])
		data = data[lenchunk:]
		index += lenchunk

	# we're done with the header
	# now mess one of the part of it and save the rest of data

	mess = random.choice(['quantization', 'huffman'])
	count = 0

	# first get a count
	for head in parts:
		hdr, = unpack(">H", head[0:2])
		if mess == 'quantization' and hdr == 0xFFDB:
			count += 1
		elif mess == 'huffman' and hdr == 0xFFC4:
			count += 1

	# select one to mess between these
	#print(mess+ " => " + str(count))
	which_to_mess = random.randint(0, count-1)
	count = 0

	for head in parts:
		hdr, = unpack(">H", head[0:2])
		if mess == 'quantization' and hdr == 0xFFDB:
			if count == which_to_mess:
				# choose byte between 5 and 8, byte to corrupt
				btoc = random.randint(5, 8)
				corrupt_byte_and_save(head, btoc, 255, output)
			else:
				output.write(head)
			count += 1
		elif mess == 'huffman' and hdr == 0xFFC4:
			if count == which_to_mess:
				# choose byte above (2+2+17)21 and lower than 26, byte to corrupt
				btoc = random.randint(30, 50)
				corrupt_byte_and_save(head, btoc, 6, output)
				pass
			else:
				output.write(head)
			count += 1
		else:
			output.write(head)

	output.write(data)

if len(sys.argv) != 3:
    print(sys.argv[0] + ": image.jpg corrupt.jpg")
    sys.exit(1)

corrupt_header(open(sys.argv[1], 'rb').read(), sys.argv[2])


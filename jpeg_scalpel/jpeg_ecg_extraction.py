#!/usr/bin/env python

from struct import *
import math
import os


def extract_ecg(data, output_dir):

	index = 0
	lenchunk = 0
	data_copy = data
	file_count = 1;
	previous_index = index;

	# TODO also put quantization tables (DCT) and  Huffman tables in separate files
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
			# quantization table
			#if hdr == 0xffdb
			# huffman table
			#elif hdr == 0xffc4:

		# last chunk that we process is the start of scan
		if hdr == 0xffda:
			# create the directory if not present
			if not os.path.exists(output_dir):
				os.mkdir(output_dir)

			# write everything until this index
			print("saving header")
			open(output_dir+'/' + str(file_count).zfill(2) +'_header.jpg', 'wb').write(data_copy[:index])

			file_count += 1
			print("saving scan "+str(file_count).zfill(2))
			open(output_dir+'/' + str(file_count).zfill(2) +'_scan.jpg', 'wb').write(data[:lenchunk])

			# and continue
			data = data[lenchunk:]
			index += lenchunk
			break

		# go to next chunk
		data = data[lenchunk:]
		index += lenchunk



	# now put whatever was before in a header file

	# Now we enter a loop of:
	# Start of scan - ECS
	# Restart (or not, as set by the restart interval markers in the header)
	# ...
	# Start of scan - ECS again
	# ...
	# until end of file FFD9
	# if we replace one of the start of scan FFDA with eof FFD9 then
	# if the image will only load the first scan/drawing until that point
	# When in scanline/progressive vs baseline we directly draw what
	# we got at that point (I assume)

	# TODO we could possibly break FF00 (real FF) and FFD0-FFD7 (restart markers)
	previous_index = index
	lenchunk = 0
	while(True):
		# read 2 bytes
		hdr, = unpack(">H", data[0:2])
		# we reached the end of the file
		if hdr == 0xffd9:
		    break
		elif hdr == 0xffda:
			# we reached another scan layer, write what we got so far
			file_count += 1
			print("saving data "+str(file_count).zfill(2))
			open(output_dir+'/' + str(file_count).zfill(2) +'_data.jpg', 'wb').write(data_copy[previous_index:index])

			# write the header separately
			lenchunk, = unpack(">H", data[2:4])
			lenchunk+=2
			file_count += 1
			print("saving scan "+str(file_count).zfill(2))
			open(output_dir+'/' + str(file_count).zfill(2) +'_scan.jpg', 'wb').write(data[:lenchunk])

			# and continue
			previous_index = index + lenchunk
		else:
			lenchunk = 2

		# go to next 2 bytes
		data = data[lenchunk:]
		index += lenchunk

	# last scan layer to save before the ffd9 EoI
	file_count += 1
	print("saving data "+str(file_count).zfill(2))
	open(output_dir+'/' + str(file_count).zfill(2) +'_data.jpg', 'wb').write(data_copy[previous_index:index])
	previous_index = index

	# finish by writing 0xffd9 to a file
	file_count += 1
	print("finished saving FFD9")
	open(output_dir+'/' + str(file_count).zfill(2) +'_end.jpg', 'wb').write(data[0:2])


extract_ecg(open('../world_map.jpg', 'rb').read(), 'output_folder')


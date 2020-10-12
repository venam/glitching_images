#!/usr/bin/env python3

import numpy
import PIL.Image
import sys

if len(sys.argv) < 3:
    print(sys.argv[0] + ": image.jpg image.data [interleaved | planar]")
    sys.exit(1)

image = PIL.Image.open(sys.argv[1])
out = open(sys.argv[2], "wb")
pixels = numpy.asarray(image).flatten().flatten()

if len(sys.argv) < 4 or sys.argv[3] == "interleaved":
    out.write(pixels)
elif sys.argv[3] == "planar":
    out.write(bytes(pixels[0::3]))
    out.write(bytes(pixels[1::3]))
    out.write(bytes(pixels[2::3]))
else:
    print("Unknown option:", sys.argv[3])
    sys.exit(1)

from PIL import Image
import colorsys
import sys

im  = Image.open("../world_map.jpg")

lightness_threshold = 0.20

def rgb_to_int(r):
    out = r[0];
    out = (out << 8) + r[1];
    out = (out << 8) + r[2];
    return out

def int_to_rgb(out):
    red = (out >> 16) & 0xFF;
    green = (out >> 8) & 0xFF;
    blue = out & 0xFF;
    return (red, green, blue)

def get_first_not_black(im, x, y):
    while x < im.width-1:
        x += 1
        col = im.getpixel((x, y))
        h,l,s = colorsys.rgb_to_hls(col[0]/255.0, col[1]/255.0, col[2]/255.0)
        if l >= lightness_threshold:
            return x
    return -1

def get_next_black(im, x, y):
    x += 1

    while x < im.width-1:
        x += 1
        col = im.getpixel((x, y))
        h,l,s = colorsys.rgb_to_hls(col[0]/255.0, col[1]/255.0, col[2]/255.0)
        if l <= lightness_threshold:
            return x
    return x-1


for y in range(im.height):
    x = 0
    while x != -1 and x < im.width:
        col_arr = []
        start = get_first_not_black(im, x, y)
        x = start
        end = get_next_black(im, x, y)
        x = end
        if start == -1 or end == -1:
            break
        else:
            #print "col: " + str(y) + " - start: " + str(start) + " - end: " + str(end)
            for i in range(start, end):
                col_arr.append(rgb_to_int(im.getpixel((i, y))))
            col_arr.sort()
            for i in range(start, end):
                im.putpixel((i, y), int_to_rgb(col_arr.pop(0)))

im.save("sorted.jpg", "JPEG")

# to modify pixel


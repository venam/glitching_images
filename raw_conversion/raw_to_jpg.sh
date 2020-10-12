# Example:
# ./raw_to_jpg.sh world_map.data world_map.jpg "2000x1479" 1
# 1 for interleaved, 0 for planar
#
# We can do that using imagemagick but not GIMP because:
# file-raw-load procedure only allows interactive mode
# The run mode { RUN-INTERACTIVE (0) }
if [ $# -lt 4 ]
then
	echo "$0: image.data image.jpg widthxheight [1|0, for interleaved or planar]"
	exit
fi

if [ "XX$4XX" == "XX1XX" ]
then
	convert -size $3 -depth 8 rgb:$1 $2
else
	convert -size $3 -interlace plane -depth 8 rgb:$1 $2
fi

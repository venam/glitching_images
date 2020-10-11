# Example:
# ./jpg_to_raw.sh world_map.jpg world_map.data 1
# 1 for interleaved, 0 for planar
#
# Only GIMP can create planar images, even the following only gives interleaved
# stream -interlace plane -map rgb -storage-type char world_map.jpg stream.planar.data
# The -interlace isn't respected in imagemagick
XDG_CONFIG_HOME=$PWD
export XDG_CONFIG_HOME
echo $XDG_CONFIG_HOME
if [ $# -lt 3 ]
then
	echo "$0: image.jpg image.data [1|0, for interleaved or planar]"
	exit
fi
if [ "XX$3XX" == "XX1XX" ]
then
	gimp -i -b "(jpg_to_raw \"$1\" \"$2\" #t)" -b '(gimp-quit 0)'
else
	gimp -i -b "(jpg_to_raw \"$1\" \"$2\" #f)" -b '(gimp-quit 0)'
fi

# Example:
# ./jpg_to_raw.sh world_map.jpg world_map.data 1
XDG_CONFIG_HOME=$PWD
export XDG_CONFIG_HOME
echo $XDG_CONFIG_HOME
gimp -i -b "(jpg->raw \"$1\" \"$2\" #t)" -b '(gimp-quit 0)'

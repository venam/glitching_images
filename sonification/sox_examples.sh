sox -t ul -c 1 -r 48k world_map.planar.data -t ul world_map.planar.audio.corrupt trim 0 100s : echo 0.4 0.8 10 0.9
sox -t ul -c 1 -r 48k world_map.planar.data -t ul world_map.planar.audio.corrupt trim 0 100s : phaser 0.3 0.9 1 0.7 0.5 -t
sox -t ul -c 1 -r 48k world_map.planar.data -t ul world_map.planar.audio.corrupt trim 0 100s : flanger

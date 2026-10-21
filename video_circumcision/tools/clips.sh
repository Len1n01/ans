#!/bin/bash
# name src start dur [extra crop filter]
cut() {
  local name=$1 src=$2 ss=$3 t=$4 pre=${5:-null}
  mkdir -p video/clips/$name && rm -f video/clips/$name/*.jpg
  ffmpeg -v error -y -ss $ss -i raw/$src -t $t -vf "$pre,fps=25,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,eq=contrast=1.05" -q:v 4 video/clips/$name/f%05d.jpg
  echo "$name $(ls video/clips/$name | wc -l)"
}
cut wall1918   jer1918.mp4 76 10
cut wall1918b  jer1918.mp4 106 10
cut oldcity    jer1918.mp4 166 8
cut panorama   jer1918.mp4 19 7
cut arrival    jews1913.mp4 107 10
cut telaviv    jews1913.mp4 422 10
cut children13 jews1913.mp4 560 10
cut gymnasia   jews1913.mp4 669 9
cut pil_wall   pilgrim.mp4 545 12 "crop=iw:ih*0.86:0:0"
cut pil_jer    pilgrim.mp4 562 8 "crop=iw:ih*0.86:0:0"

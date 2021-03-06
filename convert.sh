#!/bin/bash

inFormat="${1}"
outFormat="${2}"
test="${3}"

find . -name *.${inFormat} | while read line; do
  inFile="${line}"
  outFile="${line%.ape}.${outFormat}"
  echo "Found [${inFile}]  =====> [${outFile}]"
  if ! [ -z ${test} ]; then
    continue
  fi
  
  if [ ${outFormat} == "mp3" ]; then
    ffmpeg -i "${inFile}" -map_metadata 0:s:0 -b:a 320k "${outFile}" </dev/null
    #ffmpeg -i "${inFile}"  "${i%.*}.mp3" -map_metadata 0:s:0 -id3v2_version 3 -write_id3v1 1 -b:a 320k
  else
    ffmpeg -i "${inFile}" -map_metadata 0:s:0 "${outFile}" </dev/null
  fi
done

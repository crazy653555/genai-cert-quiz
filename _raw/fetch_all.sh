#!/bin/bash
set -u
cd "$(dirname "$0")"
FFBIN="/c/Users/crazy/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-9.0.2-full_build/bin"
mkdir -p subs frames vids

while IFS='|' read -r idx vid; do
  [ -z "$vid" ] && continue
  echo "=== [$idx] $vid ==="

  # subtitle
  if [ ! -f "subs/${idx}_${vid}.zh-TW.vtt" ]; then
    PYTHONIOENCODING=utf-8 python -m yt_dlp --skip-download --write-auto-sub --write-sub \
      --sub-lang "zh-Hant,zh-TW,zh,zh-Hans" --sub-format vtt \
      -o "subs/${idx}_${vid}.%(ext)s" "https://www.youtube.com/watch?v=${vid}" \
      >> fetch.log 2>&1
  fi

  # video 720p (or best available video+audio) for frame capture
  if [ ! -f "vids/${idx}_${vid}.mp4" ]; then
    PYTHONIOENCODING=utf-8 python -m yt_dlp -f "136+139/134+139/best" --ffmpeg-location "$FFBIN" \
      -o "vids/${idx}_${vid}.%(ext)s" "https://www.youtube.com/watch?v=${vid}" \
      >> fetch.log 2>&1
  fi

  # extract frame at t=2s
  if [ -f "vids/${idx}_${vid}.mp4" ] && [ ! -f "frames/${idx}_${vid}.jpg" ]; then
    "$FFBIN/ffmpeg" -y -ss 2 -i "vids/${idx}_${vid}.mp4" -frames:v 1 "frames/${idx}_${vid}.jpg" >> fetch.log 2>&1
  fi

  # remove video to save space after frame extracted
  if [ -f "frames/${idx}_${vid}.jpg" ] && [ -f "vids/${idx}_${vid}.mp4" ]; then
    rm -f "vids/${idx}_${vid}.mp4"
  fi

done < ids.txt

echo "DONE ALL"

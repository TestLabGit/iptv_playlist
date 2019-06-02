#!/bin/sh

git_config() {
  git config --global user.email "sv.ivan1996@gmail.com"
  git config --global user.name "Svichkaryov"
}

git_commit() {
  git checkout master
  dateAndMonth=`date "+%d-%m-%Y %T"` 
  mv ../data/lplaylist.m3u ../data/lplaylist_prev.m3u
  cp core/result_playlist/*.m3u ../data
  git add ../data/
  git commit -m "Travis update: $dateAndMonth (Build $TRAVIS_BUILD_NUMBER)" -m "[skip ci]"
}

git_push() {
  git remote rm origin
  git remote add origin https://${GH_TOKEN}@github.com/h4qz04/iptv_playlist.git > /dev/null 2>&1
  git push origin master --quiet > /dev/null 2>&1
}

BLACK='\033[0;30m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'

git_config
PLAYLIST_LC=`wc -l core/result_playlist/lplaylist.m3u | awk '{print $1}'`
echo -en "${YELLOW} lplaylist ${GRAY} consist ${GREEN}$PLAYLIST_LC ${GRAY}line ${NORMAL}\n" 
if [ `wc -l core/result_playlist/lplaylist.m3u | awk '{print $1}'` -ge "10" ]; then
  echo -en "${YELLOW} lplaylist line count >= 10${NORMAL}\n"   
  git_commit
else
  echo -en "${YELLOW} lplaylist line count < 10${NORMAL}\n"   
  false
fi

if [ $? -eq 0 ]; then
  echo -en "${GREEN}New commit with changed files exists. Uploading to GitHub${NORMAL}\n"
  git_push
else
  echo -en "${BLUE}No changes. Nothing to do${NORMAL}\n"
fi
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
  cd ..
  git add data/
  git commit -m "Travis update: $dateAndMonth (Build $TRAVIS_BUILD_NUMBER)" -m "[skip ci]"
}

git_push() {
  git remote rm origin
  git remote add origin https://${GH_TOKEN}@github.com/h4qz04/iptv_playlist.git > /dev/null 2>&1
  git push origin master --quiet > /dev/null 2>&1
}

git_config
if [ `wc -l core/result_playlist/lplaylist.m3u | awk '{print $1}'` -ge "10" ]; then
  git_commit
else
  false
fi

if [ $? -eq 0 ]; then
  echo "New commit with changed files exists. Uploading to GitHub"
  git_push
else
  echo "No changes. Nothing to do"
fi
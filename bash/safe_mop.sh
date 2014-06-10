#!/bin/bash
# author: Armagan Kimyonoglu
# rm files and directories safely by checking open files

if [ -z $1 ]; then
  echo "usage: ./safe_mop.sh /tmp # safely clean tmp directory"
  exit
fi

PARENT_DIR=$1

filter_and_remove() {
  if [ -d $1 ]; then
    for i in `ls -A1 $1`;
    do
      filter_and_remove $1/$i
    done
    if [ "$PARENT_DIR" != "$1" ]; then
      echo "[INFO] trying to safely rm directory $1"
      rmdir $1
    fi
  elif sudo lsof $1 &>/dev/null; then
    echo "[WARN] cannot rm $1 (resource busy)"
  else
    echo "[INFO] trying to safely rm $1"
    rm $1
  fi
}

filter_and_remove $1
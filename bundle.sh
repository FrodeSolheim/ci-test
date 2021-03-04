#!/bin/sh

set -e

. fsbuild/plugin.pre.sh

mkdir -p $PLUGIN_READMEDIR
cp README.md $PLUGIN_READMEDIR/ReadMe.txt

mkdir -p $PLUGIN_BINDIR
cp ci-test$EXE $PLUGIN_BINDIR

. fsbuild/plugin.post.sh

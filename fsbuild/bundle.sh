. fsbuild/plugin.sh

mkdir -p $PLUGIN_DIR
echo $PACKAGE_VERSION > $PLUGIN_DIR/Version.txt
cp README.md $PLUGIN_DIR/ReadMe.txt

mkdir -p $PLUGIN_BIN_DIR
echo $PACKAGE_VERSION > $PLUGIN_BIN_DIR/Version.txt
cp ci-test$EXE $PLUGIN_BIN_DIR

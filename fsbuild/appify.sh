#!/bin/sh
set -e

DIR=$1
APP_NAME=$2
EXECUTABLE=$3
BUNDLE_ID=$4

TEMP_APP=fsbuild/_build/temp.app

echo "Creating temporary app at $TEMP_APP"
rm -Rf $TEMP_APP
mkdir -p $TEMP_APP/Contents/MacOS
# mv "$1"/* $TEMP_APP/Contents/MacOS/
# mv $TEMP_APP/Contents/MacOS/Version.txt "$1"/
echo "Copy $DIR/$EXECUTABLE -> $TEMP_APP/Contents/MacOS/"
mv $DIR/$EXECUTABLE $TEMP_APP/Contents/MacOS/

echo "Writing Info.plist"

P=$TEMP_APP/Contents/Info.plist
echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" >> $P
echo "<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">" >> $P
echo "<plist version=\"1.0\">" >> $P
echo "<dict>" >> $P
echo "<key>CFBundleDevelopmentRegion</key>" >> $P
echo "<string>English</string>" >> $P
echo "<key>CFBundleDisplayName</key>" >> $P
echo "<string>$APP_NAME</string>" >> $P
echo "<key>CFBundleExecutable</key>" >> $P
echo "<string>$EXECUTABLE</string>" >> $P
echo "<key>CFBundleIdentifier</key>" >> $P
echo "<string>$BUNDLE_ID</string>" >> $P
echo "<key>CFBundleInfoDictionaryVersion</key>" >> $P
echo "<string>6.0</string>" >> $P
echo "<key>CFBundleName</key>" >> $P
echo "<string>$APP_NAME</string>" >> $P
echo "<key>CFBundlePackageType</key>" >> $P
echo "<string>APPL</string>" >> $P
echo "<key>CFBundleShortVersionString</key>" >> $P
echo "<string>1.0.0</string>" >> $P
echo "<key>CFBundleSignature</key>" >> $P
echo "<string>????</string>" >> $P
echo "<key>CFBundleVersion</key>" >> $P
echo "<string>1.0.0</string>" >> $P
echo "<key>LSMinimumSystemVersion</key>" >> $P
echo "<string>10.6.0</string>" >> $P
echo "<key>NSAppleScriptEnabled</key>" >> $P
echo "<false/>" >> $P
echo "<key>NSMainNibFile</key>" >> $P
echo "<string></string>" >> $P
echo "<key>NSPrincipalClass</key>" >> $P
echo "<string>NSApplication</string>" >> $P
echo "<key>LSUIPresentationMode</key>" >> $P
echo "<integer>4</integer>" >> $P
echo "</dict>" >> $P
echo "</plist>" >> $P

echo "Moving $TEMP_APP -> $DIR/$APP_NAME.app"
mv $TEMP_APP $DIR/$APP_NAME.app
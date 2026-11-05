#!/bin/zsh
# Builds and installs "MW Casual": the same game with the simple one-bar beatmaker,
# its own sunset-colored icon and its own bundle id (so it sits next to MAN'S WAR, with separate saves).
# Usage: ./build-casual.sh [device-id]   (run after the main app's ~/Developer/mans-war-app is set up, see README.md)
set -e
HERE=${0:A:h}; GAME=${HERE:h}; W=~/Developer/mans-war-app; C=$W/ios-casual
DEVICE=${1:-00008110-000538811E0A801E}; TEAM=MV7LU95GFV
cp "$HERE/build-www.mjs" "$W/"
(cd $W && GAME_DIR="$GAME" STUDIO=casual OUT=www-casual node build-www.mjs)
rsync -a --delete --exclude build --exclude build-device --exclude 'App/App/public' $W/ios/ $C/
rm -rf $C/App/App/public && cp -R $W/www-casual $C/App/App/public
sed -e 's/"com.maidysound.manswar"/"com.maidysound.manswar.casual"/' -e "s/\"MAN'S WAR\"/\"MW Casual\"/" $W/ios/App/App/capacitor.config.json > $C/App/App/capacitor.config.json
sed -i '' 's/PRODUCT_BUNDLE_IDENTIFIER = com.maidysound.manswar;/PRODUCT_BUNDLE_IDENTIFIER = com.maidysound.manswar.casual;/' $C/App/App.xcodeproj/project.pbxproj
/usr/libexec/PlistBuddy -c "Set :CFBundleDisplayName MW Casual" $C/App/App/Info.plist
cp "$HERE/casual-icon/AppIcon-512@2x.png" $C/App/App/Assets.xcassets/AppIcon.appiconset/AppIcon-512@2x.png
for n in splash-2732x2732.png splash-2732x2732-1.png splash-2732x2732-2.png; do cp "$HERE/casual-icon/splash.png" $C/App/App/Assets.xcassets/Splash.imageset/$n; done
cd $C/App
xcodebuild -project App.xcodeproj -scheme App -configuration Debug -destination "id=$DEVICE" -derivedDataPath build-device DEVELOPMENT_TEAM=$TEAM CODE_SIGN_STYLE=Automatic -allowProvisioningUpdates build | grep -E "error:|BUILD (SUCCEEDED|FAILED)"
xcrun devicectl device install app --device $DEVICE build-device/Build/Products/Debug-iphoneos/App.app

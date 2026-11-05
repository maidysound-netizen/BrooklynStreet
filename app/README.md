# 📱 MAN'S WAR 앱 (아이폰)

게임(`../index.html`)을 그대로 앱 안에 넣는다. three.js도 앱 안에 들어가서 **인터넷 없이** 돌고, **웹 주소에 올리지 않아도** 된다.

## 왜 빌드는 Mac 안쪽 디스크에서 하나
외장하드(exFAT)는 npm과 Xcode가 쓰는 바로가기 파일(심볼릭 링크)을 못 만든다. 그래서 이 폴더는 **설정 원본**만 보관하고, 실제 빌드는 `~/Developer/mans-war-app`에서 한다.

## 처음 한 번
```bash
mkdir -p ~/Developer/mans-war-app && cp -R package.json capacitor.config.json build-www.mjs ios ~/Developer/mans-war-app/
cd ~/Developer/mans-war-app && npm install
```

## 게임을 고친 뒤 앱에 반영
```bash
cd ~/Developer/mans-war-app && GAME_DIR="/Volumes/Crucial X6/학교과제/game/brooklyn-fps" node build-www.mjs && npx cap copy ios
```
그다음 Xcode에서 `ios/App/App.xcodeproj`를 열고 ▶ (시뮬레이터 또는 연결한 아이폰).

## 내 아이폰에 설치 (USB 연결, 무료 개인 팀 · 7일마다 다시)
```bash
cd ~/Developer/mans-war-app/ios/App && xcodebuild -project App.xcodeproj -scheme App -configuration Debug -destination 'generic/platform=iOS' -derivedDataPath build-device DEVELOPMENT_TEAM=MV7LU95GFV CODE_SIGN_STYLE=Automatic -allowProvisioningUpdates build
```
```bash
xcrun devicectl device install app --device 00008110-000538811E0A801E ~/Developer/mans-war-app/ios/App/build-device/Build/Products/Debug-iphoneos/App.app
```

## 손댄 것 (Capacitor 기본 템플릿과 다른 점)
- 앱 아이콘·시작 화면: `make_icon.py`로 그림 (밤하늘 + 킹스 스트리트 스카이라인 + 노란 왕관 + 타이틀처럼 흰 글씨에 빨간 그림자 "MW")
- iOS 27은 scene 방식이 아닌 앱을 바로 종료시킨다 → `AppDelegate.swift`에 `SceneDelegate`, `Info.plist`에 `UIApplicationSceneManifest` 추가
- 최소 iOS 15 (Xcode 27은 14를 지원하지 않음)
- 상태 표시줄 숨김, 세로·가로 모두
- Capacitor CLI가 SPM인데도 CocoaPods를 찾는 버그: 처음 `cap add ios` 때만 가짜 `pod` 명령으로 통과시킴 (이미 만들어 둔 `ios/`를 쓰면 필요 없음)

## 아직 안 한 것
- 앱스토어: Apple 개발자 계정(연 $99) 필요 (지금은 무료 개인 팀이라 7일마다 다시 설치)
- 안드로이드: 이 Mac에 Android Studio가 없음

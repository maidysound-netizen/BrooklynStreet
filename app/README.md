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

## 손댄 것 (Capacitor 기본 템플릿과 다른 점)
- iOS 27은 scene 방식이 아닌 앱을 바로 종료시킨다 → `AppDelegate.swift`에 `SceneDelegate`, `Info.plist`에 `UIApplicationSceneManifest` 추가
- 최소 iOS 15 (Xcode 27은 14를 지원하지 않음)
- 상태 표시줄 숨김, 세로·가로 모두
- Capacitor CLI가 SPM인데도 CocoaPods를 찾는 버그: 처음 `cap add ios` 때만 가짜 `pod` 명령으로 통과시킴 (이미 만들어 둔 `ios/`를 쓰면 필요 없음)

## 아직 안 한 것
- 앱 아이콘·시작 화면 (지금은 Capacitor 기본 아이콘)
- 실제 아이폰 설치: Xcode에서 내 Apple ID로 서명하면 내 폰에 7일짜리로 무료 설치 가능. 앱스토어는 Apple 개발자 계정(연 $99) 필요
- 안드로이드: 이 Mac에 Android Studio가 없음

<!-- markdownlint-configure-file {"MD022": false, "MD031": false, "MD032": false, "MD029": false, "MD007": false, "MD009": false, "MD034": false} -->
# Flutter Production Configuration Guide

## Client App (User-facing app)

### Android Production Setup

1. **Update app/build.gradle**

```gradle
android {
    defaultConfig {
        applicationId "com.gymgenius.client"
        minSdkVersion 21
        targetSdkVersion 34
        versionCode 1
        versionName "1.0.0"
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

2. **Create keystore for signing**

```bash
keytool -genkey -v -keystore gymgenius-client-release.keystore \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias gymgenius-client
```

3. **Create android/key.properties**

```properties
storePassword=YOUR_STORE_PASSWORD
keyPassword=YOUR_KEY_PASSWORD
keyAlias=gymgenius-client
storeFile=../gymgenius-client-release.keystore
```

4. **Update android/app/build.gradle to use keystore**

```gradle
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
            storePassword keystoreProperties['storePassword']
        }
    }
}
```

### iOS Production Setup

1. **Update ios/Runner/Info.plist**

```xml
<key>CFBundleIdentifier</key>
<string>com.gymgenius.client</string>
<key>CFBundleShortVersionString</key>
<string>1.0.0</string>
<key>CFBundleVersion</key>
<string>1</string>
```

2. **Xcode Configuration**
   - Open `ios/Runner.xcworkspace` in Xcode
   - Select Runner → Signing & Capabilities
   - Select your development team
   - Set Bundle Identifier: `com.gymgenius.client`
   - Enable automatic signing

3. **App Store Connect Setup**
   - Create app in App Store Connect
   - Set up screenshots (6.5", 5.5" displays)
   - Add app icon (1024x1024 px)
   - Fill app description and keywords

### Environment Configuration

Create `lib/config/environment.dart`:

```dart
class Environment {
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'https://api.gymgenius.com',
  );
  
  static const String socketUrl = String.fromEnvironment(
    'SOCKET_URL',
    defaultValue: 'wss://api.gymgenius.com',
  );
  
  static const bool isProduction = bool.fromEnvironment('PRODUCTION', defaultValue: false);
}
```

### Build Commands

```bash
# Android Release APK
flutter build apk --release --dart-define=API_BASE_URL=https://api.gymgenius.com --dart-define=PRODUCTION=true

# Android App Bundle (for Play Store)
flutter build appbundle --release --dart-define=API_BASE_URL=https://api.gymgenius.com --dart-define=PRODUCTION=true

# iOS Release
flutter build ios --release --dart-define=API_BASE_URL=https://api.gymgenius.com --dart-define=PRODUCTION=true
```

## Trainer App

### Android

- **Application ID**: `com.gymgenius.trainer`
- **Version Code**: 1
- **Version Name**: "1.0.0"
- **Keystore Alias**: `gymgenius-trainer`

### iOS

- **Bundle Identifier**: `com.gymgenius.trainer`
- **Version**: 1.0.0
- **Build Number**: 1

## Pre-deployment Checklist

- [ ] Update version numbers in pubspec.yaml
- [ ] Test on real devices (Android & iOS)
- [ ] Run `flutter analyze` - should have 0 errors
- [ ] Run `flutter test` - all tests pass
- [ ] Configure app icons for all platforms
- [ ] Add splash screens
- [ ] Set up Firebase (Analytics, Crashlytics)
- [ ] Configure deep links
- [ ] Test payment flows (Razorpay integration)
- [ ] Test push notifications
- [ ] Review app permissions (Camera, Location, Storage)
- [ ] Add privacy policy URL
- [ ] Add terms of service URL
- [ ] Configure ProGuard rules (Android)
- [ ] Enable R8 full mode (Android)
- [ ] Test on different screen sizes
- [ ] Test with slow network conditions
- [ ] Verify SSL certificate pinning
- [ ] Review crash reporting setup

## Play Store Requirements

1. **App Content Rating**: Fill questionnaire
2. **Target Audience**: 13+ (fitness apps)
3. **Privacy Policy**: Required URL
4. **Screenshots**: Minimum 2 per device type
5. **Feature Graphic**: 1024 x 500 px
6. **App Icon**: 512 x 512 px (high-res)
7. **Short Description**: Max 80 characters
8. **Full Description**: Max 4000 characters

## App Store Requirements

1. **App Preview Video**: 15-30 seconds (optional)
2. **Screenshots**: Required for 6.5" and 5.5" displays
3. **App Icon**: 1024 x 1024 px (no alpha channel)
4. **Age Rating**: 12+ (fitness content)
5. **Keywords**: Max 100 characters
6. **Support URL**: Required
7. **Marketing URL**: Optional
8. **Privacy Policy URL**: Required

## Firebase Setup

Add Firebase configuration files:

- Android: `android/app/google-services.json`
- iOS: `ios/Runner/GoogleService-Info.plist`

## Security Hardening

1. **Enable SSL Pinning**
2. **Obfuscate Code**: Use `--obfuscate` flag
3. **Split Debug Info**: Use `--split-debug-info` flag
4. **Remove Debug Prints**: Use kReleaseMode checks
5. **Secure Storage**: Use flutter_secure_storage for tokens
6. **API Key Protection**: Never commit API keys

## Performance Optimization

1. **Reduce App Size**: Enable R8, remove unused resources
2. **Lazy Loading**: Load screens on demand
3. **Image Optimization**: Use cached_network_image
4. **Code Splitting**: Use deferred imports
5. **Minimize Dependencies**: Audit pubspec.yaml

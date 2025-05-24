# .github/workflows/build.yml
name: Build APK - Attendance Bunker

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build-attendance-bunker-apk:
    runs-on: ubuntu-latest
    env:
      ANDROID_HOME: ${{ github.workspace }}/.buildozer/android/platform/android-sdk
      PATH: ${{ env.PATH }}:${{ env.ANDROID_HOME }}/cmdline-tools/latest/bin:${{ env.ANDROID_HOME }}/platform-tools

    steps:
    - name: Checkout Attendance Bunker repository
      uses: actions/checkout@v4

    - name: Set up Python 3.10
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install Buildozer and system dependencies
      run: |
        sudo apt update
        sudo apt install -y zip unzip openjdk-17-jdk python3-pip python3-setuptools git
        python3 -m pip install --upgrade pip
        pip install buildozer cython

    - name: Accept Android SDK licenses
      run: |
        yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses

    - name: Install Android SDK Build Tools 34.0.0
      run: |
        yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager "build-tools;34.0.0"

    - name: Build APK for Attendance Bunker
      run: buildozer android debug

    - name: Upload Attendance Bunker APK artifact
      uses: actions/upload-artifact@v4
      with:
        name: attendance-bunker-apk
        path: bin/*.apk

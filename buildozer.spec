[app]

title = PeakMeasure
package.name = PeakMeasure
package.domain = gsog.eigeneDomain

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1
requirements = python3,kivy,plyer

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a

icon.filename = images/PeakMeasureLogo.png

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = main
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0

[buildozer]
log_level = 2

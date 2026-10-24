plugins { id("com.android.application") }

android {
    namespace = "io.github.g19479574996t.tmuxcodeagent"
    compileSdk = 36

    defaultConfig {
        applicationId = "io.github.g19479574996t.tmuxcodeagent"
        minSdk = 26
        targetSdk = 36
        versionCode = 10002
        versionName = "1.0.0-rc2"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
}

// app/src/main/kotlin/com/example/androidmaster/MyApplication.kt
package com.example.androidmaster

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        // App initialization
    }
}

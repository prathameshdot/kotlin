# Module 2.1: Android Basics & Activity Lifecycle
## Understanding the Foundation of Android Apps

---

## 📖 What is Android?

Android is an operating system for mobile devices. An Android app consists of:
- **Activities** - Screens the user sees
- **Services** - Background processes
- **Content Providers** - Data management
- **Broadcast Receivers** - Listen for system events

We'll focus on **Activities** first since they're the most visible to users.

---

## 1️⃣ What is an Activity?

An **Activity** is a single screen with a user interface. Think of it like a page in a book:
- The main screen is one Activity
- The settings screen is another Activity
- Each screen can open another screen

### **Example: Social Media App**

```
MainActivity (Feed Screen)
    ↓ User taps a post
PostDetailActivity (Details Screen)
    ↓ User taps profile
ProfileActivity (Profile Screen)
```

---

## 2️⃣ Creating Your First Activity

### **Activity Code (Kotlin)**

```kotlin
// MainActivity.kt
package com.example.myapp

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.widget.Button
import android.widget.TextView

class MainActivity : AppCompatActivity() {
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)  // Load layout file
        
        // Find UI elements
        val welcomeText = findViewById<TextView>(R.id.welcomeText)
        val clickButton = findViewById<Button>(R.id.clickButton)
        
        // Set text
        welcomeText.text = "Welcome to Android!"
        
        // Handle button click
        clickButton.setOnClickListener {
            welcomeText.text = "Button clicked!"
        }
    }
}
```

### **Layout File (XML)**

```xml
<!-- activity_main.xml -->
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">
    
    <TextView
        android:id="@+id/welcomeText"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Hello, Android!"
        android:textSize="24sp" />
    
    <Button
        android:id="@+id/clickButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Click Me" />
    
</LinearLayout>
```

### **Register in Manifest**

```xml
<!-- AndroidManifest.xml -->
<activity
    android:name=".MainActivity"
    android:exported="true">
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
</activity>
```

---

## 3️⃣ Activity Lifecycle - The Most Important Concept!

### **What is Lifecycle?**

The lifecycle is the series of states an Activity goes through from creation to destruction.

```
┌─────────────┐
│  Created    │ Activity is created
└──────┬──────┘
       │
┌──────▼─────────┐
│  Started       │ Activity becomes visible
└──────┬──────────┘
       │
┌──────▼─────────┐
│  Resumed       │ Activity is in foreground (user can interact)
└──────┬──────────┘
       │
┌──────▼──────────┐
│  Paused        │ Activity is still visible but loses focus
└──────┬──────────┘
       │
┌──────▼──────────┐
│  Stopped       │ Activity is no longer visible
└──────┬──────────┘
       │
┌──────▼──────────┐
│  Destroyed     │ Activity is completely removed
└─────────────────┘
```

### **Lifecycle Methods - Code That Runs at Each State**

```kotlin
class MainActivity : AppCompatActivity() {
    
    // ✅ Called when activity is created
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        println("onCreate called")
        // Load data, initialize variables
    }
    
    // ✅ Called just before activity becomes visible
    override fun onStart() {
        super.onStart()
        println("onStart called")
    }
    
    // ✅ Called when activity is ready to interact with user
    override fun onResume() {
        super.onResume()
        println("onResume called")
        // Start animations, play music, etc.
    }
    
    // ✅ Called when activity loses focus (but still visible)
    override fun onPause() {
        super.onPause()
        println("onPause called")
        // Pause animations, stop music
    }
    
    // ✅ Called when activity is no longer visible
    override fun onStop() {
        super.onStop()
        println("onStop called")
    }
    
    // ✅ Called when activity is destroyed
    override fun onDestroy() {
        super.onDestroy()
        println("onDestroy called")
        // Clean up resources
    }
}
```

### **Real-World Example: Video Player**

```kotlin
class VideoPlayerActivity : AppCompatActivity() {
    private lateinit var mediaPlayer: MediaPlayer
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_video_player)
        mediaPlayer = MediaPlayer.create(this, R.raw.my_video)
    }
    
    override fun onResume() {
        super.onResume()
        // User came back - play video
        if (!mediaPlayer.isPlaying) {
            mediaPlayer.start()
        }
    }
    
    override fun onPause() {
        super.onPause()
        // User switched to another app - pause video
        if (mediaPlayer.isPlaying) {
            mediaPlayer.pause()
        }
    }
    
    override fun onDestroy() {
        super.onDestroy()
        // Clean up
        mediaPlayer.release()
    }
}
```

### **Lifecycle Scenarios**

**Scenario 1: User Opens App**
```
onCreate → onStart → onResume
(App is running and visible)
```

**Scenario 2: User Switches Apps**
```
onPause (activity still visible but no longer in focus)
→ onStop (activity no longer visible)
```

**Scenario 3: User Comes Back**
```
onStart → onResume
(App is running again)
```

**Scenario 4: Device Rotation**
```
onPause → onStop → onDestroy
→ onCreate → onStart → onResume
(Activity is recreated!)
```

**Scenario 5: User Exits App**
```
onPause → onStop → onDestroy
(Activity is destroyed)
```

---

## 4️⃣ Saving Data During Rotation

When device rotates, the Activity is destroyed and recreated. Here's how to save data:

```kotlin
class MainActivity : AppCompatActivity() {
    private var counter = 0
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // Restore saved data
        if (savedInstanceState != null) {
            counter = savedInstanceState.getInt("counter", 0)
            println("Restored counter: $counter")
        }
    }
    
    // ✅ Called before activity is destroyed
    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putInt("counter", counter)
        println("Saved counter: $counter")
    }
}
```

---

## 5️⃣ Starting Another Activity (Intent)

### **Opening Another Activity**

```kotlin
class MainActivity : AppCompatActivity() {
    fun openSecondActivity() {
        val intent = Intent(this, SecondActivity::class.java)
        startActivity(intent)
    }
}

// In AndroidManifest.xml - register SecondActivity:
<activity android:name=".SecondActivity" />
```

### **Passing Data Between Activities**

```kotlin
// MainActivity - send data
class MainActivity : AppCompatActivity() {
    fun openUserProfile(userId: Int) {
        val intent = Intent(this, UserProfileActivity::class.java)
        intent.putExtra("userId", userId)           // Send Int
        intent.putExtra("userName", "Alice")        // Send String
        startActivity(intent)
    }
}

// UserProfileActivity - receive data
class UserProfileActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_user_profile)
        
        // Get data from intent
        val userId = intent.getIntExtra("userId", -1)
        val userName = intent.getStringExtra("userName") ?: "Unknown"
        
        println("User: $userName, ID: $userId")
    }
}
```

### **Getting Result Back from Another Activity**

```kotlin
// MainActivity - start for result
class MainActivity : AppCompatActivity() {
    fun selectPhoto() {
        val intent = Intent(this, PhotoPickerActivity::class.java)
        startActivityForResult(intent, PHOTO_REQUEST_CODE)
    }
    
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        
        if (requestCode == PHOTO_REQUEST_CODE && resultCode == RESULT_OK) {
            val selectedPhotoPath = data?.getStringExtra("photoPath")
            println("Selected photo: $selectedPhotoPath")
        }
    }
    
    companion object {
        const val PHOTO_REQUEST_CODE = 100
    }
}

// PhotoPickerActivity - send result back
class PhotoPickerActivity : AppCompatActivity() {
    fun onPhotoSelected(photoPath: String) {
        val intent = Intent()
        intent.putExtra("photoPath", photoPath)
        setResult(RESULT_OK, intent)
        finish()  // Close this activity
    }
}
```

---

## 6️⃣ Common Lifecycle Issues & Solutions

### **Issue 1: Memory Leak - Listeners Not Cleaned**

```kotlin
// ❌ BAD - Listener not removed
override fun onResume() {
    super.onResume()
    sensorManager.registerListener(listener, sensor, SENSOR_DELAY_NORMAL)
}

// ✅ GOOD - Listener removed
override fun onPause() {
    super.onPause()
    sensorManager.unregisterListener(listener)
}
```

### **Issue 2: Database Connections**

```kotlin
// ❌ BAD - Database left open
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    database.open()  // Never closed!
}

// ✅ GOOD - Proper open/close
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    database.open()
}

override fun onDestroy() {
    super.onDestroy()
    database.close()
}
```

### **Issue 3: Coroutines in Wrong Scope**

```kotlin
// ❌ BAD - Activity might be destroyed
GlobalScope.launch {
    val data = fetchData()
    updateUI(data)  // Crash if activity is destroyed!
}

// ✅ GOOD - Activity-aware coroutines
lifecycleScope.launch {
    val data = fetchData()
    updateUI(data)  // Safe!
}
```

---

## 🎓 Practice Questions & Answers

### **Q1: What happens to an Activity when the device rotates?**
**A**: `onPause → onStop → onDestroy` then `onCreate → onStart → onResume`. The Activity is recreated.

### **Q2: When should I use `onStop()` vs `onPause()`?**
**A**: `onPause()` when activity loses focus, `onStop()` when it's no longer visible.

### **Q3: Where should I initialize UI elements?**
**A**: In `onCreate()` after calling `setContentView()`.

### **Q4: How do I pass data between activities?**
**A**: Use `Intent.putExtra()` to send and `intent.getExtra()` to receive.

### **Q5: What's the difference between `finish()` and `System.exit()`?**
**A**: `finish()` closes the activity properly, `System.exit()` is dangerous and kills the entire app.

---

## 💡 Key Takeaways

1. ✅ Activities are screens in your app
2. ✅ Lifecycle has 7 states: created, started, resumed, paused, stopped, destroyed
3. ✅ Always clean up resources in appropriate lifecycle methods
4. ✅ Use `savedInstanceState` to save data during rotation
5. ✅ Use Intent to navigate and pass data
6. ✅ Use `lifecycleScope` for coroutines to prevent leaks

---

## 🏋️ Hands-On Exercise

Create an app with:
1. MainActivity with a counter button
2. Save counter value during rotation
3. Open a second activity with SetValue button
4. Get value back from second activity
5. Update counter with returned value

---

**Next: [Module 2.2 - XML Layouts (Complete Guide)](07_ANDROID_XML_LAYOUTS.md)**

# Module 2.3: Intent & Navigation - Complete Guide

## 🧭 What is Intent?

An **Intent** is a messaging object in Android that requests an action from another component (Activity, Service, Broadcast Receiver). It's like sending a letter with instructions.

### **Types of Intents**

```
Intents
├── Explicit Intent (target specific component)
└── Implicit Intent (let system find component)
```

---

## 📤 Explicit Intents - Direct Navigation

### **Starting Another Activity**
```kotlin
// In Activity, Fragment, or Context
val intent = Intent(this, SecondActivity::class.java)
startActivity(intent)
```

### **Passing Data Between Activities**
```kotlin
// SENDING DATA
val intent = Intent(this, UserDetailActivity::class.java)
intent.putExtra("user_id", 123)
intent.putExtra("user_name", "Alice")
intent.putExtra("user_email", "alice@example.com")
intent.putExtra("is_premium", true)
startActivity(intent)

// RECEIVING DATA
class UserDetailActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val userId = intent.getIntExtra("user_id", -1)
        val userName = intent.getStringExtra("user_name") ?: "Unknown"
        val userEmail = intent.getStringExtra("user_email") ?: ""
        val isPremium = intent.getBooleanExtra("is_premium", false)
        
        println("User: $userName ($userEmail) - Premium: $isPremium")
    }
}
```

### **Passing Objects (Parcelable)**
```kotlin
// Step 1: Make your class Parcelable
@Parcelize
data class User(
    val id: Int,
    val name: String,
    val email: String,
    val age: Int
) : Parcelable

// Step 2: Pass in Intent
val user = User(1, "Alice", "alice@email.com", 25)
val intent = Intent(this, UserProfileActivity::class.java)
intent.putExtra("user", user)
startActivity(intent)

// Step 3: Retrieve in another Activity
class UserProfileActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val user = intent.getParcelableExtra<User>("user")
        user?.let {
            println("${it.name} - ${it.email}")
        }
    }
}
```

---

## 🔄 startActivityForResult - Get Data Back

### **Request Data from Another Activity**
```kotlin
// ACTIVITY 1: Request data
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val intent = Intent(this, SelectContactActivity::class.java)
        startActivityForResult(intent, REQUEST_CODE)
    }
    
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        
        if (requestCode == REQUEST_CODE && resultCode == RESULT_OK) {
            val selectedName = data?.getStringExtra("contact_name")
            val selectedPhone = data?.getStringExtra("contact_phone")
            
            println("Selected: $selectedName ($selectedPhone)")
        }
    }
    
    companion object {
        const val REQUEST_CODE = 100
    }
}

// ACTIVITY 2: Send data back
class SelectContactActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // When user selects a contact
        onContactSelected("Alice", "+1234567890")
    }
    
    private fun onContactSelected(name: String, phone: String) {
        val resultIntent = Intent()
        resultIntent.putExtra("contact_name", name)
        resultIntent.putExtra("contact_phone", phone)
        setResult(RESULT_OK, resultIntent)
        finish()
    }
}
```

### **Modern Way: Activity Result Contracts**
```kotlin
class MainActivity : AppCompatActivity() {
    // Define contract
    private val selectContactLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == RESULT_OK) {
            val selectedName = result.data?.getStringExtra("contact_name")
            val selectedPhone = result.data?.getStringExtra("contact_phone")
            println("Selected: $selectedName ($selectedPhone)")
        }
    }
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Launch activity with contract
        val intent = Intent(this, SelectContactActivity::class.java)
        selectContactLauncher.launch(intent)
    }
}
```

---

## 🔍 Implicit Intents - System Finds Component

Implicit intents don't specify a target. Android finds matching components.

### **Common Implicit Intents**
```kotlin
// Send Email
val emailIntent = Intent(Intent.ACTION_SEND).apply {
    type = "message/rfc822"
    putExtra(Intent.EXTRA_EMAIL, arrayOf("recipient@example.com"))
    putExtra(Intent.EXTRA_SUBJECT, "Hello")
    putExtra(Intent.EXTRA_TEXT, "This is the email content")
}
startActivity(Intent.createChooser(emailIntent, "Send Email"))

// Open Website
val webIntent = Intent(Intent.ACTION_VIEW, "https://www.google.com".toUri())
startActivity(webIntent)

// Make Phone Call
val callIntent = Intent(Intent.ACTION_CALL)
callIntent.data = Uri.parse("tel:+1234567890")
if (ContextCompat.checkSelfPermission(this, Manifest.permission.CALL_PHONE)
    == PackageManager.PERMISSION_GRANTED) {
    startActivity(callIntent)
}

// Send SMS
val smsIntent = Intent(Intent.ACTION_SENDTO)
smsIntent.data = Uri.parse("smsto:+1234567890")
smsIntent.putExtra("sms_body", "Hello!")
startActivity(smsIntent)

// Open Map
val mapIntent = Intent(Intent.ACTION_VIEW)
mapIntent.data = Uri.parse("geo:37.7749,-122.4194?z=10")
startActivity(mapIntent)

// Search on Google
val searchIntent = Intent(Intent.ACTION_WEB_SEARCH)
searchIntent.putExtra(SearchManager.QUERY, "Kotlin Android")
startActivity(searchIntent)

// Share Content
val shareIntent = Intent(Intent.ACTION_SEND).apply {
    type = "text/plain"
    putExtra(Intent.EXTRA_TEXT, "Check this awesome article!")
}
startActivity(Intent.createChooser(shareIntent, "Share"))
```

---

## 🗂️ Navigation Patterns in Android

### **Activity-Based Navigation Stack**
```kotlin
// Activity A → Activity B → Activity C
//
// When user presses back from C, goes to B
// When user presses back from B, goes to A
// When user presses back from A, exits app

// In MainActivity
val intent = Intent(this, SecondActivity::class.java)
startActivity(intent)

// In SecondActivity
val intent = Intent(this, ThirdActivity::class.java)
startActivity(intent)

// Press back automatically handles the back stack
```

### **Back Stack Management**
```kotlin
// Clear back stack and start fresh
val intent = Intent(this, HomeActivity::class.java)
intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
startActivity(intent)

// Clear stack up to specific activity
intent.flags = Intent.FLAG_ACTIVITY_CLEAR_TOP
startActivity(intent)

// Single task (reuses existing instance)
intent.flags = Intent.FLAG_ACTIVITY_SINGLE_TOP
startActivity(intent)
```

---

## 📱 Real-World Example: Complete Navigation Flow

```kotlin
// ===== MAIN ACTIVITY (Login Screen) =====
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        val loginButton = findViewById<Button>(R.id.login_button)
        val emailInput = findViewById<EditText>(R.id.email_input)
        
        loginButton.setOnClickListener {
            val email = emailInput.text.toString()
            
            // Navigate to home with email
            val intent = Intent(this, HomeActivity::class.java)
            intent.putExtra("user_email", email)
            startActivity(intent)
            
            // Don't show login screen again
            finish()
        }
    }
}

// ===== HOME ACTIVITY (User's Home Screen) =====
class HomeActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home)
        
        val userEmail = intent.getStringExtra("user_email") ?: "Unknown"
        val profileButton = findViewById<Button>(R.id.view_profile_button)
        val settingsButton = findViewById<Button>(R.id.settings_button)
        val logoutButton = findViewById<Button>(R.id.logout_button)
        
        // View Profile
        profileButton.setOnClickListener {
            val intent = Intent(this, ProfileActivity::class.java)
            intent.putExtra("user_email", userEmail)
            startActivityForResult(intent, REQUEST_CODE_PROFILE)
        }
        
        // Settings
        settingsButton.setOnClickListener {
            val intent = Intent(this, SettingsActivity::class.java)
            startActivity(intent)
        }
        
        // Logout
        logoutButton.setOnClickListener {
            val intent = Intent(this, MainActivity::class.java)
            intent.flags = Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_NEW_TASK
            startActivity(intent)
            finish()
        }
    }
    
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == REQUEST_CODE_PROFILE && resultCode == RESULT_OK) {
            val updatedEmail = data?.getStringExtra("updated_email")
            println("Profile updated: $updatedEmail")
        }
    }
    
    companion object {
        const val REQUEST_CODE_PROFILE = 101
    }
}

// ===== PROFILE ACTIVITY =====
class ProfileActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_profile)
        
        val userEmail = intent.getStringExtra("user_email") ?: "Unknown"
        val editButton = findViewById<Button>(R.id.edit_button)
        val saveButton = findViewById<Button>(R.id.save_button)
        val emailEditText = findViewById<EditText>(R.id.email_edit)
        
        editButton.setOnClickListener {
            emailEditText.isEnabled = true
        }
        
        saveButton.setOnClickListener {
            val newEmail = emailEditText.text.toString()
            val resultIntent = Intent()
            resultIntent.putExtra("updated_email", newEmail)
            setResult(RESULT_OK, resultIntent)
            finish()
        }
    }
}

// ===== SETTINGS ACTIVITY =====
class SettingsActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_settings)
        
        val backButton = findViewById<Button>(R.id.back_button)
        backButton.setOnClickListener {
            finish()  // Return to previous activity
        }
    }
}
```

---

## 🎯 Intent Filters - Receive Implicit Intents

### **In AndroidManifest.xml**
```xml
<activity
    android:name=".ShareActivity"
    android:exported="true">
    <intent-filter>
        <action android:name="android.intent.action.SEND" />
        <category android:name="android.intent.category.DEFAULT" />
        <data android:mimeType="text/plain" />
    </intent-filter>
</activity>
```

### **Handle Incoming Intent**
```kotlin
class ShareActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Handle intent
        when (intent?.action) {
            Intent.ACTION_SEND -> {
                val sharedText = intent.getStringExtra(Intent.EXTRA_TEXT)
                println("Received text: $sharedText")
            }
        }
    }
}
```

---

## ✅ Practice Questions

1. **What's the difference between Explicit and Implicit Intent?**
   - Explicit: specify exact component; Implicit: let system find matching component

2. **How do you pass data between activities?**
   - Use `intent.putExtra()` to put data and `intent.getExtra()` to retrieve

3. **What does `startActivityForResult` do?**
   - Start an activity and expect a result back via `onActivityResult`

4. **How do you go back to previous activity?**
   - Call `finish()` or press back button

5. **What are intent flags used for?**
   - Control back stack behavior (FLAG_ACTIVITY_NEW_TASK, FLAG_ACTIVITY_CLEAR_TOP, etc)

---

## 🎓 Summary

- **Intent**: Messaging object for requesting actions
- **Explicit Intent**: Direct navigation to specific Activity
- **Implicit Intent**: Let system find appropriate app/component
- **putExtra/getExtra**: Pass data between activities
- **startActivityForResult**: Get data back from another activity
- **Back Stack**: Automatic navigation history management
- **Intent Flags**: Control how activities are added to back stack

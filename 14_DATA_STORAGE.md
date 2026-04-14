# Module 4.1: SharedPreferences & DataStore - Data Storage

## 💾 SharedPreferences - Simple Key-Value Storage

### **Write Data**
```kotlin
val sharedPref = context.getSharedPreferences("app_preferences", Context.MODE_PRIVATE)

sharedPref.edit().apply {
    putString("user_name", "Alice")
    putInt("user_age", 25)
    putBoolean("is_premium", true)
    putFloat("app_rating", 4.5f)
    apply()  // or commit() for synchronous
}
```

### **Read Data**
```kotlin
val sharedPref = context.getSharedPreferences("app_preferences", Context.MODE_PRIVATE)

val userName = sharedPref.getString("user_name", "Guest")
val userAge = sharedPref.getInt("user_age", 0)
val isPremium = sharedPref.getBoolean("is_premium", false)
val rating = sharedPref.getFloat("app_rating", 0f)
```

### **Delete Data**
```kotlin
sharedPref.edit().apply {
    remove("user_name")  // Remove specific key
    clear()              // Clear all
    apply()
}
```

## 📦 DataStore - Modern Replacement for SharedPreferences

### **Setup DataStore**
```kotlin
//  build.gradle
dependencies {
    implementation "androidx.datastore:datastore-preferences:1.0.0"
}

// Create DataStore
val userPreferences = context.createDataStore(name = "user_preferences")
```

### **Write with DataStore**
```kotlin
suspend fun saveUserName(name: String) {
    userPreferences.edit { settings ->
        settings[stringPreferencesKey("user_name")] = name
    }
}
```

### **Read with DataStore**
```kotlin
fun getUserNameFlow(): Flow<String> {
    return userPreferences.data.map { settings ->
        settings[stringPreferencesKey("user_name")] ?: "Guest"
    }
}

// Use in Compose
val userName = getUserNameFlow().collectAsState("Guest").value
```

## 🎓 Summary

- **SharedPreferences**: Simple key-value, synchronous (old)
- **DataStore**: Modern, asynchronous, type-safe (new)

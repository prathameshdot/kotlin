# Module 7.2: Security & Best Practices

## 🔐 Secure Data Storage

### **Encrypt Sensitive Data**
```kotlin
// Use EncryptedSharedPreferences
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .build()

val encryptedSharedPreferences = EncryptedSharedPreferences.create(
    context,
    "secret_settings",
    masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)

encryptedSharedPreferences.edit().apply {
    putString("api_key", "secret_key")
    apply()
}
```

## 🛡️ API Security

### **Use HTTPS Only**
```kotlin
// ✅ GOOD
val url = "https://api.example.com"

// ❌ BAD
val url = "http://api.example.com"  // No encryption!
```

### **Store Keys Securely**
```kotlin
// ❌ BAD: Keys in source code
const val API_KEY = "sk_live_abc123xyz"

// ✅ GOOD: Keys in BuildConfig or environment
buildTypes {
    release {
        buildConfigField "String", "API_KEY", "\"" + System.getenv("API_KEY") + "\""
    }
}

// Use in code
val apiKey = BuildConfig.API_KEY
```

## 🔑 Authentication Best Practices

```kotlin
// Store auth tokens securely
val encryptedPrefs = EncryptedSharedPreferences.create(...)
encryptedPrefs.edit {
    putString("auth_token", authToken)
}

// Add token to requests
val interceptor = Interceptor { chain ->
    val originalRequest = chain.request()
    val token = getAuthToken()  // From encrypted storage
    
    val newRequest = originalRequest.newBuilder()
        .addHeader("Authorization", "Bearer $token")
        .build()
    
    chain.proceed(newRequest)
}
```

## ✅ Best Practices Summary

- Use HTTPS for all network requests
- Store sensitive data encrypted
- Validate user input
- Use latest library versions
- Handle errors gracefully
- Never hardcode secrets
- Use ProGuard/R8 for release builds
- Request minimum required permissions
- Validate SSL certificates

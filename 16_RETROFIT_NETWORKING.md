# Module 5.1: Retrofit & HTTP Requests - Networking

## 🌐 Retrofit Setup

### **Dependencies**
```gradle
dependencies {
    implementation "com.squareup.retrofit2:retrofit:2.10.0"
    implementation "com.squareup.retrofit2:converter-gson:2.10.0"
    implementation "com.squareup.okhttp3:logging-interceptor:4.11.0"
}
```

### **Create API Interface**
```kotlin
interface ApiService {
    @GET("users")
    suspend fun getUsers(): List<User>
    
    @GET("users/{id}")
    suspend fun getUserById(@Path("id") userId: Int): User
    
    @GET("users")
    suspend fun searchUsers(@Query("q") query: String): List<User>
    
    @POST("users")
    suspend fun createUser(@Body user: User): User
    
    @PUT("users/{id}")
    suspend fun updateUser(@Path("id") userId: Int, @Body user: User): User
    
    @DELETE("users/{id}")
    suspend fun deleteUser(@Path("id") userId: Int)
}
```

### **Retrofit Client**
```kotlin
object RetrofitClient {
    private const val BASE_URL = "https://api.example.com/"
    
    val apiService: ApiService by lazy {
        val logger = HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        }
        
        val okHttpClient = OkHttpClient.Builder()
            .addInterceptor(logger)
            .build()
        
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
}
```

### **Make Requests**
```kotlin
// Simple request
val users = RetrofitClient.apiService.getUsers()

// With error handling
try {
    val user = RetrofitClient.apiService.getUserById(1)
    println("User: ${user.name}")
} catch (e: Exception) {
    println("Error: ${e.message}")
}
```

## 🔄 Result Pattern for Error Handling

```kotlin
sealed class Result<T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error<T>(val exception: Exception) : Result<T>()
    class Loading<T> : Result<T>()
}

class UserRepository {
    suspend fun getUsers(): Result<List<User>> = try {
        val users = RetrofitClient.apiService.getUsers()
        Result.Success(users)
    } catch (e: Exception) {
        Result.Error(e)
    }
}

// Usage
when (val result = repository.getUsers()) {
    is Result.Success -> println("Users: ${result.data}")
    is Result.Error -> println("Error: ${result.exception.message}")
    is Result.Loading -> println("Loading...")
}
```

## 🎓 Summary

Retrofit simplifies HTTP communication with type-safe API definitions.

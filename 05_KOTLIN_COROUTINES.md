# Module 1.5: Coroutines - Asynchronous Programming
## Handle Long Tasks Without Blocking UI

---

## 📖 What are Coroutines?

Coroutines let you run long operations (like network requests) **without freezing your app**. Think of it like ordering food - the restaurant doesn't stop serving everyone because they're making your order.

---

## 1️⃣ Why Coroutines Matter in Android

### **The Problem: Blocking Operations**

```kotlin
// ❌ This freezes the UI while loading data!
fun loadUserData() {
    val data = makeNetworkRequest()  // Takes 5 seconds
    updateUI(data)                   // Stuck waiting!
}

// Meanwhile, user taps buttons - nothing happens! 😤
```

### **The Solution: Coroutines**

```kotlin
// ✅ This doesn't freeze the UI!
fun loadUserData() {
    // Runs in background, doesn't block main thread
    lifecycleScope.launch {
        val data = makeNetworkRequest()  // Happens in background
        updateUI(data)                   // Updates UI when ready
    }
}

// Meanwhile, user can still interact with app! 😊
```

---

## 2️⃣ Basic Coroutine Concepts

### **Launch - Fire and Forget**

```kotlin
// Start a task that you don't need to wait for
GlobalScope.launch {
    println("Background task started")
    Thread.sleep(2000)
    println("Background task finished")
}
println("Main thread continues")

// Output:
// Main thread continues
// Background task started
// Background task finished (after 2 sec)
```

### **Async - Wait for Result**

```kotlin
// Start a task and wait for its result
lifecycleScope.launch {
    val data = async { fetchUserData() }  // Start task
    val result = data.await()             // Wait for result
    updateUI(result)
}

// Think of it like:
// You order food (async) and wait for it (await) before eating
```

### **Dispatchers - Choose Your Thread**

```kotlin
lifecycleScope.launch(Dispatchers.Default) {
    // Heavy computation
    val result = complexCalculation()  // Uses background thread
    
    // Switch to Main thread to update UI
    withContext(Dispatchers.Main) {
        updateUI(result)
    }
}

// Common dispatchers:
// - Dispatchers.Main: UI thread
// - Dispatchers.Default: Background computation
// - Dispatchers.IO: Network and disk operations
```

---

## 3️⃣ Real-World Example: Fetch User Data

### **Without Coroutines (Callback Hell)**

```kotlin
// ❌ Messy and hard to read
fun loadUserWithCallbacks(userId: Int) {
    ApiClient.getUser(userId, object : Callback {
        override fun onSuccess(user: User) {
            val preferences = user.preferences
            ApiClient.getUserPosts(userId, object : Callback {
                override fun onSuccess(posts: List<Post>) {
                    updateUI(user, posts, preferences)
                }
                override fun onFailure(error: Exception) {
                    showError(error.message)
                }
            })
        }
        override fun onFailure(error: Exception) {
            showError(error.message)
        }
    })
}
```

### **With Coroutines (Clean and Sequential)**

```kotlin
// ✅ Sequential, readable code
fun loadUser(userId: Int) {
    lifecycleScope.launch {
        try {
            // Sequential calls - reads like normal code
            val user = fetchUser(userId)        // Wait for user
            val preferences = fetchPreferences(userId)  // Then preferences
            val posts = fetchUserPosts(userId)  // Then posts
            
            // Update UI with all data
            updateUI(user, posts, preferences)
        } catch (exception: Exception) {
            showError(exception.message)
        }
    }
}

// Network functions (must run in coroutine or be suspend functions)
suspend fun fetchUser(userId: Int): User = withContext(Dispatchers.IO) {
    return@withContext apiClient.getUser(userId)
}

suspend fun fetchPreferences(userId: Int): UserPreferences = 
    withContext(Dispatchers.IO) {
        return@withContext apiClient.getPreferences(userId)
    }

suspend fun fetchUserPosts(userId: Int): List<Post> = 
    withContext(Dispatchers.IO) {
        return@withContext apiClient.getUserPosts(userId)
    }
```

---

## 4️⃣ Suspend Functions

### **What is a Suspend Function?**

A suspend function can be paused and resumed without blocking the thread.

```kotlin
// Regular function (blocks thread)
fun getName(): String {
    Thread.sleep(2000)  // Freezes!
    return "Alice"
}

// Suspend function (doesn't block)
suspend fun getName(): String {
    delay(2000)  // Pauses coroutine, doesn't freeze thread!
    return "Alice"
}

// Can only call suspend functions from coroutines
lifecycleScope.launch {
    val name = getName()  // ✅ OK
    println(name)
}

// getName()  // ❌ ERROR! Not in a coroutine
```

### **withContext - Switch Threads**

```kotlin
suspend fun fetchUserData(): UserData {
    // Even though we're in a suspend function...
    // Switch to IO thread for network call
    return withContext(Dispatchers.IO) {
        // Network request on IO thread
        val user = apiClient.getUser()
        val posts = apiClient.getUserPosts()
        return@withContext UserData(user, posts)
    }
    // Automatically back to caller's thread
}

lifecycleScope.launch {
    val data = fetchUserData()  // Runs on caller's dispatcher
    updateUI(data)              // Update UI
}
```

---

## 5️⃣ Practical Android Example: Weather App

```kotlin
data class WeatherData(
    val temperature: Double,
    val conditions: String,
    val humidity: Int
)

class WeatherViewModel : ViewModel() {
    private val _weather = MutableLiveData<WeatherData>()
    val weather: LiveData<WeatherData> = _weather
    
    fun fetchWeather(city: String) {
        viewModelScope.launch {
            try {
                // Show loading state
                _weather.value = null
                
                // Fetch data in background
                val weatherData = withContext(Dispatchers.IO) {
                    // Call API
                    weatherApi.getWeather(city)
                }
                
                // Update UI with data
                _weather.value = weatherData
                
            } catch (exception: Exception) {
                println("Error fetching weather: ${exception.message}")
            }
        }
    }
}

// Usage in Activity/Fragment
class WeatherFragment : Fragment() {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        val viewModel = ViewModelProvider(this).get(WeatherViewModel::class.java)
        
        // Observe weather data
        viewModel.weather.observe(viewLifecycleOwner) { weatherData ->
            temperatureText.text = "${weatherData.temperature}°C"
            conditionsText.text = weatherData.conditions
            humidityText.text = "Humidity: ${weatherData.humidity}%"
        }
        
        // Fetch weather for New York
        viewModel.fetchWeather("New York")
    }
}
```

---

## 6️⃣ Error Handling in Coroutines

```kotlin
viewModelScope.launch {
    try {
        val user = fetchUser(userId)
        updateUI(user)
    } catch (exception: IOException) {
        // Network error
        showError("No internet connection")
    } catch (exception: HttpException) {
        // Server error
        showError("Server error: ${exception.message}")
    } catch (exception: Exception) {
        // Other errors
        showError("Something went wrong")
    }
}

// With timeout
viewModelScope.launch {
    try {
        withTimeoutOrNull(5000) {  // 5 second timeout
            val data = fetchUserData()
            updateUI(data)
        } ?: showError("Request timed out")
    } catch (exception: Exception) {
        showError(exception.message)
    }
}
```

---

## 7️⃣ Parallel Operations

```kotlin
// Run multiple tasks in parallel
viewModelScope.launch {
    try {
        // Start both requests at the same time
        val userDeferred = async { fetchUser(userId) }
        val postsDeferred = async { fetchUserPosts(userId) }
        
        // Wait for both to complete
        val user = userDeferred.await()
        val posts = postsDeferred.await()
        
        // Both done, update UI
        updateUI(user, posts)
        
    } catch (exception: Exception) {
        showError(exception.message)
    }
}
```

---

## 🎓 Practice Questions & Answers

### **Q1: What's the difference between launch and async?**
**A**: `launch` is fire-and-forget, `async` returns a value you can await.

### **Q2: Why is `delay()` better than `Thread.sleep()`?**
**A**: `delay()` suspends the coroutine without blocking the thread, while `sleep()` freezes the thread.

### **Q3: When should I use `Dispatchers.IO` vs `Dispatchers.Main`?**
**A**: Use IO for network/disk, Main for UI updates.

### **Q4: What's a suspend function?**
**A**: A function that can be paused and resumed without blocking the thread. Only callable from coroutines.

---

## 💡 Key Takeaways

1. ✅ Coroutines prevent UI freezing during long operations
2. ✅ Use `launch` for independent tasks, `async` for results
3. ✅ Use `withContext` to switch threads
4. ✅ Suspend functions don't block threads
5. ✅ Always use `viewModelScope` in Activities/Fragments
6. ✅ Proper error handling is essential

---

**Next: [Module 2.1 - Android Basics & Activity Lifecycle](06_ANDROID_BASICS.md)**

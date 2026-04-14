# Module 26: Android Interview Questions
## Prepare for Job Interviews

---

## 🎯 Interview Preparation Guide

This module has compiled interview questions that are commonly asked by Android companies. Study these thoroughly along with the projects you've built.

---

## ⭐ EASY Questions (Junior Level)

### **Q1: What is Android?**
**Answer**:
Android is an open-source operating system for mobile devices. It's built on Linux kernel and developed by Google. It allows developers to build applications that can run on various devices.

### **Q2: What is an Activity?**
**Answer**:
An Activity is a single-screen interface in an Android application. Each screen is an Activity. Activities manage the interaction between the user and the app.

### **Q3: What is the difference between onCreate and onStart?**
**Answer**:
- `onCreate()`: Called when the activity is first created. Data is initialized here.
- `onStart()`: Called when the activity becomes visible to the user. Called after onCreate().

### **Q4: How do you pass data between Activities?**
**Answer**:
Using an Intent with extras (Bundle):
```kotlin
val intent = Intent(this, SecondActivity::class.java)
intent.putExtra("key", value)
startActivity(intent)

// Receiving
val value = intent.getExtra("key")
```

### **Q5: What are Fragments?**
**Answer**:
Fragments are reusable UI components that run within an Activity. They have their own lifecycle and can be added/removed dynamically. Useful for supporting multiple screen sizes.

### **Q6: What is SharedPreferences?**
**Answer**:
SharedPreferences is used to store key-value pairs of simple data. It's suitable for storing small data like user preferences, login tokens, settings.

### **Q7: What is the difference between Intent and Bundle?**
**Answer**:
- **Intent**: Used to start an activity or service. Can contain data (Bundle).
- **Bundle**: Container for key-value pairs, used to pass data.

### **Q8: What is AndroidManifest.xml?**
**Answer**:
It's a configuration file that describes the structure of the Android app. It lists activities, services, permissions, API level requirements, etc.

### **Q9: What are the types of permissions?**
**Answer**:
1. **Normal Permissions**: Granted automatically. Example: INTERNET
2. **Dangerous Permissions**: Require runtime approval. Example: CAMERA, LOCATION

### **Q10: What is Gradle in Android?**
**Answer**:
Gradle is a build automation tool used to compile, build, and package Android applications. The build.gradle file contains dependencies and build configurations.

---

## 🟡 MEDIUM Questions (Mid Level)

### **Q11: Explain the Activity Lifecycle completely**
**Answer**:
```
onCreate  → Create activity, initialize data
        ↓
onStart   → Activity becomes visible
        ↓
onResume  → Activity is in foreground, user can interact
        ↓
onPause   → Activity loses focus but still visible
        ↓
onStop    → Activity no longer visible
        ↓
onDestroy → Activity is destroyed
```

When device rotates: onPause → onStop → onDestroy → onCreate → onStart → onResume

### **Q12: What is MVVM Architecture?**
**Answer**:
MVVM divides the app into three layers:
- **Model**: Data layer
- **View**: UI layer (Activities/Fragments)
- **ViewModel**: Logic layer (business logic, handles data)

Benefits: Testable, reusable, survives configuration changes.

### **Q13: What are LiveData and StateFlow?**
**Answer**:
Both are observable data containers:
- **LiveData**: Lifecycle-aware, older pattern
- **StateFlow**: State management, Coroutine-based, modern

StateFlow is recommended for new projects.

### **Q14: What are Coroutines and why use them?**
**Answer**:
Coroutines are lightweight threads that don't block. They let you run long operations without freezing the UI.

```kotlin
lifecycleScope.launch {  // Does NOT block UI
    val data = fetchData()  // Can pause/resume
    updateUI(data)
}
```

### **Q15: What is the difference between launch and async?**
**Answer**:
- `launch`: Fire-and-forget, doesn't return value
- `async`: Returns a value that you can await

```kotlin
lifecycleScope.launch {
    val data = async { fetchData() }.await()
}
```

### **Q16: Explain Jetpack Compose**
**Answer**:
Jetpack Compose is Google's modern UI toolkit that uses declarative programming. Instead of XML, you write Kotlin functions.

Advantages:
- Code reuse (composable functions)
- Easy state management
- Type-safe
- Automatic recomposition

### **Q17: What is the remember function in Compose?**
**Answer**:
`remember` keeps state across recompositions.

```kotlin
var count = remember { mutableStateOf(0) }
```

When state changes, Compose automatically re-renders affected composables.

### **Q18: What is the Modifier in Compose?**
**Answer**:
Modifiers control how a composable looks and behaves. They can be chained together.

```kotlin
Modifier
    .size(100.dp)
    .padding(16.dp)
    .background(Color.Blue)
    .clickable { }
```

### **Q19: What is Room Database?**
**Answer**:
Room is an abstraction layer over SQLite. It provides:
- Type safety
- Compile-time SQL verification
- Coroutine support
- Flow support for observing data changes

```kotlin
@Entity
data class User(
    @PrimaryKey val id: Int,
    val name: String
)

@Dao
interface UserDao {
    @Query("SELECT * FROM user")
    fun getAllUsers(): Flow<List<User>>
}
```

### **Q20: What is Retrofit?**
**Answer**:
Retrofit is a type-safe HTTP client for Android. It converts HTTP APIs into Kotlin interfaces.

```kotlin
interface ApiService {
    @GET("users/{id}")
    suspend fun getUser(@Path("id") userId: Int): User
}
```

---

## 🔴 HARD Questions (Senior Level)

### **Q21: Explain the difference between suspend functions and regular functions**
**Answer**:
- **Regular functions**: Block the thread
- **Suspend functions**: Can be paused and resumed without blocking the thread

Suspend functions can only be called from coroutines or other suspend functions.

```kotlin
suspend fun getUser(): User = withContext(Dispatchers.IO) {
    // Network call on IO thread
}
```

### **Q22: What is Dependency Injection and how is Hilt used?**
**Answer**:
DI means providing dependencies from outside instead of creating inside.

```kotlin
@Singleton
@Provides
@Module
@InstallIn(SingletonComponent::class)
class AppModule {
    @Provides
    fun provideApiService(): ApiService {
        return Retrofit.Builder()
            .baseUrl("https://api.example.com")
            .build()
            .create(ApiService::class.java)
    }
}

@HiltViewModel
class UserViewModel @Inject constructor(
    val repository: UserRepository
) : ViewModel()
```

Benefits: Easy testing, loose coupling, centralized configuration.

### **Q23: Explain memory leaks and how to prevent them**
**Answer**:
Memory leaks occur when objects are not released even when no longer needed.

**Common causes**:
1. Unregistered listeners
2. Inner class references
3. Static references to Activity/Context

**Prevention**:
```kotlin
override fun onResume() {
    sensorManager.registerListener(listener, sensor, SENSOR_DELAY_NORMAL)
}

override fun onPause() {
    sensorManager.unregisterListener(listener)  // Unregister!
}

// Use weak references
private var activity: WeakReference<MainActivity>? = null
```

### **Q24: What is the difference between implicit and explicit Intent?**
**Answer**:
- **Explicit**: Specify exact activity to start
  ```kotlin
  Intent(this, ProfileActivity::class.java)
  ```
- **Implicit**: Let Android choose app/activity
  ```kotlin
  Intent(Intent.ACTION_SEND).apply {
      type = "text/plain"
  }
  ```

### **Q25: How does Jetpack Compose's recomposition work?**
**Answer**:
Compose recomposes only the parts that depend on changed state. This is more efficient than recreating the entire screen.

```kotlin
@Composable
fun MyScreen() {
    var count = remember { mutableStateOf(0) }
    
    Column {
        Button(onClick = { count.value++ }) {  // Only this button recomposes
            Text("${count.value}")
        }
        ExpensiveComposable()  // This doesn't recompose if it doesn't depend on count
    }
}
```

### **Q26: Explain the difference between GlobalScope and viewModelScope**
**Answer**:
- **GlobalScope**: Coroutine lives for entire app duration. Can cause leaks.
- **viewModelScope**: Coroutine is canceled when ViewModel is destroyed. Safe.

```kotlin
// ❌ Bad
GlobalScope.launch {
    val data = fetchData()
    updateUI(data)  // Crash if activity destroyed
}

// ✅ Good
lifecycleScope.launch {
    val data = fetchData()
    updateUI(data)  // Safe!
}
```

### **Q27: What are Broadcast Receivers and when to use them?**
**Answer**:
Broadcast Receivers listen for system or app events.

```kotlin
class MyReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context?, intent: Intent?) {
        when (intent?.action) {
            Intent.ACTION_BATTERY_LOW -> {
                // Battery is low
            }
        }
    }
}
```

Use cases:
- Network state changes
- Battery level changes
- App updates
- Custom app events

### **Q28: What is the difference between Thread and Coroutine?**
**Answer**:
| Feature | Thread | Coroutine |
|---------|--------|-----------|
| Memory | Heavy (1-2MB) | Lightweight (few KB) |
| Switching | Managed by OS | Managed by runtime |
| Blocking | Blocks thread | Doesn't block thread |
| Count | Limited (~100s) | Thousands possible |

```kotlin
// Thread
Thread {
    val data = fetchData()  // Blocks thread!
}.start()

// Coroutine
lifecycleScope.launch {
    val data = fetchData()  // Doesn't block!"
}
```

### **Q29: Explain Scoped Storage in Android**
**Answer**:
Scoped Storage restricts file access for security. Apps can only access:
- App-specific directory: `getExternalFilesDir()`
- MediaStore for media files
- SAF (Storage Access Framework) for other files

### **Q30: What is ANR (Application Not Responding)?**
**Answer**:
ANR occurs when the app doesn't respond for 5+ seconds. Causes:
- Long operations on main thread
- Deadlocks

Solution:
- Use Coroutines/async tasks
- Move heavy work off main thread
- Use background services

---

## 📲 Android Studio Questions

### **Q31: How do you debug an Android app?**
**Answer**:
1. Set breakpoints
2. Run in Debug mode (Shift + F9)
3. Use Logcat to view logs
4. Use Android Profiler to check memory/CPU
5. Use Layout Inspector for UI debugging

### **Q32: What are the different build types?**
**Answer**:
- **Debug**: For development, debuggable
- **Release**: For production, optimized, minified
- **Staging**: For QA testing

### **Q33: How do you handle screen rotation?**
**Answer**:
1. Save state in `onSaveInstanceState()`
2. Restore in `onCreate()`

```kotlin
override fun onSaveInstanceState(outState: Bundle) {
    outState.putInt("counter", counter)
}

override fun onCreate(savedInstanceState: Bundle?) {
    counter = savedInstanceState?.getInt("counter") ?: 0
}
```

---

## 🌐 Behavioral Questions

### **Q34: Tell us about a challenging project you worked on**
**Strategy**: Prepare a story with:
- Problem you faced
- Your solution
- Result and learning

### **Q35: How do you stay updated with Android development?**
**Answer**:
- Read official Android documentation
- Follow Android blogs
- Contribute to open-source
- Attend conferences/webinars
- Practice on side projects

### **Q36: Describe a time when code review feedback helped you improve**
**Strategy**: Show humility and growth mindset. Explain how you incorporated feedback.

---

## 💻 Coding Interview Tips

1. **Clarify Requirements**: Ask questions before coding
2. **Explain Your Approach**: Think out loud
3. **Start Simple**: Then optimize
4. **Handle Edge Cases**: Discuss potential issues
5. **Test Your Code**: Walk through examples
6. **Discuss Trade-offs**: Why did you choose this approach?

### Example Coding Problem:
**Q: Implement a function to search for a word in a grid**

```kotlin
fun searchWord(grid: Array<CharArray>, word: String): Boolean {
    for (i in grid.indices) {
        for (j in grid[i].indices) {
            if (grid[i][j] == word[0]) {
                if (dfs(grid, word, 0, i, j, Array(grid.size) { BooleanArray(grid[0].size) })) {
                    return true
                }
            }
        }
    }
    return false
}

private fun dfs(
    grid: Array<CharArray>,
    word: String,
    index: Int,
    i: Int,
    j: Int,
    visited: Array<BooleanArray>
): Boolean {
    if (index == word.length) return true
    if (i < 0 || i >= grid.size || j < 0 || j >= grid[i].size) return false
    if (visited[i][j]) return false
    if (grid[i][j] != word[index]) return false
    
    visited[i][j] = true
    
    // Check all 4 directions
    val found = dfs(grid, word, index + 1, i + 1, j, visited) ||
                dfs(grid, word, index + 1, i - 1, j, visited) ||
                dfs(grid, word, index + 1, i, j + 1, visited) ||
                dfs(grid, word, index + 1, i, j - 1, visited)
    
    visited[i][j] = false
    return found
}
```

---

## 🎯 Interview Checklist

Before the interview:
- ✅ Review Android lifecycle
- ✅ Understand MVVM and Compose
- ✅ Know Coroutines well
- ✅ Practice coding on leetcode
- ✅ Prepare project stories
- ✅ Know your resume inside-out
- ✅ Mock interview with friend
- ✅ Get good sleep night before

During interview:
- ✅ Listen carefully
- ✅ Ask clarifying questions
- ✅ Think before answering
- ✅ Admit if you don't know something
- ✅ Ask good questions about the role
- ✅ Be enthusiastic and positive

---

## 📚 Resources for Interview Prep

- **Official Android Docs**: https://developer.android.com
- **Coding Practice**: LeetCode, HackerRank
- **YouTube Channels**: Philipp Lackner, Traversy Media
- **Open Source**: Contribute to Android projects
- **Mock Interviews**: Practice with peers

---

**Congratulations! You've completed the Android Developer Course! 🎉**

**Next Steps**:
1. Build your own app
2. Contribute to open-source
3. Apply for Android Developer jobs
4. Keep learning new technologies
5. Network with other developers


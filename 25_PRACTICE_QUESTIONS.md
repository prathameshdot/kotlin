# Module 25: Practice Questions & Answers
## Complete Q&A for Android Development Mastery

---

## 📚 Kotlin Fundamentals Q&A

### **Q1: Explain the difference between val and var with a real-world example**
**Level**: Beginner

**Answer**:
- `val` = immutable (read-only), cannot be changed after assignment
- `var` = mutable, can be changed after assignment

**Real Example - Bank Account**:
```kotlin
val accountNumber = "1234567890"  // Never changes - permanent
var balance = 1000.0              // Changes with every transaction

// This works
balance = 950.0  // Withdrawal

// This crashes
accountNumber = "0987654321"  // ❌ ERROR!
```

**Best Practice**: Always use `val` by default, only use `var` when you need to change the value.

---

### **Q2: What is null safety and why is it important?**
**Level**: Beginner

**Answer**:
Null safety means the language prevents `null` errors at compile time instead of runtime crashes.

```kotlin
// Java (Unsafe)
String name = null;
int length = name.length();  // ❌ NullPointerException at runtime!

// Kotlin (Safe)
val name: String? = null  // Explicitly nullable
val length = name?.length  // Safe - returns null if name is null
val nameOrDefault = name ?: "Unknown"  // Provides default if null
```

**Why It Matters**:
- Prevents app crashes
- Forces you to handle null cases
- Makes code safer and more reliable

---

### **Q3: What are extension functions and when would you use them?**
**Level**: Intermediate

**Answer**:
Extension functions let you add new methods to existing classes without inheritance.

```kotlin
// Add method to String class
fun String.wordCount(): Int = this.split(" ").size

// Add method to Int class
fun Int.isEven(): Boolean = this % 2 == 0

// Usage
println("Hello Android World".wordCount())  // 3
println(10.isEven())                        // true
println(7.isEven())                         // false

// Real app example - validate email
fun String.isValidEmail(): Boolean {
    return this.contains("@") && this.contains(".")
}

// In your code
if (userInput.isValidEmail()) {
    saveEmail(userInput)
}
```

**When to Use**:
- Add utility methods to built-in types
- Make code more readable
- Don't modify existing classes

---

### **Q4: Compare lambda vs regular functions**
**Level**: Intermediate

**Answer**:
```kotlin
// Regular function
fun add(a: Int, b: Int): Int = a + b

// Lambda (unnamed function, assigned to variable)
val addLambda = { a: Int, b: Int -> a + b }
val addLambda2: (Int, Int) -> Int = { a, b -> a + b }

// Usage
println(add(5, 3))         // 8
println(addLambda(5, 3))   // 8

// Lambdas are especially useful for collections
val numbers = listOf(1, 2, 3, 4, 5)
val doubled = numbers.map { it * 2 }  // Lambda here!
val evens = numbers.filter { it % 2 == 0 }  // Lambda here!
```

**When to Use Lambdas**:
- Pass to higher-order functions
- Use with collections (map, filter, etc)
- Event handlers and callbacks

---

### **Q5: Explain coroutines and why they're better than threads**
**Level**: Advanced

**Answer**:
Coroutines are lightweight, suspendable functions that don't block threads.

```kotlin
// ❌ Bad - Blocks UI thread
fun loadData() {
    val data = apiClient.getUser()  // Freezes UI!
    updateUI(data)
}

// ✅ Good - Uses coroutine
fun loadData() {
    lifecycleScope.launch {
        val data = apiClient.getUser()  // Doesn't freeze UI
        updateUI(data)
    }
}
```

**Advantages**:
- Lightweight (thousands per app vs threads)
- Don't block threads
- Sequential code (looks normal)
- Better error handling

---

## 🏗️ Android Fundamentals Q&A

### **Q6: Explain the Activity Lifecycle with a practical example**
**Level**: Beginner

**Answer**:
Lifecycle is the series of states an Activity goes through:

```
onCreate    → Activity is created, initialize UI
onStart     → Activity becomes visible
onResume    → Activity is running, user can interact
onPause     → Activity loses focus but is visible
onStop      → Activity is no longer visible
onDestroy   → Activity is destroyed
```

**Practical Example - Music Player**:
```kotlin
class MusicPlayerActivity : AppCompatActivity() {
    private lateinit var mediaPlayer: MediaPlayer
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_music)
        mediaPlayer = MediaPlayer.create(this, R.raw.song)
    }
    
    override fun onResume() {
        super.onResume()
        mediaPlayer.start()  // User comes back - play music
    }
    
    override fun onPause() {
        super.onPause()
        mediaPlayer.pause()  // User switches app - pause music
    }
    
    override fun onDestroy() {
        super.onDestroy()
        mediaPlayer.release()  // Clean up resources
    }
}
```

---

### **Q7: How do you save data when device rotates?**
**Level**: Intermediate

**Answer**:
When device rotates, Activity is destroyed and recreated. Save data with `onSaveInstanceState`:

```kotlin
class MainActivity : AppCompatActivity() {
    private var counter = 0
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // Restore saved data
        if (savedInstanceState != null) {
            counter = savedInstanceState.getInt("counterKey", 0)
        }
    }
    
    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putInt("counterKey", counter)
    }
}
```

**Important**: This only saves simple data during rotation. For persistent data, use:
- SharedPreferences (small data)
- Room Database (large data)
- DataStore (modern preference)

---

### **Q8: Explain Intent and Bundle**
**Level**: Intermediate

**Answer**:
- **Intent**: Message to Android to navigate to another screen
- **Bundle**: Container to pass data between activities

```kotlin
// MainActivity - Send to SecondActivity
val intent = Intent(this, SecondActivity::class.java)
intent.putExtra("userId", 123)
intent.putExtra("userName", "Alice")
startActivity(intent)

// SecondActivity - Receive data
val userId = intent.getIntExtra("userId", -1)
val userName = intent.getStringExtra("userName") ?: "Unknown"
```

**Types of Intents**:
```kotlin
// Explicit intent (to specific activity)
val intent = Intent(this, ProfileActivity::class.java)

// Implicit intent (let Android choose)
val intent = Intent(Intent.ACTION_SEND)
intent.type = "text/plain"
intent.putExtra(Intent.EXTRA_TEXT, "Message")
startActivity(intent)
```

---

### **Q9: What are Fragments and when should you use them?**
**Level**: Intermediate

**Answer**:
Fragments are reusable UI components that run within an Activity:

```kotlin
class HomeFragment : Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_home, container, false)
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        // Initialize UI here
    }
}

// In Activity
supportFragmentManager.beginTransaction()
    .replace(R.id.fragmentContainer, HomeFragment())
    .addToBackStack(null)
    .commit()
```

**When to Use**:
- Reusable UI components
- Multi-pane layouts (phone vs tablet)
- Navigation (home, profile, settings)

---

### **Q10: What are Activities vs Services?**
**Level**: Intermediate

**Answer**:
- **Activity**: User-visible, interactive screen
- **Service**: Background process, no UI

```kotlin
// Activity - visible, interactive
class MainActivity : AppCompatActivity() {
    // User sees this screen
}

// Service - background work
class DownloadService : Service() {
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // Download file in background
        downloadFile()
        return START_STICKY
    }
}

// Start service from Activity
val intent = Intent(this, DownloadService::class.java)
startService(intent)
```

---

## 🎨 Jetpack Compose Q&A

### **Q11: What makes Compose different from XML layouts?**
**Level**: Beginner

**Answer**:

| Feature | XML | Compose |
|---------|-----|---------|
| **Style** | Declarative XML | Kotlin code |
| **Reuse** | Hard | Easy (just functions) |
| **State** | ManualUpdates | Automatic re-render |
| **Type Safety** | NOT safe | Type-safe |
| **Learning** | Separate concepts | One language |

```kotlin
// XML (Old Way)
<!-- activity_main.xml -->
<Button android:text="Click" android:onClick="onButtonClick" />

// Compose (New Way)
@Composable
fun MyScreen() {
    Button(onClick = { println("Clicked") }) {
        Text("Click")
    }
}
```

---

### **Q12: How does state management work in Compose?**
**Level**: Intermediate

**Answer**:
When state changes, Compose re-renders the UI automatically:

```kotlin
@Composable
fun Counter() {
    var count = remember { mutableStateOf(0) }  // Create state
    
    Column {
        Text("Count: ${count.value}")
        
        Button(onClick = {
            count.value++  // Change state
            // UI automatically re-renders!
        }) {
            Text("Increment")
        }
    }
}

// Cleaner syntax with destructuring
@Composable
fun CounterCleaner() {
    var (count, setCount) = remember { mutableStateOf(0) }
    
    Column {
        Text("Count: $count")
        Button(onClick = { setCount(count + 1) }) {
            Text("Increment")
        }
    }
}
```

**Key Points**:
- `remember` keeps state across recomposes
- When state changes, Compose re-renders affected composables
- Only re-renders, doesn't destroy and recreate

---

### **Q13: Explain Modifiers**
**Level**: Intermediate

**Answer**:
Modifiers control how composables look and behave:

```kotlin
@Composable
fun UserCard() {
    Text(
        "Alice",
        modifier = Modifier
            .fillMaxWidth()                    // Width 100%
            .padding(16.dp)                    // Inside space
            .background(Color.LightBlue)       // Background color
            .border(2.dp, Color.Blue)          // Border
            .clip(RoundedCornerShape(8.dp))    // Rounded corners
            .clickable { println("Clicked") }  // Clickable
    )
}
```

**Common Modifiers**:
```kotlin
Modifier.size(100.dp)           // Fixed size
Modifier.fillMaxWidth()         // 100% width
Modifier.fillMaxHeight()        // 100% height
Modifier.fillMaxSize()          // 100% both
Modifier.padding(16.dp)         // Space inside
Modifier.background(Color.Blue) // Background
Modifier.weight(1f)             // Share space
Modifier.alpha(0.5f)            // Transparency
```

---

### **Q14: What's the difference between Column and Row?**
**Level**: Beginner

**Answer**:
- **Column**: Arranges items vertically (top-to-bottom)
- **Row**: Arranges items horizontally (left-to-right)

```kotlin
@Composable
fun ColumnExample() {
    Column {
        Text("Item 1")
        Text("Item 2")
        Text("Item 3")
        // Stacked vertically
    }
}

@Composable
fun RowExample() {
    Row {
        Text("Left")
        Text("Center")
        Text("Right")
        // Arranged horizontally
    }
}
```

---

### **Q15: When should you use LazyColumn?**
**Level**: Intermediate

**Answer**:
Use `LazyColumn` for long lists (like RecyclerView in XML Android):

```kotlin
@Composable
fun UserList() {
    val users = (1..1000).map { "User $it" }
    
    // ❌ Bad - loads all 1000 items at once
    Column {
        for (user in users) {
            Text(user)  // Memory heavy!
        }
    }
    
    // ✅ Good - only renders visible items
    LazyColumn {
        items(users.size) { index ->
            Text(users[index])  // Memory efficient!
        }
    }
}
```

**Advantages**:
- Only renders visible items
- Memory efficient
- Smooth scrolling
- Reuses composables

---

## 🏛️ Architecture & Design Q&A

### **Q16: Explain MVVM Architecture**
**Level**: Intermediate

**Answer**:
MVVM separates code into three layers:

```
View (UI)
   ↕
ViewModel (Logic)
   ↕
Model (Data)
```

```kotlin
// Model - Data
data class User(val id: Int, val name: String, val email: String)

// ViewModel - Business Logic
class UserViewModel : ViewModel() {
    private val _users = MutableLiveData<List<User>>()
    val users: LiveData<List<User>> = _users
    
    fun loadUsers() {
        viewModelScope.launch {
            val users = apiService.getUsers()
            _users.value = users
        }
    }
}

// View - UI
@Composable
fun UserListScreen(viewModel: UserViewModel) {
    val users by viewModel.users.observeAsState(emptyList())
    
    LazyColumn {
        items(users.size) { index ->
            UserItem(users[index])
        }
    }
}
```

**Benefits**:
- Testable
- Reusable
- Organized
- Survives configuration changes

---

### **Q17: What is Dependency Injection and why use Hilt?**
**Level**: Advanced

**Answer**:
DI means providing dependencies from outside instead of inside:

```kotlin
// ❌ Bad - Hard to test, tightly coupled
class UserRepository {
    val apiService = RetrofitClient.create()  // Created inside
    
    fun getUser(id: Int) = apiService.getUser(id)
}

// ✅ Good - Depends on provided service
class UserRepository(val apiService: ApiService) {
    fun getUser(id: Int) = apiService.getUser(id)
}
```

**With Hilt (Modern Approach)**:
```kotlin
@Singleton  // Create only once
@Provides   // Provide this dependency
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

// In ViewModel - Hilt injects automatically
@HiltViewModel
class UserViewModel @Inject constructor(
    val userRepository: UserRepository
) : ViewModel() {
    fun loadUser(id: Int) {
        val user = userRepository.getUser(id)
    }
}

// In Activity - Hilt injects ViewModel
@AndroidEntryPoint
class MainActivity : AppCompatActivity() {
    private val viewModel: UserViewModel by viewModels()
}
```

**Benefits**:
- Easy testing (pass mock objects)
- Loose coupling
- Centralized config
- Less boilerplate

---

### **Q18: Compare SharedPreferences vs Room Database**
**Level**: Intermediate

**Answer**:

| Feature | SharedPreferences | Room |
|---------|------------------|------|
| **Data Type** | Key-value pairs | Structured tables |
| **Data Size** | Small (< 5MB) | Large databases |
| **Queries** | Not supported | Complex SQL queries |
| **Performance** | Fast | Very fast |
| **Use Case** | Settings, tokens | User data, posts |

```kotlin
// SharedPreferences - Simple key-value
val prefs = getSharedPreferences("settings", Context.MODE_PRIVATE)
prefs.edit().putString("userName", "Alice").apply()

val userName = prefs.getString("userName", "Unknown")

// Room Database - Structured data
@Entity
data class User(
    @PrimaryKey val id: Int,
    val name: String,
    val email: String
)

@Dao
interface UserDao {
    @Query("SELECT * FROM user WHERE id = :userId")
    suspend fun getUser(userId: Int): User
    
    @Insert
    suspend fun insertUser(user: User)
}

// Usage
val userDao = database.userDao()
val user = userDao.getUser(1)
```

---

### **Q19: Explain Navigation Component**
**Level**: Intermediate

**Answer**:
Navigation Component manages app navigation declaratively:

```kotlin
// In XML (nav_graph.xml)
<?xml version="1.0" encoding="utf-8"?>
<navigation xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/nav_graph"
    app:startDestination="@id/homeFragment">
    
    <fragment android:id="@+id/homeFragment"
        android:name="com.example.HomeFragment" />
    
    <fragment android:id="@+id/profileFragment"
        android:name="com.example.ProfileFragment" />
    
    <action
        android:id="@+id/action_home_to_profile"
        app:destination="@id/profileFragment" />
</navigation>

// In Fragment code
findNavController().navigate(R.id.action_home_to_profile)

// With Compose
@Composable
fun Navigation() {
    val navController = rememberNavController()
    
    NavHost(navController, startDestination = "home") {
        composable("home") { HomeScreen(navController) }
        composable("profile") { ProfileScreen(navController) }
    }
}
```

---

### **Q20: What are Broadcast Receivers?**
**Level**: Intermediate

**Answer**:
Broadcast Receivers listen for system or app events:

```kotlin
// Create receiver
class NetworkChangeReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context?, intent: Intent?) {
        val networkInfo = ConnectivityManager.getNetworkInfo(0)
        if (networkInfo?.isConnected == true) {
            println("Connected to network")
        } else {
            println("Disconnected from network")
        }
    }
}

// Register in AndroidManifest.xml
<receiver android:name=".NetworkChangeReceiver">
    <intent-filter>
        <action android:name="android.net.conn.CONNECTIVITY_CHANGE" />
    </intent-filter>
</receiver>

// Or register dynamically
val receiver = NetworkChangeReceiver()
val filter = IntentFilter(ConnectivityManager.CONNECTIVITY_ACTION)
registerReceiver(receiver, filter)
```

**Common Used For**:
- Network state changes
- Battery low
- Device boot
- Custom app events

---

## 🔧 Common Issues & Solutions

### **Q21: Why is my app crashing with NullPointerException?**
**Level**: Beginner

**Answer**:
Accessing null value. Use null safety:

```kotlin
// ❌ Crash
val name = getUserName()  // Can be null
println(name.length)      // Crash if null!

// ✅ Safe
val name = getUserName()
println(name?.length)     // null if name is null

// ✅ With default
println(name?.length ?: 0)  // 0 if name is null
```

---

### **Q22: Memory leak with listeners**
**Level**: Intermediate

**Answer**:
Always unregister listeners:

```kotlin
// ❌ Leak
override fun onResume() {
    super.onResume()
    sensorManager.registerListener(listener, sensor, SENSOR_DELAY_NORMAL)
}

// ✅ Fixed
override fun onPause() {
    super.onPause()
    sensorManager.unregisterListener(listener)  // Unregister!
}
```

---

### **Q23: UI doesn't update after data change**
**Level**: Intermediate

**Answer**:
Make data observable:

```kotlin
// ❌ Doesn't trigger recompose
var count = 0
count++  // UI doesn't update

// ✅ Triggers recompose
var (count, setCount) = remember { mutableStateOf(0) }
setCount(count + 1)  // UI updates automatically
```

---

### **Q24: App hangs when loading data**
**Level**: Intermediate

**Answer**:
Use coroutines instead of blocking calls:

```kotlin
// ❌ Hangs UI
fun loadData() {
    val data = apiClient.getUser()  // Blocks!
    updateUI(data)
}

// ✅ Doesn't hang
fun loadData() {
    lifecycleScope.launch {
        val data = withContext(Dispatchers.IO) {
            apiClient.getUser()  // Background thread
        }
        updateUI(data)  // Back to main thread
    }
}
```

---

### **Q25: State lost when Activity recreates**
**Level**: Intermediate

**Answer**:
Save and restore state:

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    
    if (savedInstanceState != null) {
        counter = savedInstanceState.getInt("counter", 0)
    }
}

override fun onSaveInstanceState(outState: Bundle) {
    super.onSaveInstanceState(outState)
    outState.putInt("counter", counter)
}
```

---

## 📊 Summary

✅ **You should now understand**:
- Kotlin fundamentals and advanced concepts
- Android Activity lifecycle
- XML layouts and Jetpack Compose
- State management
- Architecture patterns (MVVM)
- Networking and databases
- Common issues and solutions

✅ **Next Steps**:
1. Build real projects (Todo, Weather, Chat apps)
2. Study open-source Android apps
3. Read Android documentation
4. Practice on LeetCode/HackerRank
5. Build your own app and publish to Play Store

---

**Advanced: [Module 26 - Interview Questions](26_INTERVIEW_QUESTIONS.md)**

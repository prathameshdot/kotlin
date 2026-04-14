# 🔥 2000+ Questions - QUICK REFERENCE & SAMPLE ANSWERS

## HOW TO USE THIS FILE

This file contains **sample questions with complete answers** organized by topic. Use this to:
1. Understand the answer format
2. See code examples for each concept
3. Study before interviews
4. Review weak areas

---

## KOTLIN - QUICK REFERENCE

### Q: What's the difference between val and var?

**Answer:**
```
val → immutable (cannot reassign after initialization)
var → mutable (can reassign multiple times)

Example:
val name = "John"   // CANNOT change
name = "Jane"       // ❌ COMPILE ERROR

var age = 30        // CAN change
age = 31            // ✅ OK
```

### Q: Explain nullable types and null safety.

**Answer:**
```kotlin
// Non-nullable (safe by default)
val name: String = "John"  // must have value
val x: String = null       // ❌ ERROR

// Nullable (explicit)
val surname: String? = null  // OK
val length = surname?.length // returns null if surname is null

// Elvis operator
val display = surname ?: "Unknown"  // default if null

// Not-null assertion (dangerous!)
val len = surname!!.length  // ❌ throws exception if null
```

### Q: What are scope functions and when to use each?

**Answer:**
```kotlin
// let: returns result, good for null checking
"Hello".let { it.length }  // 5

// apply: returns this, good for object initialization
Person().apply { 
    name = "John"
    age = 30 
}  // returns modified Person

// run: returns result, similar to let but with this
"Hello".run {
    length + 5  // 10
}

// with: no return, good for multiple operations
with(person) {
    println(name)
    println(age)
}

// also: returns this, good for debugging
"Hello".also {
    println("Length: ${it.length}")
}  // returns "Hello"
```

### Q: What's the difference between Sequence and List?

**Answer:**
```kotlin
// List: eager evaluation (all operations applied immediately)
val list = (1..1000000).toList()
    .map { it * 2 }    // ↔️ evaluates 1M items
    .filter { it > 100 }  // ↔️ evaluates 1M items
    .toList()

// Sequence: lazy evaluation (operations deferred until terminal)
val seq = (1..1000000).asSequence()
    .map { it * 2 }        // ❌ not evaluated
    .filter { it > 100 }   // ❌ not evaluated
    .toList()              // ✅ NOW evaluated (only needed items)
```

### Q: What are data classes and what methods do they generate?

**Answer:**
```kotlin
data class Person(val name: String, val age: Int)

// Automatically generates:
// 1. equals() - structural equality
// 2. hashCode() - for use in collections
// 3. toString() - "Person(name=John, age=30)"
// 4. copy() - create modified copy
// 5. componentN() - destructuring

val p1 = Person("John", 30)
val p2 = Person("John", 30)
println(p1 == p2)  // true

val p3 = p1.copy(age = 31)
val (name, age) = p1
```

### Q: Explain sealed classes and their use case.

**Answer:**
```kotlin
// Sealed class: restrict inheritance to predefined subclasses
sealed class Result {
    data class Success(val data: String) : Result()
    data class Error(val exception: Exception) : Result()
    object Loading : Result()
}

// When expression is exhaustive (must handle all cases)
fun handleResult(result: Result) = when (result) {
    is Result.Success -> println(result.data)
    is Result.Error -> println(result.exception.message)
    is Result.Loading -> println("Loading...")
    // No else needed - compiler knows all cases
}
```

### Q: What are generics and type bounds?

**Answer:**
```kotlin
// Basic generics
fun <T> printList(list: List<T>) {
    for (item in list) println(item)
}

// Type bounds (constraint type parameter)
fun <T : Number> doubleValue(value: T): Double {
    return value.toDouble() * 2
}
doubleValue(5)      // ✅ Int extends Number
doubleValue(3.14)   // ✅ Double extends Number
doubleValue("Hi")   // ❌ ERROR

// Multiple bounds
fun <T> copy(from: Array<T>, to: Array<T>) 
    where T : Cloneable, T : Comparable<T> {
    // T must extend both Cloneable AND Comparable
}
```

### Q: What are higher-order functions and lambdas?

**Answer:**
```kotlin
// Lambda: anonymous function
val add = { x: Int, y: Int -> x + y }
println(add(2, 3))  // 5

// Higher-order: takes function as parameter
fun calculate(a: Int, b: Int, op: (Int, Int) -> Int): Int {
    return op(a, b)
}
calculate(5, 3, { x, y -> x + y })  // 8
calculate(5, 3) { x, y -> x - y }   // 2 (trailing lambda)

// Returns function
fun getOperation(type: String): (Int, Int) -> Int {
    return when (type) {
        "add" -> { x, y -> x + y }
        "sub" -> { x, y -> x - y }
        else -> { _, _ -> 0 }
    }
}
```

### Q: What are coroutines and how do they differ from threads?

**Answer:**
```kotlin
// Coroutines: lightweight, suspendable, async
launch {  // fire and forget
    val data = fetchData()  // suspends, doesn't block thread
    updateUI(data)
}

async {  // returns result
    val result = calculateBig()  // suspends
    result
}

// Threads: heavyweight, block entire thread
Thread {
    val data = fetchDataBlocking()  // blocks entire thread
    updateUI(data)
}.start()

// Coroutines use less memory and context switching
// More efficient for async operations
```

---

## ANDROID - QUICK REFERENCE

### Q: What is the Activity lifecycle?

**Answer:**
```
onCreate()    → Called when Activity created
   ↓
onStart()     → Activity becomes visible
   ↓
onResume()    → Activity interactive (HAS FOCUS)
   ↓
onPause()     → Another activity comes to foreground
   ↓
onStop()      → Activity is no longer visible
   ↓
onDestroy()   → Activity is destroyed

Optional: onRestart() → Called before onStart if restarting
```

**Code Example:**
```kotlin
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        Log.d("TAG", "onCreate")
    }
    
    override fun onStart() {
        super.onStart()
        Log.d("TAG", "onStart - visible")
    }
    
    override fun onResume() {
        super.onResume()
        Log.d("TAG", "onResume - interactive")
        startCamera()
    }
    
    override fun onPause() {
        super.onPause()
        Log.d("TAG", "onPause - losing focus")
        stopCamera()
    }
}
```

### Q: How to save and restore Activity state?

**Answer:**
```kotlin
// Saving
override fun onSaveInstanceState(outState: Bundle) {
    super.onSaveInstanceState(outState)
    outState.putString("name", editText.text.toString())
    outState.putInt("score", score)
}

// Restoring
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    setContentView(R.layout.activity_main)
    
    if (savedInstanceState != null) {
        val name = savedInstanceState.getString("name", "")
        val score = savedInstanceState.getInt("score", 0)
        // Restore UI
    }
}
```

### Q: What's the difference between explicit and implicit Intent?

**Answer:**
```kotlin
// Explicit Intent (specify exact activity)
val intent = Intent(this, SecondActivity::class.java)
intent.putExtra("user_id", 123)
startActivity(intent)

// Implicit Intent (let system choose app)
val intent = Intent(Intent.ACTION_VIEW)
intent.data = Uri.parse("https://www.google.com")
startActivity(intent)

// Implicit Intent (phone call)
val intent = Intent(Intent.ACTION_CALL)
intent.data = Uri.parse("tel:+1234567890")
if (ContextCompat.checkSelfPermission(this, 
    Manifest.permission.CALL_PHONE) == PERMISSION_GRANTED) {
    startActivity(intent)
}
```

### Q: What is Fragment lifecycle?

**Answer:**
```
onAttach()        → Fragment attached to Activity
   ↓
onCreate()        → Activity/Fragment created
   ↓
onCreateView()    → Create UI components
   ↓
onViewCreated()   → Safe to setup views after inflate
   ↓
onStart()         → Fragment visible
   ↓
onResume()        → Fragment interactive (HAS FOCUS)
   ↓
onPause()         → Fragment losing focus
   ↓
onStop()          → Fragment no longer visible
   ↓
onDestroyView()   → Destroy view hierarchy
   ↓
onDestroy()       → Fragment destroyed
   ↓
onDetach()        → Fragment detached from Activity
```

---

## JETPACK COMPOSE - QUICK REFERENCE

### Q: What is @Composable annotation?

**Answer:**
```kotlin
// @Composable marks function as composable
// Can only be called from other @Composables
@Composable
fun MyScreen() {
    Text("Hello World")
    Button(onClick = { }) {
        Text("Click Me")
    }
}

// Cannot call from regular functions
fun regularFunction() {
    MyScreen()  // ❌ ERROR: can only call from @Composable
}

// Must call from @Composable
@Composable
fun ParentScreen() {
    MyScreen()  // ✅ OK
}
```

### Q: What is State and remember?

**Answer:**
```kotlin
@Composable
fun Counter() {
    // remember: state survives recomposition
    var count by remember { mutableStateOf(0) }
    
    Column {
        Text("Count: $count")
        Button(onClick = { count++ }) {
            Text("Increment")
        }
    }
}

// vs without remember (doesn't survive recomposition)
@Composable
fun BadCounter() {
    var count = 0  // ❌ reset on every recomposition
    
    Button(onClick = { count++ }) {
        Text("Count: $count")  // always 0
    }
}
```

### Q: What are Modifiers?

**Answer:**
```kotlin
@Composable
fun ModifierExample() {
    Text(
        text = "Hello",
        modifier = Modifier
            .fillMaxWidth()              // 100% width
            .padding(16.dp)              // padding all sides
            .background(Color.Blue)      // background color
            .clip(RoundedCornerShape(8.dp))  // rounded corners
            .clickable { /* handle click */ }  // click handler
    )
}

// Modifier order matters (applied left to right)
Modifier
    .size(100.dp)
    .padding(10.dp)  // padding INSIDE size
    .border(2.dp, Color.Red)
```

### Q: How to do navigation in Compose?

**Answer:**
```kotlin
@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    
    NavHost(
        navController = navController,
        startDestination = "home"
    ) {
        composable("home") {
            HomeScreen(navController)
        }
        composable("profile/{userId}") { backStackEntry ->
            val userId = backStackEntry.arguments?.getString("userId")
            ProfileScreen(userId)
        }
    }
}

@Composable
fun HomeScreen(navController: NavController) {
    Button(onClick = {
        navController.navigate("profile/123")
    }) {
        Text("Go to Profile")
    }
}
```

### Q: What is LazyColumn?

**Answer:**
```kotlin
@Composable
fun UserList(users: List<User>) {
    LazyColumn {
        items(users) { user ->
            UserCard(user = user)
        }
    }
}

// vs Column (bad for large lists)
@Composable
fun BadUserList(users: List<User>) {
    Column {  // ❌ renders ALL items at once
        users.forEach { user ->
            UserCard(user = user)
        }
    }
}

// LazyColumn only renders visible items (better performance)
```

---

## DATABASE - QUICK REFERENCE

### Q: How to create Room entity?

**Answer:**
```kotlin
@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    
    @ColumnInfo(name = "user_name")
    val name: String,
    
    val email: String,
    
    @Ignore
    val tempData: String = ""  // not saved
)
```

### Q: How to create DAO?

**Answer:**
```kotlin
@Dao
interface UserDao {
    @Query("SELECT * FROM users")
    suspend fun getAllUsers(): List<UserEntity>
    
    @Query("SELECT * FROM users WHERE id = :id")
    fun observeUser(id: Int): Flow<UserEntity>
    
    @Insert
    suspend fun insertUser(user: UserEntity)
    
    @Update
    suspend fun updateUser(user: UserEntity)
    
    @Delete
    suspend fun deleteUser(user: UserEntity)
}
```

---

## NETWORKING - QUICK REFERENCE

### Q: How to create Retrofit interface?

**Answer:**
```kotlin
interface ApiService {
    @GET("users")
    suspend fun getUsers(): Response<List<User>>
    
    @GET("users/{id}")
    suspend fun getUserById(@Path("id") id: Int): User
    
    @GET("users")
    suspend fun searchUsers(@Query("query") query: String): List<User>
    
    @POST("users")
    suspend fun createUser(@Body user: User): User
    
    @PUT("users/{id}")
    suspend fun updateUser(@Path("id") id: Int, @Body user: User): User
    
    @DELETE("users/{id}")
    suspend fun deleteUser(@Path("id") id: Int): Response<Unit>
}
```

### Q: How to setup Retrofit?

**Answer:**
```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    
    @Singleton
    @Provides
    fun provideRetrofit(): Retrofit {
        return Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .addConverterFactory(GsonConverterFactory.create())
            .client(provideOkHttpClient())
            .build()
    }
    
    @Singleton
    @Provides
    fun provideOkHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .addInterceptor(HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            })
            .connectTimeout(30, TimeUnit.SECONDS)
            .build()
    }
    
    @Singleton
    @Provides
    fun provideApiService(retrofit: Retrofit): ApiService {
        return retrofit.create(ApiService::class.java)
    }
}
```

---

## MVVM/ARCHITECTURE - QUICK REFERENCE

### Q: What is MVVM pattern?

**Answer:**
```
Model ←→ ViewModel ←→ View
 ↓         ↓           ↓
Database  LiveData    UI
API       StateFlow   Activity/
          Compose

Model: Data layer (database, API, entity objects)
ViewModel: State management, business logic
View: UI layer (Activity, Fragment, Compose screen)
```

### Q: How to create ViewModel?

**Answer:**
```kotlin
class UserViewModel : ViewModel() {
    private val _users = MutableLiveData<Result<List<User>>>()
    val users: LiveData<Result<List<User>>> = _users
    
    fun loadUsers() = viewModelScope.launch {
        _users.value = Result.Loading
        try {
            val result = userRepository.getUsers()
            _users.value = Result.Success(result)
        } catch (e: Exception) {
            _users.value = Result.Error(e)
        }
    }
}

sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val exception: Exception) : Result<Nothing>()
    object Loading : Result<Nothing>()
}
```

### Q: What is Hilt DI?

**Answer:**
```kotlin
// 1. Add @HiltAndroidApp to Application
@HiltAndroidApp
class MyApplication : Application()

// 2. Create Hilt module
@Module
@InstallIn(SingletonComponent::class)
object AppModule {
    @Singleton
    @Provides
    fun provideDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "app-database"
        ).build()
    }
}

// 3. Use @Inject in Activity/Fragment
@AndroidEntryPoint
class MainActivity : AppCompatActivity() {
    @Inject
    lateinit var repository: UserRepository
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // repository is injected by Hilt
    }
}
```

---

## PERFORMANCE - QUICK REFERENCE

### Q: What causes ANR (Application Not Responding)?

**Answer:**
```
ANR = Main thread blocked for >5 seconds

❌ BAD:
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    
    val data = heavyComputation()  // ⏰ blocks main thread
    val users = database.getAllUsers()  // ⏰ blocks main thread
}

✅ GOOD:
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    
    viewModel.loadData()  // offloaded to background
}

// In ViewModel
fun loadData() = viewModelScope.launch(Dispatchers.IO) {
    val data = heavyComputation()
    val users = database.getAllUsers()
    
    withContext(Dispatchers.Main) {
        updateUI(data, users)
    }
}
```

---

## SECURITY - QUICK REFERENCE

### Q: How to securely store API key?

**Answer:**
```kotlin
// ❌ BAD: in BuildConfig (visible in apk)
class ApiConfig {
    companion object {
        const val API_KEY = "abc123xyz"
    }
}

// ✅ GOOD: in local.properties (not in git)
// local.properties (add to .gitignore)
API_KEY=abc123xyz

// build.gradle
buildTypes {
    debug {
        buildConfigField("String", "API_KEY", 
            "\"${getLocalProperty("API_KEY")}\"")
    }
}

// ✅ BEST: encrypted in server response
// Never hardcode secrets in code
// Use OAuth/JWT tokens from server instead
```

---

## KEY TAKEAWAYS

✅ **Kotlin**: Focus on null safety, generics, coroutines
✅ **Android**: Understand lifecycle deeply
✅ **Compose**: Think declaratively about UI
✅ **MVVM**: Separate concerns (Model, View, ViewModel)
✅ **Performance**: Main thread awareness, optimization techniques
✅ **Security**: Never hardcode secrets, use encryption

---

## 🚀 NEXT STEPS

1. Review each section above 
2. Try to answer without reading answer
3. Implement code examples in Android Studio
4. Check full details in main question files
5. Pass your interview! 🎉

Good luck! You've got this! 💪

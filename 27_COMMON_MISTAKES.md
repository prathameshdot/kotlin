# Module 27: Common Mistakes & Solutions

## ❌ Mistake 1: Memory Leaks

```kotlin
// ❌ WRONG: Listener not removed - memory leak!
class MyActivity : AppCompatActivity() {
    private val listener = object : EventListener {
        override fun onEvent() { println("Event") }
    }
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        EventBus.register(listener)  // Registered
        // NEVER unregistered - Activity can't be garbage collected!
    }
}

// ✅ CORRECT: Remove listener
class MyActivity : AppCompatActivity() {
    private val listener = object : EventListener {
        override fun onEvent() { println("Event") }
    }
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        EventBus.register(listener)
    }
    
    override fun onDestroy() {
        EventBus.unregister(listener)  // Clean up!
        super.onDestroy()
    }
}
```

## ❌ Mistake 2: NullPointerException

```kotlin
// ❌ WRONG: No null checks
val email = intent.getStringExtra("email")
println(email.length)  // Crash if email is null!

// ✅ CORRECT: Check for null
val email = intent.getStringExtra("email") ?: "unknown@email.com"
println(email.length)

// ✅ OR: Use safe call
val length = intent.getStringExtra("email")?.length ?: 0
```

## ❌ Mistake 3: UI Thread Blocking

```kotlin
// ❌ WRONG: Blocks main thread - freezes UI
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    
    val data = expensiveNetworkCall()  // 5 seconds - UI frozen!
    displayData(data)
}

// ✅ CORRECT: Use coroutine
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    
    lifecycleScope.launch {
        val data = withContext(Dispatchers.IO) {
            expensiveNetworkCall()
        }
        displayData(data)
    }
}
```

## ❌ Mistake 4: Partial Update Error

```kotlin
// ❌ WRONG: Partial update - BeforeSave accesses missing fields
data class Enquiry(val products: List<Product>, val notes: List<Note>)

val partialEnquiry = Enquiry(
    products = listOf(newProduct),  // Only new products!
    notes = listOf()
)
api.updateEnquiry(partialEnquiry)  // 500 Error!

// ✅ CORRECT: Send complete entity
val completeEnquiry = api.getEnquiry(enquiryId)
completeEnquiry.products = completeEnquiry.products + newProduct
completeEnquiry.notes = completeEnquiry.notes + newNote
api.updateEnquiry(completeEnquiry)
```

## ❌ Mistake 5: Sending Computed Fields

```kotlin
// ❌ WRONG: API returns computed field - don't send it back!
val response = api.getQuotation(1)
// response.lineTotal = 500 (computed from quantity * price)

// Sending it back causes 500 error
val updated = response.copy(lineTotal = 600)
api.updateQuotation(updated)  // 500 Error!

// ✅ CORRECT: Remove computed fields before sending
val toSend = response.copy(
    lineTotal = null,  // Remove computed
    grandTotal = null  // Remove computed
)
api.updateQuotation(toSend)
```

## ❌ Mistake 6: State Not Updated in Recomposition

```kotlin
// ❌ WRONG: Creating state outside remember
@Composable
fun Counter() {
    var count = 0  // Re-created every recomposition!
    
    Button(onClick = { count++ }) {
        Text("Count: $count")  // Always 0!
    }
}

// ✅ CORRECT: Use remember
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }
    
    Button(onClick = { count++ }) {
        Text("Count: $count")  // Persists across recompositions
    }
}
```

## ❌ Mistake 7: Fragment Orientation Change

```kotlin
// ❌ WRONG: State lost on rotation
class MyFragment : Fragment() {
    private var userData: User? = null  // Lost on rotation!
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        userData = loadUserData()
    }
}

// ✅ CORRECT: Use ViewModel
class MyFragment : Fragment() {
    private val viewModel: UserViewModel by viewModels()
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        // viewModel survives rotation
    }
}
```

## ❌ Mistake 8: Missing Required API Call

```kotlin
// ❌ WRONG: No session priming
try {
    val result = api.createEnquiry(enquiry)  // 400 Error!
} catch (e: Exception) {
    // What went wrong?
}

// ✅ CORRECT: Prime the session first
try {
    api.getContactList()  // Initialize CSRF token
    val result = api.createEnquiry(enquiry)  // Now works!
} catch (e: Exception) {
    // Handle error
}
```

## ❌ Mistake 9: Wrong API Endpoint

```kotlin
// ❌ WRONG: Using wrong module path
api.getQuotationProducts()  // 404!

// ✅ CORRECT: Reports module path
// Endpoint: /Services/Reports/QuotationProducts/, NOT /Services/Quotation/
api.getQuotationProducts()  // Works when mapped to Reports module
```

## ❌ Mistake 10: Hardcoded Values

```kotlin
// ❌ WRONG: Hardcoded API key
const val API_KEY = "sk_live_abc123xyz"
retrofit.addHeader("Authorization", "Bearer $API_KEY")

// Also wrong: Hardcoded IDs
val companyId = 1  // Might be different in production!

// ✅ CORRECT: From environment/config
val apiKey = BuildConfig.API_KEY  // From gradle
val companyId = getCurrentUserCompanyId()  // From context
```

## 📋 Quick Reference

| Mistake | Cause | Solution |
|---------|-------|----------|
| Memory Leak | Listeners not removed | Use onDestroy() |
| Null Error | No null checks | Use `?.` or `?:` |
| UI Freeze | Blocking main thread | Use Coroutines |
| 500 Error | Partial entity update | Send complete entity |
| 500 Error | Computed fields in payload | Remove them |
| State Lost | Not using ViewModel | Use remember/ViewModel |
| Rotation Loss | State in Activity | Use ViewModel |
| API Error | No session | Add preflight call |
| 404 Error | Wrong endpoint | Check API docs |
| 400 Error | Hardcoded values | Use config/BuildConfig |

## 🎓 Summary

These are the top 10 mistakes Android developers make. Avoid them by:
- Understanding lifecycle
- Using ViewModel for state
- Always checking for null
- Using Coroutines for async
- Reading API documentation
- Testing before production


# Module 2.4: Fragments & Fragment Lifecycle - Complete Guide

## 🧩 What Are Fragments?

A **Fragment** is a reusable piece of UI that can be used in multiple Activities. Think of it as a sub-Activity or a building block for Android UIs. Fragments must always be hosted in an Activity.

### **Fragment vs Activity**

```
Activity                          Fragment
- Full screen                     - Part of screen
- Can exist independently         - Must be in an Activity
- Lifecycle: 7 states            - Lifecycle: 12 states (more complex)
- Heavier weight                  - Lighter weight
- One per screen usually          - Multiple per screen possible
```

---

## 📊 Fragment Lifecycle

Fragments have MORE lifecycle methods than Activities (12 vs 7):

### **Complete Fragment Lifecycle**
```
Fragment Lifecycle:
onCreate()              ← Fragment created
onCreateView()          ← UI created (inflate layout)
onViewCreated()         ← UI is ready (access views)
onStart()              ← Fragment becoming visible
onResume()             ← Fragment fully visible and interactive
onPause()              ← Fragment losing focus
onStop()               ← Fragment no longer visible
onDestroyView()        ← UI destroyed (clean up views)
onDestroy()            ← Fragment destroyed
onDetach()             ← Detached from Activity
```

---

## 🎯 Creating Fragments

### **Basic Fragment**
```kotlin
class HomeFragment : Fragment() {
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Initialize non-UI data
        println("HomeFragment created")
    }
    
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_home, container, false)
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        // Setup views - this is where you find and configure UI elements
        val titleText = view.findViewById<TextView>(R.id.title)
        titleText.text = "Welcome to Home"
    }
    
    override fun onStart() {
        super.onStart()
        println("HomeFragment started")
    }
    
    override fun onResume() {
        super.onResume()
        println("HomeFragment resumed (visible)")
    }
    
    override fun onPause() {
        super.onPause()
        println("HomeFragment paused")
    }
    
    override fun onStop() {
        super.onStop()
        println("HomeFragment stopped")
    }
    
    override fun onDestroyView() {
        super.onDestroyView()
        println("HomeFragment views destroyed")
    }
    
    override fun onDestroy() {
        super.onDestroy()
        println("HomeFragment destroyed")
    }
}
```

---

## 🔀 Fragment Transactions - Add/Replace Fragments

### **Add Fragment to Activity**
```kotlin
// In Activity
val fragment = HomeFragment()
supportFragmentManager.beginTransaction()
    .add(R.id.fragment_container, fragment)
    .commit()
```

### **Replace Fragment**
```kotlin
val newFragment = ProfileFragment()
supportFragmentManager.beginTransaction()
    .replace(R.id.fragment_container, newFragment)
    .addToBackStack(null)  // Allow pressing back to return
    .commit()
```

### **Transaction with Animation**
```kotlin
supportFragmentManager.beginTransaction()
    .setCustomAnimations(
        R.anim.slide_in,    // enter
        R.anim.slide_out    // exit
    )
    .replace(R.id.fragment_container, newFragment)
    .addToBackStack(null)
    .commit()
```

---

## 📤 Passing Data to Fragments

### **Via Arguments Bundle**
```kotlin
// Create fragment with arguments
fun createUserFragment(userId: Int, userName: String): UserFragment {
    val fragment = UserFragment()
    val args = Bundle().apply {
        putInt("user_id", userId)
        putString("user_name", userName)
    }
    fragment.arguments = args
    return fragment
}

// In Fragment, retrieve arguments
class UserFragment : Fragment() {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        val userId = arguments?.getInt("user_id") ?: 0
        val userName = arguments?.getString("user_name") ?: "Unknown"
        
        println("User: $userName ($userId)")
    }
}

// Use in Activity
val fragment = createUserFragment(123, "Alice")
supportFragmentManager.beginTransaction()
    .replace(R.id.fragment_container, fragment)
    .addToBackStack(null)
    .commit()
```

### **Shared ViewModel (Modern Way)**
```kotlin
// Shared data between Fragment and Activity
class UserViewModel : ViewModel() {
    private val _userName = MutableLiveData<String>()
    val userName: LiveData<String> = _userName
    
    fun setUserName(name: String) {
        _userName.value = name
    }
}

// In Activity
class MainActivity : AppCompatActivity() {
    private val viewModel: UserViewModel by viewModels()
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Share data
        viewModel.setUserName("Alice")
    }
}

// In Fragment
class ProfileFragment : Fragment() {
    private val viewModel: UserViewModel by viewModels()
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        // Access shared data
        viewModel.userName.observe(viewLifecycleOwner) { name ->
            println("User name: $name")
        }
    }
}
```

---

## 💬 Communication Between Fragments

### **Via Interface Callback**
```kotlin
// Interface for communication
interface OnUserSelectedListener {
    fun onUserSelected(userId: Int)
}

// Fragment 1: Emits event
class UserListFragment : Fragment(), OnUserSelectedListener {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        val userButton = view.findViewById<Button>(R.id.select_user_button)
        userButton.setOnClickListener {
            (activity as? OnUserSelectedListener)?.onUserSelected(123)
        }
    }
    
    override fun onUserSelected(userId: Int) {
        println("Selected user: $userId")
    }
}

// Fragment 2: Receives event
class UserDetailFragment : Fragment() {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        (activity as? OnUserSelectedListener)?.onUserSelected(456)
    }
}

// Activity: Implements listener
class MainActivity : AppCompatActivity(), OnUserSelectedListener {
    override fun onUserSelected(userId: Int) {
        val fragment = UserDetailFragment()
        val args = Bundle().apply { putInt("user_id", userId) }
        fragment.arguments = args
        supportFragmentManager.beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .addToBackStack(null)
            .commit()
    }
}
```

### **Via SharedViewModel (Better Way)**
```kotlin
class UserViewModel : ViewModel() {
    private val _selectedUserId = MutableLiveData<Int>()
    val selectedUserId: LiveData<Int> = _selectedUserId
    
    fun selectUser(userId: Int) {
        _selectedUserId.value = userId
    }
}

// Fragment 1: Sends event
class UserListFragment : Fragment() {
    private val viewModel: UserViewModel by viewModels()
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        val userButton = view.findViewById<Button>(R.id.select_user_button)
        userButton.setOnClickListener {
            viewModel.selectUser(123)  // Emit event
        }
    }
}

// Fragment 2: Listens to event
class UserDetailFragment : Fragment() {
    private val viewModel: UserViewModel by viewModels()
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        viewModel.selectedUserId.observe(viewLifecycleOwner) { userId ->
            println("Detail for user: $userId")
            loadUserDetails(userId)
        }
    }
    
    private fun loadUserDetails(userId: Int) {
        // Load and display user details
    }
}
```

---

## 📱 Real-World Example: Bottom Navigation with Fragments

```kotlin
// ===== ACTIVITY WITH BOTTOM NAVIGATION =====
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        val bottomNav = findViewById<BottomNavigationView>(R.id.bottom_navigation)
        
        // Set initial fragment
        if (savedInstanceState == null) {
            replaceFragment(HomeFragment())
        }
        
        // Handle navigation
        bottomNav.setOnItemSelectedListener { item ->
            when (item.itemId) {
                R.id.nav_home -> {
                    replaceFragment(HomeFragment())
                    true
                }
                R.id.nav_search -> {
                    replaceFragment(SearchFragment())
                    true
                }
                R.id.nav_profile -> {
                    replaceFragment(ProfileFragment())
                    true
                }
                else -> false
            }
        }
    }
    
    private fun replaceFragment(fragment: Fragment) {
        supportFragmentManager.beginTransaction()
            .replace(R.id.fragment_container, fragment)
            .commit()
    }
}

// ===== HOME FRAGMENT =====
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
        
        val titleText = view.findViewById<TextView>(R.id.title)
        titleText.text = "Home Screen"
    }
}

// ===== SEARCH FRAGMENT =====
class SearchFragment : Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_search, container, false)
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        val searchInput = view.findViewById<EditText>(R.id.search_input)
        searchInput.hint = "Search here..."
    }
}

// ===== PROFILE FRAGMENT =====
class ProfileFragment : Fragment() {
    private val viewModel: ProfileViewModel by viewModels()
    
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_profile, container, false)
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        val nameText = view.findViewById<TextView>(R.id.user_name)
        val editButton = view.findViewById<Button>(R.id.edit_button)
        
        // Observe user data
        viewModel.userProfile.observe(viewLifecycleOwner) { user ->
            nameText.text = user.name
        }
        
        editButton.setOnClickListener {
            // Navigate to edit fragment
            parentFragmentManager.beginTransaction()
                .replace(R.id.fragment_container, EditProfileFragment())
                .addToBackStack(null)
                .commit()
        }
    }
}
```

---

## 🔙 Back Stack Management

```kotlin
// Add fragment to back stack
supportFragmentManager.beginTransaction()
    .replace(R.id.fragment_container, newFragment)
    .addToBackStack("fragment_tag")  // Named back stack entry
    .commit()

// Check if back stack has entries
if (supportFragmentManager.backStackEntryCount > 0) {
    supportFragmentManager.popBackStack()
}

// Clear entire back stack
supportFragmentManager.popBackStack(null, FragmentManager.POP_BACK_STACK_INCLUSIVE)

// Go back programmatically
supportFragmentManager.popBackStack()
```

---

## ✅ Practice Questions

1. **What's the difference between Fragment and Activity?**
   - Fragments are lightweight, reusable UI components; Activities are full screens

2. **When should you use onCreateView vs onViewCreated?**
   - onCreateView: Inflate layout; onViewCreated: Setup UI elements

3. **How do you pass data to a Fragment?**
   - Use Bundle with arguments or SharedViewModel

4. **What's the purpose of addToBackStack?**
   - Allows returning to previous fragment when pressing back

5. **How do fragments communicate with each other?**
   - Via Activity, SharedViewModel, or interface callbacks

---

## 🎓 Summary

- **Fragment**: Reusable UI component within Activity
- **Lifecycle**: 12 methods (more complex than Activity)
- **Fragment Transactions**: Add, replace, remove fragments dynamically
- **Data Passing**: Bundle or SharedViewModel
- **Back Stack**: Fragment navigation history
- **Communication**: Via Activity, SharedViewModel, or callbacks
- **Modern Approach**: Use Jetpack Fragments library and SharedViewModel

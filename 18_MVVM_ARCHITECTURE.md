# Module 6.1: MVVM Architecture - Professional Development Pattern

## 🏗️ MVVM Pattern Overview

```
Model ← → ViewModel ← → View
(Data)    (Logic)      (UI)
```

### **Model Layer**
```kotlin
// Data classes
data class User(val id: Int, val name: String, val email: String)
data class Post(val id: Int, val title: String, val body: String)

// Repository
class UserRepository(private val api: ApiService, private val dao: UserDao) {
    suspend fun getUser(id: Int): Result<User> = try {
        val user = api.getUserById(id)
        dao.insertUser(user)
        Result.Success(user)
    } catch (e: Exception) {
        Result.Error(e)
    }
}
```

### **ViewModel Layer**
```kotlin
class UserViewModel(private val repository: UserRepository) : ViewModel() {
    private val _user = MutableLiveData<Result<User>>()
    val user: LiveData<Result<User>> = _user
    
    fun loadUser(userId: Int) {
        viewModelScope.launch {
            _user.value = Result.Loading()
            _user.value = repository.getUser(userId)
        }
    }
}
```

### **View Layer**
```kotlin
class UserActivity : AppCompatActivity() {
    private val viewModel: UserViewModel by viewModels()
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        viewModel.user.observe(this) { result ->
            when (result) {
                is Result.Success -> displayUser(result.data)
                is Result.Error -> showError(result.exception.message)
                is Result.Loading -> showLoading()
            }
        }
        
        viewModel.loadUser(1)
    }
    
    private fun displayUser(user: User) { /* ... */ }
    private fun showError(message: String?) { /* ... */ }
    private fun showLoading() { /* ... */ }
}
```

## 🎯 MVVM Benefits

- **Separation of Concerns**: Each layer has clear responsibility
- **Testability**: ViewModel can be tested without UI
- **Reusability**: ViewModel can be shared across multiple Views
- **Lifecycle Aware**: ViewModel survives configuration changes

## 🎓 Summary

MVVM is the recommended architecture pattern for professional Android apps.

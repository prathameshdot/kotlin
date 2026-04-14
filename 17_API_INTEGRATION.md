# Module 5.2: Real API Integration - Practical Examples

## 🔗 Complete API Integration Example

### **Models with Gson**
```kotlin
data class Post(
    @SerializedName("userId")
    val userId: Int,
    @SerializedName("id")
    val id: Int,
    @SerializedName("title")
    val title: String,
    @SerializedName("body")
    val body: String
)

data class User(
    @SerializedName("id")
    val id: Int,
    @SerializedName("name")
    val name: String,
    @SerializedName("email")
    val email: String
)
```

### **API Service**
```kotlin
interface JsonPlaceholderApi {
    @GET("posts")
    suspend fun getPosts(): List<Post>
    
    @GET("posts/{id}")
    suspend fun getPostById(@Path("id") id: Int): Post
    
    @POST("posts")
    suspend fun createPost(@Body post: Post): Post
    
    @GET("users")
    suspend fun getUsers(): List<User>
}
```

### **Repository**
```kotlin
class PostRepository(private val api: JsonPlaceholderApi) {
    suspend fun getPosts(): Result<List<Post>> = try {
        val posts = api.getPosts()
        Result.Success(posts)
    } catch (e: Exception) {
        Result.Error(e)
    }
    
    suspend fun getPostById(id: Int): Result<Post> = try {
        val post = api.getPostById(id)
        Result.Success(post)
    } catch (e: Exception) {
        Result.Error(e)
    }
}
```

### **Usage in ViewModel**
```kotlin
class PostViewModel(private val repository: PostRepository) : ViewModel() {
    private val _posts = MutableLiveData<Result<List<Post>>>()
    val posts: LiveData<Result<List<Post>>> = _posts
    
    fun loadPosts() {
        viewModelScope.launch {
            _posts.value = Result.Loading()
            _posts.value = repository.getPosts()
        }
    }
}
```

## 🎓 Summary

Complete pattern for API integration from models to ViewModel.

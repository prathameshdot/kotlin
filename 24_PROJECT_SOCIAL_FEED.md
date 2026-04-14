# Project 3: Social Media Feed App - Complete Implementation

## 📱 Project Overview

Build a **Social Media Feed App** with:
- User authentication
- Post feed with pagination
- Like/comment functionality
- User profiles
- Real API integration
- MVVM + Hilt architecture
- Jetpack Compose UI

## 🏗️ Architecture

```
Data Layer (Models + API)
        ↓
Repository Layer
        ↓
ViewModel Layer
        ↓
UI Layer (Compose)
```

## 📋 Models

```kotlin
@Serializable
data class User(
    val id: Int,
    val username: String,
    val email: String,
    @SerializedName("profile_image")
    val profileImage: String,
    val bio: String
)

@Serializable
data class Post(
    val id: Int,
    @SerializedName("user_id")
    val userId: Int,
    val content: String,
    @SerializedName("created_at")
    val createdAt: String,
    @SerializedName("like_count")
    var likeCount: Int = 0,
    @SerializedName("comment_count")
    var commentCount: Int = 0,
    @SerializedName("is_liked")
    var isLiked: Boolean = false
)

@Serializable
data class Comment(
    val id: Int,
    @SerializedName("user_id")
    val userId: Int,
    @SerializedName("post_id")
    val postId: Int,
    val text: String,
    val username: String,
    @SerializedName("created_at")
    val createdAt: String
)
```

## 🔌 API Service

```kotlin
interface SocialMediaApi {
    @GET("posts?page={page}")
    suspend fun getFeed(@Path("page") page: Int): List<Post>
    
    @GET("posts/{id}/comments")
    suspend fun getComments(@Path("id") postId: Int): List<Comment>
    
    @POST("posts/{id}/like")
    suspend fun likePost(@Path("id") postId: Int): Post
    
    @POST("posts/{id}/comment")
    suspend fun addComment(
        @Path("id") postId: Int,
        @Body commentRequest: CommentRequest
    ): Comment
    
    @GET("users/{id}")
    suspend fun getUser(@Path("id") userId: Int): User
}

data class CommentRequest(val text: String)
```

## 🗄️ Data Layer

```kotlin
@Dao
interface PostDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertPosts(posts: List<Post>)
    
    @Query("SELECT * FROM posts ORDER BY created_at DESC")
    fun observePosts(): Flow<List<Post>>
    
    @Update
    suspend fun updatePost(post: Post)
}

@Dao
interface UserDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUser(user: User)
    
    @Query("SELECT * FROM users WHERE id = :userId")
    suspend fun getUser(userId: Int): User?
}

@Database(entities = [Post::class, User::class, Comment::class], version = 1)
abstract class SocialMediaDatabase : RoomDatabase() {
    abstract fun postDao(): PostDao
    abstract fun userDao(): UserDao
}
```

## 📦 Repository

```kotlin
class FeedRepository(
    private val api: SocialMediaApi,
    private val postDao: PostDao,
    private val userDao: UserDao
) {
    fun observeFeed(): Flow<List<Post>> = postDao.observePosts()
    
    suspend fun loadFeed(page: Int): Result<List<Post>> = try {
        val posts = api.getFeed(page)
        postDao.insertPosts(posts)
        Result.Success(posts)
    } catch (e: Exception) {
        Result.Error(e)
    }
    
    suspend fun likePost(postId: Int): Result<Post> = try {
        val updatedPost = api.likePost(postId)
        postDao.updatePost(updatedPost)
        Result.Success(updatedPost)
    } catch (e: Exception) {
        Result.Error(e)
    }
}
```

## 📱 ViewModel

```kotlin
@HiltViewModel
class FeedViewModel @Inject constructor(
    private val repository: FeedRepository
) : ViewModel() {
    private val _feedState = MutableLiveData<FeedState>()
    val feedState: LiveData<FeedState> = _feedState
    
    val feed = repository.observeFeed().stateIn(
        viewModelScope,
        SharingStarted.Lazily,
        emptyList()
    )
    
    fun loadFeed(page: Int = 1) {
        viewModelScope.launch {
            _feedState.value = FeedState.Loading
            when (val result = repository.loadFeed(page)) {
                is Result.Success -> _feedState.value = FeedState.Success
                is Result.Error -> _feedState.value = FeedState.Error(result.exception)
                is Result.Loading -> {}
            }
        }
    }
    
    fun likePost(postId: Int) {
        viewModelScope.launch {
            repository.likePost(postId)
        }
    }
}

sealed class FeedState {
    object Loading : FeedState()
    object Success : FeedState()
    data class Error(val exception: Exception) : FeedState()
}
```

## 🎨 UI Layer (Compose)

```kotlin
@Composable
fun FeedScreen(viewModel: FeedViewModel = hiltViewModel()) {
    val feed = viewModel.feed.collectAsState(emptyList()).value
    val state = viewModel.feedState.collectAsState(FeedState.Success).value
    
    LaunchedEffect(Unit) {
        viewModel.loadFeed()
    }
    
    when (state) {
        is FeedState.Loading -> LoadingScreen()
        is FeedState.Error -> ErrorScreen(state.exception)
        is FeedState.Success -> {
            LazyColumn {
                items(feed, key = { it.id }) { post ->
                    PostCard(
                        post = post,
                        onLikeClick = { viewModel.likePost(post.id) }
                    )
                }
            }
        }
    }
}

@Composable
fun PostCard(post: Post, onLikeClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            // User info
            Row(verticalAlignment = Alignment.CenterVertically) {
                Image(
                    painter = painterResource(R.drawable.avatar),
                    contentDescription = "Avatar",
                    modifier = Modifier
                        .size(40.dp)
                        .clip(CircleShape)
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text("@${post.id}", fontWeight = FontWeight.Bold)
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            // Post content
            Text(post.content)
            
            Spacer(modifier = Modifier.height(8.dp))
            
            // Like and comment
            Row {
                Button(onClick = onLikeClick) {
                    Text("❤️ ${post.likeCount}")
                }
                Spacer(modifier = Modifier.width(8.dp))
                Button(onClick = {}) {
                    Text("💬 ${post.commentCount}")
                }
            }
        }
    }
}
```

## 📦 Dependency Injection

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object DataModule {
    @Provides
    @Singleton
    fun provideDatabase(context: Context): SocialMediaDatabase {
        return Room.databaseBuilder(
            context,
            SocialMediaDatabase::class.java,
            "social_db"
        ).build()
    }
    
    @Provides
    fun providePostDao(database: SocialMediaDatabase) = database.postDao()
    
    @Provides
    fun provideUserDao(database: SocialMediaDatabase) = database.userDao()
}

@Module
@InstallIn(SingletonComponent::class)
object RepositoryModule {
    @Provides
    @Singleton
    fun provideFeedRepository(
        api: SocialMediaApi,
        postDao: PostDao,
        userDao: UserDao
    ): FeedRepository {
        return FeedRepository(api, postDao, userDao)
    }
}
```

## 🧪 Testing

```kotlin
class FeedViewModelTest {
    private lateinit var viewModel: FeedViewModel
    private val mockRepository = mockk<FeedRepository>()
    
    @Before
    fun setup() {
        viewModel = FeedViewModel(mockRepository)
    }
    
    @Test
    fun testLoadFeed() = runTest {
        every { mockRepository.loadFeed(1) } returns Result.Success(emptyList())
        
        viewModel.loadFeed()
        
        assertEquals(FeedState.Success, viewModel.feedState.value)
    }
}
```

## 📊 Features to Add

1. Pagination
2. Real-time notifications
3. Direct messaging
4. Post creation
5. User follow/unfollow
6. Search functionality
7. Trending hashtags
8. Photo uploads
9. Video playback
10. User blocking

## 🎓 Learning Outcomes

After building this project, you'll understand:
- Complete MVVM architecture
- Hilt dependency injection
- Jetpack Compose advanced patterns
- Real API integration with pagination
- Local database management
- Authentication flows
- Production-ready code organization

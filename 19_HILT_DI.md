# Module 6.2: Dependency Injection with Hilt

## 💉 Hilt Setup

### **Dependencies**
```gradle
dependencies {
    implementation "com.google.dagger:hilt-android:2.48"
    kapt "com.google.dagger:hilt-compiler:2.48"
    implementation "androidx.hilt:hilt-lifecycle-viewmodel:1.0.0-alpha03"
}
```

### **Create Modules**
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
            .build()
    }
    
    @Singleton
    @Provides
    fun provideApiService(retrofit: Retrofit): ApiService {
        return retrofit.create(ApiService::class.java)
    }
}

@Module
@InstallIn(SingletonComponent::class)
object RepositoryModule {
    @Singleton
    @Provides
    fun provideUserRepository(api: ApiService): UserRepository {
        return UserRepository(api)
    }
}
```

### **Inject in ViewModel**
```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {
    // ViewModel code
}
```

### **Inject in Activity**
```kotlin
@AndroidEntryPoint
class UserActivity : AppCompatActivity() {
    private val viewModel: UserViewModel by viewModels()
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Activity code
    }
}
```

## 🎓 Summary

Hilt simplifies dependency injection and automatically creates object graphs.

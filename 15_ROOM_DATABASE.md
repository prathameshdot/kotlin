# Module 4.2: Room Database - Complete Guide

## 🏗️ Room Database Setup

### **Dependencies**
```gradle
dependencies {
    implementation "androidx.room:room-runtime:2.6.0"
    kapt "androidx.room:room-compiler:2.6.0"
    implementation "androidx.room:room-ktx:2.6.0"
}
```

### **Entity (Table)**
```kotlin
@Entity(tableName = "users")
data class User(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    
    @ColumnInfo(name = "user_name")
    val name: String,
    
    val email: String,
    val age: Int
)
```

### **DAO (Database Access Object)**
```kotlin
@Dao
interface UserDao {
    // Create
    @Insert
    suspend fun insertUser(user: User): Long
    
    // Read
    @Query("SELECT * FROM users")
    suspend fun getAllUsers(): List<User>
    
    @Query("SELECT * FROM users WHERE id = :userId")
    suspend fun getUserById(userId: Int): User?
    
    // Update
    @Update
    suspend fun updateUser(user: User)
    
    // Delete
    @Delete
    suspend fun deleteUser(user: User)
    
    @Query("DELETE FROM users WHERE id = :userId")
    suspend fun deleteUserById(userId: Int)
    
    // Flow for real-time updates
    @Query("SELECT * FROM users")
    fun observeAllUsers(): Flow<List<User>>
}
```

### **Database**
```kotlin
@Database(entities = [User::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
    
    companion object {
        @Volatile private var instance: AppDatabase? = null
        
        fun getInstance(context: Context): AppDatabase {
            return instance ?: synchronized(this) {
                Room.databaseBuilder(
                    context,
                    AppDatabase::class.java,
                    "app_database"
                ).build().also { instance = it }
            }
        }
    }
}
```

### **Usage**
```kotlin
// Insert
val database = AppDatabase.getInstance(context)
val user = User(name = "Alice", email = "alice@email.com", age = 25)
database.userDao().insertUser(user)

// Query
val users = database.userDao().getAllUsers()

// Observe in real-time
database.userDao().observeAllUsers().collect { users ->
    println("Users updated: ${users.size}")
}

// Update
val updatedUser = user.copy(age = 26)
database.userDao().updateUser(updatedUser)

// Delete
database.userDao().deleteUser(user)
```

## 🎓 Summary

Room provides type-safe database access with less boilerplate than SQLite.

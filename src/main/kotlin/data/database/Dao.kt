// app/src/main/kotlin/com/example/androidmaster/data/database/Dao.kt
package com.example.androidmaster.data.database

import androidx.room.*
import kotlinx.coroutines.flow.Flow

// === USER DAO ===
@Dao
interface UserDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUser(user: UserEntity)
    
    @Query("SELECT * FROM users WHERE id = :userId")
    suspend fun getUserById(userId: Int): UserEntity?
    
    @Query("SELECT * FROM users")
    fun observeAllUsers(): Flow<List<UserEntity>>
    
    @Update
    suspend fun updateUser(user: UserEntity)
    
    @Delete
    suspend fun deleteUser(user: UserEntity)
}

// === POST DAO ===
@Dao
interface PostDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertPost(post: PostEntity)
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertPosts(posts: List<PostEntity>)
    
    @Query("SELECT * FROM posts ORDER BY created_at DESC")
    fun observeAllPosts(): Flow<List<PostEntity>>
    
    @Query("SELECT * FROM posts WHERE id = :postId")
    suspend fun getPostById(postId: Int): PostEntity?
    
    @Query("SELECT * FROM posts WHERE user_id = :userId")
    fun observePostsByUser(userId: Int): Flow<List<PostEntity>>
    
    @Update
    suspend fun updatePost(post: PostEntity)
    
    @Delete
    suspend fun deletePost(post: PostEntity)
}

// === TODO DAO ===
@Dao
interface TodoDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertTodo(todo: TodoEntity): Long
    
    @Query("SELECT * FROM todos WHERE id = :todoId")
    suspend fun getTodoById(todoId: Int): TodoEntity?
    
    @Query("SELECT * FROM todos ORDER BY due_date ASC, priority DESC")
    fun observeAllTodos(): Flow<List<TodoEntity>>
    
    @Query("SELECT * FROM todos WHERE isCompleted = 0 ORDER BY due_date ASC")
    fun observeActiveTodos(): Flow<List<TodoEntity>>
    
    @Query("SELECT * FROM todos WHERE priority = :priority ORDER BY created_at DESC")
    fun observeTodosByPriority(priority: Int): Flow<List<TodoEntity>>
    
    @Update
    suspend fun updateTodo(todo: TodoEntity)
    
    @Delete
    suspend fun deleteTodo(todo: TodoEntity)
    
    @Query("DELETE FROM todos WHERE id = :todoId")
    suspend fun deleteTodoById(todoId: Int)
}

// === CONTACT DAO ===
@Dao
interface ContactDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertContact(contact: ContactEntity)
    
    @Query("SELECT * FROM contacts ORDER BY name ASC")
    fun observeAllContacts(): Flow<List<ContactEntity>>
    
    @Query("SELECT * FROM contacts WHERE name LIKE '%' || :query || '%'")
    fun searchContacts(query: String): Flow<List<ContactEntity>>
    
    @Update
    suspend fun updateContact(contact: ContactEntity)
    
    @Delete
    suspend fun deleteContact(contact: ContactEntity)
}

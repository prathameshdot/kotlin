// app/src/main/kotlin/com/example/androidmaster/data/repository/UserRepository.kt
package com.example.androidmaster.data.repository

import com.example.androidmaster.data.database.UserDao
import com.example.androidmaster.data.database.UserEntity
import com.example.androidmaster.data.remote.ApiService
import com.example.androidmaster.data.remote.User
import javax.inject.Inject

class UserRepository @Inject constructor(
    private val apiService: ApiService,
    private val userDao: UserDao
) {
    suspend fun getUsers(): List<User> {
        return try {
            val users = apiService.getUsers()
            // Save to local database
            users.forEach { user ->
                userDao.insertUser(UserEntity(
                    id = user.id,
                    name = user.name,
                    email = user.email,
                    age = user.age,
                    profileImage = user.profileImage
                ))
            }
            users
        } catch (e: Exception) {
            throw e
        }
    }
    
    suspend fun getUserById(userId: Int): User {
        return apiService.getUserById(userId)
    }
    
    suspend fun createUser(user: User): User {
        return apiService.createUser(user)
    }
    
    suspend fun updateUser(userId: Int, user: User): User {
        return apiService.updateUser(userId, user)
    }
    
    suspend fun deleteUser(userId: Int) {
        apiService.deleteUser(userId)
    }
    
    fun observeLocalUsers() = userDao.observeAllUsers()
}

// === POST REPOSITORY ===
class PostRepository @Inject constructor(
    private val apiService: ApiService,
    private val postDao: com.example.androidmaster.data.database.PostDao
) {
    suspend fun getPosts(page: Int = 1): List<com.example.androidmaster.data.remote.Post> {
        return try {
            val response = apiService.getPostsPaginated(page, 10)
            response.items
        } catch (e: Exception) {
            throw e
        }
    }
    
    suspend fun getPostById(postId: Int): com.example.androidmaster.data.remote.Post {
        return apiService.getPostById(postId)
    }
    
    suspend fun searchPosts(query: String): List<com.example.androidmaster.data.remote.Post> {
        return apiService.searchPosts(query)
    }
    
    suspend fun createPost(post: com.example.androidmaster.data.remote.Post): com.example.androidmaster.data.remote.Post {
        return apiService.createPost(post)
    }
    
    suspend fun likePost(postId: Int): com.example.androidmaster.data.remote.Post {
        return apiService.likePost(postId)
    }
    
    fun observeLocalPosts() = postDao.observeAllPosts()
}

// === TODO REPOSITORY ===
class TodoRepository @Inject constructor(
    private val todoDao: com.example.androidmaster.data.database.TodoDao
) {
    suspend fun addTodo(todo: com.example.androidmaster.data.database.TodoEntity) {
        todoDao.insertTodo(todo)
    }
    
    suspend fun updateTodo(todo: com.example.androidmaster.data.database.TodoEntity) {
        todoDao.updateTodo(todo)
    }
    
    suspend fun deleteTodo(todoId: Int) {
        todoDao.deleteTodoById(todoId)
    }
    
    suspend fun markAsComplete(todoId: Int) {
        val todo = todoDao.getTodoById(todoId)
        todo?.let {
            todoDao.updateTodo(it.copy(isCompleted = true))
        }
    }
    
    fun observeAllTodos() = todoDao.observeAllTodos()
    
    fun observeActiveTodos() = todoDao.observeActiveTodos()
    
    fun observeTodosByPriority(priority: Int) = todoDao.observeTodosByPriority(priority)
}

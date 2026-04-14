// app/src/main/kotlin/com/example/androidmaster/data/database/Entity.kt
package com.example.androidmaster.data.database

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

// === USER ENTITY ===
@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    
    @ColumnInfo(name = "user_name")
    val name: String,
    
    val email: String,
    val age: Int,
    
    @ColumnInfo(name = "profile_image")
    val profileImage: String? = null
)

// === POST ENTITY ===
@Entity(tableName = "posts")
data class PostEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    
    @ColumnInfo(name = "user_id")
    val userId: Int,
    
    val title: String,
    val content: String,
    
    @ColumnInfo(name = "created_at")
    val createdAt: String,
    
    @ColumnInfo(name = "like_count")
    var likeCount: Int = 0,
    
    var isLiked: Boolean = false
)

// === TODO ENTITY ===
@Entity(tableName = "todos")
data class TodoEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    
    val title: String,
    val description: String,
    val priority: Int = 1,  // 1=Low, 2=Medium, 3=High
    var isCompleted: Boolean = false,
    
    @ColumnInfo(name = "created_at")
    val createdAt: Long = System.currentTimeMillis(),
    
    @ColumnInfo(name = "due_date")
    val dueDate: Long? = null
)

// === CONTACT ENTITY ===
@Entity(tableName = "contacts")
data class ContactEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    
    val name: String,
    val phone: String,
    val email: String
)

// app/src/main/kotlin/com/example/androidmaster/data/remote/Models.kt
package com.example.androidmaster.data.remote

import com.google.gson.annotations.SerializedName

// === USER MODEL ===
data class User(
    val id: Int,
    val name: String,
    val email: String,
    val age: Int,
    @SerializedName("profile_image")
    val profileImage: String? = null
)

// === POST MODEL ===
data class Post(
    val id: Int,
    @SerializedName("user_id")
    val userId: Int,
    val title: String,
    val content: String,
    @SerializedName("created_at")
    val createdAt: String,
    @SerializedName("like_count")
    val likeCount: Int = 0,
    val isLiked: Boolean = false
)

// === API RESPONSE ===
data class ApiResponse<T>(
    val success: Boolean,
    val data: T?,
    val error: String?
)

// === LIST RESPONSE ===
data class ListResponse<T>(
    val items: List<T>,
    val total: Int,
    val page: Int
)

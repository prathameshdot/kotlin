// app/src/main/kotlin/com/example/androidmaster/data/remote/ApiService.kt
package com.example.androidmaster.data.remote

import retrofit2.http.*

interface ApiService {
    
    // === USER ENDPOINTS ===
    @GET("users")
    suspend fun getUsers(): List<User>
    
    @GET("users/{id}")
    suspend fun getUserById(@Path("id") userId: Int): User
    
    @POST("users")
    suspend fun createUser(@Body user: User): User
    
    @PUT("users/{id}")
    suspend fun updateUser(@Path("id") userId: Int, @Body user: User): User
    
    @DELETE("users/{id}")
    suspend fun deleteUser(@Path("id") userId: Int)
    
    // === POST ENDPOINTS ===
    @GET("posts")
    suspend fun getPosts(): List<Post>
    
    @GET("posts?page={page}&limit={limit}")
    suspend fun getPostsPaginated(
        @Query("page") page: Int,
        @Query("limit") limit: Int
    ): ListResponse<Post>
    
    @GET("posts/{id}")
    suspend fun getPostById(@Path("id") postId: Int): Post
    
    @GET("posts?search={query}")
    suspend fun searchPosts(@Query("search") query: String): List<Post>
    
    @POST("posts")
    suspend fun createPost(@Body post: Post): Post
    
    @PUT("posts/{id}")
    suspend fun updatePost(@Path("id") postId: Int, @Body post: Post): Post
    
    @DELETE("posts/{id}")
    suspend fun deletePost(@Path("id") postId: Int)
    
    @POST("posts/{id}/like")
    suspend fun likePost(@Path("id") postId: Int): Post
    
    // === COMMENT ENDPOINTS ===
    @GET("posts/{id}/comments")
    suspend fun getPostComments(@Path("id") postId: Int): List<Comment>
    
    data class Comment(val id: Int, val postId: Int, val text: String)
    
    // === SEARCH ENDPOINT ===
    @GET("search")
    suspend fun search(@Query("q") query: String): SearchResults
    
    data class SearchResults(
        val users: List<User>,
        val posts: List<Post>
    )
}

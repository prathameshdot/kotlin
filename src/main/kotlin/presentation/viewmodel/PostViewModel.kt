// app/src/main/kotlin/com/example/androidmaster/presentation/viewmodel/PostViewModel.kt
package com.example.androidmaster.presentation.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.androidmaster.data.remote.Post
import com.example.androidmaster.data.repository.PostRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class PostViewModel @Inject constructor(
    private val repository: PostRepository
) : ViewModel() {
    
    private val _posts = MutableLiveData<Result<List<Post>>>()
    val posts: LiveData<Result<List<Post>>> = _posts
    
    private val _currentPost = MutableLiveData<Result<Post>>()
    val currentPost: LiveData<Result<Post>> = _currentPost
    
    private val _searchResults = MutableLiveData<Result<List<Post>>>()
    val searchResults: LiveData<Result<List<Post>>> = _searchResults
    
    fun loadPosts(page: Int = 1) {
        viewModelScope.launch {
            _posts.value = Result.Loading()
            _posts.value = try {
                val postList = repository.getPosts(page)
                Result.Success(postList)
            } catch (e: Exception) {
                Result.Error(e)
            }
        }
    }
    
    fun searchPosts(query: String) {
        viewModelScope.launch {
            _searchResults.value = Result.Loading()
            _searchResults.value = try {
                val results = repository.searchPosts(query)
                Result.Success(results)
            } catch (e: Exception) {
                Result.Error(e)
            }
        }
    }
    
    fun loadPostById(postId: Int) {
        viewModelScope.launch {
            _currentPost.value = Result.Loading()
            _currentPost.value = try {
                val post = repository.getPostById(postId)
                Result.Success(post)
            } catch (e: Exception) {
                Result.Error(e)
            }
        }
    }
    
    fun createPost(post: Post) {
        viewModelScope.launch {
            try {
                repository.createPost(post)
                loadPosts()
            } catch (e: Exception) {
                _posts.value = Result.Error(e)
            }
        }
    }
    
    fun likePost(postId: Int) {
        viewModelScope.launch {
            try {
                repository.likePost(postId)
                loadPostById(postId)
            } catch (e: Exception) {
                _currentPost.value = Result.Error(e)
            }
        }
    }
}

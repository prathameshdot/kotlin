// app/src/main/kotlin/com/example/androidmaster/presentation/viewmodel/UserViewModel.kt
package com.example.androidmaster.presentation.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.androidmaster.data.remote.User
import com.example.androidmaster.data.repository.UserRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject

sealed class Result<T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error<T>(val exception: Exception) : Result<T>()
    class Loading<T> : Result<T>()
}

@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {
    
    private val _users = MutableLiveData<Result<List<User>>>()
    val users: LiveData<Result<List<User>>> = _users
    
    private val _currentUser = MutableLiveData<Result<User>>()
    val currentUser: LiveData<Result<User>> = _currentUser
    
    fun loadUsers() {
        viewModelScope.launch {
            _users.value = Result.Loading()
            _users.value = try {
                val userList = repository.getUsers()
                Result.Success(userList)
            } catch (e: Exception) {
                Result.Error(e)
            }
        }
    }
    
    fun loadUserById(userId: Int) {
        viewModelScope.launch {
            _currentUser.value = Result.Loading()
            _currentUser.value = try {
                val user = repository.getUserById(userId)
                Result.Success(user)
            } catch (e: Exception) {
                Result.Error(e)
            }
        }
    }
    
    fun createUser(user: User) {
        viewModelScope.launch {
            try {
                repository.createUser(user)
                loadUsers()
            } catch (e: Exception) {
                _users.value = Result.Error(e)
            }
        }
    }
}

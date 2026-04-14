// app/src/main/kotlin/com/example/androidmaster/presentation/viewmodel/TodoViewModel.kt
package com.example.androidmaster.presentation.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.androidmaster.data.database.TodoEntity
import com.example.androidmaster.data.repository.TodoRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class TodoViewModel @Inject constructor(
    private val repository: TodoRepository
) : ViewModel() {
    
    val allTodos: StateFlow<List<TodoEntity>> = repository.observeAllTodos()
        .stateIn(
            scope = viewModelScope,
            started = kotlinx.coroutines.flow.SharingStarted.Lazily,
            initialValue = emptyList()
        )
    
    val activeTodos: StateFlow<List<TodoEntity>> = repository.observeActiveTodos()
        .stateIn(
            scope = viewModelScope,
            started = kotlinx.coroutines.flow.SharingStarted.Lazily,
            initialValue = emptyList()
        )
    
    fun addTodo(todo: TodoEntity) {
        viewModelScope.launch {
            repository.addTodo(todo)
        }
    }
    
    fun updateTodo(todo: TodoEntity) {
        viewModelScope.launch {
            repository.updateTodo(todo)
        }
    }
    
    fun deleteTodo(todoId: Int) {
        viewModelScope.launch {
            repository.deleteTodo(todoId)
        }
    }
    
    fun markAsComplete(todoId: Int) {
        viewModelScope.launch {
            repository.markAsComplete(todoId)
        }
    }
    
    fun getTodosByPriority(priority: Int): StateFlow<List<TodoEntity>> {
        return repository.observeTodosByPriority(priority)
            .stateIn(
                scope = viewModelScope,
                started = kotlinx.coroutines.flow.SharingStarted.Lazily,
                initialValue = emptyList()
            )
    }
}

// Import for StateFlow
import kotlinx.coroutines.flow.stateIn

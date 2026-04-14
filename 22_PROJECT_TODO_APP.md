# Module 22: Project 1 - Complete Todo App
## Beginner to Advanced: Real-World Application

---

## 🎯 Project Overview

Build a complete **Todo App** with:
- Add, edit, delete todos
- Mark todos as complete
- Save to database (Room)
- Modern UI (Jetpack Compose)
- MVVM Architecture

**What You'll Learn**:
- Room Database (Persistence)
- State Management (MVVM)
- Jetpack Compose UI
- Coroutines (Threading)
- Data binding

---

## 📁 Project Structure

```
TodoApp/
├── data/
│   ├── database/
│   │   ├── TodoDatabase.kt
│   │   └── TodoDao.kt
│   └── models/
│       └── Todo.kt
├── ui/
│   ├── screens/
│   │   └── TodoListScreen.kt
│   └── viewmodels/
│       └── TodoViewModel.kt
└── MainActivity.kt
```

---

## Step 1️⃣: Create Data Model

```kotlin
// data/models/Todo.kt
package com.example.todoapp.data

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.time.LocalDateTime

@Entity(tableName = "todos")
data class Todo(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val title: String,
    val description: String = "",
    val isCompleted: Boolean = false,
    val createdAt: String = LocalDateTime.now().toString(),
    val dueDate: String? = null
)
```

---

## Step 2️⃣: Create Database (Room)

```kotlin
// data/database/TodoDao.kt
package com.example.todoapp.data

import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Dao
interface TodoDao {
    // Read all todos
    @Query("SELECT * FROM todos ORDER BY createdAt DESC")
    fun getAllTodos(): Flow<List<Todo>>
    
    // Read completed todos
    @Query("SELECT * FROM todos WHERE isCompleted = 1")
    fun getCompletedTodos(): Flow<List<Todo>>
    
    // Read pending todos
    @Query("SELECT * FROM todos WHERE isCompleted = 0")
    fun getPendingTodos(): Flow<List<Todo>>
    
    // Get single todo
    @Query("SELECT * FROM todos WHERE id = :id")
    suspend fun getTodoById(id: Int): Todo
    
    // Search todos
    @Query("SELECT * FROM todos WHERE title LIKE '%' || :query || '%'")
    fun searchTodos(query: String): Flow<List<Todo>>
    
    // Create todo
    @Insert
    suspend fun insertTodo(todo: Todo)
    
    // Update todo
    @Update
    suspend fun updateTodo(todo: Todo)
    
    // Delete todo
    @Delete
    suspend fun deleteTodo(todo: Todo)
    
    // Delete all todos
    @Query("DELETE FROM todos")
    suspend fun deleteAllTodos()
}

// data/database/TodoDatabase.kt
package com.example.todoapp.data

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(entities = [Todo::class], version = 1, exportSchema = false)
abstract class TodoDatabase : RoomDatabase() {
    abstract fun todoDao(): TodoDao
    
    companion object {
        @Volatile
        private var INSTANCE: TodoDatabase? = null
        
        fun getDatabase(context: Context): TodoDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    TodoDatabase::class.java,
                    "todo_database"
                ).build()
                INSTANCE = instance
                instance
            }
        }
    }
}
```

---

## Step 3️⃣: Create Repository

```kotlin
// data/TodoRepository.kt
package com.example.todoapp.data

import kotlinx.coroutines.flow.Flow

class TodoRepository(private val todoDao: TodoDao) {
    
    // Read operations
    val allTodos: Flow<List<Todo>> = todoDao.getAllTodos()
    val completedTodos: Flow<List<Todo>> = todoDao.getCompletedTodos()
    val pendingTodos: Flow<List<Todo>> = todoDao.getPendingTodos()
    
    fun searchTodos(query: String): Flow<List<Todo>> = todoDao.searchTodos(query)
    
    // Write operations
    suspend fun addTodo(todo: Todo) = todoDao.insertTodo(todo)
    suspend fun updateTodo(todo: Todo) = todoDao.updateTodo(todo)
    suspend fun deleteTodo(todo: Todo) = todoDao.deleteTodo(todo)
    suspend fun deleteAllTodos() = todoDao.deleteAllTodos()
    
    // Mark as completed
    suspend fun markCompleted(todo: Todo) {
        todoDao.updateTodo(todo.copy(isCompleted = true))
    }
    
    // Mark as pending
    suspend fun markPending(todo: Todo) {
        todoDao.updateTodo(todo.copy(isCompleted = false))
    }
}
```

---

## Step 4️⃣: Create ViewModel

```kotlin
// ui/viewmodels/TodoViewModel.kt
package com.example.todoapp.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.todoapp.data.Todo
import com.example.todoapp.data.TodoRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class TodoViewModel(private val repository: TodoRepository) : ViewModel() {
    
    // UI State
    private val _todos = MutableStateFlow<List<Todo>>(emptyList())
    val todos: StateFlow<List<Todo>> = _todos.asStateFlow()
    
    private val _filter = MutableStateFlow<TodoFilter>(TodoFilter.ALL)
    val filter: StateFlow<TodoFilter> = _filter.asStateFlow()
    
    private val _selectedTodo = MutableStateFlow<Todo?>(null)
    val selectedTodo: StateFlow<Todo?> = _selectedTodo.asStateFlow()
    
    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery.asStateFlow()
    
    init {
        loadTodos()
    }
    
    fun loadTodos() {
        viewModelScope.launch {
            when (_filter.value) {
                TodoFilter.ALL -> repository.allTodos.collect { _todos.value = it }
                TodoFilter.COMPLETED -> repository.completedTodos.collect { _todos.value = it }
                TodoFilter.PENDING -> repository.pendingTodos.collect { _todos.value = it }
            }
        }
    }
    
    fun setFilter(filter: TodoFilter) {
        _filter.value = filter
        loadTodos()
    }
    
    fun addTodo(title: String, description: String = "", dueDate: String? = null) {
        viewModelScope.launch {
            val newTodo = Todo(
                title = title,
                description = description,
                dueDate = dueDate
            )
            repository.addTodo(newTodo)
        }
    }
    
    fun updateTodo(todo: Todo) {
        viewModelScope.launch {
            repository.updateTodo(todo)
        }
    }
    
    fun deleteTodo(todo: Todo) {
        viewModelScope.launch {
            repository.deleteTodo(todo)
        }
    }
    
    fun toggleTodoCompletion(todo: Todo) {
        viewModelScope.launch {
            val updated = todo.copy(isCompleted = !todo.isCompleted)
            repository.updateTodo(updated)
        }
    }
    
    fun selectTodo(todo: Todo?) {
        _selectedTodo.value = todo
    }
    
    fun searchTodos(query: String) {
        _searchQuery.value = query
        if (query.isEmpty()) {
            loadTodos()
        } else {
            viewModelScope.launch {
                repository.searchTodos(query).collect { _todos.value = it }
            }
        }
    }
}

enum class TodoFilter {
    ALL, COMPLETED, PENDING
}
```

---

## Step 5️⃣: Create UI (Jetpack Compose)

```kotlin
// ui/screens/TodoListScreen.kt
package com.example.todoapp.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.todoapp.data.Todo
import com.example.todoapp.ui.viewmodels.TodoFilter
import com.example.todoapp.ui.viewmodels.TodoViewModel

@Composable
fun TodoListScreen(viewModel: TodoViewModel) {
    val todos by viewModel.todos.collectAsState()
    val filter by viewModel.filter.collectAsState()
    val searchQuery by viewModel.searchQuery.collectAsState()
    val selectedTodo by viewModel.selectedTodo.collectAsState()
    
    var showAddDialog by remember { mutableStateOf(false) }
    
    Scaffold(
        floatingActionButton = {
            FloatingActionButton(
                onClick = { showAddDialog = true },
                containerColor = MaterialTheme.colorScheme.primary
            ) {
                Icon(Icons.Default.Add, contentDescription = "Add Todo")
            }
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            // Search bar
            SearchBar(
                query = searchQuery,
                onQueryChange = { viewModel.searchTodos(it) },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(8.dp)
            )
            
            // Filter buttons
            FilterButtons(
                selectedFilter = filter,
                onFilterSelected = { viewModel.setFilter(it) },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(8.dp)
            )
            
            // Todo list
            if (todos.isEmpty()) {
                EmptyState()
            } else {
                LazyColumn {
                    items(todos) { todo ->
                        TodoItem(
                            todo = todo,
                            onToggleCompletion = { viewModel.toggleTodoCompletion(it) },
                            onDelete = { viewModel.deleteTodo(it) },
                            onSelect = { viewModel.selectTodo(it) }
                        )
                    }
                }
            }
        }
    }
    
    // Add Todo Dialog
    if (showAddDialog) {
        AddTodoDialog(
            onAdd = { title, description, dueDate ->
                viewModel.addTodo(title, description, dueDate)
                showAddDialog = false
            },
            onDismiss = { showAddDialog = false }
        )
    }
    
    // Edit Todo Dialog
    if (selectedTodo != null) {
        EditTodoDialog(
            todo = selectedTodo!!,
            onUpdate = { updated ->
                viewModel.updateTodo(updated)
                viewModel.selectTodo(null)
            },
            onDismiss = { viewModel.selectTodo(null) }
        )
    }
}

@Composable
fun SearchBar(
    query: String,
    onQueryChange: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    TextField(
        value = query,
        onValueChange = onQueryChange,
        placeholder = { Text("Search todos...") },
        leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
        modifier = modifier.fillMaxWidth(),
        singleLine = true
    )
}

@Composable
fun FilterButtons(
    selectedFilter: TodoFilter,
    onFilterSelected: (TodoFilter) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier.horizontalScroll(rememberScrollState()),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        TodoFilter.values().forEach { filter ->
            FilterChip(
                selected = selectedFilter == filter,
                onClick = { onFilterSelected(filter) },
                label = { Text(filter.name) },
                leadingIcon = if (selectedFilter == filter) {
                    { Icon(Icons.Default.Done, contentDescription = null) }
                } else {
                    null
                }
            )
        }
    }
}

@Composable
fun TodoItem(
    todo: Todo,
    onToggleCompletion: (Todo) -> Unit,
    onDelete: (Todo) -> Unit,
    onSelect: (Todo) -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .padding(8.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Checkbox(
                checked = todo.isCompleted,
                onCheckedChange = { onToggleCompletion(todo) }
            )
            
            Column(
                modifier = Modifier
                    .weight(1f)
                    .padding(start = 16.dp)
            ) {
                Text(
                    text = todo.title,
                    style = MaterialTheme.typography.bodyLarge
                )
                if (todo.description.isNotEmpty()) {
                    Text(
                        text = todo.description,
                        style = MaterialTheme.typography.bodySmall
                    )
                }
                if (todo.dueDate != null) {
                    Text(
                        text = "Due: ${todo.dueDate}",
                        style = MaterialTheme.typography.labelSmall
                    )
                }
            }
            
            IconButton(onClick = { onSelect(todo) }) {
                Icon(Icons.Default.Edit, contentDescription = "Edit")
            }
            
            IconButton(onClick = { onDelete(todo) }) {
                Icon(Icons.Default.Delete, contentDescription = "Delete")
            }
        }
    }
}

@Composable
fun EmptyState() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .wrapContentSize(Alignment.Center),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Icon(
            Icons.Default.Info,
            contentDescription = null,
            modifier = Modifier.size(64.dp)
        )
        Spacer(Modifier.height(16.dp))
        Text("No todos yet! Add one to get started.")
    }
}

@Composable
fun AddTodoDialog(
    onAdd: (String, String, String?) -> Unit,
    onDismiss: () -> Unit
) {
    var title by remember { mutableStateOf("") }
    var description by remember { mutableStateOf("") }
    var dueDate by remember { mutableStateOf("") }
    
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Add New Todo") },
        text = {
            Column(modifier = Modifier.fillMaxWidth()) {
                TextField(
                    value = title,
                    onValueChange = { title = it },
                    label = { Text("Title") },
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(Modifier.height(8.dp))
                TextField(
                    value = description,
                    onValueChange = { description = it },
                    label = { Text("Description") },
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(Modifier.height(8.dp))
                TextField(
                    value = dueDate,
                    onValueChange = { dueDate = it },
                    label = { Text("Due Date") },
                    modifier = Modifier.fillMaxWidth()
                )
            }
        },
        confirmButton = {
            Button(
                onClick = {
                    if (title.isNotBlank()) {
                        onAdd(title, description, dueDate.ifBlank { null })
                    }
                }
            ) {
                Text("Add")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}

@Composable
fun EditTodoDialog(
    todo: Todo,
    onUpdate: (Todo) -> Unit,
    onDismiss: () -> Unit
) {
    var title by remember { mutableStateOf(todo.title) }
    var description by remember { mutableStateOf(todo.description) }
    var dueDate by remember { mutableStateOf(todo.dueDate ?: "") }
    
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Edit Todo") },
        text = {
            Column(modifier = Modifier.fillMaxWidth()) {
                TextField(
                    value = title,
                    onValueChange = { title = it },
                    label = { Text("Title") },
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(Modifier.height(8.dp))
                TextField(
                    value = description,
                    onValueChange = { description = it },
                    label = { Text("Description") },
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(Modifier.height(8.dp))
                TextField(
                    value = dueDate,
                    onValueChange = { dueDate = it },
                    label = { Text("Due Date") },
                    modifier = Modifier.fillMaxWidth()
                )
            }
        },
        confirmButton = {
            Button(
                onClick = {
                    val updated = todo.copy(
                        title = title,
                        description = description,
                        dueDate = dueDate.ifBlank { null }
                    )
                    onUpdate(updated)
                }
            ) {
                Text("Update")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}
```

---

## Step 6️⃣: Setup MainActivity

```kotlin
// MainActivity.kt
package com.example.todoapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.todoapp.data.TodoDatabase
import com.example.todoapp.data.TodoRepository
import com.example.todoapp.ui.screens.TodoListScreen
import com.example.todoapp.ui.theme.TodoAppTheme
import com.example.todoapp.ui.viewmodels.TodoViewModel
import com.example.todoapp.ui.viewmodels.TodoViewModelFactory

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val database = TodoDatabase.getDatabase(this)
        val repository = TodoRepository(database.todoDao())
        val viewModelFactory = TodoViewModelFactory(repository)
        
        setContent {
            TodoAppTheme {
                Surface(color = MaterialTheme.colorScheme.background) {
                    val viewModel = viewModel<TodoViewModel>(factory = viewModelFactory)
                    TodoListScreen(viewModel)
                }
            }
        }
    }
}

// ViewModelFactory
package com.example.todoapp.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.todoapp.data.TodoRepository

class TodoViewModelFactory(private val repository: TodoRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(TodoViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return TodoViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
```

---

## Step 7️⃣: Add Dependencies (build.gradle.kts)

```gradle
dependencies {
    // Jetpack Compose
    implementation("androidx.compose.ui:ui:1.5.0")
    implementation("androidx.compose.material3:material3:1.1.0")
    implementation("androidx.compose.runtime:runtime:1.5.0")
    
    // Room Database
    implementation("androidx.room:room-runtime:2.5.2")
    implementation("androidx.room:room-ktx:2.5.2")
    kapt("androidx.room:room-compiler:2.5.2")
    
    // Lifecycle
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.6.1")
    implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.6.1")
    
    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.1")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.1")
}
```

---

## 📊 Features Implemented

✅ Add new todos
✅ Edit existing todos
✅ Delete todos
✅ Mark todos as complete
✅ Filter todos (all, completed, pending)
✅ Search todos
✅ Persistent storage (Room Database)
✅ Modern UI (Jetpack Compose)
✅ MVVM Architecture
✅ Coroutines for background tasks

---

## 🏋️ Exercises

1. Add due date picker dialog
2. Add priority levels (High, Medium, Low)
3. Add categories/tags
4. Add statistics (total, completed, pending)
5. Add export to CSV
6. Add notification reminders
7. Add dark mode toggle
8. Add undo/redo functionality

---

**Next: [Project 2 - Weather App](23_PROJECT_WEATHER_APP.md)**

// app/src/main/kotlin/com/example/androidmaster/MainActivity.kt
package com.example.androidmaster

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Home
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            AndroidMasterTheme {
                MainApp()
            }
        }
    }
}

@Composable
fun MainApp() {
    val navController = rememberNavController()
    var selectedTab by remember { mutableStateOf(0) }
    
    Scaffold(
        bottomBar = {
            NavigationBar {
                NavigationBarItem(
                    selected = selectedTab == 0,
                    onClick = { selectedTab = 0; navController.navigate("home") },
                    label = { Text("Home") },
                    icon = { Icon(Icons.Filled.Home, contentDescription = "Home") }
                )
                NavigationBarItem(
                    selected = selectedTab == 1,
                    onClick = { selectedTab = 1; navController.navigate("todos") },
                    label = { Text("Todos") },
                    icon = { Icon(Icons.Filled.Add, contentDescription = "Todos") }
                )
                NavigationBarItem(
                    selected = selectedTab == 2,
                    onClick = { selectedTab = 2; navController.navigate("forms") },
                    label = { Text("Forms") },
                    icon = { Icon(Icons.Filled.Home, contentDescription = "Forms") }
                )
            }
        }
    ) { padding ->
        NavHost(
            navController = navController,
            startDestination = "home",
            modifier = Modifier.padding(padding)
        ) {
            composable("home") { HomeScreen(navController) }
            composable("todos") { TodoListScreen(navController) }
            composable("forms") { FormDemoScreen(navController) }
            composable("ui_components") { UIComponentsScreen(navController) }
            composable("animations") { AnimationDemoScreen(navController) }
        }
    }
}

@Composable
fun HomeScreen(navController: NavController) {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        item {
            Text(
                "Android Master Course",
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.primary
            )
        }
        
        item {
            WelcomeCard()
        }
        
        item {
            Button(
                onClick = { navController.navigate("ui_components") },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Explore UI Components")
            }
        }
        
        item {
            Button(
                onClick = { navController.navigate("animations") },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Animation Examples")
            }
        }
        
        item {
            Button(
                onClick = { navController.navigate("forms") },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Form Components")
            }
        }
        
        items(5) { index ->
            PostCard(title = "Post $index", content = "This is sample post content $index")
        }
    }
}

@Composable
fun WelcomeCard() {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp),
        elevation = CardDefaults.cardElevation(8.dp),
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(
            modifier = Modifier
                .background(MaterialTheme.colorScheme.primaryContainer)
                .padding(16.dp)
        ) {
            Text(
                "Welcome to Android Master!",
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onPrimaryContainer
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                "Learn Kotlin, Jetpack Compose, and Android development from zero to hero.",
                color = MaterialTheme.colorScheme.onPrimaryContainer
            )
        }
    }
}

@Composable
fun PostCard(title: String, content: String) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(4.dp),
        elevation = CardDefaults.cardElevation(4.dp)
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Text(title, fontWeight = FontWeight.Bold, fontSize = 16.sp)
            Spacer(modifier = Modifier.height(4.dp))
            Text(content, fontSize = 14.sp, color = Color.Gray)
            Spacer(modifier = Modifier.height(8.dp))
            Row {
                Button(onClick = {}, modifier = Modifier.weight(1f)) {
                    Text("Like")
                }
                Spacer(modifier = Modifier.width(4.dp))
                Button(onClick = {}, modifier = Modifier.weight(1f)) {
                    Text("Comment")
                }
            }
        }
    }
}

@Composable
fun TodoListScreen(navController: NavController) {
    var todoText by remember { mutableStateOf("") }
    val todoList = remember { mutableStateListOf("Learn Kotlin", "Build App", "Master Compose") }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text("My Todos", fontSize = 20.sp, fontWeight = FontWeight.Bold)
        
        Spacer(modifier = Modifier.height(12.dp))
        
        Row(modifier = Modifier.fillMaxWidth()) {
            TextField(
                value = todoText,
                onValueChange = { todoText = it },
                label = { Text("Add todo...") },
                modifier = Modifier.weight(1f)
            )
            Button(onClick = {
                if (todoText.isNotEmpty()) {
                    todoList.add(todoText)
                    todoText = ""
                }
            }) {
                Text("Add")
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        LazyColumn {
            items(todoList.size) { index ->
                TodoItemCard(todoList[index], onDelete = { todoList.removeAt(index) })
            }
        }
    }
}

@Composable
fun TodoItemCard(text: String, onDelete: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(text, modifier = Modifier.weight(1f))
            Button(onClick = onDelete) {
                Text("Delete")
            }
        }
    }
}

@Composable
fun FormDemoScreen(navController: NavController) {
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var isChecked by remember { mutableStateOf(false) }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.Center
    ) {
        TextField(
            value = email,
            onValueChange = { email = it },
            label = { Text("Email") },
            modifier = Modifier.fillMaxWidth()
        )
        
        Spacer(modifier = Modifier.height(12.dp))
        
        TextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("Password") },
            modifier = Modifier.fillMaxWidth()
        )
        
        Spacer(modifier = Modifier.height(12.dp))
        
        Row(verticalAlignment = Alignment.CenterVertically) {
            Checkbox(
                checked = isChecked,
                onCheckedChange = { isChecked = it }
            )
            Text("Remember me")
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Button(
            onClick = { /* Handle login */ },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Login")
        }
    }
}

@Composable
fun UIComponentsScreen(navController: NavController) {
    LazyColumn(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        item { Text("Button Variants", fontWeight = FontWeight.Bold, fontSize = 18.sp) }
        item {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(onClick = {}) { Text("Primary") }
                OutlinedButton(onClick = {}) { Text("Outlined") }
                TextButton(onClick = {}) { Text("Text") }
            }
        }
        
        item { Spacer(modifier = Modifier.height(12.dp)) }
        item { Text("Cards", fontWeight = FontWeight.Bold, fontSize = 18.sp) }
        item { PostCard("Card Title", "Card content example") }
        
        item { Spacer(modifier = Modifier.height(12.dp)) }
        item { Text("Grid/Flex Layout", fontWeight = FontWeight.Bold, fontSize = 18.sp) }
        item {
            Column {
                repeat(3) {
                    Row {
                        repeat(2) {
                            Box(
                                modifier = Modifier
                                    .weight(1f)
                                    .height(100.dp)
                                    .background(MaterialTheme.colorScheme.primaryContainer)
                                    .padding(4.dp),
                                contentAlignment = Alignment.Center
                            ) {
                                Text("Grid Item")
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun AnimationDemoScreen(navController: NavController) {
    var isExpanded by remember { mutableStateOf(false) }
    val size by animateDpAsState(targetValue = if (isExpanded) 200.dp else 100.dp)
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("Animation Demo", fontSize = 20.sp, fontWeight = FontWeight.Bold)
        
        Spacer(modifier = Modifier.height(32.dp))
        
        Box(
            modifier = Modifier
                .size(size)
                .background(MaterialTheme.colorScheme.primary)
        )
        
        Spacer(modifier = Modifier.height(32.dp))
        
        Button(onClick = { isExpanded = !isExpanded }) {
            Text(if (isExpanded) "Shrink" else "Expand")
        }
    }
}

// Import needed for animations
import androidx.compose.animation.animateDpAsState

@Composable
fun AndroidMasterTheme(content: @Composable () -> Unit) {
    MaterialTheme(content = content)
}

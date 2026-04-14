# Module 3.3: Advanced Compose Patterns

## 🎯 Recomposition & State Management

Compose recomposes (re-renders) when state changes. Only affected composables recompose.

```kotlin
// Good: Only affected recomposes
var count by remember { mutableStateOf(0) }

Button(onClick = { count++ }) {  // Recomposes only when count changes
    Text("Count: $count")
}

// Bad: Causes unnecessary recompositions
// Creating state outside remember
val itemList = mutableStateOf(listOf())  // Re-created every recomposition!
```

## 🎨 Custom Composables & Composition

```kotlin
@Composable
fun UserCard(name: String, email: String) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(name, style = MaterialTheme.typography.headlineSmall)
            Text(email, color = Color.Gray)
        }
    }
}

// Usage
Column {
    UserCard("Alice", "alice@email.com")
    UserCard("Bob", "bob@email.com")
}
```

## 🔄 State Hoisting

```kotlin
// Before: State inside composable
@Composable
fun CounterBad() {
    var count by remember { mutableStateOf(0) }
    Button(onClick = { count++ }) { Text("Count: $count") }
}

// After: State hoisted to parent
@Composable
fun CounterGood(count: Int, onCountChange: (Int) -> Unit) {
    Button(onClick = { onCountChange(count + 1) }) { 
        Text("Count: $count") 
    }
}

@Composable
fun ParentScreen() {
    var count by remember { mutableStateOf(0) }
    CounterGood(count) { count = it }
}
```

## 🌊 Side Effects

```kotlin
// LaunchedEffect: Run code when key changes
LaunchedEffect(userId) {
    loadUserProfile(userId)
}

// DisposableEffect: Cleanup
DisposableEffect(Unit) {
    onDispose {
        // Cleanup code
    }
}

// SideEffect: Run after every recomposition
SideEffect {
    analytics.trackScreen("ProfileScreen")
}
```

## 📊 Lists with LazyColumn/LazyRow

```kotlin
LazyColumn {
    items(userList.size) { index ->
        UserItem(userList[index])
    }
}

// Better with item IDs
LazyColumn {
    items(userList, key = { it.id }) { user ->
        UserItem(user)
    }
}

// Horizontal scrolling
LazyRow {
    items(categoryList) { category ->
        CategoryChip(category)
    }
}
```

## 🎬 Advanced Animations

```kotlin
// Smooth color transition
val backgroundColor by animateColorAsState(
    targetValue = if (isSelected) Color.Blue else Color.Gray
)

// Content fade in/out
AnimatedContent(
    targetState = currentScreen,
    transitionSpec = {
        fadeIn() with fadeOut()
    }
) { screen ->
    when (screen) {
        Screen.Home -> HomeScreen()
        Screen.Profile -> ProfileScreen()
    }
}
```

## 🎓 Summary

Key patterns for professional Compose development.

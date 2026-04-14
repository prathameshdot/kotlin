# Module 3.4: Navigation in Jetpack Compose

## 🧭 Compose Navigation Setup

```kotlin
// Dependencies
implementation "androidx.navigation:navigation-compose:2.7.0"

// Create NavController
val navController = rememberNavController()

NavHost(navController = navController, startDestination = "home") {
    composable("home") { HomeScreen(navController) }
    composable("profile/{userId}") { backStackEntry ->
        ProfileScreen(
            userId = backStackEntry.arguments?.getString("userId") ?: "",
            navController = navController
        )
    }
    composable("settings") { SettingsScreen(navController) }
}
```

## 📤 Navigation Between Screens

```kotlin
@Composable
fun HomeScreen(navController: NavController) {
    Button(onClick = { 
        navController.navigate("profile/123")
    }) {
        Text("Go to Profile")
    }
}

@Composable
fun ProfileScreen(userId: String, navController: NavController) {
    Button(onClick = { 
        navController.navigate("settings")
    }) {
        Text("Go to Settings")
    }
}
```

## 🔙 Back Navigation

```kotlin
// Navigate back
navController.popBackStack()

// Navigate back to specific destination
navController.popBackStack("home", inclusive = false)

// Check if can navigate back
if (navController.previousBackStackEntry != null) {
    navController.popBackStack()
}
```

## 📊 Bottom Navigation

```kotlin
@Composable
fun MainScreen() {
    val navController = rememberNavController()
    val items = listOf("Home", "Search", "Profile")
    
    Scaffold(
        bottomBar = {
            NavigationBar {
                items.forEach { item ->
                    NavigationBarItem(
                        selected = navController.currentDestination?.route == item,
                        onClick = { navController.navigate(item) },
                        label = { Text(item) },
                        icon = { Icon(Icons.Filled.Home, null) }
                    )
                }
            }
        }
    ) { padding ->
        NavHost(navController, startDestination = "Home") {
            composable("Home") { HomeScreen() }
            composable("Search") { SearchScreen() }
            composable("Profile") { ProfileScreen() }
        }
    }
}
```

## 🎓 Summary

Modern navigation in Jetpack Compose using Navigation Compose library.

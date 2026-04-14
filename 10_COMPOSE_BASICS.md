# Module 3.1: Jetpack Compose Basics
## Modern UI Development for Android

---

## 📖 What is Jetpack Compose?

Jetpack Compose is Google's modern way to build Android UIs using **declarative programming**. Instead of writing XML, you write Kotlin code that describes what the UI should look like.

### **Comparison: XML vs Compose**

```
❌ XML (Old Way)              ✅ Compose (New Way)
- Write XML files             - Write Kotlin functions
- Hard to reuse               - Reusable composables
- Hard to share logic         - Easy state management
- Verbose                     - Concise
- Not type-safe               - Type-safe
```

---

## 1️⃣ First Composable Function

Think of a **composable function** as a recipe that returns a piece of UI.

```kotlin
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

// Simple composable - just displays text
@Composable
fun Greeting() {
    Text("Hello, Android!")
}

// Composable with parameter
@Composable
fun PersonGreeting(name: String) {
    Text("Hello, $name!")
}

// Composable that returns different things
@Composable
fun UserMessage(isLoggedIn: Boolean) {
    if (isLoggedIn) {
        Text("Welcome back!")
    } else {
        Text("Please log in")
    }
}
```

**Key Points**:
- Functions must have `@Composable` annotation
- Must start with capital letter (by convention)
- Return type is `Unit`
- Can contain conditionals and loops

---

## 2️⃣ Basic Composables

### **Text - Display Text**

```kotlin
@Composable
fun TextExample() {
    Text(
        text = "Hello, Compose!",
        fontSize = 24.sp,          // Size in scale-independent pixels
        fontStyle = FontStyle.Italic,
        fontWeight = FontWeight.Bold,
        color = Color.Blue
    )
}
```

### **Button - Clickable**

```kotlin
@Composable
fun ButtonExample() {
    var clicked = remember { mutableStateOf(false) }
    
    Button(
        onClick = {
            clicked.value = true
        },
        modifier = Modifier.padding(16.dp)
    ) {
        Text("Click Me!")
    }
    
    if (clicked.value) {
        Text("Button was clicked!")
    }
}
```

### **TextField - User Input**

```kotlin
@Composable
fun InputExample() {
    var text = remember { mutableStateOf("") }
    
    TextField(
        value = text.value,
        onValueChange = { newValue ->
            text.value = newValue
        },
        label = { Text("Enter name") },
        modifier = Modifier
            .padding(16.dp)
            .fillMaxWidth()
    )
    
    Text("You entered: ${text.value}")
}
```

### **Image - Display Images**

```kotlin
@Composable
fun ImageExample() {
    Image(
        painter = painterResource(id = R.drawable.profile_image),
        contentDescription = "Profile picture",
        modifier = Modifier
            .size(100.dp)
            .clip(CircleShape),
        contentScale = ContentScale.Crop
    )
}
```

### **Checkbox - Yes/No**

```kotlin
@Composable
fun CheckboxExample() {
    var isChecked = remember { mutableStateOf(false) }
    
    Row(modifier = Modifier.padding(16.dp)) {
        Checkbox(
            checked = isChecked.value,
            onCheckedChange = { newValue ->
                isChecked.value = newValue
            }
        )
        Text("I agree to terms")
    }
}
```

---

## 3️⃣ State Management: The Heart of Compose

### **What is State?**

State is any data that changes. When state changes, Compose re-renders the UI.

```kotlin
@Composable
fun CounterExample() {
    // Create mutable state
    var count = remember { mutableStateOf(0) }
    
    Column(modifier = Modifier.padding(16.dp)) {
        Text("Count: ${count.value}")
        
        Button(onClick = {
            count.value++  // Update state
        }) {
            Text("Increment")
        }
        
        Button(onClick = {
            count.value--
        }) {
            Text("Decrement")
        }
    }
}

// When count.value changes, Compose automatically re-renders!
```

### **Destructuring State (Cleaner Syntax)**

```kotlin
@Composable
fun CounterCleaner() {
    var (count, setCount) = remember { mutableStateOf(0) }
    
    Column(modifier = Modifier.padding(16.dp)) {
        Text("Count: $count")
        
        Button(onClick = { setCount(count + 1) }) {
            Text("Increment")
        }
        
        Button(onClick = { setCount(count - 1) }) {
            Text("Decrement")
        }
    }
}
```

---

## 4️⃣ Layouts: Arranging Composables

### **Column - Vertical Stack**

```kotlin
@Composable
fun ColumnExample() {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("Item 1")
        Text("Item 2")
        Text("Item 3")
        // Items stacked vertically
    }
}
```

### **Row - Horizontal Stack**

```kotlin
@Composable
fun RowExample() {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
       horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text("Left")
        Text("Right")
        // Items arranged horizontally
    }
}
```

### **Box - Layered Stack (Like FrameLayout)**

```kotlin
@Composable
fun BoxExample() {
    Box(
        modifier = Modifier
            .size(200.dp)
            .background(Color.Blue)
    ) {
        // Background
        Image(
            painter = painterResource(id = R.drawable.background),
            contentDescription = null,
            modifier = Modifier.matchParentSize()
        )
        
        // Overlay text
        Text(
            "Overlay Text",
            modifier = Modifier.align(Alignment.Center),
            color = Color.White
        )
    }
}
```

---

## 5️⃣ Modifiers: Styling & Sizing

Modifiers are how you style and position composables.

```kotlin
@Composable
fun ModifierExample() {
    Text(
        "Styled Text",
        modifier = Modifier
            .size(width = 200.dp, height = 100.dp)  // Size
            .padding(16.dp)                         // Internal space
            .background(Color.LightBlue)            // Background color
            .border(2.dp, Color.Blue)               // Border
            .clip(RoundedCornerShape(8.dp))         // Rounded corners
            .clickable { println("Clicked!") }      // Clickable
    )
}
```

### **Common Modifiers**

```kotlin
Modifier
    .size(100.dp)                               // Fixed size
    .fillMaxWidth()                             // Full screen width
    .fillMaxHeight()                            // Full screen height
    .fillMaxSize()                              // Full screen
    .wrapContentSize()                          // Only needed space
    
    .padding(16.dp)                             // Inside space
    .padding(top = 8.dp, bottom = 8.dp)         // Individual sides
    
    .background(Color.Blue)                     // Background color
    .background(RoundedCornerShape(8.dp))       // Rounded
    .border(2.dp, Color.Black)                  // Border
    .clip(CircleShape)                          // Circular
    
    .align(Alignment.Center)                    // Position in Box
    .weight(1f)                                 // Share space in Row/Column
    .clickable { }                              // Clickable action
    .enabled(false)                             // Disable interaction
    .alpha(0.5f)                                // Transparency
```

---

## 6️⃣ Real-World Example: User Profile Screen

```kotlin
@Composable
fun UserProfileScreen(userId: Int) {
    var (userName, setUserName) = remember { mutableStateOf("Alice Developer") }
    var (userEmail, setUserEmail) = remember { mutableStateOf("alice@email.com") }
    var (isEditing, setIsEditing) = remember { mutableStateOf(false) }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
            .verticalScroll(rememberScrollState()),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        // Profile Image
        Image(
            painter = painterResource(id = R.drawable.profile_image),
            contentDescription = "Profile",
            modifier = Modifier
                .size(120.dp)
                .clip(CircleShape),
            contentScale = ContentScale.Crop
        )
        
        Spacer(Modifier.height(16.dp))
        
        // Name
        if (isEditing) {
            TextField(
                value = userName,
                onValueChange = setUserName,
                label = { Text("Name") },
                modifier = Modifier.fillMaxWidth()
            )
        } else {
            Text(
                userName,
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold
            )
        }
        
        Spacer(Modifier.height(8.dp))
        
        // Email
        if (isEditing) {
            TextField(
                value = userEmail,
                onValueChange = setUserEmail,
                label = { Text("Email") },
                modifier = Modifier.fillMaxWidth()
            )
        } else {
            Text(
                userEmail,
                fontSize = 14.sp,
                color = Color.Gray
            )
        }
        
        Spacer(Modifier.height(24.dp))
        
        // Edit/Save Button
        Button(
            onClick = { setIsEditing(!isEditing) },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text(if (isEditing) "Save" else "Edit Profile")
        }
        
        // Logout Button
        Button(
            onClick = { logout() },
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 8.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Color.Red)
        ) {
            Text("Logout")
        }
    }
}
```

---

## 7️⃣ Reusable Composables

Compose is all about reusability!

```kotlin
// Simple reusable composable
@Composable
fun UserCard(
    name: String,
    email: String,
    onDelete: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(name, fontSize = 18.sp, fontWeight = FontWeight.Bold)
            Text(email, fontSize = 14.sp)
            
            Button(
                onClick = onDelete,
                modifier = Modifier
                    .align(Alignment.End)
                    .padding(top = 8.dp)
            ) {
                Text("Delete")
            }
        }
    }
}

// Using the composable
@Composable
fun UserListScreen() {
    val users = listOf(
        Pair("Alice", "alice@email.com"),
        Pair("Bob", "bob@email.com"),
        Pair("Charlie", "charlie@email.com")
    )
    
    LazyColumn {
        items(users.size) { index ->
            val (name, email) = users[index]
            UserCard(
                name = name,
                email = email,
                onDelete = { println("Delete $name") }
            )
        }
    }
}
```

---

## 8️⃣ Lists: LazyColumn and LazyRow

```kotlin
@Composable
fun ListExample() {
    val items = (1..100).map { "Item $it" }
    
    // LazyColumn - only renders visible items (efficient!)
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(items.size) { index ->
            Item ListItemComponent(items[index])
        }
    }
}

@Composable
fun ListItemComponent(text: String) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Text(
            text,
            modifier = Modifier.padding(16.dp),
            fontSize = 16.sp
        )
    }
}
```

---

## 🎓 Practice Questions & Answers

### **Q1: What is a composable function?**
**A**: A function that describes a piece of UI. Uses `@Composable` annotation and is reusable.

### **Q2: How do you manage state in Compose?**
**A**: Use `remember { mutableStateOf(...) }` to create mutable state.

### **Q3: What's the difference between Column and Row?**
**A**: Column stacks items vertically, Row stacks them horizontally.

### **Q4: When should I use LazyColumn?**
**A**: For long lists. It only renders visible items, making it memory-efficient.

### **Q5: What are modifiers?**
**A**: Functions that modify how a composable looks and behaves (size, padding, color, etc).

---

## 💡 Key Takeaways

1. ✅ Compose uses declarative programming - describe what UI should look like
2. ✅ Composables are reusable functions that return UI
3. ✅ Use `remember` to manage state
4. ✅ When state changes, UI automatically re-renders
5. ✅ Modifiers control styling and positioning
6. ✅ LazyColumn for efficient long lists

---

## 🏋️ Hands-On Exercise

Create a Compose app with:
1. A form with name and email fields
2. A submit button
3. Display submitted data in a list below
4. Use state to manage form inputs
5. Make the list items reusable composables

---

**Next: [Module 3.2 - Layouts & Modifiers](11_COMPOSE_LAYOUTS.md)**

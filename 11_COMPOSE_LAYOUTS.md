# Module 3.2: Jetpack Compose Layouts & Modifiers - Complete Guide

## 🎨 Layout Composables in Compose

### **Column - Vertical Stack**
```kotlin
Column(
    modifier = Modifier
        .fillMaxWidth()
        .padding(16.dp),
    verticalArrangement = Arrangement.Center,
    horizontalAlignment = Alignment.CenterHorizontally
) {
    Text("First item")
    Text("Second item")
    Text("Third item")
}
```

### **Row - Horizontal Stack**
```kotlin
Row(
    modifier = Modifier
        .fillMaxWidth()
        .height(100.dp),
    horizontalArrangement = Arrangement.SpaceEvenly,
    verticalAlignment = Alignment.CenterVertically
) {
    Button(onClick = {}) { Text("Left") }
    Button(onClick = {}) { Text("Center") }
    Button(onClick = {}) { Text("Right") }
}
```

### **Box - Overlapping Stack**
```kotlin
Box(
    modifier = Modifier
        .size(200.dp)
        .background(Color.Blue)
) {
    Text("Background", modifier = Modifier.align(Alignment.TopStart))
    Button(onClick = {}, modifier = Modifier.align(Alignment.Center)) {
        Text("Center Button")
    }
}
```

### **Spacer - Add Space**
```kotlin
Column {
    Text("Top")
    Spacer(modifier = Modifier.height(16.dp))
    Text("Bottom")
}
```

---

## 🎪 Modifier Deep Dive

Modifiers are chainable functions that add behavior/appearance to composables.

### **Size Modifiers**
```kotlin
Text("Text", modifier = Modifier
    .width(200.dp)
    .height(50.dp)
)

Text("Text", modifier = Modifier.size(100.dp))

Text("Text", modifier = Modifier
    .fillMaxWidth()       // Fill parent width
    .fillMaxHeight()      // Fill parent height
    .fillMaxSize()        // Fill both
)

Text("Text", modifier = Modifier
    .wrapContentWidth()
    .wrapContentHeight()
)
```

### **Padding & Margin**
```kotlin
// Padding (inside)
Text("Text", modifier = Modifier.padding(16.dp))
Text("Text", modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp))

// Offset (outside margin)
Text("Text", modifier = Modifier.offset(x = 10.dp, y = 20.dp))
```

### **Background & Border**
```kotlin
Text("Text", modifier = Modifier
    .background(Color.Blue, shape = RoundedCornerShape(8.dp))
    .padding(16.dp)
)

Text("Text", modifier = Modifier.border(
    width = 2.dp,
    color = Color.Red,
    shape = RoundedCornerShape(8.dp)
))
```

### **Clip & Shadow**
```kotlin
Image(
    painter = painterResource(R.drawable.image),
    contentDescription = "Image",
    modifier = Modifier.clip(CircleShape)
)

Card(modifier = Modifier.shadow(elevation = 8.dp)) {
    Text("Card content")
}
```

### **Click & Interaction**
```kotlin
Text("Clickable Text", modifier = Modifier.clickable {
    println("Text clicked!")
})

Button(
    onClick = { /* Handle click */ },
    modifier = Modifier
        .size(100.dp)
        .clip(CircleShape)
) {
    Text("Circular")
}
```

---

## 🌈 Color Schemes in Compose

### **Material Colors**
```kotlin
// Light theme
val lightColors = lightColorScheme(
    primary = Color(0xFF6200EE),
    secondary = Color(0xFF03DAC6),
    tertiary = Color(0xFF018786),
    background = Color.White,
    surface = Color.White,
    onPrimary = Color.White,
    onSecondary = Color.Black,
    onBackground = Color.Black,
    onSurface = Color.Black
)

// Dark theme
val darkColors = darkColorScheme(
    primary = Color(0xFFBB86FC),
    secondary = Color(0xFF03DAC6),
    tertiary = Color(0xFF03DAC6),
    background = Color(0xFF121212),
    surface = Color(0xFF1F1F1F),
    onPrimary = Color.Black,
    onSecondary = Color.Black,
    onBackground = Color.White,
    onSurface = Color.White
)

// Use in theme
MaterialTheme(colorScheme = lightColors) {
    // Your app
}
```

### **Using Theme Colors**
```kotlin
Text("Primary color", color = MaterialTheme.colorScheme.primary)

Box(modifier = Modifier.background(MaterialTheme.colorScheme.surface)) {
    Text("On surface", color = MaterialTheme.colorScheme.onSurface)
}
```

---

## 🎬 Animations in Compose

### **Simple State Animation**
```kotlin
var isExpanded by remember { mutableStateOf(false) }

val size by animateDpAsState(
    targetValue = if (isExpanded) 200.dp else 100.dp
)

Box(
    modifier = Modifier
        .size(size)
        .background(Color.Blue)
        .clickable { isExpanded = !isExpanded }
)
```

### **Transition Animation**
```kotlin
var isVisible by remember { mutableStateOf(true) }

AnimatedVisibility(
    visible = isVisible,
    enter = slideInHorizontally(),
    exit = slideOutHorizontally()
) {
    Box(modifier = Modifier
        .size(100.dp)
        .background(Color.Red)
    )
}
```

---

## 📱 Real UI Examples

### **Card Component**
```kotlin
Card(
    modifier = Modifier
        .fillMaxWidth()
        .padding(16.dp),
    elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text("Card Title", style = MaterialTheme.typography.headlineSmall)
        Spacer(modifier = Modifier.height(8.dp))
        Text("Card content description", style = MaterialTheme.typography.bodyMedium)
    }
}
```

### **Button Variants**
```kotlin
// Primary Button
Button(onClick = { }) {
    Text("Primary")
}

// Outlined Button
OutlinedButton(onClick = { }) {
    Text("Outlined")
}

// Text Button
TextButton(onClick = { }) {
    Text("Text Button")
}

// FAB (Floating Action Button)
FloatingActionButton(onClick = { }) {
    Icon(Icons.Filled.Add, "Add")
}
```

### **Form Fields**
```kotlin
var emailText by remember { mutableStateOf("") }
var passwordText by remember { mutableStateOf("") }

TextField(
    value = emailText,
    onValueChange = { emailText = it },
    label = { Text("Email") },
    modifier = Modifier.fillMaxWidth()
)

TextField(
    value = passwordText,
    onValueChange = { passwordText = it },
    label = { Text("Password") },
    visualTransformation = PasswordVisualTransformation(),
    modifier = Modifier.fillMaxWidth()
)
```

---

## ✅ Practice Questions

1. What's the difference between Column and Row?
2. What does Modifier.fillMaxSize() do?
3. How do you add padding with Modifier?
4. What's the purpose of Spacer?
5. How do you access theme colors in Compose?

# Module 1.1: Kotlin Basics - Zero to Hero
## "Spoon-Feeding" Level Introduction to Kotlin

---

## 📖 What is Kotlin?

Think of Kotlin as an **upgraded version of Java**. It's like comparing a modern smartphone to a landline phone - they both make calls, but one is much easier to use!

**Key Facts**:
- Created by JetBrains (the company behind Android Studio)
- Runs on the Java Virtual Machine (JVM)
- Used for Android development (officially recommended by Google)
- More concise and safe than Java

---

## 🎯 Why Learn Kotlin?

| Feature | Java | Kotlin |
|---------|------|--------|
| Null Safety | Manual checks | Built-in protection |
| Code Length | Verbose | Concise |
| Learning Curve | Steep | Gentle |
| Android Support | Yes | Official Standard |
| Compile Errors | Runtime errors possible | Compile-time safety |

---

## 1️⃣ Variables & Data Types

### **Basic Concept**: Variables are containers that hold values

**Think of it like this**: A variable is like a box. You label it with a name and put something inside.

### **Declaration Syntax**
```kotlin
// Immutable (cannot be changed after creation)
val variableName: DataType = value

// Mutable (can be changed)
var variableName: DataType = value
```

### **⭐ Key Difference: `val` vs `var`**

```kotlin
// val = Permanent (like writing in ink)
val name = "Android"
name = "iOS"  // ❌ ERROR! Cannot change

// var = Changeable (like writing in pencil)
var age = 25
age = 26  // ✅ OK! Can change
```

**Rule**: Always use `val` by default, use `var` only when you need to change the value.

### **Data Types in Kotlin**

```kotlin
// Numbers
val integer: Int = 42
val longNumber: Long = 9999999999L
val floatingPoint: Float = 3.14f
val decimal: Double = 2.718

// Text
val text: String = "Hello, Android!"
val singleChar: Char = 'A'

// Boolean (True/False)
val isLearning: Boolean = true

// Type Inference (Kotlin figures out the type automatically)
val greeting = "Hello"  // Kotlin knows this is String
val count = 10          // Kotlin knows this is Int
```

### **Real-World Example: Mobile App**
```kotlin
// A user registration scenario
val userId = 101                    // ID never changes
val userEmail = "user@email.com"   // Email is fixed after signup
var userName = "John Doe"          // Name might be updated
var userAge = 25                   // Age changes every year
val isVerified = true              // Account status
```

---

## 2️⃣ Strings: Working with Text

### **String Templates (Embedding Variables in Text)**

```kotlin
val name = "Android"
val version = 14

// ❌ Old way (verbose)
val message = "Welcome to " + name + " version " + version

// ✅ Modern way (String Template)
val message = "Welcome to $name version $version"

// ✅ For complex expressions, use ${}
val message2 = "Next year I'll be ${25 + 1} years old"
```

### **String Operations**

```kotlin
val text = "KOTLIN"

text.length             // Returns: 6
text.lowercase()        // Returns: "kotlin"
text.uppercase()        // Returns: "KOTLIN"
text.contains("TL")     // Returns: true
text.startsWith("KOT")  // Returns: true
text.replace("K", "C")  // Returns: "COTLIN"
text.substring(0, 3)    // Returns: "KOT" (characters 0-2)
```

### **Practical Example: Building a Welcome Message**
```kotlin
val firstName = "Alice"
val lastName = "Developer"
val appVersion = "2.5"

val welcomeMessage = "Hello, $firstName $lastName! Welcome to MyApp v$appVersion"
//Output: "Hello, Alice Developer! Welcome to MyApp v2.5"
```

---

## 3️⃣ Collections: Storing Multiple Values

### **Arrays (Fixed Size)**

```kotlin
// Declaration
val numbers: IntArray = intArrayOf(1, 2, 3, 4, 5)

// Access elements (index starts at 0)
numbers[0]   // First element: 1
numbers[2]   // Third element: 3
numbers.size // Total elements: 5
```

### **Lists (Dynamic, Immutable)**

```kotlin
// Immutable list - cannot add/remove items
val fruits = listOf("Apple", "Banana", "Orange")
fruits[0]           // "Apple"
fruits.size         // 3
fruits.contains("Apple")  // true

// Can create from array
val numbers = listOf(1, 2, 3, 4, 5)
```

### **Mutable Lists (Can Add/Remove)**

```kotlin
// Can add and remove items
val shoppingList = mutableListOf("Milk", "Bread")
shoppingList.add("Eggs")
shoppingList.remove("Milk")
// Result: ["Bread", "Eggs"]

shoppingList[0]  // "Bread"
```

### **Sets (No Duplicates)**

```kotlin
val coupons = setOf("SAVE10", "SAVE10", "SAVE20")
// Result: ["SAVE10", "SAVE20"] (duplicate removed automatically)

coupons.size  // 2
```

### **Maps (Key-Value Pairs)**

```kotlin
// Like a dictionary or phone book
val userProfile = mapOf(
    "name" to "John",
    "age" to 25,
    "email" to "john@email.com"
)

// Access by key
userProfile["name"]   // "John"
userProfile["age"]    // 25

// Mutable version
val settings = mutableMapOf<String, String>()
settings["theme"] = "dark"
settings["language"] = "English"
```

### **Real-World Example: Shopping App**
```kotlin
// App uses different collections for different purposes

val productIds = intArrayOf(101, 102, 103)          // Fixed inventory IDs

val cartItems = mutableListOf("Shirt", "Pants")     // Items can be added/removed
cartItems.add("Shoes")

val uniqueCategories = setOf("Electronics", "Clothing", "Books")  // No duplicates

val productDetails = mapOf(
    "shirt" to "Blue Cotton Shirt",
    "price" to 29.99,
    "inStock" to true
)
```

---

## 4️⃣ Conditional Statements (If/Else)

### **Basic If Statement**

```kotlin
val age = 16

if (age >= 18) {
    println("You can vote")
} else {
    println("You are too young to vote")
}
// Output: "You are too young to vote"
```

### **Multiple Conditions**

```kotlin
val score = 75

when {
    score >= 90 -> println("Grade: A")
    score >= 80 -> println("Grade: B")
    score >= 70 -> println("Grade: C")
    else -> println("Grade: F")
}
// Output: "Grade: C"
```

### **When Expression (More Elegant)**

```kotlin
val day = 3

val dayName = when (day) {
    1 -> "Monday"
    2 -> "Tuesday"
    3 -> "Wednesday"
    4 -> "Thursday"
    5 -> "Friday"
    6, 7 -> "Weekend"  // Multiple values for same result
    else -> "Invalid day"
}
// dayName = "Wednesday"
```

### **Real-World Example: User Validation**
```kotlin
val userAge = 20
val hasDriverLicense = false

if (userAge >= 18 && hasDriverLicense) {
    println("Can apply for car insurance")
} else if (userAge >= 18) {
    println("Please get a driver's license first")
} else {
    println("Must be 18 or older")
}
```

---

## 5️⃣ Loops: Repeating Code

### **For Loop (Iterate Over Collections)**

```kotlin
// Loop through a list
val fruits = listOf("Apple", "Banana", "Orange")

for (fruit in fruits) {
    println(fruit)
}
// Output:
// Apple
// Banana
// Orange

// Loop with range
for (i in 1..5) {
    println(i)  // Prints: 1 2 3 4 5
}

// Loop with range and step
for (i in 1..10 step 2) {
    println(i)  // Prints: 1 3 5 7 9
}
```

### **While Loop (Repeat While Condition is True)**

```kotlin
var count = 0

while (count < 3) {
    println("Count: $count")
    count++
}
// Output:
// Count: 0
// Count: 1
// Count: 2
```

### **Real-World Example: Processing Orders**
```kotlin
val orders = listOf("Order1", "Order2", "Order3", "Order4")

for (order in orders) {
    println("Processing $order...")
}

// Or with index
for ((index, order) in orders.withIndex()) {
    println("Processing order ${index + 1}: $order")
}
```

---

## 6️⃣ Functions: Reusable Code Blocks

### **Basic Function**

```kotlin
// Define a function
fun greet(name: String) {
    println("Hello, $name!")
}

// Call the function
greet("Alice")    // Output: "Hello, Alice!"
greet("Bob")      // Output: "Hello, Bob!"
```

### **Function with Return Value**

```kotlin
fun add(a: Int, b: Int): Int {
    return a + b
}

val result = add(5, 3)  // result = 8
println(result)         // Output: 8

// Shorter version (single expression)
fun multiply(a: Int, b: Int) = a * b

val product = multiply(4, 5)  // product = 20
```

### **Function with Default Parameters**

```kotlin
fun displayMessage(message: String, priority: String = "Normal") {
    println("[$priority] $message")
}

displayMessage("First task")              // [Normal] First task
displayMessage("Urgent task", "High")     // [High] Urgent task
```

### **Function with Multiple Return Values**

```kotlin
// Using Pair
fun calculateStats(numbers: List<Int>): Pair<Int, Int> {
    return Pair(numbers.sum(), numbers.size)
}

val (total, count) = calculateStats(listOf(10, 20, 30))
// total = 60, count = 3

// Or using Data Class (better)
data class Stats(val sum: Int, val count: Int)

fun calculateStats2(numbers: List<Int>): Stats {
    return Stats(numbers.sum(), numbers.size)
}

val stats = calculateStats2(listOf(10, 20, 30))
println("Sum: ${stats.sum}, Count: ${stats.count}")
```

### **Real-World Example: Calculator App**
```kotlin
fun calculateTotal(price: Double, quantity: Int, discount: Double = 0.0): Double {
    val subtotal = price * quantity
    return subtotal - (subtotal * discount / 100)
}

val bill1 = calculateTotal(100.0, 2)              // 200.0
val bill2 = calculateTotal(100.0, 2, 10.0)       // 180.0 (10% off)
```

---

## 7️⃣ Null Safety: Kotlin's Superpower

### **The Problem with Null**

In many languages, `null` can cause crashes:
```kotlin
val name: String = null  // ❌ ERROR! Kotlin prevents this
val name = "Alice"
println(name.length)     // Safe! 5
```

### **Nullable Types**

```kotlin
// Explicitly nullable
val age: Int? = null     // OK!
val name: String? = null // OK!

// Non-null assertion (when you're sure it's not null)
val age: Int? = 25
println(age!! + 5)       // 30 (use !! carefully!)

// Safe call operator
val name: String? = "Android"
val length = name?.length   // 7 (if name is not null)

// Elvis operator (use default if null)
val city: String? = null
val displayCity = city ?: "Unknown"  // "Unknown"
```

### **Real-World Example: API Response**
```kotlin
// When you get data from a server
data class User(
    val id: Int,
    val name: String,
    val phone: String?  // Not all users have phone
)

val user = User(1, "John", null)
val displayPhone = user.phone ?: "No phone provided"
println(displayPhone)  // "No phone provided"
```

---

## 8️⃣ Classes: Building Objects

### **Basic Class**

```kotlin
class Person {
    var name = "Unknown"
    var age = 0
}

val person = Person()
person.name = "Alice"
person.age = 25
println("${person.name} is ${person.age} years old")
// Output: "Alice is 25 years old"
```

### **Constructor**

```kotlin
// Primary constructor (simple)
class Dog(val name: String, val breed: String)

val dog = Dog("Buddy", "Golden Retriever")
println(dog.name)   // "Buddy"

// Constructor with default values
class Cat(
    val name: String = "Whiskers",
    val age: Int = 1
)

val cat1 = Cat()                    // Uses defaults
val cat2 = Cat("Felix", 3)          // Custom values
```

### **Methods**

```kotlin
class Calculator {
    fun add(a: Int, b: Int): Int {
        return a + b
    }
    
    fun subtract(a: Int, b: Int) = a - b
}

val calc = Calculator()
println(calc.add(5, 3))       // 8
println(calc.subtract(10, 3)) // 7
```

### **Properties with Getters/Setters**

```kotlin
class Rectangle(val width: Double, val height: Double) {
    val area: Double
        get() = width * height  // Computed property
    
    val perimeter: Double
        get() = 2 * (width + height)
}

val rect = Rectangle(5.0, 3.0)
println(rect.area)      // 15.0
println(rect.perimeter) // 16.0
```

### **Real-World Example: User Profile**
```kotlin
class UserProfile(
    val userId: Int,
    var username: String,
    var email: String,
    var isVerified: Boolean = false
) {
    fun displayInfo() {
        val status = if (isVerified) "Verified" else "Unverified"
        println("User: $username | Email: $email | Status: $status")
    }
}

val user = UserProfile(101, "alice_dev", "alice@email.com")
user.displayInfo()
// Output: "User: alice_dev | Email: alice@email.com | Status: Unverified"

user.isVerified = true
user.displayInfo()
// Output: "User: alice_dev | Email: alice@email.com | Status: Verified"
```

---

## 🎓 Practice Questions & Answers

### **Q1: What's the difference between `val` and `var`?**
**A**: `val` is immutable (cannot change), `var` is mutable (can change). Use `val` by default.

### **Q2: What is a nullable type?**
**A**: A type that can hold `null` value. Declared with `?` like `String?` or `Int?`.

### **Q3: What does the Elvis operator `?:` do?**
**A**: Provides a default value if the left side is null. `val city = userCity ?: "New York"`

### **Q4: What's the difference between `for` and `while` loops?**
**A**: `for` iterates over collections, `while` repeats while a condition is true.

### **Q5: What is a class?**
**A**: A blueprint for creating objects. It defines properties (data) and methods (functions).

---

## 💡 Key Takeaways

1. ✅ Use `val` for immutable, `var` for mutable variables
2. ✅ Kotlin is null-safe by default
3. ✅ String templates make code cleaner
4. ✅ Functions are reusable code blocks
5. ✅ Collections store multiple values efficiently
6. ✅ Classes create blueprints for objects

---

## 🏋️ Hands-On Exercise

Create a Kotlin program that:
1. Declares a data class `Book` with `title`, `author`, `price`
2. Creates a mutable list of 3 books
3. Calculates and prints the total cost
4. Finds the cheapest book
5. Displays all books with a loop

```kotlin
// Your solution here
```

---

**Next: [Module 1.2 - OOP in Kotlin](02_KOTLIN_OOP.md)**

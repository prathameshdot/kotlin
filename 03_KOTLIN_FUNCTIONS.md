# Module 1.3: Functions & Lambdas in Kotlin
## Mastering Functional Programming

---

## 📖 What are Functions?

Functions are reusable blocks of code that perform specific tasks. Lambdas are anonymous functions - functions without names that you can pass around like values.

---

## 1️⃣ Function Fundamentals

### **Basic Function Declaration**

```kotlin
fun greet(name: String): String {
    return "Hello, $name!"
}

val message = greet("Alice")
println(message)  // "Hello, Alice!"
```

### **Single Expression Functions**

```kotlin
fun add(a: Int, b: Int) = a + b

println(add(5, 3))  // 8
```

### **Functions with Default Parameters**

```kotlin
fun createUser(
    username: String,
    email: String,
    isAdmin: Boolean = false,
    age: Int = 18
): String {
    return "User: $username, Admin: $isAdmin"
}

createUser("alice_dev", "alice@email.com")
createUser("bob_admin", "bob@email.com", true)
createUser("charlie", "charlie@email.com", age = 25)
```

### **Named Arguments (Make Code Clearer)**

```kotlin
fun buildHouse(
    color: String,
    rooms: Int,
    hasGarage: Boolean,
    hasPool: Boolean
) {
    println("House: $color, $rooms rooms, Garage: $hasGarage, Pool: $hasPool")
}

// Without named arguments - confusing!
buildHouse("Blue", 4, true, false)

// With named arguments - crystal clear!
buildHouse(
    color = "Blue",
    rooms = 4,
    hasGarage = true,
    hasPool = false
)
```

### **Variable Number of Arguments (vararg)**

```kotlin
fun printNumbers(vararg numbers: Int) {
    for (num in numbers) {
        println(num)
    }
}

printNumbers(1)
printNumbers(1, 2, 3, 4, 5)

// Spread operator (*) to pass array as vararg
val arr = intArrayOf(10, 20, 30)
printNumbers(*arr)

// Real example
fun makeShoppingList(vararg items: String) {
    println("Shopping list:")
    items.forEachIndexed { index, item ->
        println("${index + 1}. $item")
    }
}

makeShoppingList("Apple", "Milk", "Bread", "Eggs")
```

---

## 2️⃣ Lambdas: Anonymous Functions

### **What is a Lambda?**

A lambda is an unnamed function that you can pass around like a value.

```kotlin
// Regular function
fun multiply(a: Int, b: Int): Int = a * b

// Same thing as lambda
val multiplyLambda: (Int, Int) -> Int = { a, b -> a * b }

println(multiply(5, 3))              // 15
println(multiplyLambda(5, 3))        // 15
```

### **Lambda Syntax**

```kotlin
// Type 1: Complete with type annotation
val add: (Int, Int) -> Int = { a, b -> a + b }

// Type 2: Type inference (simpler)
val subtract = { a: Int, b: Int -> a - b }

// Type 3: Single parameter (implicit)
val square = { x: Int -> x * x }
val squareSimple = { x: Int -> x * x }

// Type 4: Even simpler for single parameter
val double: (Int) -> Int = { it * 2 }  // 'it' is implicit parameter

println(add(10, 5))           // 15
println(square(4))            // 16
println(double(5))            // 10
```

### **Real-World Example: Filtering Numbers**

```kotlin
val numbers = listOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

// Lambda to filter even numbers
val evenNumbers = numbers.filter { it % 2 == 0 }
println(evenNumbers)  // [2, 4, 6, 8, 10]

// Lambda to transform numbers
val doubled = numbers.map { it * 2 }
println(doubled)  // [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

// Lambda to find first odd number
val firstOdd = numbers.find { it % 2 != 0 }
println(firstOdd)  // 1
```

---

## 3️⃣ Higher-Order Functions: Functions That Take Functions

```kotlin
// Function that takes a lambda as parameter
fun operate(a: Int, b: Int, operation: (Int, Int) -> Int): Int {
    return operation(a, b)
}

val result1 = operate(5, 3, { x, y -> x + y })      // 8
val result2 = operate(5, 3, { x, y -> x * y })      // 15
val result3 = operate(5, 3, { x, y -> x - y })      // 2

// Cleaner syntax when lambda is last parameter
val result4 = operate(5, 3) { x, y -> x + y }  // 8

// Function that returns a lambda
fun getMultiplier(factor: Int): (Int) -> Int {
    return { value -> value * factor }
}

val double = getMultiplier(2)
val triple = getMultiplier(3)

println(double(5))  // 10
println(triple(5))  // 15
```

### **Real-World Example: Button Click Handler**

```kotlin
// Simulating Android button click
fun Button(label: String, onClick: (String) -> Unit) {
    println("Button: $label (clickable)")
    // When clicked:
    onClick(label)
}

// Usage
Button("Submit") { buttonLabel ->
    println("User clicked: $buttonLabel")
}

Button("Cancel") { buttonLabel ->
    println("User clicked: $buttonLabel")
}
```

---

## 4️⃣ Common Collection Operations

### **map - Transform Elements**

```kotlin
val numbers = listOf(1, 2, 3, 4, 5)

// Transform each number
val doubled = numbers.map { it * 2 }
println(doubled)  // [2, 4, 6, 8, 10]

// Transform to different type
val asStrings = numbers.map { "Number: $it" }
println(asStrings)  // [Number: 1, Number: 2, ...]

// Real example: Convert user IDs to user objects
data class User(val id: Int, val name: String)
val userIds = listOf(1, 2, 3)
val users = userIds.map { User(it, "User $it") }
```

### **filter - Keep Only Matching Elements**

```kotlin
val numbers = listOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

val evenNumbers = numbers.filter { it % 2 == 0 }
println(evenNumbers)  // [2, 4, 6, 8, 10]

// Real example: Get active users
data class UserStatus(val name: String, val isActive: Boolean)
val users = listOf(
    UserStatus("Alice", true),
    UserStatus("Bob", false),
    UserStatus("Charlie", true)
)
val activeUsers = users.filter { it.isActive }
```

### **find/firstOrNull - Find First Match**

```kotlin
val numbers = listOf(1, 2, 3, 4, 5)

val firstEven = numbers.find { it % 2 == 0 }
println(firstEven)  // 2

val firstGreaterThan10 = numbers.find { it > 10 }
println(firstGreaterThan10)  // null

val firstEvenOrZero = numbers.firstOrNull { it % 2 == 0 } ?: 0
println(firstEvenOrZero)  // 2
```

### **fold/reduce - Aggregate Values**

```kotlin
val numbers = listOf(1, 2, 3, 4, 5)

// fold: aggregate with initial value
val sum = numbers.fold(0) { accumulator, value ->
    accumulator + value
}
println(sum)  // 15

// reduce: aggregate without initial value
val product = numbers.reduce { accumulator, value ->
    accumulator * value
}
println(product)  // 120 (1*2*3*4*5)

// Real example: Calculate total cart price
val items = listOf(
    10.0,  // Item 1
    20.0,  // Item 2
    15.0   // Item 3
)
val totalPrice = items.fold(0.0) { total, price -> total + price }
println(totalPrice)  // 45.0
```

### **forEach - Iterate**

```kotlin
val fruits = listOf("Apple", "Banana", "Orange")

fruits.forEach { fruit ->
    println("I like $fruit")
}

// With index
fruits.forEachIndexed { index, fruit ->
    println("${index + 1}. $fruit")
}
```

### **groupBy - Group Elements**

```kotlin
val numbers = listOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

val grouped = numbers.groupBy { it % 2 == 0 }
println(grouped)
// {false=[1, 3, 5, 7, 9], true=[2, 4, 6, 8, 10]}

// Real example: Group users by status
data class User(val name: String, val status: String)
val users = listOf(
    User("Alice", "Active"),
    User("Bob", "Inactive"),
    User("Charlie", "Active")
)
val grouped = users.groupBy { it.status }
// {Active=[Alice, Charlie], Inactive=[Bob]}
```

---

## 5️⃣ Chaining Operations

```kotlin
val numbers = listOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

// Chain multiple operations
val result = numbers
    .filter { it % 2 == 0 }        // Keep even: [2, 4, 6, 8, 10]
    .map { it * 2 }                // Double: [4, 8, 12, 16, 20]
    .filter { it > 10 }            // Keep > 10: [12, 16, 20]
    .fold(0) { acc, value -> acc + value }  // Sum: 48

println(result)  // 48

// Real example: Process shopping cart
data class Product(val name: String, val price: Double, val quantity: Int)

val cart = listOf(
    Product("Laptop", 1000.0, 1),
    Product("Mouse", 25.0, 2),
    Product("Keyboard", 75.0, 1)
)

val totalCost = cart
    .map { it.price * it.quantity }  // Individual totals
    .fold(0.0) { total, cost -> total + cost }  // Sum

println(totalCost)  // 1125.0
```

---

## 6️⃣ Scope Functions: with, let, apply, run

### **let - Use Non-Null Value**

```kotlin
val name: String? = "Alice"

// Safe way to use nullable value
name?.let { nonNullName ->
    println("Name is: $nonNullName")  // This won't run if name is null
}

// Real example: API response
data class User(val id: Int, val name: String)
var user: User? = null

user = User(1, "Alice")

user?.let { u ->
    println("Displaying user: ${u.name}")
    // Perform more operations
}
```

### **apply - Configure Object**

```kotlin
class Person {
    var name = ""
    var age = 0
    var email = ""
}

// Without apply
val person1 = Person()
person1.name = "Alice"
person1.age = 25
person1.email = "alice@email.com"

// With apply (cleaner)
val person2 = Person().apply {
    name = "Alice"
    age = 25
    email = "alice@email.com"
}

// Real example: Android's Intent configuration
// val intent = Intent().apply {
//     action = Intent.ACTION_SEND
//     type = "text/plain"
//     putExtra(Intent.EXTRA_TEXT, "Hello!")
// }
```

### **run - Execute and Return Value**

```kotlin
val result = run {
    val x = 10
    val y = 20
    x + y
}
println(result)  // 30

// Real example: Complex calculation
val calculation = run {
    val basePrice = 100.0
    val taxRate = 0.1
    val discount = 0.05
    
    (basePrice + (basePrice * taxRate)) * (1 - discount)
}
println(calculation)  // 104.95
```

### **with - Call Methods on Object**

```kotlin
class Car {
    var brand = ""
    var color = ""
    fun describe() = "A $color $brand"
}

val myCar = Car()

with(myCar) {
    brand = "Toyota"
    color = "Blue"
    println(describe())  // A Blue Toyota
}
```

---

## 🎓 Practice Questions & Answers

### **Q1: What's the difference between a lambda and a regular function?**
**A**: Lambdas are anonymous functions that can be passed as values. Regular functions are named and defined separately.

### **Q2: What does `it` refer to in a lambda?**
**A**: `it` is the implicit name for a lambda's single parameter. `{ it * 2 }` is short for `{ x -> x * 2 }`.

### **Q3: What is a higher-order function?**
**A**: A function that takes another function as a parameter or returns a function.

### **Q4: When should I use `map` vs `filter`?**
**A**: Use `map` to transform elements, `filter` to keep only matching elements.

### **Q5: What's the purpose of scope functions like `let` and `apply`?**
**A**: They let you call methods and access properties within a scope, with `it` (let) or `this` (apply) referring to the object.

---

## 💡 Key Takeaways

1. ✅ Lambdas are unnamed functions you can pass around
2. ✅ Higher-order functions take/return functions
3. ✅ Collection operations (map, filter, fold) are powerful tools
4. ✅ Chaining operations creates elegant, readable code
5. ✅ Scope functions provide convenient ways to work with objects
6. ✅ Use descriptive names for lambda parameters when they're not obvious

---

## 🏋️ Hands-On Exercise

Write a Kotlin program that:

1. Create a list of products with prices
2. Use `filter` to get products under $50
3. Use `map` to apply 10% discount
4. Use `forEach` to print each product
5. Use `fold` to calculate total price

```kotlin
// Your solution here
```

---

**Next: [Module 1.4 - Collections & Sequences](04_KOTLIN_COLLECTIONS.md)**

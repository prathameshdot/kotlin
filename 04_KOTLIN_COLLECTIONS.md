# Module 1.4: Kotlin Collections & Sequences

## 📚 Complete Guide to Collections in Kotlin

Collections are fundamental data structures for storing multiple values. Kotlin provides several types of collections, each optimized for different use cases.

---

## 🎯 Collections Overview

```
Collections
├── Lists (Ordered, Mutable/Immutable)
├── Sets (Unique, Unordered)
├── Maps (Key-Value pairs)
└── Sequences (Lazy evaluation)
```

---

## 📋 Lists - Ordered Collections

### **Immutable List (val)**
```kotlin
// Create immutable lists
val fruits = listOf("Apple", "Banana", "Orange")
val numbers = listOf(1, 2, 3, 4, 5)
val mixed = listOf("text", 123, true)

// Access elements
println(fruits[0])              // Apple
println(fruits.get(1))          // Banana
println(fruits.first())         // Apple
println(fruits.last())          // Orange
println(fruits.size)            // 3

// Check if contains
println(fruits.contains("Apple"))  // true
println("Mango" in fruits)         // false

// Get index
println(fruits.indexOf("Banana"))  // 1
```

### **Mutable List (var)**
```kotlin
// Create mutable lists
val shoppingCart = mutableListOf<String>()
val topics = mutableListOf("Kotlin", "Android")

// Add elements
shoppingCart.add("Milk")
shoppingCart.add("Bread")
topics.add("Compose")

// Remove elements
shoppingCart.remove("Milk")
topics.removeAt(0)              // Remove by index

// Modify elements
topics[0] = "Advanced Kotlin"
topics.set(1, "Jetpack")

// Get elements
println(topics[0])              // Advanced Kotlin

// Clear all
topics.clear()

// Add multiple
shoppingCart.addAll(listOf("Eggs", "Butter"))
```

### **List Operations**
```kotlin
val numbers = listOf(1, 2, 3, 4, 5)

// Iterations
for (num in numbers) {
    println(num)
}

// With index
for ((index, value) in numbers.withIndex()) {
    println("$index: $value")
}

// Functional operations
println(numbers.sum())          // 15
println(numbers.average())      // 3.0
println(numbers.min())          // 1
println(numbers.max())          // 5
println(numbers.sorted())       // [1,2,3,4,5]
println(numbers.reversed())     // [5,4,3,2,1]

// Chunk
numbers.chunked(2).forEach { println(it) }  // [1,2], [3,4], [5]

// Take and drop
println(numbers.take(3))        // [1,2,3]
println(numbers.takeLast(2))    // [4,5]
println(numbers.drop(2))        // [3,4,5]
println(numbers.dropLast(1))    // [1,2,3,4]
```

---

## 🏷️ Sets - Unique Collections

### **Immutable Set**
```kotlin
// Create immutable sets
val colors = setOf("Red", "Green", "Blue")
val uniqueNumbers = setOf(1, 2, 3, 1, 2)  // [1,2,3] - duplicates removed

// Access (no index)
println(colors.size)            // 3
println(colors.contains("Red")) // true

// Iteration
for (color in colors) {
    println(color)
}

// Convert to list
val colorList = colors.toList()
```

### **Mutable Set**
```kotlin
val tags = mutableSetOf<String>()

// Add elements
tags.add("kotlin")
tags.add("android")
tags.add("compose")
tags.add("kotlin")              // Duplicate - not added

println(tags.size)              // 3

// Remove
tags.remove("android")

// Check membership
println("kotlin" in tags)       // true

// Clear
tags.clear()
```

### **Set Operations**
```kotlin
val set1 = setOf(1, 2, 3, 4)
val set2 = setOf(3, 4, 5, 6)

// Union (combine all)
println(set1.union(set2))       // [1,2,3,4,5,6]

// Intersection (common)
println(set1.intersect(set2))   // [3,4]

// Difference (in set1 but not set2)
println(set1.subtract(set2))    // [1,2]
```

---

## 🗺️ Maps - Key-Value Pairs

### **Immutable Map**
```kotlin
// Create immutable maps
val scores = mapOf("Alice" to 90, "Bob" to 85, "Carol" to 92)
val capitals = mapOf(
    "India" to "Delhi",
    "USA" to "Washington DC",
    "UK" to "London"
)

// Access by key
println(scores["Alice"])        // 90
println(scores.get("Bob"))      // 85
println(scores.getOrDefault("Dave", 0))  // 0

// Check if key/value exists
println(scores.containsKey("Alice"))      // true
println(scores.containsValue(90))         // true

// Get all keys and values
println(scores.keys)            // [Alice, Bob, Carol]
println(scores.values)          // [90, 85, 92]

// Iterate
for ((name, score) in scores) {
    println("$name: $score")
}

// Size
println(scores.size)            // 3
```

### **Mutable Map**
```kotlin
val userProfiles = mutableMapOf<String, Int>()

// Add/put
userProfiles["Alice"] = 25
userProfiles["Bob"] = 30
userProfiles.put("Carol", 28)

// Modify
userProfiles["Alice"] = 26

// Remove
userProfiles.remove("Bob")

// Clear
userProfiles.clear()

// Add all from another map
userProfiles.putAll(mapOf("David" to 35, "Eve" to 29))
```

### **Map Operations**
```kotlin
val employees = mapOf(
    "John" to 50000,
    "Sarah" to 60000,
    "Mike" to 55000
)

// Filter by value
val highEarners = employees.filter { it.value > 53000 }

// Filter by key
val namesWithJ = employees.filterKeys { it.startsWith("J") }

// Transform values
val bonuses = employees.mapValues { it.value * 0.1 }

// Transform to list of pairs
val pairs = employees.toList()

// Group map entries
val grouped = employees.entries.groupBy { it.value }
```

---

## 🔄 Sequences - Lazy Evaluation

Sequences are like lists but evaluate lazily (only when needed). Perfect for large datasets!

### **Create Sequences**
```kotlin
// From list
val listSequence = listOf(1, 2, 3, 4, 5).asSequence()

// Generate infinite
val infiniteSequence = generateSequence(1) { it + 1 }

// Sequence builder
val customSequence = sequence {
    yield(1)
    yield(2)
    yield(3)
}

// range
val rangeSequence = (1..1000).asSequence()
```

### **Lazy vs Eager Evaluation**
```kotlin
// EAGER - evaluates all at once (List)
val list = listOf(1, 2, 3, 4, 5)
val result1 = list
    .map { println("map: $it"); it * 2 }
    .filter { println("filter: $it"); it > 5 }
    .toList()
// Prints: map: 1-5, then filter: 2-10

// LAZY - evaluates only what's needed (Sequence)
val sequence = sequenceOf(1, 2, 3, 4, 5)
val result2 = sequence
    .map { println("map: $it"); it * 2 }
    .filter { println("filter: $it"); it > 5 }
    .toList()
// Prints: map: 1, filter: 2, map: 2, filter: 4, ... (only needed elements)
```

### **Performance: When to Use Sequences**

```kotlin
// GOOD for sequences: Large data with early termination
val largeList = (1..1_000_000).toList()
val first5Evens = largeList
    .asSequence()
    .filter { it % 2 == 0 }
    .take(5)
    .toList()

// NOT needed for small lists
val smallList = listOf(1, 2, 3)
smallList.filter { it > 1 }    // Just use list operations
```

---

## 🎯 Collection Transformation Operations

### **Map - Transform Each Element**
```kotlin
val numbers = listOf(1, 2, 3, 4, 5)

// Double each number
val doubled = numbers.map { it * 2 }  // [2, 4, 6, 8, 10]

// Convert to strings
val strings = numbers.map { "Number: $it" }

// Complex transformation
data class Product(val id: Int, val name: String)
val products = listOf(Product(1, "Laptop"), Product(2, "Phone"))
val names = products.map { it.name }  // ["Laptop", "Phone"]
```

### **Filter - Keep Only Matching**
```kotlin
val numbers = listOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

// Even numbers
val evens = numbers.filter { it % 2 == 0 }  // [2, 4, 6, 8, 10]

// Greater than 5
val large = numbers.filter { it > 5 }  // [6, 7, 8, 9, 10]

// Not empty
val texts = listOf("", "Hello", "", "World")
val nonEmpty = texts.filter { it.isNotEmpty() }  // ["Hello", "World"]
```

### **Fold & Reduce - Aggregate Values**
```kotlin
val numbers = listOf(1, 2, 3, 4, 5)

// Fold - provides initial value
val sumFold = numbers.fold(0) { acc, value -> acc + value }  // 15
val productFold = numbers.fold(1) { acc, value -> acc * value }  // 120

// Reduce - first element is initial
val sumReduce = numbers.reduce { acc, value -> acc + value }  // 15

// Build string with fold
val textList = listOf("Hello", "World", "Kotlin")
val sentence = textList.fold("") { acc, word -> if (acc.isEmpty()) word else "$acc $word" }
// "Hello World Kotlin"
```

### **GroupBy - Group Elements**
```kotlin
val words = listOf("apple", "apricot", "banana", "blueberry", "cherry")

// Group by first letter
val grouped = words.groupBy { it.first() }
// {a: [apple, apricot], b: [banana, blueberry], c: [cherry]}

// Group by length
data class Person(val name: String, val age: Int)
val people = listOf(
    Person("Alice", 25),
    Person("Bob", 30),
    Person("Carol", 25)
)
val byAge = people.groupBy { it.age }
// {25: [Alice, Carol], 30: [Bob]}
```

### **Chaining Operations**
```kotlin
val numbers = listOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

// Complex chain
val result = numbers
    .filter { it > 3 }              // [4, 5, 6, 7, 8, 9, 10]
    .map { it * 2 }                 // [8, 10, 12, 14, 16, 18, 20]
    .take(3)                        // [8, 10, 12]
    .sum()                          // 30

println(result)  // 30

// With data
data class Order(val id: Int, val amount: Double)
val orders = listOf(
    Order(1, 100.0),
    Order(2, 250.0),
    Order(3, 75.0),
    Order(4, 300.0)
)

val totalHighValue = orders
    .filter { it.amount > 100 }
    .map { it.amount }
    .sum()
// 550.0
```

---

## 🔍 Useful Collection Functions

### **Sorting**
```kotlin
val numbers = listOf(5, 2, 8, 1, 9, 3)

println(numbers.sorted())           // [1, 2, 3, 5, 8, 9]
println(numbers.sortedDescending()) // [9, 8, 5, 3, 2, 1]

// Sort objects by property
data class Student(val name: String, val grade: Int)
val students = listOf(
    Student("Alice", 85),
    Student("Bob", 92),
    Student("Carol", 78)
)

println(students.sortedBy { it.grade })
// [Carol(78), Alice(85), Bob(92)]
```

### **Find Operations**
```kotlin
val numbers = listOf(1, 2, 3, 4, 5)

println(numbers.find { it > 3 })        // 4 (first match)
println(numbers.findLast { it > 3 })    // 5 (last match)
println(numbers.any { it > 4 })         // true (at least one)
println(numbers.all { it > 0 })         // true (all match)
println(numbers.none { it < 0 })        // true (none match)
```

### **Distinct & Unique**
```kotlin
val numbers = listOf(1, 2, 2, 3, 3, 3, 4)

println(numbers.distinct())             // [1, 2, 3, 4]
println(numbers.distinctBy { it % 2 })  // [1, 2] - odd and even

// Remove duplicates but keep order
val list = listOf("a", "b", "a", "c", "b")
println(list.distinct())                // [a, b, c]
```

### **Partition - Split Into Two Lists**
```kotlin
val numbers = listOf(1, 2, 3, 4, 5, 6)

val (evens, odds) = numbers.partition { it % 2 == 0 }
println(evens)  // [2, 4, 6]
println(odds)   // [1, 3, 5]
```

---

## 📊 Real-World Examples

### **Shopping Cart**
```kotlin
data class Item(val name: String, val price: Double, val quantity: Int)

val cart = listOf(
    Item("Laptop", 1000.0, 1),
    Item("Mouse", 25.0, 2),
    Item("Keyboard", 75.0, 1)
)

// Total price
val total = cart
    .map { it.price * it.quantity }
    .sum()  // 1225.0

// Items over 100
val expensive = cart.filter { it.price > 100 }

// Item names
val names = cart.map { it.name }

// Grouped by price range
val grouped = cart.groupBy { 
    when {
        it.price < 50 -> "Cheap"
        it.price < 500 -> "Medium"
        else -> "Expensive"
    }
}
```

### **Data Processing**
```kotlin
data class Employee(val name: String, val department: String, val salary: Int)

val employees = listOf(
    Employee("Alice", "Engineering", 120000),
    Employee("Bob", "Sales", 80000),
    Employee("Carol", "Engineering", 110000),
    Employee("David", "HR", 75000),
    Employee("Eve", "Sales", 85000)
)

// Average salary by department
val byDept = employees.groupBy { it.department }
byDept.forEach { (dept, emps) ->
    val avg = emps.map { it.salary }.average()
    println("$dept: Average = $avg")
}

// Employees earning more than 100k
val highEarners = employees
    .filter { it.salary > 100000 }
    .sortedByDescending { it.salary }
    .map { it.name }
```

---

## ✅ Practice Questions

1. **What's the difference between a List and a Set?**
   - Answer: List maintains order and allows duplicates; Set has no order and no duplicates.

2. **When should you use Sequences instead of Lists?**
   - Answer: When working with large datasets or when you only need a subset of results (lazy evaluation).

3. **What does `map` do to a collection?**
   - Answer: Transforms each element using a function and returns a new collection with transformed elements.

4. **How do you find the sum of numbers > 5 in a list?**
   - Answer: `list.filter { it > 5 }.sum()`

5. **What's the difference between `fold` and `reduce`?**
   - Answer: `fold` takes an initial value; `reduce` uses the first element as initial value.

---

## 🎓 Summary

- **Lists**: Ordered, with index access - use `listOf()` and `mutableListOf()`
- **Sets**: Unique values only - use `setOf()` and `mutableSetOf()`
- **Maps**: Key-value pairs - use `mapOf()` and `mutableMapOf()`
- **Sequences**: Lazy evaluation - use `.asSequence()` or `sequence {}`
- **Operations**: `map`, `filter`, `fold`, `groupBy`, `sort` transform and manipulate data
- **Choose wisely**: Lists for most cases, Sets for unique values, Sequences for large datasets

# Module 1.2: OOP in Kotlin - Object-Oriented Programming
## Inheritance, Polymorphism, Encapsulation, Abstraction

---

## 📖 What is OOP?

OOP is a way of organizing code by creating **objects** that represent real-world things. Think of it like building with LEGO blocks - each block has a specific purpose and can combine with other blocks.

**4 Pillars of OOP**:
1. **Encapsulation** - Hide internal details
2. **Inheritance** - Reuse code from parent classes
3. **Polymorphism** - Use objects in different ways
4. **Abstraction** - Simplify complex systems

---

## 1️⃣ Encapsulation: Hiding Details

### **Visibility Modifiers (Controls Who Can Access)**

```kotlin
class BankAccount {
    private var balance = 1000      // Only this class can access
    protected var accountType = "Savings"  // This class + subclasses
    internal var branch = "Main Street"    // Package-level access
    var accountNumber = "12345"     // Anyone can access (public by default)
    
    private fun calculateInterest(): Double {
        return balance * 0.05  // Only internal use
    }
    
    public fun getBalance(): Double {
        return balance  // Public method to check balance
    }
}

val account = BankAccount()
println(account.getBalance())  // ✅ Can access public method
// println(account.balance)    // ❌ ERROR! Private property
```

### **Getters and Setters (Controlled Access)**

```kotlin
class Person {
    var age: Int = 0
        set(value) {
            if (value > 0) {
                field = value  // 'field' represents the actual value
            } else {
                println("Age must be positive!")
            }
        }
    
    val canVote: Boolean
        get() = age >= 18
}

val person = Person()
person.age = 25        // ✅ Calls setter
person.age = -5        // ❌ Validation fails
println(person.canVote)  // true (gets value from getter)
```

### **Real-World Example: Online Shopping**
```kotlin
class Product(
    val productId: Int,
    val name: String,
    private var stockCount: Int = 0
) {
    fun addStock(quantity: Int) {
        if (quantity > 0) {
            stockCount += quantity
        }
    }
    
    fun isAvailable() = stockCount > 0
    
    fun getStockCount(): Int = stockCount  // Controlled access
}

val product = Product(1, "Laptop", 5)
product.addStock(10)
println(product.getStockCount())  // 15
// product.stockCount = -5  // ❌ ERROR! Cannot modify directly
```

---

## 2️⃣ Inheritance: Reusing Code

### **Parent and Child Classes**

```kotlin
// Parent class (Superclass)
open class Animal(val name: String) {
    fun eat() {
        println("$name is eating")
    }
    
    open fun makeSound() {  // 'open' allows override
        println("Some generic sound")
    }
}

// Child class (Subclass)
class Dog(name: String, val breed: String) : Animal(name) {
    override fun makeSound() {  // Override parent method
        println("$name barks: Woof! Woof!")
    }
}

class Cat(name: String) : Animal(name) {
    override fun makeSound() {
        println("$name meows: Meow!")
    }
}

// Using inheritance
val dog = Dog("Buddy", "Golden Retriever")
dog.eat()          // Inherited from Animal
dog.makeSound()    // Overridden in Dog class

val cat = Cat("Whiskers")
cat.eat()          // Inherited from Animal
cat.makeSound()    // Overridden in Cat class
```

### **Is-A Relationship**

```kotlin
// "Dog is-a Animal"
val dog = Dog("Buddy", "Golden Retriever")
if (dog is Animal) {
    println("Dog is an Animal")  // ✅ True
}

// You can store a Dog in an Animal reference
val animal: Animal = Dog("Buddy", "Golden Retriever")
animal.makeSound()  // Calls Dog's version
```

### **Real-World Example: Vehicle System**
```kotlin
// Base vehicle class
open class Vehicle(
    val brand: String,
    val color: String,
    protected var speed: Int = 0
) {
    open fun accelerate() {
        speed += 10
        println("$brand accelerated to $speed km/h")
    }
    
    open fun displayInfo() {
        println("$brand $color vehicle, speed: $speed km/h")
    }
}

// Car inherits from Vehicle
class Car(brand: String, color: String) : Vehicle(brand, color) {
    override fun accelerate() {
        super.accelerate()  // Call parent method
        println("Car is now cruising smoothly")
    }
}

// Bike inherits from Vehicle
class Bike(brand: String, color: String) : Vehicle(brand, color) {
    override fun accelerate() {
        speed += 20  // Bikes accelerate faster
        println("Bike accelerated to $speed km/h")
    }
}

val myCar = Car("Toyota", "Blue")
val myBike = Bike("Harley", "Black")

myCar.accelerate()    // Toyota accelerated to 10 km/h
myBike.accelerate()   // Bike accelerated to 20 km/h
```

---

## 3️⃣ Polymorphism: Many Forms

### **Method Overriding (Same Method, Different Behavior)**

```kotlin
open class Payment {
    open fun process(amount: Double) {
        println("Processing payment of $$amount")
    }
}

class CreditCardPayment : Payment() {
    override fun process(amount: Double) {
        println("🏦 Processing credit card payment: $$amount")
        println("Charging 2% fee: $${amount * 0.02}")
    }
}

class PayPalPayment : Payment() {
    override fun process(amount: Double) {
        println("📱 Processing PayPal payment: $$amount")
        println("Charging 1% fee: $${amount * 0.01}")
    }
}

class CryptoCurrencyPayment : Payment() {
    override fun process(amount: Double) {
        println("🔐 Processing cryptocurrency payment: $$amount")
        println("No fees!")
    }
}

// Polymorphism in action
fun processPayment(payment: Payment, amount: Double) {
    payment.process(amount)  // Calls appropriate version
}

// Same function, different behaviors
processPayment(CreditCardPayment(), 100.0)
processPayment(PayPalPayment(), 100.0)
processPayment(CryptoCurrencyPayment(), 100.0)
```

### **Collections with Polymorphism**

```kotlin
// All payment types can be stored in same list
val payments: List<Payment> = listOf(
    CreditCardPayment(),
    PayPalPayment(),
    CryptoCurrencyPayment()
)

val totalAmount = 100.0

for (payment in payments) {
    payment.process(totalAmount)  // Each behaves differently
    println("---")
}
```

---

## 4️⃣ Abstraction: Defining Contracts

### **Abstract Classes (Cannot Be Instantiated)**

```kotlin
// Abstract class - defines what subclasses MUST do
abstract class Shape {
    abstract fun calculateArea(): Double
    abstract fun calculatePerimeter(): Double
    
    // Concrete method (same for all shapes)
    fun displayInfo() {
        println("Area: ${calculateArea()}")
        println("Perimeter: ${calculatePerimeter()}")
    }
}

class Circle(val radius: Double) : Shape() {
    override fun calculateArea() = Math.PI * radius * radius
    override fun calculatePerimeter() = 2 * Math.PI * radius
}

class Rectangle(val width: Double, val height: Double) : Shape() {
    override fun calculateArea() = width * height
    override fun calculatePerimeter() = 2 * (width + height)
}

// Using abstract classes
val circle = Circle(5.0)
circle.displayInfo()

val rectangle = Rectangle(4.0, 6.0)
rectangle.displayInfo()

// val shape = Shape()  // ❌ ERROR! Cannot instantiate abstract class
```

### **Interfaces (Multiple Contracts)**

```kotlin
interface Flyable {
    fun fly()
}

interface Swimmable {
    fun swim()
}

class Duck : Flyable, Swimmable {
    override fun fly() {
        println("Duck is flying")
    }
    
    override fun swim() {
        println("Duck is swimming")
    }
}

val duck = Duck()
duck.fly()    // Duck is flying
duck.swim()   // Duck is swimming
```

### **Real-World Example: Database Abstraction**
```kotlin
// Abstraction - define what all databases must do
interface Database {
    fun connect()
    fun query(sql: String): String
    fun close()
}

// Concrete implementations
class MySQLDatabase : Database {
    override fun connect() = println("Connecting to MySQL...")
    override fun query(sql: String) = "MySQL result: $sql"
    override fun close() = println("Closed MySQL connection")
}

class MongoDBDatabase : Database {
    override fun connect() = println("Connecting to MongoDB...")
    override fun query(sql: String) = "MongoDB result: $sql"
    override fun close() = println("Closed MongoDB connection")
}

// Your app code works with any database
fun executeQuery(db: Database, query: String) {
    db.connect()
    val result = db.query(query)
    println(result)
    db.close()
}

executeQuery(MySQLDatabase(), "SELECT * FROM users")
executeQuery(MongoDBDatabase(), "db.users.find({})")
```

---

## 5️⃣ Data Classes: Simplified Objects

### **Purpose: Store Data**

```kotlin
// Regular class (verbose)
class Person {
    val name: String
    val age: Int
    
    constructor(name: String, age: Int) {
        this.name = name
        this.age = age
    }
    
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is Person) return false
        return name == other.name && age == other.age
    }
}

// Data class (concise)
data class PersonData(val name: String, val age: Int)

// Automatically provides:
// - equals() and hashCode()
// - toString() 
// - copy()
// - destructuring

val person1 = PersonData("Alice", 25)
val person2 = PersonData("Alice", 25)

println(person1 == person2)  // true (compares values)
println(person1)              // PersonData(name=Alice, age=25)

// Destructuring
val (name, age) = person1
println("$name is $age years old")

// Copy with changes
val person3 = person1.copy(age = 26)
```

### **Real-World Example: User Model**
```kotlin
data class User(
    val id: Int,
    val username: String,
    val email: String,
    val isVerified: Boolean = false
)

data class Post(
    val id: Int,
    val author: User,
    val content: String,
    val likes: Int = 0
)

val user = User(1, "alice_dev", "alice@email.com")
val post = Post(101, user, "My first post!", 5)

println(post)  // Shows all data nicely
val (postId, author, content) = post
println("Post by ${author.username}: $content")
```

---

## 6️⃣ Delegation: "Has-A" Relationship

### **Composition (Better Than Inheritance in Many Cases)**

```kotlin
// Don't inherit - compose!
interface Speaker {
    fun speak()
}

class Teacher(val name: String) : Speaker {
    override fun speak() {
        println("$name is teaching")
    }
}

class Student(
    val name: String,
    val speaker: Speaker  // Composition
) {
    fun learn() {
        println("$name is learning...")
        speaker.speak()
    }
}

val teacher = Teacher("Mr. Smith")
val student = Student("Alice", teacher)
student.learn()
// Output:
// Alice is learning...
// Mr. Smith is teaching
```

### **Delegation Pattern**

```kotlin
interface Logger {
    fun log(message: String)
}

class ConsoleLogger : Logger {
    override fun log(message: String) {
        println("[LOG] $message")
    }
}

// Delegate to ConsoleLogger
class FileLogger(val logger: Logger) : Logger by logger

val fileLogger = FileLogger(ConsoleLogger())
fileLogger.log("Found error!")  // Uses ConsoleLogger's implementation
```

---

## 7️⃣ Extension Functions: Add Methods to Existing Classes

```kotlin
// Add a method to String without modifying String class
fun String.wordCount(): Int = this.split(" ").size

val text = "Hello Android Development"
println(text.wordCount())  // 3

// More practical examples
fun String.isEmail(): Boolean = this.contains("@") && this.contains(".")

fun Int.isEven(): Boolean = this % 2 == 0
fun Int.isOdd(): Boolean = this % 2 != 0

println("alice@email.com".isEmail())  // true
println(10.isEven())                   // true
println(7.isOdd())                    // true

// Real-world: Add business logic without modifying original classes
fun String.capitalize(): String = this.replaceFirstChar { it.uppercase() }
fun List<Int>.average(): Double = if (isEmpty()) 0.0 else sum().toDouble() / size

val numbers = listOf(10, 20, 30)
println(numbers.average())  // 20.0
```

---

## 🎓 Practice Questions & Answers

### **Q1: What's the difference between abstract class and interface?**
**A**: Abstract class can have concrete methods and state; interface only defines contracts (though Kotlin interfaces can have default implementations).

### **Q2: What is polymorphism?**
**A**: Ability to use objects of different types through same interface. Same method call, different behaviors.

### **Q3: Why use encapsulation?**
**A**: To hide internal details, prevent invalid operations, and control how data is accessed and modified.

### **Q4: What's the difference between inheritance and composition?**
**A**: Inheritance (is-a): Dog IS-A Animal. Composition (has-a): Car HAS-A Engine. Use composition when inheritance is too rigid.

### **Q5: When should I use data classes?**
**A**: When you primarily need to store data. They automatically provide equals(), hashCode(), toString().

---

## 💡 Key Takeaways

1. ✅ **Encapsulation**: Use `private`, `protected` to control access
2. ✅ **Inheritance**: Use `open` and `override` to extend behavior
3. ✅ **Polymorphism**: Same method, different behaviors depending on object type
4. ✅ **Abstraction**: Use abstract classes/interfaces to define contracts
5. ✅ **Data Classes**: Use for storing data with minimal boilerplate
6. ✅ **Composition**: Often better than inheritance for flexibility

---

## 🏋️ Hands-On Exercise

Create an OOP system for a **Zoo**:

1. Create an abstract `Animal` class with:
   - `name`, `age`, `diet` properties
   - `eat()`, `sleep()` concrete methods
   - `makeSound()` abstract method

2. Create `Lion`, `Elephant`, `Parrot` classes inheriting from `Animal`

3. Create a `Keeper` class that can:
   - Feed any animal
   - Make the animal make sound

4. Create a Zoo that manages animals

```kotlin
// Your solution here
```

---

**Next: [Module 1.3 - Functions & Lambdas](03_KOTLIN_FUNCTIONS.md)**

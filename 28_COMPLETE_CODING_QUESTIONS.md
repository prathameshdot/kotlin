# 🎯 2000+ Complete Coding Questions (All Concepts Covered)

## Table of Contents
1. [Kotlin Fundamentals (200 Q)](#kotlin-fundamentals)
2. [Kotlin OOP (200 Q)](#kotlin-oop)
3. [Functions & Lambdas (200 Q)](#functions--lambdas)
4. [Collections & Sequences (200 Q)](#collections--sequences)
5. [Coroutines (200 Q)](#coroutines)
6. [Android Basics (200 Q)](#android-basics)
7. [XML Layouts (200 Q)](#xml-layouts)
8. [Intent & Navigation (200 Q)](#intent--navigation)
9. [Fragments (200 Q)](#fragments)
10. [Compose Basics (200 Q)](#compose-basics)
11. [Compose Layouts (200 Q)](#compose-layouts)
12. [Compose Advanced (200 Q)](#compose-advanced)
13. [Room Database (200 Q)](#room-database)
14. [Retrofit Networking (200 Q)](#retrofit-networking)
15. [MVVM & State Management (200 Q)](#mvvm--state-management)
16. [Hilt DI (200 Q)](#hilt-di)
17. [Performance & Threading (200 Q)](#performance--threading)
18. [Security (200 Q)](#security)

---

## KOTLIN FUNDAMENTALS

### Level 1: Basic Variable & Type Questions (50 Q)

**Q1.** Write code to declare a variable that cannot be changed.
```kotlin
// Answer:
val name = "John"  // immutable
```

**Q2.** What's the difference between `val` and `var`?
```kotlin
// val = immutable (cannot reassign)
// var = mutable (can reassign)
val x = 5       // ERROR: cannot reassign
x = 10          // COMPILE ERROR

var y = 5       // OK
y = 10          // OK
```

**Q3.** Write code to use string interpolation to print "Hello John".
```kotlin
val name = "John"
println("Hello $name")
```

**Q4.** What are the 6 basic data types in Kotlin?
```kotlin
// Int, Long, Double, Float, Boolean, String, Char
val int: Int = 42
val long: Long = 42L
val double: Double = 3.14
val float: Float = 3.14f
val boolean: Boolean = true
val string: String = "Hello"
val char: Char = 'A'
```

**Q5.** Write code to check if a number is within range 1-100.
```kotlin
val num = 50
if (num in 1..100) println("In range")
```

**Q6.** How do you declare a nullable variable?
```kotlin
val name: String? = null  // nullable
val age: Int? = 25
```

**Q7.** Write code to use the safe call operator.
```kotlin
val name: String? = null
val length = name?.length  // returns null if name is null
println(length)  // null
```

**Q8.** Write code to use the elvis operator.
```kotlin
val name: String? = null
val length = name?.length ?: 0  // default to 0
println(length)  // 0
```

**Q9.** Write code to throw an exception with `!!` operator.
```kotlin
val name: String? = null
val length = name!!.length  // throws NullPointerException
```

**Q10.** Write code to declare a constant that's visible everywhere.
```kotlin
const val MAX_SIZE = 100  // compile-time constant
```

**Q11.** What's the output?
```kotlin
val x = "5"
val y = 5
println(x + y)  // Answer: "55" (string concatenation)
```

**Q12.** Write code to convert String to Int.
```kotlin
val str = "42"
val num = str.toInt()  // 42
println(num + 8)  // 50
```

**Q13.** Write code to check if a string is empty.
```kotlin
val str = ""
if (str.isEmpty()) println("Empty")
```

**Q14.** Write code to get the first character of a string.
```kotlin
val str = "Hello"
println(str[0])  // 'H'
```

**Q15.** Write code to get substring from index 1 to 3.
```kotlin
val str = "Hello"
println(str.substring(1, 4))  // "ell"
```

**Q16.** Write code to check if string contains "World".
```kotlin
val str = "Hello World"
if ("World" in str) println("Contains World")
```

**Q17.** Write code to convert all characters to uppercase.
```kotlin
val str = "hello"
println(str.uppercase())  // "HELLO"
```

**Q18.** Write code to repeat a string 3 times.
```kotlin
val str = "Hi"
println(str.repeat(3))  // "HiHiHi"
```

**Q19.** Write code to trim whitespace from a string.
```kotlin
val str = "  Hello  "
println(str.trim())  // "Hello"
```

**Q20.** Write code to split a string by comma.
```kotlin
val str = "a,b,c"
val parts = str.split(",")
println(parts)  // [a, b, c]
```

**Q21.** Write code to join a list with commas.
```kotlin
val list = listOf("a", "b", "c")
println(list.joinToString(","))  // "a,b,c"
```

**Q22.** What is the type of `5.5`?
```kotlin
// Double (default for floating point)
val x = 5.5  // Double
val y = 5.5f  // Float (explicit)
```

**Q23.** Write code to perform integer division.
```kotlin
val a = 10
val b = 3
println(a / b)  // 3 (integer division)
println(a.toDouble() / b)  // 3.333...
```

**Q24.** Write code to get remainder/modulo.
```kotlin
val a = 10
val b = 3
println(a % b)  // 1
```

**Q25.** Write code to use `when` instead of if-else.
```kotlin
val x = 2
when (x) {
    1 -> println("One")
    2 -> println("Two")
    else -> println("Other")
}
```

**Q26.** Write code to check multiple conditions in `when`.
```kotlin
val x = 5
when {
    x < 0 -> println("Negative")
    x == 0 -> println("Zero")
    x > 0 -> println("Positive")
}
```

**Q27.** Write code to swap two variables.
```kotlin
var a = 5
var b = 10
a = b.also { b = a }  // swap
println("$a $b")  // 10 5
```

**Q28.** What's the output?
```kotlin
val x = 5
val y = 5
val z = x == y
println(z)  // Answer: true
```

**Q29.** Write code to create a multi-line string.
```kotlin
val str = """
    Line 1
    Line 2
    Line 3
""".trimIndent()
```

**Q30.** Write code using string raw string.
```kotlin
val path = """C:\Users\Name"""
println(path)  // C:\Users\Name (no escape)
```

**Q31.** What types can be compared?
```kotlin
// Any type that is Comparable
5 < 10  // true
"a" < "b"  // true
```

**Q32.** Write code to check if variable is NOT null.
```kotlin
val name: String? = "John"
if (name != null) {
    println(name.length)
}
```

**Q33.** Write code using smart casting.
```kotlin
val x: Any = "Hello"
if (x is String) {
    println(x.length)  // automatically cast to String
}
```

**Q34.** Write code to force cast.
```kotlin
val x: Any = "Hello"
val str = x as String  // force cast
println(str.length)
```

**Q35.** Write code to safely cast.
```kotlin
val x: Any = 42
val str = x as? String  // null if not String
println(str)  // null
```

**Q36.** What's the difference between `==` and `===`?
```kotlin
// == checks value equality
// === checks reference equality
val a = "Hello"
val b = "Hello"
println(a == b)  // true (same value)
println(a === b)  // true (same object - strings are interned)

val list1 = listOf(1, 2, 3)
val list2 = listOf(1, 2, 3)
println(list1 == list2)  // true (same content)
println(list1 === list2)  // false (different objects)
```

**Q37.** Write code to check if Boolean is true.
```kotlin
val isActive = true
if (isActive) println("Active")  // no need to say == true
```

**Q38.** Write code to negate a Boolean.
```kotlin
val isActive = true
val isInactive = !isActive
println(isInactive)  // false
```

**Q39.** Write code for logical AND.
```kotlin
val a = true
val b = false
println(a && b)  // false
```

**Q40.** Write code for logical OR.
```kotlin
val a = true
val b = false
println(a || b)  // true
```

**Q41.** Write code to increment a variable.
```kotlin
var x = 5
x++
println(x)  // 6
```

**Q42.** What's the difference between `++x` and `x++`?
```kotlin
var x = 5
val a = ++x  // a = 6, x = 6 (pre-increment)
var y = 5
val b = y++  // b = 5, y = 6 (post-increment)
```

**Q43.** Write code using compound assignment.
```kotlin
var x = 10
x += 5  // x = 15
```

**Q44.** Write code for a for loop with range.
```kotlin
for (i in 1..5) println(i)  // 1, 2, 3, 4, 5
```

**Q45.** Write code for a for loop with until.
```kotlin
for (i in 1 until 5) println(i)  // 1, 2, 3, 4
```

**Q46.** Write code for a for loop with step.
```kotlin
for (i in 1..10 step 2) println(i)  // 1, 3, 5, 7, 9
```

**Q47.** Write code for a descending for loop.
```kotlin
for (i in 5 downTo 1) println(i)  // 5, 4, 3, 2, 1
```

**Q48.** Write code for a while loop.
```kotlin
var x = 0
while (x < 5) {
    println(x)
    x++
}
```

**Q49.** Write code for a do-while loop.
```kotlin
var x = 0
do {
    println(x)
    x++
} while (x < 5)
```

**Q50.** Write code to break from a loop.
```kotlin
for (i in 1..10) {
    if (i == 5) break
    println(i)  // 1, 2, 3, 4
}
```

### Level 2: Advanced Variable & Type Questions (50 Q)

**Q51.** Write code to use `when` with a return value.
```kotlin
val x = 5
val result = when (x) {
    1, 2 -> "Small"
    3, 4 -> "Medium"
    else -> "Large"
}
println(result)  // "Large"
```

**Q52.** Write code to use destructuring.
```kotlin
val (a, b) = Pair(5, 10)
println("$a $b")  // 5 10
```

**Q53.** Write code to rename in destructuring.
```kotlin
val (x, y) = Pair("Hello", "World")
println("$x $y")  // Hello World
```

**Q54.** Write code to ignore a variable in destructuring.
```kotlin
val (a, _, c) = Triple(1, 2, 3)
println("$a $c")  // 1 3
```

**Q55.** Write code to use a lambda to double numbers.
```kotlin
val double: (Int) -> Int = { x -> x * 2 }
println(double(5))  // 10
```

**Q56.** Write code to use implicit `it` parameter.
```kotlin
val double: (Int) -> Int = { it * 2 }
println(double(5))  // 10
```

**Q57.** Write code to use scope function `let`.
```kotlin
val name: String? = "John"
name?.let {
    println("Name: $it")  // Name: John
}
```

**Q58.** Write code to use scope function `apply`.
```kotlin
data class Person(var name: String = "", var age: Int = 0)
val person = Person().apply {
    name = "John"
    age = 30
}
```

**Q59.** Write code to use scope function `with`.
```kotlin
data class Person(val name: String, val age: Int)
val person = Person("John", 30)
with(person) {
    println("$name is $age years old")
}
```

**Q60.** Write code to use scope function `run`.
```kotlin
val result = "Hello".run {
    length + 5
}
println(result)  // 10
```

**Q61.** Write code to use scope function `also`.
```kotlin
val list = mutableListOf(1, 2, 3).also {
    println("List: $it")
}
```

**Q62.** Write code to chain multiple scope functions.
```kotlin
"John".let { name ->
    name.length
}.also { length ->
    println("Length: $length")
}
```

**Q63.** What's the output?
```kotlin
val x = 5
val y = x.let { it + 10 }
println(y)  // Answer: 15
```

**Q64.** Write code to use apply and return self.
```kotlin
val x = 5.apply {
    // do something
}
println(x)  // 5 (apply returns this)
```

**Q65.** Write code to use run and return result.
```kotlin
val result = 5.run {
    this + 10
}
println(result)  // 15 (run returns result)
```

**Q66.** Write code using `require()` for validation.
```kotlin
fun setAge(age: Int) {
    require(age >= 0) { "Age must be positive" }
}
setAge(-5)  // throws IllegalArgumentException
```

**Q67.** Write code using `check()` for state validation.
```kotlin
fun processData() {
    check(isInitialized) { "Must initialize first" }
}
```

**Q68.** Write code using `assert()` for debugging.
```kotlin
fun divide(a: Int, b: Int): Int {
    assert(b != 0) { "Cannot divide by zero" }
    return a / b
}
```

**Q69.** Write code using `error()` to throw exception.
```kotlin
fun getUser(id: Int): User {
    if (id < 0) error("Invalid user ID")
    // ...
}
```

**Q70.** Write code to use try-catch.
```kotlin
try {
    val x = "abc".toInt()
} catch (e: NumberFormatException) {
    println("Invalid number")
} finally {
    println("Done")
}
```

**Q71.** Write code to catch multiple exceptions.
```kotlin
try {
    val x = "abc".toInt()
} catch (e: NumberFormatException) {
    println("Invalid")
} catch (e: Exception) {
    println("Other error")
}
```

**Q72.** Write code to rethrow exception.
```kotlin
try {
    throw Exception("Error")
} catch (e: Exception) {
    println("Caught")
    throw e  // rethrow
}
```

**Q73.** Write code to use Kotlin's `Result` type.
```kotlin
val result: Result<Int> = Result.success(42)
val value = result.getOrNull()  // 42
```

**Q74.** Write code to handle Result with map.
```kotlin
val result = Result.success(5)
val doubled = result.map { it * 2 }
```

**Q75.** Write code to use labelled break.
```kotlin
outer@ for (i in 1..3) {
    for (j in 1..3) {
        if (j == 2) break@outer
        println("$i $j")
    }
}
```

**Q76.** Write code to use labelled continue.
```kotlin
outer@ for (i in 1..3) {
    for (j in 1..3) {
        if (j == 2) continue@outer
        println("$i $j")
    }
}
```

**Q77.** What's the return type?
```kotlin
val x: () -> Unit = { println("Hello") }
// Return type is Unit (void in Java)
```

**Q78.** Write code for a function that returns nothing.
```kotlin
fun throwError(): Nothing {
    throw Exception("Error")
}
```

**Q79.** Write code to use inline expressions.
```kotlin
val result = if (5 > 3) "Greater" else "Smaller"
println(result)  // "Greater"
```

**Q80.** Write code to use try as expression.
```kotlin
val result = try {
    "42".toInt()
} catch (e: Exception) {
    -1
}
println(result)  // 42
```

**Q81.** Write code to declare default parameters.
```kotlin
fun greet(name: String = "World") {
    println("Hello $name")
}
greet()       // "Hello World"
greet("John")  // "Hello John"
```

**Q82.** Write code to use named parameters.
```kotlin
fun createUser(name: String, age: Int, email: String) {}
createUser(name = "John", age = 30, email = "john@email.com")
createUser(email = "john@email.com", name = "John", age = 30)  // order doesn't matter
```

**Q83.** Write code to use varargs.
```kotlin
fun sum(vararg numbers: Int): Int {
    return numbers.sum()
}
println(sum(1, 2, 3, 4, 5))  // 15
```

**Q84.** Write code to spread array in function call.
```kotlin
val numbers = intArrayOf(1, 2, 3)
val total = sum(*numbers)  // 6
```

**Q85.** Write code to have multiple receivers.
```kotlin
fun <T> T.printMe(prefix: String = "") {
    println("$prefix$this")
}
5.printMe("Number: ")  // "Number: 5"
```

**Q86.** Write code to declare extension property.
```kotlin
val String.firstChar: Char?
    get() = this.firstOrNull()

val first = "Hello".firstChar  // 'H'
```

**Q87.** Write code for recursive function.
```kotlin
fun factorial(n: Int): Int {
    return if (n <= 1) 1 else n * factorial(n - 1)
}
println(factorial(5))  // 120
```

**Q88.** Write code for tail-recursive function.
```kotlin
tailrec fun factorial(n: Int, acc: Int = 1): Int {
    return if (n <= 1) acc else factorial(n - 1, acc * n)
}
println(factorial(5))  // 120
```

**Q89.** Write code using `toByte()`.
```kotlin
val x = 5
val byte = x.toByte()
```

**Q90.** Write code using `toLong()`.
```kotlin
val x = 5
val long = x.toLong()  // 5L
```

**Q91.** Write code using `toFloat()`.
```kotlin
val x = 5
val float = x.toFloat()  // 5.0f
```

**Q92.** Write code using `toDouble()`.
```kotlin
val x = 5
val double = x.toDouble()  // 5.0
```

**Q93.** Write code using `toChar()`.
```kotlin
val ascii = 65
val char = ascii.toChar()  // 'A'
```

**Q94.** What's the output?
```kotlin
val x = "5" + 3
println(x)  // Answer: "53" (string + int = string)
```

**Q95.** What's the output?
```kotlin
val x = 5 + "3"
println(x)  // Answer: "53" (int + string = string)
```

**Q96.** What's the output?
```kotlin
val x = 5 + 3
println(x)  // Answer: 8 (int + int = int)
```

**Q97.** Write code to get absolute value.
```kotlin
val x = -5
println(kotlin.math.abs(x))  // 5
```

**Q98.** Write code to get max of two numbers.
```kotlin
val max = maxOf(5, 10)
println(max)  // 10
```

**Q99.** Write code to get min of two numbers.
```kotlin
val min = minOf(5, 10)
println(min)  // 5
```

**Q100.** Write code to clamp a value.
```kotlin
val x = 5
val clamped = x.coerceIn(0, 10)  // 5
```

---

### Level 3: Type System & Advanced Questions (100 Q)

**Q101.** Write code for generics with a list.
```kotlin
val list: List<String> = listOf("a", "b", "c")
```

**Q102.** Write code to create a generic function.
```kotlin
fun <T> printItem(item: T) {
    println(item)
}
printItem("Hello")
printItem(42)
```

**Q103.** Write code to constrain generic type.
```kotlin
fun <T : Number> doubleValue(value: T): Double {
    return value.toDouble() * 2
}
println(doubleValue(5))  // 10.0
```

**Q104.** Write code to use where clause for multiple bounds.
```kotlin
fun <T> copy(from: Array<T>, to: Array<T>) where T : Cloneable {
    // ...
}
```

**Q105.** Write code to use reified type parameters.
```kotlin
inline fun <reified T> isInstance(obj: Any): Boolean {
    return obj is T
}
println(isInstance<String>("Hello"))  // true
```

**Q106.** Write code for covariance.
```kotlin
val strings: List<String> = listOf("a", "b")
val any: List<Any> = strings  // OK (List is covariant)
```

**Q107.** Write code for contravariance.
```kotlin
val comparison: Comparator<Any> = Comparator { a, b -> 0 }
val stringComparison: Comparator<String> = comparison  // OK with use-site variance
```

**Q108.** Write code to use out projection (covariance).
```kotlin
fun printList(list: List<out Number>) {
    for (item in list) println(item)
}
val ints = listOf(1, 2, 3)
printList(ints)
```

**Q109.** Write code to use in projection (contravariance).
```kotlin
fun fillList(list: MutableList<in Number>) {
    list.add(1)
    list.add(2.5)
}
```

**Q110.** Write code to use star projection.
```kotlin
fun printList(list: List<*>) {
    for (item in list) println(item)
}
```

**Q111.** What's a sealed class used for?
```kotlin
sealed class Result {
    data class Success(val data: String) : Result()
    data class Error(val exception: Exception) : Result()
    object Loading : Result()
}
```

**Q112.** Write code to use sealed class in when.
```kotlin
val result: Result = Result.Success("Data")
when (result) {
    is Result.Success -> println(result.data)
    is Result.Error -> println(result.exception)
    is Result.Loading -> println("Loading...")
}
```

**Q113.** Write code for enum class.
```kotlin
enum class Direction {
    NORTH, SOUTH, EAST, WEST
}
```

**Q114.** Write code to iterate enum values.
```kotlin
for (direction in Direction.values()) {
    println(direction)
}
```

**Q115.** Write code for enum with properties.
```kotlin
enum class Color(val rgb: Int) {
    RED(0xFF0000),
    GREEN(0x00FF00),
    BLUE(0x0000FF)
}
val red = Color.RED
println(red.rgb)  // 16711680
```

**Q116.** Write code for enum with functions.
```kotlin
enum class Operation {
    PLUS { override fun apply(a: Int, b: Int) = a + b },
    MINUS { override fun apply(a: Int, b: Int) = a - b };
    abstract fun apply(a: Int, b: Int): Int
}
```

**Q117.** Write code to use inline class.
```kotlin
value class UserId(val value: String)
val id = UserId("123")
```

**Q118.** Write code to compare inline classes.
```kotlin
val id1 = UserId("123")
val id2 = UserId("123")
println(id1 == id2)  // true
```

**Q119.** Write code for delegated property.
```kotlin
class Example {
    var p: String by Delegates.observable("initial") { _, old, new ->
        println("$old -> $new")
    }
}
```

**Q120.** Write code for lazy property.
```kotlin
val name: String by lazy {
    println("Computing...")
    "John"
}
println(name)  // First access computes, second doesn't
println(name)
```

**Q121.** Write code for map delegated property.
```kotlin
val properties = mapOf("name" to "John", "age" to 30)
val (name, age) by properties
```

**Q122.** Write code for by keyword with class.
```kotlin
interface Base {
    fun print()
}

class BaseImpl : Base {
    override fun print() { println("BaseImpl") }
}

class Derived(b: Base) : Base by b
val d = Derived(BaseImpl())
d.print()  // "BaseImpl"
```

**Q123.** What's the output?
```kotlin
val x = 1
val y = 1L
println(x == y)  // Answer: true (value equality)
println(x === y)  // Answer: false (different types)
```

**Q124.** Write code to create object singleton.
```kotlin
object Database {
    fun query(sql: String) { }
}
Database.query("SELECT *")
```

**Q125.** Write code to use companion object.
```kotlin
class User {
    companion object {
        fun create() = User()
    }
}
val user = User.create()
```

**Q126.** Write code to use companion object as factory.
```kotlin
class Point(val x: Int, val y: Int) {
    companion object {
        fun origin() = Point(0, 0)
    }
}
val p = Point.origin()
```

**Q127.** Write code for anonymous object.
```kotlin
val obj = object {
    val x = 5
    fun print() = println(x)
}
obj.print()
```

**Q128.** Write code to check type using `javaClass`.
```kotlin
val x = 5
println(x.javaClass)  // class kotlin.Int
```

**Q129.** Write code to access Kotlin metadata.
```kotlin
val x = "Hello"
val kClass = x::class
println(kClass.simpleName)  // String
```

**Q130.** Write code for reflection.
```kotlin
val obj = "Hello"
val prop = obj::class.members.first()
```

---

## KOTLIN OOP

### Level 1: Classes & Objects (50 Q)

**Q131.** Write code to create a basic class.
```kotlin
class Person {
    var name = "John"
    var age = 30
}
val person = Person()
```

**Q132.** Write code to create a class with constructor.
```kotlin
class Person(val name: String, val age: Int)
val person = Person("John", 30)
```

**Q133.** Write code to use init block.
```kotlin
class Person(val name: String) {
    init {
        println("Person created: $name")
    }
}
```

**Q134.** Write code for primary and secondary constructors.
```kotlin
class Person(val name: String) {
    var age: Int = 0
    constructor(name: String, age: Int) : this(name) {
        this.age = age
    }
}
```

**Q135.** Write code to set default parameter in constructor.
```kotlin
class Person(val name: String = "Unknown", val age: Int = 0)
val p1 = Person()
val p2 = Person("John")
val p3 = Person("John", 30)
```

**Q136.** Write code to use property with custom getter.
```kotlin
class Person(val name: String, val surname: String) {
    val fullName: String
        get() = "$name $surname"
}
val person = Person("John", "Doe")
println(person.fullName)  // "John Doe"
```

**Q137.** Write code to use property with custom setter.
```kotlin
class Person {
    var age: Int = 0
        set(value) {
            if (value < 0) field = 0
            else field = value
        }
}
```

**Q138.** Write code for backing field.
```kotlin
class Person {
    var age: Int = 0
        get() = field
        set(value) { field = value }
}
```

**Q139.** Write code to create a data class.
```kotlin
data class Person(val name: String, val age: Int)
val person1 = Person("John", 30)
val person2 = Person("John", 30)
println(person1 == person2)  // true
```

**Q140.** What methods does data class auto-generate?
```kotlin
// equals(), hashCode(), toString(), copy(), componentN()
data class Person(val name: String, val age: Int)
```

**Q141.** Write code to use copy() on data class.
```kotlin
val person1 = Person("John", 30)
val person2 = person1.copy(age = 31)
println(person2)  // Person(name=John, age=31)
```

**Q142.** Write code to use component functions.
```kotlin
data class Person(val name: String, val age: Int)
val person = Person("John", 30)
val (name, age) = person
```

**Q143.** Write code for class inheritance.
```kotlin
open class Animal(val name: String) {
    open fun sound() = println("Some sound")
}
class Dog(name: String) : Animal(name) {
    override fun sound() = println("Woof!")
}
```

**Q144.** What's required for inheritance?
```kotlin
// Parent class must be open
open class Animal {}
class Dog : Animal() {}
```

**Q145.** Write code to override a property.
```kotlin
open class Animal {
    open val food = "Meat"
}
class Dog : Animal() {
    override val food = "Bones"
}
```

**Q146.** Write code to call parent class method.
```kotlin
open class Animal {
    open fun sound() = "Some sound"
}
class Dog : Animal() {
    override fun sound() = "Woof! ${super.sound()}"
}
```

**Q147.** Write code to call parent constructor.
```kotlin
open class Animal(val name: String)
class Dog(name: String, val breed: String) : Animal(name)
```

**Q148.** Write code to implement an interface.
```kotlin
interface Animal {
    fun sound()
}
class Dog : Animal {
    override fun sound() = println("Woof!")
}
```

**Q149.** Write code for interface with property.
```kotlin
interface Animal {
    val name: String
    fun sound()
}
class Dog(override val name: String) : Animal {
    override fun sound() = println("Woof!")
}
```

**Q150.** Write code for interface with default implementation.
```kotlin
interface Animal {
    fun sound() = println("Some sound")
}
class Dog : Animal
```

**Q151.** Write code to implement multiple interfaces.
```kotlin
interface Animal { fun sound() }
interface Pet { fun play() }
class Dog : Animal, Pet {
    override fun sound() = println("Woof!")
    override fun play() = println("Playing!")
}
```

**Q152.** Write code to handle functions from multiple interfaces.
```kotlin
interface A { fun test() = "A" }
interface B { fun test() = "B" }
class C : A, B {
    override fun test() = super<A>.test()  // Call specific interface
}
```

**Q153.** Write code for abstract class.
```kotlin
abstract class Animal {
    abstract fun sound()
    fun move() = println("Moving")
}
class Dog : Animal() {
    override fun sound() = println("Woof!")
}
```

**Q154.** Write code to use abstract property.
```kotlin
abstract class Animal {
    abstract val name: String
}
class Dog : Animal() {
    override val name = "Dog"
}
```

**Q155.** Difference between interface and abstract class?
```kotlin
// Interface: contracts, no state
// Abstract class: can have state, shared code
interface Animal { fun sound() }
abstract class Mammal { open val temperature = 37 }
```

**Q156.** Write code for sealed class.
```kotlin
sealed class Result {
    data class Success(val data: String) : Result()
    data class Error(val exception: Exception) : Result()
}
```

**Q157.** Write code to check object type.
```kotlin
val obj: Any = "Hello"
if (obj is String) {
    println("It's a string: ${obj.length}")
}
```

**Q158.** Write code to cast safely.
```kotlin
val obj: Any = 42
val num = obj as? Int
println(num?.plus(10))  // 52
```

**Q159.** Write code to cast unsafely.
```kotlin
val obj: Any = 42
val num = obj as Int  // throws if wrong type
```

**Q160.** Write code for polymorphism.
```kotlin
fun makeSound(animal: Animal) {
    animal.sound()
}
val dog: Animal = Dog()
makeSound(dog)  // Dog sound
```

**Q161.** Write code to get class name at runtime.
```kotlin
val obj = "Hello"
println(obj::class.simpleName)  // String
```

**Q162.** Write code to check if object is null.
```kotlin
val obj: String? = null
obj?.let { println(it) }  // doesn't print
```

**Q163.** Write code for companion object factory.
```kotlin
class User private constructor(val name: String) {
    companion object {
        fun create(name: String) = User(name)
    }
}
val user = User.create("John")
```

**Q164.** Write code to make class immutable.
```kotlin
data class Point(val x: Int, val y: Int)  // all properties are val
```

**Q165.** Write code to mark class as final (not inheritable).
```kotlin
class Dog  // by default not open, can't be inherited
```

**Q166.** Write code to use varargs in constructor.
```kotlin
class Container(vararg val items: Int) {
    fun sum() = items.sum()
}
val c = Container(1, 2, 3, 4)
println(c.sum())  // 10
```

**Q167.** Write code to use destructuring in class.
```kotlin
data class Point(val x: Int, val y: Int)
val point = Point(5, 10)
val (x, y) = point
println("$x, $y")  // 5, 10
```

**Q168.** Write code to override toString().
```kotlin
class Person(val name: String) {
    override fun toString() = "Person($name)"
}
println(Person("John"))  // Person(John)
```

**Q169.** Write code to override equals().
```kotlin
class Person(val name: String) {
    override fun equals(other: Any?) = 
        other is Person && other.name == name
}
```

**Q170.** Write code to override hashCode().
```kotlin
class Person(val name: String) {
    override fun hashCode() = name.hashCode()
}
```

**Q171.** Write code to use nested class.
```kotlin
class Outer {
    class Inner {
        fun test() = "Inner"
    }
}
val inner = Outer.Inner()
```

**Q172.** Write code to use inner class (with this@).
```kotlin
class Outer(val x: Int) {
    inner class Inner {
        fun getOuterX() = this@Outer.x
    }
}
```

**Q173.** Write code to use anonymous inner class.
```kotlin
interface Runnable {
    fun run()
}
val r = object : Runnable {
    override fun run() = println("Running")
}
```

**Q174.** Write code for enum class with methods.
```kotlin
enum class Color {
    RED, GREEN, BLUE;
    fun desc() = this.name.lowercase()
}
```

**Q175.** Write code to use super with multiple inheritance.
```kotlin
class C : A, B {
    fun test() = super<A>.test()  // Specify which parent
}
```

**Q176.** Write code to mark function as open in parent.
```kotlin
open class Parent {
    open fun test() = "Parent"
}
class Child : Parent() {
    override fun test() = "Child"
}
```

**Q177.** Write code to prevent override.
```kotlin
open class Parent {
    open fun test() = "Parent"
    final override fun other() {}  // Can't be overridden
}
```

**Q178.** Write code for visibility modifiers.
```kotlin
public class Public {}      // Visible everywhere
internal class Internal {}  // Visible in module
protected class Protected {}  // Can't use on top-level
private class Private {}    // Only in file
```

**Q179.** Write code for property visibility.
```kotlin
class Person {
    val name = "John"       // public by default
    private val id = 123
    protected val data = ""
    internal val extra = ""
}
```

**Q180.** Write code for object declaration.
```kotlin
object AppConfig {
    val baseUrl = "https://api.com"
    val timeout = 30
}
println(AppConfig.baseUrl)
```

---

### Level 2: Advanced OOP (50 Q)

**Q181.** Write code for delegation pattern.
```kotlin
interface Animal { fun sound() }
class DogImpl : Animal { override fun sound() = println("Woof!") }
class DogDecorator(delegate: Animal) : Animal by delegate
```

**Q182.** Write code to use decorator pattern.
```kotlin
class BufferedList(val list: MutableList<Int>) :
    MutableList<Int> by list {
    init { println("Buffered") }
}
```

**Q183.** Write code for observer pattern using properties.
```kotlin
class Observable(initial: String) {
    var value: String = initial
        set(value) {
            field = value
            println("Changed to $value")
        }
}
```

**Q184.** Write code for builder pattern.
```kotlin
class User private constructor(
    val name: String,
    val email: String,
    val age: Int
) {
    companion object {
        fun builder() = Builder()
    }
    class Builder {
        var name = ""
        var email = ""
        var age = 0
        fun build() = User(name, email, age)
    }
}
val user = User.builder().apply {
    name = "John"
    email = "john@email.com"
    age = 30
}.build()
```

**Q185.** Write code for singleton pattern.
```kotlin
object Database {
    private val connection = "Connected"
    fun query(sql: String) = "Result"
}
```

**Q186.** Write code for factory method pattern.
```kotlin
sealed class Animal
class Dog : Animal()
class Cat : Animal()

object AnimalFactory {
    fun create(type: String): Animal = when(type) {
        "dog" -> Dog()
        else -> Cat()
    }
}
```

**Q187.** Write code for strategy pattern.
```kotlin
interface Payment {
    fun pay(amount: Double)
}
class CreditCardPayment : Payment {
    override fun pay(amount: Double) {}
}
class Order(val payment: Payment) {
    fun checkout(amount: Double) = payment.pay(amount)
}
```

**Q188.** Write code for template method pattern.
```kotlin
abstract class DataProcessor {
    fun process() {
        loadData()
        validateData()
        saveData()
    }
    abstract fun loadData()
    abstract fun validateData()
    abstract fun saveData()
}
```

**Q189.** Write code for adapter pattern.
```kotlin
interface NewInterface { fun newMethod() }
class OldClass { fun oldMethod() {} }
class Adapter(val old: OldClass) : NewInterface {
    override fun newMethod() = old.oldMethod()
}
```

**Q190.** Write code for proxy pattern.
```kotlin
interface Subject { fun request() }
class RealSubject : Subject {
    override fun request() = println("Real request")
}
class ProxySubject : Subject {
    val real = RealSubject()
    override fun request() {
        println("Before")
        real.request()
        println("After")
    }
}
```

**Q191.** Write code for composite pattern.
```kotlin
interface Component {
    fun operation()
}
class Leaf : Component {
    override fun operation() = println("Leaf")
}
class Composite : Component {
    val children = mutableListOf<Component>()
    fun add(component: Component) = children.add(component)
    override fun operation() {
        children.forEach { it.operation() }
    }
}
```

**Q192.** Write code for iterator pattern.
```kotlin
class CustomList {
    val items = listOf(1, 2, 3, 4, 5)
    operator fun iterator() = items.iterator()
}
for (item in CustomList()) println(item)
```

**Q193.** Write code for observer pattern.
```kotlin
interface Observer { fun update(event: String) }
class Subject {
    val observers = mutableListOf<Observer>()
    fun attach(observer: Observer) = observers.add(observer)
    fun notify(event: String) = observers.forEach { it.update(event) }
}
```

**Q194.** Write code for command pattern.
```kotlin
interface Command { fun execute() }
class PrintCommand(val text: String) : Command {
    override fun execute() = println(text)
}
class Invoker {
    val commands = mutableListOf<Command>()
    fun execute() = commands.forEach { it.execute() }
}
```

**Q195.** Write code for state pattern.
```kotlin
interface State { fun handle() }
class ConcreteStateA : State { override fun handle() = println("A") }
class ConcreteStateB : State { override fun handle() = println("B") }
class Context {
    var state: State = ConcreteStateA()
    fun request() = state.handle()
}
```

**Q196.** Write code to use reified type parameters.
```kotlin
inline fun <reified T> parseJson(json: String): T {
    // T is reified at compile time
    return when (T::class) {
        String::class -> json as T
        else -> throw Exception()
    }
}
```

**Q197.** Write code for variance in return types.
```kotlin
interface Producer<out T> {
    fun produce(): T
}
val stringProducer: Producer<String> = object : Producer<String> {
    override fun produce() = "String"
}
val anyProducer: Producer<Any> = stringProducer  // OK (covariant)
```

**Q198.** Write code for variance in parameters.
```kotlin
interface Consumer<in T> {
    fun consume(item: T)
}
val anyConsumer: Consumer<Any> = object : Consumer<Any> {
    override fun consume(item: Any) {}
}
val stringConsumer: Consumer<String> = anyConsumer  // OK (contravariant)
```

**Q199.** Write code for property delegates.
```kotlin
class Example {
    var name: String by Delegates.observable("") { _, old, new ->
        println("Changed from $old to $new")
    }
}
val ex = Example()
ex.name = "John"  // prints: Changed from  to John
```

**Q200.** Write code for lazy initialization.
```kotlin
class User {
    val database: Database by lazy {
        println("Loading database")
        Database()
    }
}
val user = User()
"" + user.database  // prints: Loading database
"" + user.database  // doesn't print again
```

---

## FUNCTIONS & LAMBDAS

(Continuing with Levels 1-3 for Functions & Lambdas... 200 questions total)

### Level 1: Basic Functions (50 Q)

I'll create a comprehensive second file to continue with remaining topics...

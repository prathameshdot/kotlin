# Module 2.2: XML Layouts - Building Beautiful UIs
## Complete Guide to Android Layouts

---

## 📖 What are XML Layouts?

XML layouts are files that define the structure and appearance of your Android app's screens. Think of it like HTML for Android - XML describes what widgets to show and how to arrange them.

---

## 1️⃣ Layout Files Location & Structure

```
MyApp/
├── res/
│   ├── layout/
│   │   ├── activity_main.xml
│   │   ├── activity_profile.xml
│   │   ├── fragment_home.xml
│   │   └── ...
│   ├── values/
│   │   ├── colors.xml
│   │   ├── strings.xml
│   │   └── dimens.xml
│   └── drawable/
│       └── icon.png
```

### **Basic Structure**

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">
    
    <!-- Your UI elements go here -->
    
</LinearLayout>
```

---

## 2️⃣ Basic Attributes Explained

```xml
<!-- width and height - Size of element -->
android:layout_width="match_parent"    <!-- Full available width -->
android:layout_width="wrap_content"    <!-- Just enough for content -->
android:layout_width="200dp"           <!-- Fixed 200 density-independent pixels -->

android:layout_height="match_parent"   <!-- Full available height -->
android:layout_height="wrap_content"   <!-- Just enough for content -->
android:layout_height="100dp"          <!-- Fixed 100 dp -->

<!-- Text properties -->
android:text="Hello World"             <!-- The text to display -->
android:textSize="24sp"                <!-- Text size (sp = scale-independent px) -->
android:textColor="@color/blue"        <!-- Color -->
android:textStyle="bold"               <!-- bold, italic, bold|italic -->

<!-- Padding - Space inside the element -->
android:padding="16dp"                 <!-- All sides -->
android:paddingTop="16dp"              <!-- Individual sides -->
android:paddingBottom="8dp"
android:paddingStart="12dp"            <!-- For RTL support -->
android:paddingEnd="12dp"

<!-- Margin - Space outside the element -->
android:layout_margin="16dp"           <!-- All sides -->
android:layout_marginTop="16dp"        <!-- Individual sides -->

<!-- Background color -->
android:background="@color/white"      <!-- Solid color -->
android:background="#FFFFFF"           <!-- Hex color -->

<!-- Gravity - Align content inside -->
android:gravity="center"               <!-- Center content -->
android:gravity="center_horizontal"    <!-- Center horizontally -->
android:gravity="center_vertical"      <!-- Center vertically -->

<!-- Layout gravity - Position within parent -->
android:layout_gravity="center"        <!-- Position in parent -->
```

---

## 3️⃣ Layout Types

### **LinearLayout - Items in Line (Horizontal or Vertical)**

```xml
<!-- Vertical arrangement (default) -->
<LinearLayout
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">
    
    <Button
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Button 1" />
    
    <Button
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Button 2" />
    
    <!-- Buttons stacked vertically -->
</LinearLayout>

<!-- Horizontal arrangement -->
<LinearLayout
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="horizontal">
    
    <Button
        android:layout_width="0dp"
        android:layout_weight="1"
        android:layout_height="wrap_content"
        android:text="Left" />
    
    <Button
        android:layout_width="0dp"
        android:layout_weight="1"
        android:layout_height="wrap_content"
        android:text="Right" />
    
    <!-- Buttons side by side, equal width -->
</LinearLayout>
```

**Weight Distribution** (Divide space proportionally)

```xml
<LinearLayout
    android:layout_width="match_parent"
    android:layout_height="200dp"
    android:orientation="horizontal">
    
    <!-- Takes 2/3 of space -->
    <View
        android:layout_width="0dp"
        android:layout_height="match_parent"
        android:layout_weight="2"
        android:background="@color/red" />
    
    <!-- Takes 1/3 of space -->
    <View
        android:layout_width="0dp"
        android:layout_height="match_parent"
        android:layout_weight="1"
        android:background="@color/blue" />
</LinearLayout>
```

### **FrameLayout - Stack on Top of Each Other**

```xml
<FrameLayout
    android:layout_width="match_parent"
    android:layout_height="300dp"
    android:background="@color/gray">
    
    <!-- Background image -->
    <ImageView
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:src="@drawable/background"
        android:scaleType="centerCrop" />
    
    <!-- Text overlay on top -->
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Profile"
        android:textSize="32sp"
        android:textColor="@color/white"
        android:layout_gravity="center" />
</FrameLayout>
```

### **RelativeLayout - Position Relative to Other Elements**

```xml
<RelativeLayout
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    
    <ImageView
        android:id="@+id/profileImage"
        android:layout_width="100dp"
        android:layout_height="100dp"
        android:layout_alignParentTop="true"
        android:layout_centerHorizontal="true"
        android:src="@drawable/user_profile" />
    
    <TextView
        android:id="@+id/nameText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="John Doe"
        android:layout_below="@id/profileImage"
        android:layout_centerHorizontal="true"
        android:layout_marginTop="16dp"
        android:textSize="20sp" />
    
    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="john@email.com"
        android:layout_below="@id/nameText"
        android:layout_centerHorizontal="true"
        android:layout_marginTop="8dp"
        android:textSize="14sp"
        android:gravity="center" />
</RelativeLayout>
```

### **ConstraintLayout - Professional Layouts (Recommended)**

```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    
    <!-- ImageView pinned to top -->
    <ImageView
        android:id="@+id/profileImage"
        android:layout_width="100dp"
        android:layout_height="100dp"
        android:src="@drawable/user_profile"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_marginTop="24dp" />
    
    <!-- Name below image -->
    <TextView
        android:id="@+id/nameText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="John Doe"
        android:textSize="20sp"
        android:textStyle="bold"
        app:layout_constraintTop_toBottomOf="@id/profileImage"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_marginTop="16dp" />
    
    <!-- Email below name -->
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="john@email.com"
        android:textSize="14sp"
        app:layout_constraintTop_toBottomOf="@id/nameText"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_marginTop="8dp" />
    
    <!-- Button at bottom -->
    <Button
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Edit Profile"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_margin="16dp" />
    
</androidx.constraintlayout.widget.ConstraintLayout>
```

---

## 4️⃣ Common Widgets

### **TextView - Display Text**

```xml
<TextView
    android:id="@+id/myText"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text="Hello World"
    android:textSize="16sp"
    android:textColor="@color/black"
    android:textStyle="bold"
    android:maxLines="2"
    android:ellipsize="end" />
```

### **EditText - User Input**

```xml
<EditText
    android:id="@+id/emailInput"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:hint="Enter email"
    android:inputType="email"
    android:padding="12dp" />

<!-- Common input types: -->
<!-- android:inputType="text" -->
<!-- android:inputType="email" -->
<!-- android:inputType="phone" -->
<!-- android:inputType="number" -->
<!-- android:inputType="password" -->
<!-- android:inputType="date" -->
```

### **Button - Clickable Action**

```xml
<Button
    android:id="@+id/submitButton"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text="Submit"
    android:textSize="16sp" />

<!-- Modern Material Button -->
<com.google.android.material.button.MaterialButton
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text="Click Me"
    android:backgroundTint="@color/blue" />
```

### **ImageView - Display Images**

```xml
<ImageView
    android:id="@+id/profilePhoto"
    android:layout_width="100dp"
    android:layout_height="100dp"
    android:src="@drawable/user_photo"
    android:scaleType="centerCrop"
    android:contentDescription="User Profile Photo" />
```

### **CheckBox - Yes/No Choice**

```xml
<CheckBox
    android:id="@+id/agreeCheckbox"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text="I agree to terms" />
```

### **RadioButton - Select One Option**

```xml
<RadioGroup
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical">
    
    <RadioButton
        android:id="@+id/male"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Male" />
    
    <RadioButton
        android:id="@+id/female"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Female" />
</RadioGroup>
```

### **Spinner - Dropdown Selection**

```xml
<Spinner
    android:id="@+id/countrySpinner"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:entries="@array/countries" />
```

---

## 5️⃣ Real-World Layout Example: Login Screen

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="24dp">
    
    <!-- App Logo -->
    <ImageView
        android:layout_width="100dp"
        android:layout_height="100dp"
        android:src="@drawable/app_logo"
        android:layout_gravity="center_horizontal"
        android:layout_marginBottom="32dp" />
    
    <!-- Title -->
    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Welcome Back!"
        android:textSize="28sp"
        android:textStyle="bold"
        android:gravity="center"
        android:layout_marginBottom="8dp" />
    
    <!-- Subtitle -->
    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Sign in to your account"
        android:textSize="14sp"
        android:gravity="center"
        android:textColor="@color/gray"
        android:layout_marginBottom="32dp" />
    
    <!-- Email Input -->
    <EditText
        android:id="@+id/emailInput"
        android:layout_width="match_parent"
        android:layout_height="48dp"
        android:hint="Email"
        android:inputType="email"
        android:padding="12dp"
        android:background="@drawable/edit_text_background"
        android:layout_marginBottom="16dp" />
    
    <!-- Password Input -->
    <EditText
        android:id="@+id/passwordInput"
        android:layout_width="match_parent"
        android:layout_height="48dp"
        android:hint="Password"
        android:inputType="password"
        android:padding="12dp"
        android:background="@drawable/edit_text_background"
        android:layout_marginBottom="16dp" />
    
    <!-- Forgot Password Link -->
    <TextView
        android:id="@+id/forgotPassword"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Forgot password?"
        android:textColor="@color/blue"
        android:layout_gravity="end"
        android:layout_marginBottom="24dp" />
    
    <!-- Login Button -->
    <Button
        android:id="@+id/loginButton"
        android:layout_width="match_parent"
        android:layout_height="48dp"
        android:text="Sign In"
        android:textSize="16sp"
        android:layout_marginBottom="16dp" />
    
    <!-- Sign Up Link -->
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:gravity="center"
        android:layout_marginTop="auto">
        
        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Don't have an account? " />
        
        <TextView
            android:id="@+id/signUpLink"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Sign Up"
            android:textColor="@color/blue"
            android:textStyle="bold" />
    </LinearLayout>
</LinearLayout>
```

---

## 6️⃣ Accessing Layout Elements in Code

```kotlin
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // Find elements by ID
        val emailInput = findViewById<EditText>(R.id.emailInput)
        val passwordInput = findViewById<EditText>(R.id.passwordInput)
        val loginButton = findViewById<Button>(R.id.loginButton)
        
        // Set listeners
        loginButton.setOnClickListener {
            val email = emailInput.text.toString()
            val password = passwordInput.text.toString()
            login(email, password)
        }
    }
}
```

---

## 🎓 Practice Questions & Answers

### **Q1: What's the difference between match_parent and wrap_content?**
**A**: `match_parent` takes full available space, `wrap_content` takes only needed space.

### **Q2: When should I use ConstraintLayout?**
**A**: Always! It's more powerful and flexible than LinearLayout or RelativeLayout.

### **Q3: What does dp mean?**
**A**: Density-independent pixels. Scales properly across different screen sizes.

### **Q4: How do I center content?**
**A**: Use `android:gravity="center"` to center content inside, `android:layout_gravity` to position in parent.

---

## 💡 Key Takeaways

1. ✅ XML defines UI structure
2. ✅ Use ConstraintLayout for modern layouts
3. ✅ Always use dp/sp for sizes (not px)
4. ✅ LinearLayout for simple stacking
5. ✅ Use padding for inside space, margin for outside
6. ✅ Common attributes: width, height, padding, margin, gravity

---

**Next: [Module 3.1 - Jetpack Compose Basics](10_COMPOSE_BASICS.md)**

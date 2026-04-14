# Module 7.1: Threading & Performance Optimization

## 🔄 Main Thread vs Background Threads

```kotlin
// ❌ WRONG: Blocks UI thread
val users = apiService.getUsers()  // 5 second wait - UI freezes!

// ✅ RIGHT: Use Coroutine on IO thread
viewModelScope.launch {
    val users = withContext(Dispatchers.IO) {
        apiService.getUsers()
    }
    // Update UI on Main thread
    displayUsers(users)
}
```

## 🚀 Performance Best Practices

### **Avoid Memory Leaks**
```kotlin
// ❌ BAD: Memory leak
val listener = View.OnClickListener { /* ... */ }
globalObject.addListener(listener)  // Listener never removed

// ✅ GOOD: Remove listener
override fun onDestroy() {
    globalObject.removeListener(listener)
    super.onDestroy()
}
```

### **LazyColumn Performance**
```kotlin
// ✅ GOOD: Only renders visible items
LazyColumn {
    items(hugeList, key = { it.id }) { item ->
        ItemRow(item)
    }
}

// ❌ BAD: Renders all items
Column {
    hugeList.forEach { item ->
        ItemRow(item)
    }
}
```

### **Image Loading Optimization**
```kotlin
// Use disk cache to avoid re-downloading
val imageLoader = ImageLoader.Builder(context)
    .diskCachePolicy(CachePolicy.ENABLED)
    .memoryCachePolicy(CachePolicy.ENABLED)
    .build()
```

## 🎓 Summary

Performance comes from using right tools: Coroutines, Sequences, LazyColumn, and caching.

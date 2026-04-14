# Module 23: Project 2 - Weather App (API Integration)
## Real-World API Integration & Network Requests

---

## 🎯 Project Overview

Build a **Weather App** that:
- Fetches weather data from API
- Shows current weather with temperature, humidity, wind
- Displays 7-day forecast
- Search for different cities
- Save favorite locations
- Handle errors gracefully
- Show loading states

**Technologies**:
- Retrofit (HTTP client)
- OpenWeatherMap API (free)
- Jetpack Compose (UI)
- Coroutines (Threading)
- Room Database (Favorites)

---

## 📁 Project Structure

```
WeatherApp/
├── api/
│   ├── WeatherApiService.kt
│   ├── RetrofitClient.kt
│   └── models/
│       ├── WeatherResponse.kt
│       └── ForecastResponse.kt
├── data/
│   ├── local/
│   │   ├── FavoriteDao.kt
│   │   └── AppDatabase.kt
│   └── repository/
│       └── WeatherRepository.kt
├── ui/
│   ├── screens/
│   │   ├── WeatherScreen.kt
│   │   └── ForecastScreen.kt
│   └── viewmodels/
│       └── WeatherViewModel.kt
└── MainActivity.kt
```

---

## Step 1️⃣: API Response Models

```kotlin
// api/models/WeatherResponse.kt
package com.example.weatherapp.api.models

import com.google.gson.annotations.SerializedName

data class WeatherResponse(
    val coord: Coordinates,
    val weather: List<Weather>,
    val main: MainWeatherInfo,
    val visibility: Int,
    val wind: Wind,
    val clouds: Clouds,
    val dt: Long,
    val sys: SystemInfo,
    val timezone: Int,
    val id: Int,
    val name: String,
    val cod: Int
)

data class Coordinates(
    val lon: Double,
    val lat: Double
)

data class Weather(
    val id: Int,
    val main: String,
    val description: String,
    val icon: String
)

data class MainWeatherInfo(
    val temp: Double,
    @SerializedName("feels_like")
    val feelsLike: Double,
    @SerializedName("temp_min")
    val tempMin: Double,
    @SerializedName("temp_max")
    val tempMax: Double,
    val pressure: Int,
    val humidity: Int
)

data class Wind(
    val speed: Double,
    val deg: Int,
    val gust: Double? = null
)

data class Clouds(
    val all: Int
)

data class SystemInfo(
    val country: String,
    val sunrise: Long,
    val sunset: Long
)

// Forecast response
data class ForecastResponse(
    val list: List<ForecastItem>,
    val city: City
)

data class ForecastItem(
    val dt: Long,
    val main: MainWeatherInfo,
    val weather: List<Weather>,
    val wind: Wind,
    val clouds: Clouds,
    @SerializedName("dt_txt")
    val dateText: String
)

data class City(
    val id: Int,
    val name: String,
    val coord: Coordinates,
    val country: String,
    val population: Long,
    val timezone: Int,
    val sunrise: Long,
    val sunset: Long
)
```

---

## Step 2️⃣: Retrofit API Service

```kotlin
// api/WeatherApiService.kt
package com.example.weatherapp.api

import com.example.weatherapp.api.models.ForecastResponse
import com.example.weatherapp.api.models.WeatherResponse
import retrofit2.http.GET
import retrofit2.http.Query

interface WeatherApiService {
    
    // Get current weather by city name
    @GET("weather")
    suspend fun getWeatherByCityName(
        @Query("q") cityName: String,
        @Query("appid") apiKey: String,
        @Query("units") units: String = "metric"  // Celsius
    ): WeatherResponse
    
    // Get current weather by coordinates
    @GET("weather")
    suspend fun getWeatherByCoordinates(
        @Query("lat") latitude: Double,
        @Query("lon") longitude: Double,
        @Query("appid") apiKey: String,
        @Query("units") units: String = "metric"
    ): WeatherResponse
    
    // Get 7-day forecast
    @GET("forecast")
    suspend fun getForecast(
        @Query("q") cityName: String,
        @Query("appid") apiKey: String,
        @Query("units") units: String = "metric"
    ): ForecastResponse
    
    // Get forecast by coordinates
    @GET("forecast")
    suspend fun getForecastByCoordinates(
        @Query("lat") latitude: Double,
        @Query("lon") longitude: Double,
        @Query("appid") apiKey: String,
        @Query("units") units: String = "metric"
    ): ForecastResponse
}

// api/RetrofitClient.kt
package com.example.weatherapp.api

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitClient {
    private const val BASE_URL = "https://api.openweathermap.org/data/2.5/"
    
    private val retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .addConverterFactory(GsonConverterFactory.create())
        .build()
    
    val weatherService: WeatherApiService = retrofit.create(WeatherApiService::class.java)
}
```

---

## Step 3️⃣: Local Database (Favorites)

```kotlin
// data/local/FavoriteDao.kt
package com.example.weatherapp.data.local

import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Dao
interface FavoriteDao {
    @Query("SELECT * FROM favorites")
    fun getAllFavorites(): Flow<List<FavoriteCity>>
    
    @Insert
    suspend fun addFavorite(favorite: FavoriteCity)
    
    @Delete
    suspend fun removeFavorite(favorite: FavoriteCity)
    
    @Query("SELECT * FROM favorites WHERE cityName = :cityName")
    suspend fun getFavorite(cityName: String): FavoriteCity?
}

// data/local/AppDatabase.kt
package com.example.weatherapp.data.local

import android.content.Context
import androidx.room.*

@Entity(tableName = "favorites")
data class FavoriteCity(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val cityName: String,
    val country: String,
    val latitude: Double,
    val longitude: Double
)

@Database(entities = [FavoriteCity::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun favoriteDao(): FavoriteDao
    
    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null
        
        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "weather_database"
                ).build()
                INSTANCE = instance
                instance
            }
        }
    }
}
```

---

## Step 4️⃣: Repository with Error Handling

```kotlin
// data/repository/WeatherRepository.kt
package com.example.weatherapp.data.repository

import com.example.weatherapp.api.RetrofitClient
import com.example.weatherapp.api.models.ForecastResponse
import com.example.weatherapp.api.models.WeatherResponse
import com.example.weatherapp.data.local.AppDatabase
import com.example.weatherapp.data.local.FavoriteCity
import kotlinx.coroutines.flow.Flow
import retrofit2.HttpException
import java.io.IOException

class WeatherRepository(private val database: AppDatabase) {
    private val apiService = RetrofitClient.weatherService
    private val apiKey = "YOUR_API_KEY_HERE"  // Get from openweathermap.org
    
    // Get current weather with error handling
    suspend fun getWeatherByCityName(cityName: String): Result<WeatherResponse> {
        return try {
            val result = apiService.getWeatherByCityName(cityName, apiKey)
            Result.success(result)
        } catch (e: HttpException) {
            Result.failure(Exception("HTTP Error: ${e.message}"))
        } catch (e: IOException) {
            Result.failure(Exception("Network Error: Check your internet connection"))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    // Get weather by coordinates
    suspend fun getWeatherByCoordinates(
        latitude: Double,
        longitude: Double
    ): Result<WeatherResponse> {
        return try {
            val result = apiService.getWeatherByCoordinates(latitude, longitude, apiKey)
            Result.success(result)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    // Get forecast with error handling
    suspend fun getForecast(cityName: String): Result<ForecastResponse> {
        return try {
            val result = apiService.getForecast(cityName, apiKey)
            Result.success(result)
        } catch (e: HttpException) {
            if (e.code() == 404) {
                Result.failure(Exception("City not found"))
            } else {
                Result.failure(Exception("HTTP Error: ${e.message}"))
            }
        } catch (e: IOException) {
            Result.failure(Exception("Network Error: Check your internet"))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    // Favorites management
    fun getAllFavorites(): Flow<List<FavoriteCity>> {
        return database.favoriteDao().getAllFavorites()
    }
    
    suspend fun addFavorite(city: FavoriteCity) {
        database.favoriteDao().addFavorite(city)
    }
    
    suspend fun removeFavorite(city: FavoriteCity) {
        database.favoriteDao().removeFavorite(city)
    }
    
    suspend fun isFavorite(cityName: String): Boolean {
        return database.favoriteDao().getFavorite(cityName) != null
    }
}
```

---

## Step 5️⃣: ViewModel with State Management

```kotlin
// ui/viewmodels/WeatherViewModel.kt
package com.example.weatherapp.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.weatherapp.api.models.ForecastItem
import com.example.weatherapp.api.models.WeatherResponse
import com.example.weatherapp.data.local.FavoriteCity
import com.example.weatherapp.data.repository.WeatherRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class WeatherViewModel(private val repository: WeatherRepository) : ViewModel() {
    
    // UI State
    private val _currentWeather = MutableStateFlow<WeatherResponse?>(null)
    val currentWeather: StateFlow<WeatherResponse?> = _currentWeather.asStateFlow()
    
    private val _forecast = MutableStateFlow<List<ForecastItem>>(emptyList())
    val forecast: StateFlow<List<ForecastItem>> = _forecast.asStateFlow()
    
    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()
    
    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error.asStateFlow()
    
    private val _favorites = MutableStateFlow<List<FavoriteCity>>(emptyList())
    val favorites: StateFlow<List<FavoriteCity>> = _favorites.asStateFlow()
    
    private val _isFavorite = MutableStateFlow(false)
    val isFavorite: StateFlow<Boolean> = _isFavorite.asStateFlow()
    
    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery.asStateFlow()
    
    init {
        loadFavorites()
        // Load default city
        searchWeather("London")
    }
    
    fun searchWeather(cityName: String) {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            
            val result = repository.getWeatherByCityName(cityName)
            
            result.onSuccess { weather ->
                _currentWeather.value = weather
                _isFavorite.value = repository.isFavorite(cityName)
                loadForecast(cityName)
            }.onFailure { exception ->
                _error.value = exception.message ?: "Unknown error occurred"
            }
            
            _isLoading.value = false
        }
    }
    
    private fun loadForecast(cityName: String) {
        viewModelScope.launch {
            val result = repository.getForecast(cityName)
            
            result.onSuccess { forecastResponse ->
                // Keep only one item per day (12 PM)
                val dailyForecasts = forecastResponse.list
                    .filter { it.dateText.endsWith("12:00:00") }
                    .take(7)
                _forecast.value = dailyForecasts
            }
        }
    }
    
    private fun loadFavorites() {
        viewModelScope.launch {
            repository.getAllFavorites().collect { favorites ->
                _favorites.value = favorites
            }
        }
    }
    
    fun toggleFavorite() {
        viewModelScope.launch {
            val weather = _currentWeather.value ?: return@launch
            val isFav = _isFavorite.value
            
            if (isFav) {
                val favorite = FavoriteCity(
                    cityName = weather.name,
                    country = weather.sys.country,
                    latitude = weather.coord.lat,
                    longitude = weather.coord.lon
                )
                repository.removeFavorite(favorite)
            } else {
                val favorite = FavoriteCity(
                    cityName = weather.name,
                    country = weather.sys.country,
                    latitude = weather.coord.lat,
                    longitude = weather.coord.lon
                )
                repository.addFavorite(favorite)
            }
            
            _isFavorite.value = !isFav
        }
    }
    
    fun selectFavorite(city: FavoriteCity) {
        searchWeather(city.cityName)
    }
}

class WeatherViewModelFactory(private val repository: WeatherRepository) : 
    ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(WeatherViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return WeatherViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
```

---

## Step 6️⃣: Compose UI

```kotlin
// ui/screens/WeatherScreen.kt
package com.example.weatherapp.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.weatherapp.api.models.WeatherResponse
import com.example.weatherapp.ui.viewmodels.WeatherViewModel
import java.text.SimpleDateFormat
import java.util.*

@Composable
fun WeatherScreen(viewModel: WeatherViewModel) {
    val currentWeather by viewModel.currentWeather.collectAsState()
    val forecast by viewModel.forecast.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    val error by viewModel.error.collectAsState()
    val favorites by viewModel.favorites.collectAsState()
    val isFavorite by viewModel.isFavorite.collectAsState()
    
    var searchQuery by remember { mutableStateOf("") }
    var showFavorites by remember { mutableStateOf(false) }
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Weather App") },
                actions = {
                    IconButton(onClick = { showFavorites = !showFavorites }) {
                        Icon(Icons.Default.Favorite, contentDescription = "Favorites")
                    }
                }
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            // Search Bar
            SearchBar(
                query = searchQuery,
                onQueryChange = { searchQuery = it },
                onSearch = { 
                    if (searchQuery.isNotBlank()) {
                        viewModel.searchWeather(searchQuery)
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
            )
            
            // Favorites Sheet
            if (showFavorites && favorites.isNotEmpty()) {
                FavoritesSheet(
                    favorites = favorites,
                    onSelectFavorite = { city ->
                        viewModel.selectFavorite(city)
                        showFavorites = false
                    }
                )
            }
            
            // Error Message
            if (error != null) {
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    colors = CardDefaults.cardColors(containerColor = Color(0xFFFFCDD2))
                ) {
                    Text(
                        text = "Error: ${error}",
                        modifier = Modifier.padding(16.dp),
                        color = Color(0xFFC62828)
                    )
                }
            }
            
            // Loading
            if (isLoading) {
                CircularProgressIndicator(
                    modifier = Modifier
                        .align(Alignment.CenterHorizontally)
                        .padding(32.dp)
                )
            }
            
            // Current Weather Card
            if (currentWeather != null) {
                CurrentWeatherCard(
                    weather = currentWeather!!,
                    isFavorite = isFavorite,
                    onToggleFavorite = { viewModel.toggleFavorite() }
                )
            }
            
            // Forecast List
            if (forecast.isNotEmpty()) {
                Text(
                    "7-Day Forecast",
                    modifier = Modifier.padding(16.dp),
                    fontSize = 18.sp,
                    style = MaterialTheme.typography.titleLarge
                )
                
                LazyRow(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(forecast) { item ->
                        ForecastCard(forecastItem = item)
                    }
                }
            }
        }
    }
}

@Composable
fun SearchBar(
    query: String,
    onQueryChange: (String) -> Unit,
    onSearch: () -> Unit,
    modifier: Modifier = Modifier
) {
    OutlinedTextField(
        value = query,
        onValueChange = onQueryChange,
        placeholder = { Text("Search city...") },
        leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
        trailingIcon = {
            if (query.isNotEmpty()) {
                IconButton(onClick = onSearch) {
                    Icon(Icons.Default.Search, contentDescription = "Search")
                }
            }
        },
        modifier = modifier,
        singleLine = true
    )
}

@Composable
fun CurrentWeatherCard(
    weather: WeatherResponse,
    isFavorite: Boolean,
    onToggleFavorite: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // City name
            Row(
                modifier = Modifier
                    .fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    "${weather.name}, ${weather.sys.country}",
                    fontSize = 24.sp,
                    style = MaterialTheme.typography.headlineSmall
                )
                IconButton(onClick = onToggleFavorite) {
                    Icon(
                        if (isFavorite) Icons.Default.Favorite else Icons.Default.FavoriteBorder,
                        contentDescription = "Add to favorites",
                        tint = if (isFavorite) Color.Red else Color.Gray
                    )
                }
            }
            
            Spacer(Modifier.height(16.dp))
            
            // Temperature
            Text(
                "${weather.main.temp.toInt()}°C",
                fontSize = 48.sp,
                style = MaterialTheme.typography.headlineLarge
            )
            
            // Weather description
            Text(
                weather.weather.firstOrNull()?.description?.uppercase() ?: "",
                fontSize = 16.sp,
                style = MaterialTheme.typography.bodyLarge
            )
            
            Spacer(Modifier.height(16.dp))
            
            // Weather details
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                WeatherDetail(
                    icon = "💨",
                    label = "Wind",
                    value = "${weather.wind.speed} m/s"
                )
                WeatherDetail(
                    icon = "💧",
                    label = "Humidity",
                    value = "${weather.main.humidity}%"
                )
                WeatherDetail(
                    icon = "👁",
                    label = "Visibility",
                    value = "${weather.visibility / 1000} km"
                )
            }
        }
    }
}

@Composable
fun WeatherDetail(icon: String, label: String, value: String) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(icon, fontSize = 24.sp)
        Text(label, fontSize = 12.sp)
        Text(value, fontSize = 14.sp, style = MaterialTheme.typography.bodySmall)
    }
}

@Composable
fun ForecastCard(forecastItem: com.example.weatherapp.api.models.ForecastItem) {
    Card(
        modifier = Modifier.width(100.dp)
    ) {
        Column(
            modifier = Modifier.padding(8.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Date
            val date = SimpleDateFormat("MMM dd", Locale.getDefault())
                .format(Date(forecastItem.dt * 1000))
            Text(date, fontSize = 12.sp)
            
            // Temperature
            Text("${forecastItem.main.temp.toInt()}°C", fontSize = 14.sp)
            
            // Weather icon emoji
            Text(
                getWeatherEmoji(forecastItem.weather.firstOrNull()?.main ?: ""),
                fontSize = 20.sp
            )
        }
    }
}

@Composable
fun FavoritesSheet(
    favorites: List<com.example.weatherapp.data.local.FavoriteCity>,
    onSelectFavorite: (com.example.weatherapp.data.local.FavoriteCity) -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
    ) {
        LazyColumn {
            items(favorites) { city ->
                ListItem(
                    headlineContent = { Text(city.cityName) },
                    supportingContent = { Text(city.country) },
                    modifier = Modifier.clickable { onSelectFavorite(city) }
                )
            }
        }
    }
}

private fun getWeatherEmoji(weatherMain: String): String {
    return when (weatherMain.lowercase()) {
        "clear" -> "☀️"
        "clouds" -> "☁️"
        "rain" -> "🌧️"
        "thunderstorm" -> "⛈️"
        "snow" -> "❄️"
        "mist", "smoke", "haze", "dust", "fog", "sand", "ash", "squall", "tornado" -> "🌫️"
        else -> "🌤️"
    }
}
```

---

## Step 7️⃣: Dependencies

```gradle
dependencies {
    // Retrofit
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    implementation("com.google.code.gson:gson:2.10.1")
    
    // Room
    implementation("androidx.room:room-runtime:2.5.2")
    kapt("androidx.room:room-compiler:2.5.2")
    implementation("androidx.room:room-ktx:2.5.2")
    
    // Compose & Lifecycle
    implementation("androidx.compose.ui:ui:1.5.0")
    implementation("androidx.compose.material3:material3:1.1.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.6.1")
    implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.6.1")
}
```

---

## 🎓 Key Learning Points

✅ HTTP requests with Retrofit
✅ API integration and JSON parsing
✅ Error handling and validation
✅ Loading & error states
✅ Working with external APIs
✅ Coroutines for network calls
✅ Local database persistence
✅ Complex UI with weather data

---

## 📚 Exercises

1. Add temperature unit toggle (Celsius/Fahrenheit)
2. Add hourly forecast (24 hours)
3. Add UV index and air quality
4. Add weather alerts
5. Add multiple location search history
6. Add weather notifications
7. Add rain probability
8. Add weather maps integration

---

**Next: [Module 26 - Interview Questions](26_INTERVIEW_QUESTIONS.md)**

// app/src/main/kotlin/com/example/androidmaster/di/NetworkModule.kt
package com.example.androidmaster.di

import android.content.Context
import com.example.androidmaster.data.database.AppDatabase
import com.example.androidmaster.data.remote.ApiService
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    
    private const val BASE_URL = "https://api.example.com/"
    
    @Provides
    @Singleton
    fun provideHttpClient(): OkHttpClient {
        val logger = HttpLoggingInterceptor()
        logger.level = HttpLoggingInterceptor.Level.BODY
        
        return OkHttpClient.Builder()
            .addInterceptor(logger)
            .build()
    }
    
    @Provides
    @Singleton
    fun provideRetrofit(okHttpClient: OkHttpClient): Retrofit {
        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }
    
    @Provides
    @Singleton
    fun provideApiService(retrofit: Retrofit): ApiService {
        return retrofit.create(ApiService::class.java)
    }
}

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {
    
    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AppDatabase {
        return AppDatabase.getInstance(context)
    }
    
    @Provides
    @Singleton
    fun provideUserDao(database: AppDatabase) = database.userDao()
    
    @Provides
    @Singleton
    fun providePostDao(database: AppDatabase) = database.postDao()
    
    @Provides
    @Singleton
    fun provideTodoDao(database: AppDatabase) = database.todoDao()
    
    @Provides
    @Singleton
    fun provideContactDao(database: AppDatabase) = database.contactDao()
}

@Module
@InstallIn(SingletonComponent::class)
object RepositoryModule {
    
    @Provides
    @Singleton
    fun provideUserRepository(
        apiService: ApiService,
        userDao: com.example.androidmaster.data.database.UserDao
    ): com.example.androidmaster.data.repository.UserRepository {
        return com.example.androidmaster.data.repository.UserRepository(apiService, userDao)
    }
    
    @Provides
    @Singleton
    fun providePostRepository(
        apiService: ApiService,
        postDao: com.example.androidmaster.data.database.PostDao
    ): com.example.androidmaster.data.repository.PostRepository {
        return com.example.androidmaster.data.repository.PostRepository(apiService, postDao)
    }
    
    @Provides
    @Singleton
    fun provideTodoRepository(
        todoDao: com.example.androidmaster.data.database.TodoDao
    ): com.example.androidmaster.data.repository.TodoRepository {
        return com.example.androidmaster.data.repository.TodoRepository(todoDao)
    }
}

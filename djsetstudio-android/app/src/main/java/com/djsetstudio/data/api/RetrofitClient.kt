package com.djsetstudio.data.api

import android.content.Context
import okhttp3.Interceptor
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

/**
 * Retrofit客户端管理器
 */
object RetrofitClient {

    // TODO: 修改为你的API服务器地址
    private const val BASE_URL = "https://your-api-domain.com/api/"
    // 本地测试使用: "http://10.0.2.2:5000/api/" (Android模拟器访问本机)

    private const val PREFS_NAME = "djset_prefs"
    private const val KEY_TOKEN = "access_token"

    private var token: String? = null

    /**
     * 设置认证token
     */
    fun setAuthToken(context: Context, token: String) {
        this.token = token
        context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
            .edit()
            .putString(KEY_TOKEN, token)
            .apply()
    }

    /**
     * 获取认证token
     */
    fun getAuthToken(context: Context): String? {
        if (token == null) {
            token = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
                .getString(KEY_TOKEN, null)
        }
        return token
    }

    /**
     * 清除认证token
     */
    fun clearAuthToken(context: Context) {
        token = null
        context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
            .edit()
            .remove(KEY_TOKEN)
            .apply()
    }

    /**
     * 创建认证拦截器
     */
    private fun createAuthInterceptor(context: Context): Interceptor {
        return Interceptor { chain ->
            val originalRequest = chain.request()
            val token = getAuthToken(context)

            val request = if (token != null) {
                originalRequest.newBuilder()
                    .header("Authorization", "Bearer $token")
                    .build()
            } else {
                originalRequest
            }

            chain.proceed(request)
        }
    }

    /**
     * 创建OkHttpClient
     */
    private fun createOkHttpClient(context: Context): OkHttpClient {
        val loggingInterceptor = HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        }

        return OkHttpClient.Builder()
            .addInterceptor(createAuthInterceptor(context))
            .addInterceptor(loggingInterceptor)
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .build()
    }

    /**
     * 创建Retrofit实例
     */
    fun create(context: Context): ApiService {
        val retrofit = Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(createOkHttpClient(context))
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        return retrofit.create(ApiService::class.java)
    }
}

package com.djsetstudio.data.repository

import android.content.Context
import com.djsetstudio.data.api.ApiService
import com.djsetstudio.data.api.RetrofitClient
import com.djsetstudio.data.model.*

/**
 * 数据仓库 - 处理所有数据操作
 */
class DJSetRepository(private val context: Context) {

    private val api: ApiService = RetrofitClient.create(context)

    // ==================== 认证相关 ====================

    suspend fun login(email: String, password: String): Result<LoginResponse> {
        return try {
            val response = api.login(LoginRequest(email, password))
            if (response.isSuccessful && response.body() != null) {
                val loginResponse = response.body()!!
                // 保存token
                RetrofitClient.setAuthToken(context, loginResponse.accessToken)
                Result.success(loginResponse)
            } else {
                Result.failure(Exception("登录失败: ${response.message()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun register(email: String, password: String, username: String? = null): Result<User> {
        return try {
            val response = api.register(RegisterRequest(email, password, username))
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("注册失败: ${response.message()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    fun logout() {
        RetrofitClient.clearAuthToken(context)
    }

    // ==================== 歌曲相关 ====================

    suspend fun getTracks(): Result<List<Track>> {
        return try {
            val response = api.getTracks()
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!.items)
            } else {
                Result.failure(Exception("获取歌曲列表失败"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun searchTracks(
        keyword: String? = null,
        genre: String? = null,
        minBpm: Float? = null,
        maxBpm: Float? = null
    ): Result<List<Track>> {
        return try {
            val response = api.searchTracks(keyword, null, genre, minBpm, maxBpm)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!.items)
            } else {
                Result.failure(Exception("搜索失败"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getTrackRecommendations(trackId: Int, limit: Int = 10): Result<List<Track>> {
        return try {
            val response = api.getTrackRecommendations(trackId, limit)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!.items)
            } else {
                Result.failure(Exception("获取推荐失败"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    // ==================== Set相关 ====================

    suspend fun getSets(): Result<List<DJSet>> {
        return try {
            val response = api.getSets()
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!.items)
            } else {
                Result.failure(Exception("获取Sets失败"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getSet(setId: Int): Result<DJSet> {
        return try {
            val response = api.getSet(setId)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("获取Set详情失败"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getSetRecommendations(setId: Int, limit: Int = 10): Result<List<Track>> {
        return try {
            val response = api.getSetRecommendations(setId, mapOf("limit" to limit))
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!.items)
            } else {
                Result.failure(Exception("获取推荐失败"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

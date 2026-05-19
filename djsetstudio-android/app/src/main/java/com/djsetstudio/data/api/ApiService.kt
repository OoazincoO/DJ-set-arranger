package com.djsetstudio.data.api

import com.djsetstudio.data.model.*
import retrofit2.Response
import retrofit2.http.*

/**
 * DJSet Studio API接口
 */
interface ApiService {

    // ==================== 认证相关 ====================

    @POST("auth/register")
    suspend fun register(@Body request: RegisterRequest): Response<User>

    @POST("auth/login")
    suspend fun login(@Body request: LoginRequest): Response<LoginResponse>

    @GET("auth/me")
    suspend fun getCurrentUser(): Response<User>

    // ==================== 歌曲相关 ====================

    @GET("tracks")
    suspend fun getTracks(): Response<ListResponse<Track>>

    @GET("tracks/search")
    suspend fun searchTracks(
        @Query("keyword") keyword: String? = null,
        @Query("artist") artist: String? = null,
        @Query("genre") genre: String? = null,
        @Query("min_bpm") minBpm: Float? = null,
        @Query("max_bpm") maxBpm: Float? = null
    ): Response<ListResponse<Track>>

    @GET("tracks/{id}")
    suspend fun getTrack(@Path("id") id: Int): Response<Track>

    @GET("tracks/{id}/recommend")
    suspend fun getTrackRecommendations(
        @Path("id") id: Int,
        @Query("limit") limit: Int = 10
    ): Response<ListResponse<Track>>

    // ==================== Set相关 ====================

    @GET("sets")
    suspend fun getSets(): Response<ListResponse<DJSet>>

    @GET("sets/{id}")
    suspend fun getSet(@Path("id") id: Int): Response<DJSet>

    @POST("sets/{id}/recommend")
    suspend fun getSetRecommendations(
        @Path("id") id: Int,
        @Body body: Map<String, Int>
    ): Response<ListResponse<Track>>

    @GET("sets/{id}/tracks")
    suspend fun getSetTracks(@Path("id") id: Int): Response<ListResponse<Track>>
}

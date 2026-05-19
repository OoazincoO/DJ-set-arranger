package com.djsetstudio.data.model

import com.google.gson.annotations.SerializedName

/**
 * 用户模型
 */
data class User(
    @SerializedName("id") val id: Int,
    @SerializedName("email") val email: String,
    @SerializedName("username") val username: String?,
    @SerializedName("created_at") val createdAt: String?
)

/**
 * 歌曲模型
 */
data class Track(
    @SerializedName("id") val id: Int,
    @SerializedName("title") val title: String,
    @SerializedName("artist") val artist: String?,
    @SerializedName("bpm") val bpm: Float?,
    @SerializedName("genre") val genre: String?,
    @SerializedName("key") val key: String?,
    @SerializedName("duration_sec") val durationSec: Int?,
    @SerializedName("cover_url") val coverUrl: String?
)

/**
 * DJ Set模型
 */
data class DJSet(
    @SerializedName("id") val id: Int,
    @SerializedName("name") val name: String,
    @SerializedName("description") val description: String?,
    @SerializedName("cover_url") val coverUrl: String?,
    @SerializedName("track_count") val trackCount: Int?,
    @SerializedName("track_ids") val trackIds: List<Int>?,
    @SerializedName("tracks") val tracks: List<Track>?,
    @SerializedName("created_at") val createdAt: String
)

/**
 * 登录请求
 */
data class LoginRequest(
    @SerializedName("email") val email: String,
    @SerializedName("password") val password: String
)

/**
 * 登录响应
 */
data class LoginResponse(
    @SerializedName("access_token") val accessToken: String,
    @SerializedName("user") val user: User
)

/**
 * 注册请求
 */
data class RegisterRequest(
    @SerializedName("email") val email: String,
    @SerializedName("password") val password: String,
    @SerializedName("username") val username: String?
)

/**
 * 通用列表响应
 */
data class ListResponse<T>(
    @SerializedName("items") val items: List<T>,
    @SerializedName("count") val count: Int?
)

/**
 * 错误响应
 */
data class ErrorResponse(
    @SerializedName("error") val error: String
)

package com.djsetstudio.ui

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.djsetstudio.R
import com.djsetstudio.data.api.RetrofitClient
import com.djsetstudio.data.repository.DJSetRepository
import com.google.android.material.floatingactionbutton.FloatingActionButton
import kotlinx.coroutines.launch

/**
 * 主Activity - 显示Sets列表
 */
class MainActivity : AppCompatActivity() {

    private lateinit var repository: DJSetRepository
    private lateinit var recyclerView: RecyclerView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        repository = DJSetRepository(this)

        // 检查是否已登录
        checkLoginStatus()

        // 初始化UI
        initViews()

        // 加载Sets列表
        loadSets()
    }

    private fun checkLoginStatus() {
        val token = RetrofitClient.getAuthToken(this)
        if (token == null) {
            // 未登录，跳转到登录页
            startActivity(Intent(this, LoginActivity::class.java))
            finish()
        }
    }

    private fun initViews() {
        recyclerView = findViewById(R.id.recyclerViewSets)
        recyclerView.layoutManager = LinearLayoutManager(this)

        // 浮动按钮 - 刷新
        findViewById<FloatingActionButton>(R.id.fabRefresh)?.setOnClickListener {
            loadSets()
        }
    }

    private fun loadSets() {
        lifecycleScope.launch {
            val result = repository.getSets()
            result.onSuccess { sets ->
                // TODO: 使用Adapter显示Sets
                Toast.makeText(
                    this@MainActivity,
                    "加载了 ${sets.size} 个Sets",
                    Toast.LENGTH_SHORT
                ).show()
            }.onFailure { error ->
                Toast.makeText(
                    this@MainActivity,
                    "加载失败: ${error.message}",
                    Toast.LENGTH_SHORT
                ).show()
            }
        }
    }

    override fun onResume() {
        super.onResume()
        loadSets()
    }
}

<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <h1 class="text-8xl font-bold text-gray-800">404</h1>
      <h2 class="text-2xl font-medium text-gray-600 mt-4">页面不存在</h2>
      <p class="text-gray-500 mt-2">您访问的页面不存在或已被删除</p>
      <el-button type="primary" class="mt-8" @click="$router.push('/')">返回首页</el-button>
    </div>
  </div>
</template>

<style scoped>
.not-found-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f2f5;
}

.not-found-content {
  text-align: center;
  padding: 40px;
}
</style> 
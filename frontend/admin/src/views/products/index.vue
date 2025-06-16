<template>
  <div class="products-container">
    <div class="page-header flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold">特产管理</h2>
      <el-button type="primary" @click="openAddDialog">添加特产</el-button>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="mb-4">
      <div class="flex flex-wrap gap-4">
        <el-input
          v-model="searchQuery"
          placeholder="搜索特产名称/商户名称"
          class="w-64"
          clearable
          @clear="fetchProducts"
          @keyup.enter="fetchProducts"
        >
          <template #append>
            <el-button :icon="Search" @click="fetchProducts" />
          </template>
        </el-input>

        <el-select v-model="filterStatus" placeholder="状态筛选" class="w-32" @change="fetchProducts">
          <el-option label="全部" value="" />
          <el-option label="上架中" value="active" />
          <el-option label="已下架" value="inactive" />
          <el-option label="待审核" value="pending" />
        </el-select>

        <el-select v-model="filterCategory" placeholder="分类筛选" class="w-40" @change="fetchProducts">
          <el-option label="全部分类" value="" />
          <el-option label="农产品" value="agricultural" />
          <el-option label="手工艺品" value="handicraft" />
          <el-option label="食品" value="food" />
          <el-option label="其他" value="other" />
        </el-select>
      </div>
    </el-card>

    <!-- 特产列表 -->
    <el-card v-loading="loading">
      <el-table :data="products" style="width: 100%">
        <el-table-column label="图片" width="100">
          <template #default="scope">
            <el-image 
              style="width: 60px; height: 60px" 
              :src="scope.row.cover_image" 
              fit="cover"
              :preview-src-list="[scope.row.cover_image]"
              preview-teleported
            >
              <template #error>
                <div class="image-slot">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="名称" min-width="150" />
        <el-table-column prop="merchant_name" label="所属商户" width="150" />
        <el-table-column prop="category" label="分类" width="100">
          <template #default="scope">
            <el-tag>{{ getCategoryText(scope.row.category) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="price" label="价格" width="100">
          <template #default="scope">
            <span class="text-orange-500">¥{{ parseFloat(scope.row.price).toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="stock" label="库存" width="80" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button-group>
              <el-button type="primary" size="small" text @click="viewProductDetail(scope.row)">
                详情
              </el-button>
              <el-button 
                v-if="scope.row.status === 'pending'"
                type="success" 
                size="small" 
                text
                @click="reviewProduct(scope.row, 'approved')"
              >
                通过
              </el-button>
              <el-button 
                v-if="scope.row.status === 'pending'"
                type="danger" 
                size="small" 
                text
                @click="reviewProduct(scope.row, 'rejected')"
              >
                拒绝
              </el-button>
              <el-button 
                v-if="scope.row.status !== 'pending'"
                :type="scope.row.status === 'active' ? 'warning' : 'success'" 
                size="small" 
                text
                @click="toggleProductStatus(scope.row)"
              >
                {{ scope.row.status === 'active' ? '下架' : '上架' }}
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="flex justify-center mt-4">
        <el-pagination
          :current-page="currentPage"
          :page-size="pageSize"
          :page-sizes="[10, 20, 30, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

const router = useRouter()

// 数据
const products = ref([])  // 改为空数组
const loading = ref(false)
const searchQuery = ref('')
const filterStatus = ref('')
const filterCategory = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)  // 改为0，而不是硬编码的3

// 获取特产列表
// 导入API
import {
  getProductList,
  updateProductStatus,
  deleteProduct,
  batchUpdateProducts
} from '@/api/product'

// 更新fetchProducts函数
const fetchProducts = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value,
      status: filterStatus.value,
      category: filterCategory.value
    }
    
    const response = await getProductList(params)
    console.log('API返回的完整数据:', response.data)
    console.log('results数组长度:', response.data.results?.length)
    console.log('count值:', response.data.count)
    products.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    console.error('获取产品列表失败:', error)
    ElMessage.error('获取产品列表失败')
  } finally {
    loading.value = false
  }
}

// 更新产品状态
const handleStatusChange = async (product, status) => {
  try {
    await updateProductStatus(product.id, status)
    ElMessage.success('状态更新成功')
    await fetchProducts()
  } catch (error) {
    console.error('更新产品状态失败:', error)
    ElMessage.error('更新产品状态失败')
  }
}

// 删除产品
const handleDelete = async (product) => {
  try {
    await ElMessageBox.confirm('确定要删除这个产品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await deleteProduct(product.id)
    ElMessage.success('删除成功')
    await fetchProducts()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除产品失败:', error)
      ElMessage.error('删除产品失败')
    }
  }
}
// 查看特产详情
const viewProductDetail = (product) => {
  router.push(`/products/${product.id}`)
}

// 审核特产
const reviewProduct = (product, action) => {
  ElMessage.success(`已${action === 'approved' ? '通过' : '拒绝'}特产"${product.name}"的审核`)
  product.status = action === 'approved' ? 'active' : 'rejected'
}

// 切换特产状态
const toggleProductStatus = (product) => {
  const newStatus = product.status === 'active' ? 'inactive' : 'active'
  product.status = newStatus
  ElMessage.success(`已${newStatus === 'active' ? '上架' : '下架'}特产"${product.name}"`)
}

// 打开添加特产对话框
const openAddDialog = () => {
  // 实际项目中应该打开添加特产的对话框
  ElMessage.info('添加特产功能待实现')
}

// 获取分类文本
const getCategoryText = (category) => {
  const categories = {
    'agricultural': '农产品',
    'handicraft': '手工艺品',
    'food': '食品',
    'other': '其他'
  }
  return categories[category] || '未知'
}

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    'active': 'success',
    'inactive': 'info',
    'pending': 'warning',
    'rejected': 'danger'
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const texts = {
    'active': '上架中',
    'inactive': '已下架',
    'pending': '待审核',
    'rejected': '已拒绝'
  }
  return texts[status] || '未知'
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  fetchProducts()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchProducts()
}

// 初始化
fetchProducts()
</script>

<style scoped>
.products-container {
  padding: 20px;
}
</style>
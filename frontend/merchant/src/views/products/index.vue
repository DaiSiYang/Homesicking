<template>
  <div class="products-container">
    <div class="flex justify-between items-center mb-4">
      <div class="page-title">特产管理</div>
      <router-link to="/products/create">
        <el-button type="primary" icon="Plus">添加特产</el-button>
      </router-link>
    </div>
    
    <!-- 搜索和筛选 -->
    <el-card shadow="never" class="mb-4">
      <div class="flex flex-wrap gap-4">
        <el-input
          v-model="queryParams.keyword"
          placeholder="搜索特产名称/描述"
          class="w-64"
          clearable
          @clear="handleSearch"
        >
          <template #append>
            <el-button icon="Search" @click="handleSearch" />
          </template>
        </el-input>
        
        <el-select v-model="queryParams.category" placeholder="商品分类" clearable @change="handleSearch" class="w-32">
          <el-option label="全部" value="" />
          <el-option label="食品" value="食品" />
          <el-option label="饮品" value="饮品" />
          <el-option label="工艺品" value="工艺品" />
          <el-option label="其他" value="其他" />
        </el-select>
        
        <el-select v-model="queryParams.status" placeholder="商品状态" clearable @change="handleSearch" class="w-32">
          <el-option label="全部" value="" />
          <el-option label="在售" value="在售" />
          <el-option label="下架" value="下架" />
          <el-option label="售罄" value="售罄" />
        </el-select>
      </div>
    </el-card>
    
    <!-- 商品列表 -->
    <el-card shadow="never" v-loading="loading">
      <el-table :data="productList" style="width: 100%" border>
        <el-table-column label="商品图片" width="120">
          <template #default="scope">
            <el-image 
              style="width: 80px; height: 80px"
              :src="scope.row.images && scope.row.images.length > 0 ? scope.row.images[0] : ''"
              fit="cover"
              :preview-src-list="scope.row.images"
            >
              <template #error>
                <div class="flex items-center justify-center h-full bg-gray-100">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
          </template>
        </el-table-column>
        
        <el-table-column prop="name" label="商品名称" min-width="150" />
        
        <el-table-column prop="price" label="价格" width="100">
          <template #default="scope">
            <span class="text-orange-500">¥{{ scope.row.price }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="stock" label="库存" width="80" />
        
        <el-table-column prop="sales" label="销量" width="80" />
        
        <el-table-column prop="category" label="分类" width="100" />
        
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button 
              type="primary" 
              link 
              icon="Edit" 
              @click="handleEdit(scope.row)"
            >
              编辑
            </el-button>
            
            <el-button 
              type="primary" 
              link 
              :icon="scope.row.status === '在售' ? 'SoldOut' : 'Sell'"
              @click="handleToggleStatus(scope.row)"
            >
              {{ scope.row.status === '在售' ? '下架' : '上架' }}
            </el-button>
            
            <el-popconfirm
              title="确定要删除这个特产吗？"
              @confirm="handleDelete(scope.row.id)"
            >
              <template #reference>
                <el-button type="danger" link icon="Delete">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="flex justify-end mt-4">
        <el-pagination
          :current-page="queryParams.page"
          :page-size="queryParams.limit"
          :page-sizes="[10, 20, 50, 100]"
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
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getProductList, updateProduct, deleteProduct } from '@/api/product'

const router = useRouter()
const loading = ref(false)
const productList = ref([])
const total = ref(0)

// 查询参数
const queryParams = reactive({
  page: 1,
  limit: 10,
  keyword: '',
  category: '',
  status: ''
})

// 获取商品状态类型
const getStatusType = (status) => {
  switch (status) {
    case '在售':
      return 'success'
    case '下架':
      return 'info'
    case '售罄':
      return 'danger'
    default:
      return ''
  }
}

// 获取商品列表
const getList = async () => {
  loading.value = true
  try {
    const res = await getProductList(queryParams)
    productList.value = res.data.list
    total.value = res.data.total
  } catch (error) {
    console.error('获取特产列表失败:', error)
    ElMessage.error('获取特产列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  queryParams.page = 1
  getList()
}

// 编辑商品
const handleEdit = (row) => {
  router.push(`/products/${row.id}/edit`)
}

// 切换商品状态
const handleToggleStatus = async (row) => {
  const newStatus = row.status === '在售' ? '下架' : '在售'
  try {
    await updateProduct(row.id, { status: newStatus })
    ElMessage.success(`商品已${newStatus}`)
    row.status = newStatus
  } catch (error) {
    console.error('更新商品状态失败:', error)
    ElMessage.error('更新商品状态失败')
  }
}

// 删除商品
const handleDelete = async (id) => {
  try {
    await deleteProduct(id)
    ElMessage.success('删除成功')
    getList()
  } catch (error) {
    console.error('删除特产失败:', error)
    ElMessage.error('删除特产失败')
  }
}

// 每页条数改变
const handleSizeChange = (val) => {
  queryParams.limit = val
  getList()
}

// 页码改变
const handleCurrentChange = (val) => {
  queryParams.page = val
  getList()
}

// 页面加载时获取数据
onMounted(() => {
  getList()
})
</script>

<style scoped>
.products-container {
  padding: 20px;
}
</style> 
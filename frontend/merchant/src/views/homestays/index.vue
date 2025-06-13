<template>
  <div class="homestay-container">
    <div class="page-header flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold">民宿管理</h2>
      <el-button type="primary" @click="$router.push('/homestays/create')">添加民宿</el-button>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="mb-4">
      <div class="flex flex-wrap gap-4">
        <el-input
          v-model="searchQuery"
          placeholder="搜索民宿名称"
          class="w-64"
          clearable
          @clear="fetchHomestays"
          @keyup.enter="fetchHomestays"
        >
          <template #append>
            <el-button :icon="Search" @click="fetchHomestays" />
          </template>
        </el-input>

        <el-select v-model="filterStatus" placeholder="状态筛选" class="w-32" @change="fetchHomestays">
          <el-option label="全部" value="" />
          <el-option label="上架中" value="active" />
          <el-option label="已下架" value="inactive" />
        </el-select>
      </div>
    </el-card>

    <!-- 民宿列表 -->
    <el-card v-loading="loading">
      <el-table :data="homestays" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="民宿名称" min-width="180" />
        <el-table-column label="封面图" width="120">
          <template #default="scope">
            <el-image 
              style="width: 80px; height: 60px" 
              :src="scope.row.cover_image" 
              fit="cover"
              :preview-src-list="[scope.row.cover_image]"
            />
          </template>
        </el-table-column>
        <el-table-column prop="price" label="价格/晚" width="120">
          <template #default="scope">
            <span class="text-orange-500">¥{{ scope.row.price }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="address" label="地址" min-width="200" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'active' ? 'success' : 'info'">
              {{ scope.row.status === 'active' ? '上架中' : '已下架' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button-group>
              <el-button type="primary" size="small" text @click="$router.push(`/homestays/${scope.row.id}/edit`)">
                编辑
              </el-button>
              <el-button 
                :type="scope.row.status === 'active' ? 'danger' : 'success'" 
                size="small" 
                text
                @click="toggleHomestayStatus(scope.row)"
              >
                {{ scope.row.status === 'active' ? '下架' : '上架' }}
              </el-button>
              <el-button type="danger" size="small" text @click="confirmDelete(scope.row)">
                删除
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="flex justify-center mt-4">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 30, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="fetchHomestays"
          @current-change="fetchHomestays"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { getHomestayList, updateHomestay, deleteHomestayById } from '@/api/homestay'

// 数据
const homestays = ref([
  {
    id: 1,
    name: '山水间农家乐',
    cover_image: 'https://via.placeholder.com/300x200',
    price: 298,
    address: '浙江省杭州市临安区太湖源镇',
    status: 'active'
  },
  {
    id: 2,
    name: '青山绿水民宿',
    cover_image: 'https://via.placeholder.com/300x200',
    price: 358,
    address: '浙江省杭州市临安区天目山镇',
    status: 'active'
  },
  {
    id: 3,
    name: '田园风光小屋',
    cover_image: 'https://via.placeholder.com/300x200',
    price: 268,
    address: '浙江省杭州市桐庐县',
    status: 'inactive'
  }
])
const loading = ref(false)
const searchQuery = ref('')
const filterStatus = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(3)

// 获取民宿列表
const fetchHomestays = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      limit: pageSize.value,
      search: searchQuery.value,
      status: filterStatus.value
    }
    
    const res = await getHomestayList(params)
    if (res.code === 200) {
      homestays.value = res.data.results || res.data.list || []
      total.value = res.data.total || res.data.count || 0
    }
  } catch (error) {
    console.error('获取民宿列表失败:', error)
    ElMessage.error('获取民宿列表失败')
  } finally {
    loading.value = false
  }
}

// 切换民宿状态
const toggleHomestayStatus = async (homestay) => {
  try {
    await updateHomestay(homestay.id, { 
      status: homestay.status === 'active' ? 'inactive' : 'active' 
    })
    
    homestay.status = homestay.status === 'active' ? 'inactive' : 'active'
    ElMessage.success(`${homestay.name} 已${homestay.status === 'active' ? '上架' : '下架'}`)
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 删除民宿
const deleteHomestay = async (homestay) => {
  try {
    await deleteHomestayById(homestay.id)
    
    homestays.value = homestays.value.filter(item => item.id !== homestay.id)
    ElMessage.success('删除成功')
  } catch (error) {
    console.error('删除失败:', error)
    ElMessage.error('删除失败')
  }
}

// 确认删除
const confirmDelete = (homestay) => {
  ElMessageBox.confirm(`确定要删除"${homestay.name}"吗？此操作不可恢复。`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    deleteHomestay(homestay)
  }).catch(() => {})
}


// 初始化
onMounted(() => {
  fetchHomestays()
})
</script>

<style scoped>
.homestay-container {
  padding: 20px;
}
</style>

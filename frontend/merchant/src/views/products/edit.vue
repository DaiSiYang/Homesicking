<template>
  <div class="edit-product-container">
    <div class="flex items-center mb-4">
      <el-button icon="Back" @click="goBack">返回</el-button>
      <div class="page-title ml-2">编辑特产</div>
    </div>
    
    <el-card shadow="never" v-loading="loading">
      <el-form 
        ref="productFormRef" 
        :model="productForm" 
        :rules="rules" 
        label-width="100px" 
        label-position="right"
        status-icon
      >
        <el-form-item label="特产名称" prop="name">
          <el-input v-model="productForm.name" placeholder="请输入特产名称" />
        </el-form-item>
        
        <el-form-item label="特产分类" prop="category">
          <el-select v-model="productForm.category" placeholder="请选择特产分类" class="w-full">
            <el-option label="食品" value="食品" />
            <el-option label="饮品" value="饮品" />
            <el-option label="工艺品" value="工艺品" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="价格" prop="price">
          <el-input-number 
            v-model="productForm.price" 
            :min="0" 
            :precision="2" 
            :step="0.1" 
            controls-position="right"
          />
        </el-form-item>
        
        <el-form-item label="库存" prop="stock">
          <el-input-number 
            v-model="productForm.stock" 
            :min="0" 
            :precision="0" 
            :step="1" 
            controls-position="right"
          />
        </el-form-item>
        
        <el-form-item label="特产图片" prop="images">
          <el-upload
            :file-list="fileList"
            action="#"
            list-type="picture-card"
            :http-request="uploadImage"
            :limit="5"
            :on-exceed="handleExceed"
            :before-upload="beforeUpload"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        
        <el-form-item label="特产描述" prop="description">
          <el-input 
            v-model="productForm.description" 
            type="textarea" 
            :rows="4" 
            placeholder="请输入特产描述"
          />
        </el-form-item>
        
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="productForm.status">
            <el-radio value="在售">在售</el-radio>
            <el-radio value="下架">下架</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="submitting">保存</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getProductDetail, updateProduct, uploadProductImage } from '@/api/product'

const router = useRouter()
const route = useRoute()
const productId = route.params.id
const productFormRef = ref(null)
const loading = ref(false)
const submitting = ref(false)
const fileList = ref([])

// 表单数据
const productForm = reactive({
  name: '',
  category: '',
  price: 0,
  stock: 0,
  description: '',
  images: [],
  status: '在售'
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入特产名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择特产分类', trigger: 'change' }
  ],
  price: [
    { required: true, message: '请输入价格', trigger: 'blur' },
    { type: 'number', min: 0, message: '价格不能小于0', trigger: 'blur' }
  ],
  stock: [
    { required: true, message: '请输入库存', trigger: 'blur' },
    { type: 'number', min: 0, message: '库存不能小于0', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入特产描述', trigger: 'blur' },
    { min: 10, max: 500, message: '长度在 10 到 500 个字符', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择商品状态', trigger: 'change' }
  ]
}

// 获取特产详情
const getDetail = async () => {
  loading.value = true
  try {
    const res = await getProductDetail(productId)
    
    if (res.code === 200) {
      const data = res.data
      
      // 填充表单数据
      Object.keys(productForm).forEach(key => {
        if (data[key] !== undefined) {
          productForm[key] = data[key]
        }
      })
      
      // 处理图片列表
      if (data.images && data.images.length) {
        fileList.value = data.images.map((url, index) => ({
          name: `图片${index + 1}`,
          url
        }))
      }
    }
  } catch (error) {
    console.error('获取特产详情失败:', error)
    ElMessage.error('获取特产详情失败')
  } finally {
    loading.value = false
  }
}

// 返回上一页
const goBack = () => {
  router.push('/products')
}

// 上传前验证
const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2
  
  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }
  
  return true
}

// 超出数量限制
const handleExceed = () => {
  ElMessage.warning('最多只能上传5张图片')
}

// 处理文件变化
const handleFileChange = (file) => {
  fileList.value = [...fileList.value]
}

// 处理文件移除
const handleFileRemove = (file) => {
  // 从images中移除对应的URL
  const fileUrl = file.response?.data?.url || file.url
  if (fileUrl) {
    const index = productForm.images.indexOf(fileUrl)
    if (index !== -1) {
      productForm.images.splice(index, 1)
    }
  }
}

// 自定义上传
const uploadImage = async (options) => {
  try {
    const formData = new FormData()
    formData.append('file', options.file)
    
    const res = await uploadProductImage(formData)
    
    if (res.code === 200) {
      productForm.images.push(res.data.url)
      options.onSuccess(res.data)
    } else {
      options.onError()
    }
  } catch (error) {
    console.error('上传图片失败:', error)
    options.onError()
  }
}

// 提交表单
const submitForm = async () => {
  if (!productFormRef.value) return
  
  productFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    if (productForm.images.length === 0) {
      return ElMessage.warning('请上传至少一张特产图片')
    }
    
    try {
      submitting.value = true
      await updateProduct(productId, productForm)
      ElMessage.success('更新特产成功')
      router.push('/products')
    } catch (error) {
      console.error('更新特产失败:', error)
      ElMessage.error('更新特产失败')
    } finally {
      submitting.value = false
    }
  })
}

// 重置表单
const resetForm = () => {
  getDetail()
}

// 页面加载时获取特产详情
onMounted(() => {
  getDetail()
})
</script>

<style scoped>
.edit-product-container {
  padding: 20px;
}
</style>
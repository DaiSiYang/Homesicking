<template>
  <div class="profile-container">
    <div class="page-header mb-4">
      <h2 class="text-xl font-bold">店铺信息</h2>
    </div>

    <el-card v-loading="loading">
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        label-width="120px"
        status-icon
      >
        <!-- 基本信息 -->
        <h3 class="text-lg font-medium mb-4">基本信息</h3>
        
        <el-form-item label="店铺Logo" prop="logo">
          <el-upload
            class="avatar-uploader"
            action="/api/upload"
            :show-file-list="false"
            :on-success="handleLogoSuccess"
            :before-upload="beforeAvatarUpload"
          >
            <el-avatar v-if="form.logo" :src="form.logo" :size="100" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
            <div class="mt-2 text-gray-500">点击上传Logo</div>
          </el-upload>
        </el-form-item>

        <el-form-item label="店铺名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入店铺名称" />
        </el-form-item>

        <el-form-item label="店铺简介" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入店铺简介"
          />
        </el-form-item>

        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入联系电话" />
        </el-form-item>

        <el-form-item label="营业时间" prop="business_hours">
          <el-input v-model="form.business_hours" placeholder="例如：09:00-18:00" />
        </el-form-item>

        <!-- 店铺地址 -->
        <h3 class="text-lg font-medium mb-4 mt-6">店铺地址</h3>
        
        <el-form-item label="详细地址" prop="address">
          <el-input v-model="form.address" placeholder="请输入详细地址" />
        </el-form-item>

        <!-- 店铺照片 -->
        <h3 class="text-lg font-medium mb-4 mt-6">店铺照片</h3>
        
        <el-form-item label="店铺照片" prop="images">
          <el-upload
            action="/api/upload"
            list-type="picture-card"
            :file-list="fileList"
            :on-preview="handlePictureCardPreview"
            :on-remove="handleRemove"
            :on-success="handleImageSuccess"
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
          <el-dialog v-model="dialogVisible">
            <img w-full :src="dialogImageUrl" alt="店铺照片预览" />
          </el-dialog>
        </el-form-item>

        <!-- 经营资质 -->
        <h3 class="text-lg font-medium mb-4 mt-6">经营资质</h3>
        
        <el-form-item label="营业执照" prop="license">
          <el-upload
            class="license-uploader"
            action="/api/upload"
            :show-file-list="false"
            :on-success="handleLicenseSuccess"
            :before-upload="beforeLicenseUpload"
          >
            <el-image
              v-if="form.license"
              :src="form.license"
              class="w-64 h-40 object-cover mb-2"
            />
            <el-button v-else type="primary">上传营业执照</el-button>
            <div class="mt-2 text-gray-500">请上传清晰的营业执照照片或扫描件</div>
          </el-upload>
        </el-form-item>

        <el-form-item label="法人姓名" prop="legal_person">
          <el-input v-model="form.legal_person" placeholder="请输入法人姓名" />
        </el-form-item>

        <el-form-item label="统一社会信用代码" prop="credit_code">
          <el-input v-model="form.credit_code" placeholder="请输入统一社会信用代码" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="submitting">保存修改</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { getMerchantInfo, updateMerchantInfo, uploadMerchantLogo, uploadMerchantImage, uploadLicense } from '@/api/merchant'

const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(true)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogImageUrl = ref('')

// 表单数据
const form = reactive({
  logo: '',
  name: '',
  description: '',
  phone: '',
  business_hours: '',
  address: '',
  images: [],
  license: '',
  legal_person: '',
  credit_code: ''
})

// 店铺照片列表
const fileList = ref([])

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入店铺名称', trigger: 'blur' },
    { min: 2, max: 30, message: '长度在 2 到 30 个字符', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  address: [
    { required: true, message: '请输入详细地址', trigger: 'blur' }
  ],
  legal_person: [
    { required: true, message: '请输入法人姓名', trigger: 'blur' }
  ],
  credit_code: [
    { required: true, message: '请输入统一社会信用代码', trigger: 'blur' },
    { pattern: /^[0-9A-HJ-NPQRTUWXY]{2}\d{6}[0-9A-HJ-NPQRTUWXY]{10}$/, message: '请输入正确的统一社会信用代码', trigger: 'blur' }
  ]
}

// 获取店铺信息
const fetchShopInfo = async () => {
  loading.value = true
  try {
    const res = await getMerchantInfo()
    if (res.code === 200) {
      // 填充表单
      Object.assign(form, res.data)
      
      // 设置店铺照片列表
      if (res.data.images && res.data.images.length > 0) {
        fileList.value = res.data.images.map((url, index) => ({
          name: `店铺照片${index + 1}`,
          url
        }))
      }
    }
  } catch (error) {
    console.error('获取店铺信息失败:', error)
    ElMessage.error('获取店铺信息失败')
  } finally {
    loading.value = false
  }
}

// Logo上传前验证
const beforeAvatarUpload = (file) => {
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

// Logo上传成功回调
const handleLogoSuccess = (response) => {
  // 实际项目中这里应该处理服务器返回的图片URL
  form.logo = 'https://via.placeholder.com/200x200'
  ElMessage.success('Logo上传成功')
}

// 营业执照上传前验证
const beforeLicenseUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt5M = file.size / 1024 / 1024 < 5

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt5M) {
    ElMessage.error('图片大小不能超过 5MB!')
    return false
  }
  return true
}

// 营业执照上传成功回调
const handleLicenseSuccess = (response) => {
  // 实际项目中这里应该处理服务器返回的图片URL
  form.license = 'https://via.placeholder.com/800x600'
  ElMessage.success('营业执照上传成功')
}

// 店铺照片上传成功回调
const handleImageSuccess = (response, file) => {
  // 实际项目中这里应该处理服务器返回的图片URL
  file.url = 'https://via.placeholder.com/800x600'
  form.images.push(file.url)
  ElMessage.success('照片上传成功')
}

// 照片预览
const handlePictureCardPreview = (file) => {
  dialogImageUrl.value = file.url
  dialogVisible.value = true
}

// 移除照片
const handleRemove = (file, fileList) => {
  form.images = form.images.filter(url => url !== file.url)
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        const res = await updateMerchantInfo(form)
        if (res.code === 200) {
          ElMessage.success('店铺信息更新成功')
          
          // 更新用户状态中的店铺名称
          userStore.updateShopName(form.name)
        }
      } catch (error) {
        console.error('保存失败:', error)
        ElMessage.error('保存失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

// 重置表单
const resetForm = () => {
  ElMessage.info('已重置为原始信息')
  fetchShopInfo()
}

// 初始化
onMounted(() => {
  fetchShopInfo()
})
</script>

<style scoped>
.profile-container {
  padding: 20px;
}

.avatar-uploader {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 120px;
  height: 120px;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  overflow: hidden;
}

.avatar-uploader:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>

<template>
  <div class="homestay-form-container">
    <div class="page-header flex items-center mb-4">
      <el-button icon="ArrowLeft" text @click="$router.push('/homestays')">返回</el-button>
      <h2 class="text-xl font-bold ml-2">添加民宿</h2>
    </div>

    <el-card>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        label-width="120px"
        status-icon
      >
        <el-form-item label="民宿名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入民宿名称" />
        </el-form-item>

        <el-form-item label="封面图" prop="cover_image">
          <el-upload
            class="upload-demo"
            action="/api/upload"
            :show-file-list="false"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
          >
            <el-image
              v-if="form.cover_image"
              :src="form.cover_image"
              class="w-40 h-28 object-cover mb-2"
            />
            <el-button type="primary">点击上传</el-button>
            <template #tip>
              <div class="text-gray-400 mt-1">建议上传尺寸: 800x600px, 格式: JPG/PNG</div>
            </template>
          </el-upload>
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="价格/晚" prop="price">
              <el-input-number
                v-model="form.price"
                :min="0"
                :precision="2"
                :step="10"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="可住人数" prop="capacity">
              <el-input-number
                v-model="form.capacity"
                :min="1"
                :max="20"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="地址" prop="address">
          <el-input v-model="form.address" placeholder="请输入详细地址" />
        </el-form-item>

        <el-form-item label="详细描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="请输入民宿详细描述"
          />
        </el-form-item>

        <el-form-item label="设施服务" prop="amenities">
          <el-checkbox-group v-model="form.amenities">
            <el-checkbox value="wifi" label="免费WiFi">免费WiFi</el-checkbox>
            <el-checkbox value="parking" label="免费停车">免费停车</el-checkbox>
            <el-checkbox value="breakfast" label="含早餐">含早餐</el-checkbox>
            <el-checkbox value="air_condition" label="空调">空调</el-checkbox>
            <el-checkbox value="tv" label="电视">电视</el-checkbox>
            <el-checkbox value="washer" label="洗衣机">洗衣机</el-checkbox>
            <el-checkbox value="kitchen" label="厨房">厨房</el-checkbox>
          </el-checkbox-group>
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
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const formRef = ref(null)
const submitting = ref(false)

// 表单数据
const form = reactive({
  name: '',
  cover_image: '',
  price: 298,
  capacity: 2,
  address: '',
  description: '',
  amenities: []
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入民宿名称', trigger: 'blur' },
    { min: 2, max: 30, message: '长度在 2 到 30 个字符', trigger: 'blur' }
  ],
  cover_image: [
    { required: true, message: '请上传封面图', trigger: 'change' }
  ],
  price: [
    { required: true, message: '请设置价格', trigger: 'blur' }
  ],
  capacity: [
    { required: true, message: '请设置可住人数', trigger: 'blur' }
  ],
  address: [
    { required: true, message: '请输入地址', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入详细描述', trigger: 'blur' }
  ]
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

// 上传成功回调
const handleUploadSuccess = (response) => {
  if (response.code === 200) {
    form.cover_image = response.data.url
    ElMessage.success('上传成功')
  } else {
    ElMessage.error('上传失败')
  }
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        const res = await createHomestay(form)
        if (res.code === 200) {
          ElMessage.success('民宿添加成功')
          router.push('/homestays')
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
  if (formRef.value) {
    formRef.value.resetFields()
  }
}
</script>

<style scoped>
.homestay-form-container {
  padding: 20px;
}
</style>

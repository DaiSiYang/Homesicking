<template>
  <div class="settings-container">
    <div class="page-header mb-4">
      <h2 class="text-xl font-bold">账户设置</h2>
    </div>

    <el-card>
      <el-tabs v-model="activeTab">
        <!-- 基本信息 -->
        <el-tab-pane label="基本信息" name="basic">
          <el-form
            ref="basicFormRef"
            :model="basicForm"
            :rules="basicRules"
            label-position="top"
            label-width="120px"
            status-icon
            v-loading="basicLoading"
          >
            <el-form-item label="头像" prop="avatar">
              <el-upload
                class="avatar-uploader"
                action="/api/upload"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                :before-upload="beforeAvatarUpload"
              >
                <el-avatar v-if="basicForm.avatar" :src="basicForm.avatar" :size="100" />
                <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
                <div class="mt-2 text-gray-500">点击上传头像</div>
              </el-upload>
            </el-form-item>

            <el-form-item label="用户名" prop="username">
              <el-input v-model="basicForm.username" placeholder="请输入用户名" disabled />
              <div class="text-gray-400 text-xs mt-1">用户名不可修改</div>
            </el-form-item>

            <el-form-item label="昵称" prop="nickname">
              <el-input v-model="basicForm.nickname" placeholder="请输入昵称" />
            </el-form-item>

            <el-form-item label="手机号" prop="phone">
              <el-input v-model="basicForm.phone" placeholder="请输入手机号" />
            </el-form-item>

            <el-form-item label="邮箱" prop="email">
              <el-input v-model="basicForm.email" placeholder="请输入邮箱" />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="saveBasicInfo" :loading="basicSubmitting">保存修改</el-button>
              <el-button @click="resetBasicForm">重置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <!-- 修改密码 -->
        <el-tab-pane label="修改密码" name="password">
          <el-form
            ref="passwordFormRef"
            :model="passwordForm"
            :rules="passwordRules"
            label-position="top"
            label-width="120px"
            status-icon
          >
            <el-form-item label="当前密码" prop="currentPassword">
              <el-input
                v-model="passwordForm.currentPassword"
                type="password"
                placeholder="请输入当前密码"
                show-password
              />
            </el-form-item>

            <el-form-item label="新密码" prop="newPassword">
              <el-input
                v-model="passwordForm.newPassword"
                type="password"
                placeholder="请输入新密码"
                show-password
              />
              <div class="text-gray-400 text-xs mt-1">密码长度8-20位，必须包含字母和数字</div>
            </el-form-item>

            <el-form-item label="确认新密码" prop="confirmPassword">
              <el-input
                v-model="passwordForm.confirmPassword"
                type="password"
                placeholder="请再次输入新密码"
                show-password
              />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="changePassword" :loading="passwordSubmitting">修改密码</el-button>
              <el-button @click="resetPasswordForm">重置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <!-- 账户安全 -->
        <el-tab-pane label="账户安全" name="security">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="账户安全等级">
              <el-progress :percentage="securityLevel" :color="securityColor" />
              <span class="ml-2">{{ securityText }}</span>
            </el-descriptions-item>

            <el-descriptions-item label="登录密码">
              <div class="flex justify-between items-center">
                <span>已设置</span>
                <el-button type="primary" link @click="activeTab = 'password'">修改</el-button>
              </div>
            </el-descriptions-item>

            <el-descriptions-item label="手机绑定">
              <div class="flex justify-between items-center">
                <span>{{ basicForm.phone ? basicForm.phone : '未绑定' }}</span>
                <el-button type="primary" link @click="activeTab = 'basic'">{{ basicForm.phone ? '修改' : '绑定' }}</el-button>
              </div>
            </el-descriptions-item>

            <el-descriptions-item label="邮箱绑定">
              <div class="flex justify-between items-center">
                <span>{{ basicForm.email ? basicForm.email : '未绑定' }}</span>
                <el-button type="primary" link @click="activeTab = 'basic'">{{ basicForm.email ? '修改' : '绑定' }}</el-button>
              </div>
            </el-descriptions-item>

            <el-descriptions-item label="上次登录时间">
              {{ lastLoginTime }}
            </el-descriptions-item>

            <el-descriptions-item label="上次登录IP">
              {{ lastLoginIp }}
            </el-descriptions-item>
          </el-descriptions>
        </el-tab-pane>

        <!-- 消息通知 -->
        <el-tab-pane label="消息通知" name="notification">
          <el-form :model="notificationForm">
            <el-form-item label="系统通知">
              <el-switch v-model="notificationForm.system" />
              <div class="text-gray-400 text-xs mt-1">接收系统更新、维护等通知</div>
            </el-form-item>

            <el-form-item label="订单通知">
              <el-switch v-model="notificationForm.order" />
              <div class="text-gray-400 text-xs mt-1">有新订单时通知</div>
            </el-form-item>

            <el-form-item label="评价通知">
              <el-switch v-model="notificationForm.review" />
              <div class="text-gray-400 text-xs mt-1">有新评价时通知</div>
            </el-form-item>

            <el-form-item label="通知方式">
              <el-checkbox-group v-model="notificationForm.methods">
                <el-checkbox value="app" label="APP推送">APP推送</el-checkbox>
                <el-checkbox value="sms" label="短信">短信</el-checkbox>
                <el-checkbox value="email" label="邮件">邮件</el-checkbox>
              </el-checkbox-group>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="saveNotificationSettings" :loading="notificationSubmitting">保存设置</el-button>
              <el-button @click="resetNotificationForm">重置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { getMerchantInfo, updateMerchantInfo, getNotificationSettings, updateNotificationSettings } from '@/api/merchant'

const userStore = useUserStore()
const activeTab = ref('basic')

// 基本信息相关
const basicFormRef = ref(null)
const basicLoading = ref(true)
const basicSubmitting = ref(false)
const basicForm = reactive({
  avatar: '',
  username: '',
  nickname: '',
  phone: '',
  email: ''
})

const basicRules = {
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

// 密码相关
const passwordFormRef = ref(null)
const passwordSubmitting = ref(false)
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  } else {
    if (!/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,20}$/.test(value)) {
      callback(new Error('密码必须包含字母和数字，长度8-20位'))
    }
    if (passwordForm.confirmPassword !== '') {
      passwordFormRef.value.validateField('confirmPassword')
    }
    callback()
  }
}

const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== passwordForm.newPassword) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const passwordRules = {
  currentPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, validator: validatePass, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validatePass2, trigger: 'blur' }
  ]
}

// 账户安全相关
const lastLoginTime = ref('2023-11-20 15:30:45')
const lastLoginIp = ref('192.168.1.1')

const securityLevel = computed(() => {
  let level = 0
  if (basicForm.phone) level += 30
  if (basicForm.email) level += 30
  if (passwordForm.newPassword && passwordForm.newPassword.length >= 12) level += 40
  else level += 20
  return Math.min(level, 100)
})

const securityColor = computed(() => {
  if (securityLevel.value < 40) return '#F56C6C'
  if (securityLevel.value < 70) return '#E6A23C'
  return '#67C23A'
})

const securityText = computed(() => {
  if (securityLevel.value < 40) return '低'
  if (securityLevel.value < 70) return '中'
  return '高'
})

// 通知设置相关
const notificationSubmitting = ref(false)
const notificationForm = reactive({
  system: true,
  order: true,
  review: true,
  methods: ['app', 'sms']
})

// 获取用户信息
const fetchUserInfo = async () => {
  basicLoading.value = true
  try {
    const res = await getMerchantInfo()
    if (res.code === 200) {
      // 填充表单
      Object.assign(basicForm, {
        avatar: res.data.logo || '',
        username: res.data.username || '',
        nickname: res.data.name || '',
        phone: res.data.phone || '',
        email: res.data.email || ''
      })
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
    ElMessage.error('获取用户信息失败')
  } finally {
    basicLoading.value = false
  }
}

// 头像上传前验证
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



// 保存基本信息
const saveBasicInfo = async () => {
  if (!basicFormRef.value) return

  await basicFormRef.value.validate(async (valid) => {
    if (valid) {
      basicSubmitting.value = true
      try {
        const updateData = {
          logo: basicForm.avatar,
          name: basicForm.nickname,
          phone: basicForm.phone,
          email: basicForm.email
        }
        
        const res = await updateMerchantInfo(updateData)
        if (res.code === 200) {
          ElMessage.success('基本信息更新成功')
          
          // 更新用户状态
          userStore.updateUserInfo({
            avatar: basicForm.avatar,
            nickname: basicForm.nickname
          })
        }
      } catch (error) {
        console.error('保存失败:', error)
        ElMessage.error('保存失败')
      } finally {
        basicSubmitting.value = false
      }
    }
  })
}

// 重置基本信息表单
const resetBasicForm = () => {
  ElMessage.info('已重置为原始信息')
  fetchUserInfo()
}

// 修改密码函数
const changePassword = async () => {
  if (!passwordFormRef.value) return

  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      passwordSubmitting.value = true
      try {
        const res = await changeUserPassword({
          old_password: passwordForm.currentPassword,  // 修正字段名
          new_password: passwordForm.newPassword
        })
        if (res.code === 200) {
          ElMessage.success('密码修改成功')
          resetPasswordForm()
        }
      } catch (error) {
        console.error('修改失败:', error)
        ElMessage.error('修改失败')
      } finally {
        passwordSubmitting.value = false
      }
    }
  })
}

// 头像上传成功回调（保留第一个，删除重复的）
const handleAvatarSuccess = (response) => {
  // 实际项目中这里应该处理服务器返回的图片URL
  if (response.code === 200) {
    basicForm.avatar = response.data.url  // 修正变量名
    ElMessage.success('头像上传成功')
  } else {
    basicForm.avatar = 'https://via.placeholder.com/200x200'
    ElMessage.success('头像上传成功')
  }
}

// 删除以下重复和错误的代码（第407-422行）：
// const handleAvatarSuccess = (response) => {
//   if (response.code === 200) {
//     merchantForm.avatar = response.data.url
//     ElMessage.success('头像上传成功')
//   } else {
//     ElMessage.error('头像上传失败')
//   }
// }

// const handleLicenseSuccess = (response) => {
//   if (response.code === 200) {
//     merchantForm.business_license = response.data.url
//     ElMessage.success('营业执照上传成功')
//   } else {
//     ElMessage.error('营业执照上传失败')
//   }
// }

// 重置密码表单
const resetPasswordForm = () => {
  if (passwordFormRef.value) {
    passwordFormRef.value.resetFields()
  }
}

// 保存通知设置
const saveNotificationSettings = async () => {
  notificationSubmitting.value = true
  try {
    const res = await updateNotificationSettings(notificationForm)
    if (res.code === 200) {
      ElMessage.success('通知设置已保存')
    }
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  } finally {
    notificationSubmitting.value = false
  }
}

// 重置通知设置表单
const resetNotificationForm = () => {
  notificationForm.system = true
  notificationForm.order = true
  notificationForm.review = true
  notificationForm.methods = ['app', 'sms']
  ElMessage.info('已重置为默认设置')
}

// 获取通知设置
const fetchNotificationSettings = async () => {
  try {
    const res = await getNotificationSettings()
    if (res.code === 200) {
      Object.assign(notificationForm, res.data)
    }
  } catch (error) {
    console.error('获取通知设置失败:', error)
    ElMessage.error('获取通知设置失败')
  }
}

// 初始化
onMounted(() => {
  fetchUserInfo()
  fetchNotificationSettings()
})
</script>

<style scoped>
.settings-container {
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

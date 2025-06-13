<template>
  <div class="profile-container">
    <!-- 个人信息卡片 - 重新设计 -->
    <div class="profile-hero">
      <div class="hero-background"></div>
      <div class="profile-main">
        <div class="avatar-section">
          <div class="avatar-wrapper">
            <el-avatar :size="120" :src="profileData.avatar" class="main-avatar">
              <el-icon><User /></el-icon>
            </el-avatar>
            <el-upload
              v-if="isEditing"
              class="avatar-upload-overlay"
              action="#"
              :auto-upload="false"
              :show-file-list="false"
              :on-change="handleAvatarChange"
            >
              <div class="upload-mask">
                <el-icon><Camera /></el-icon>
                <span>更换头像</span>
              </div>
            </el-upload>
          </div>
          <div class="user-basic-info">
            <h1 class="username">{{ profileData.nickname || '乡游爱好者' }}</h1>
            <p class="user-title">{{ profileData.bio || '探索乡村之美，发现生活之趣' }}</p>
            <div class="user-stats">
              <div class="stat-item">
                <span class="stat-number">{{ userStats.visitedVillages }}</span>
                <span class="stat-label">走过的乡村</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ userStats.favorites }}</span>
                <span class="stat-label">收藏</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ userStats.reviews }}</span>
                <span class="stat-label">评价</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="action-buttons">
          <el-button v-if="!isEditing" type="primary" size="large" @click="startEditing" class="edit-btn">
            <el-icon><Edit /></el-icon>
            编辑资料
          </el-button>
          <template v-else>
            <el-button size="large" @click="cancelEditing" class="cancel-btn">取消</el-button>
            <el-button type="primary" size="large" @click="saveProfile" class="save-btn">
              <el-icon><Check /></el-icon>
              保存
            </el-button>
          </template>
        </div>
      </div>
    </div>

    <!-- 详细信息表单 - 卡片式布局 -->
    <div class="profile-details">
      <el-card class="info-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon class="header-icon"><User /></el-icon>
            <span>基本信息</span>
          </div>
        </template>
        
        <el-form 
          ref="profileForm"
          :model="profileData"
          :rules="rules"
          label-position="top"
          :disabled="!isEditing"
          class="profile-form"
        >
          <div class="form-grid">
            <el-form-item label="昵称" prop="nickname">
              <el-input v-model="profileData.nickname" placeholder="请输入昵称" size="large" />
            </el-form-item>
            
            <el-form-item label="性别">
              <el-select v-model="profileData.gender" placeholder="请选择性别" size="large" class="w-full">
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="手机号码" prop="phone">
              <el-input v-model="profileData.phone" placeholder="请输入手机号码" size="large" />
            </el-form-item>
            
            <el-form-item label="电子邮箱" prop="email">
              <el-input v-model="profileData.email" placeholder="请输入电子邮箱" size="large" />
            </el-form-item>
            
            <el-form-item label="生日">
              <el-date-picker 
                v-model="profileData.birthday" 
                type="date" 
                placeholder="选择日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                size="large"
                class="w-full"
              />
            </el-form-item>
            
            <el-form-item label="所在地区">
              <el-cascader
                v-model="profileData.region"
                :options="regionOptions"
                placeholder="请选择所在地区"
                size="large"
                class="w-full"
              />
            </el-form-item>
          </div>
          
          <el-form-item label="个人简介">
            <el-input 
              v-model="profileData.bio" 
              type="textarea"
              :rows="4"
              maxlength="200"
              show-word-limit
              placeholder="分享您的乡村旅行故事或兴趣爱好"
              size="large"
            />
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 账号安全卡片 -->
      <el-card class="security-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon class="header-icon"><Lock /></el-icon>
            <span>账号安全</span>
          </div>
        </template>
        
        <div class="security-items">
          <div class="security-item">
            <div class="security-icon">
              <el-icon><Key /></el-icon>
            </div>
            <div class="security-content">
              <h3>登录密码</h3>
              <p>建议定期修改密码以保护账号安全</p>
            </div>
            <el-button type="primary" text @click="showChangePasswordDialog = true">修改</el-button>
          </div>
          
          <div class="security-item">
            <div class="security-icon">
              <el-icon><Iphone /></el-icon>
            </div>
            <div class="security-content">
              <h3>手机绑定</h3>
              <p>{{ maskPhone(profileData.phone) }}</p>
            </div>
            <el-button type="primary" text @click="showBindPhoneDialog = true">修改</el-button>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 对话框保持原有功能 -->
    <!-- 修改密码对话框 -->
    <el-dialog
      v-model="showChangePasswordDialog"
      title="修改密码"
      width="400px"
      destroy-on-close
    >
      <el-form :model="passwordForm" label-position="top" :rules="passwordRules">
        <el-form-item label="当前密码" prop="currentPassword">
          <el-input v-model="passwordForm.currentPassword" type="password" show-password size="large" />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="passwordForm.newPassword" type="password" show-password size="large" />
        </el-form-item>
        <el-form-item label="确认新密码" prop="confirmPassword">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password size="large" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showChangePasswordDialog = false" size="large">取消</el-button>
        <el-button type="primary" @click="changePassword" size="large">确认修改</el-button>
      </template>
    </el-dialog>

    <!-- 修改手机绑定对话框 -->
    <el-dialog
      v-model="showBindPhoneDialog"
      title="修改手机绑定"
      width="400px"
      destroy-on-close
    >
      <el-form :model="phoneForm" label-position="top" :rules="phoneRules">
        <el-form-item label="新手机号码" prop="newPhone">
          <el-input v-model="phoneForm.newPhone" size="large" />
        </el-form-item>
        <el-form-item label="验证码" prop="verificationCode">
          <div class="verification-code-input">
            <el-input v-model="phoneForm.verificationCode" size="large" />
            <el-button :disabled="countdown > 0" @click="sendVerificationCode" size="large">
              {{ countdown > 0 ? `${countdown}秒` : '获取验证码' }}
            </el-button>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showBindPhoneDialog = false" size="large">取消</el-button>
        <el-button type="primary" @click="bindNewPhone" size="large">确认修改</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Lock, Iphone, Edit, Check, Camera, Key } from '@element-plus/icons-vue'

// 表单引用
const profileForm = ref(null)

// 编辑状态
const isEditing = ref(false)

// 个人资料数据
const profileData = reactive({
  avatar: 'https://picsum.photos/id/1005/200/200',
  nickname: '乡游爱好者',
  gender: 'male',
  birthday: '1990-01-01',
  region: ['110000', '110100', '110101'], // 北京市-市辖区-东城区
  bio: '喜欢探索乡村美景，体验地道美食，记录乡村生活的点滴。',
  phone: '13800138000',
  email: 'user123@example.com'
})

// 保存原始数据用于取消编辑
const originalData = ref({})

// 表单验证规则
const rules = {
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号码', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入电子邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的电子邮箱格式', trigger: 'blur' }
  ]
}

// 修改密码相关
const showChangePasswordDialog = ref(false)
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})
const passwordRules = {
  currentPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 8, message: '密码长度不能少于8个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 修改手机绑定相关
const showBindPhoneDialog = ref(false)
const phoneForm = reactive({
  newPhone: '',
  verificationCode: ''
})
const phoneRules = {
  newPhone: [
    { required: true, message: '请输入新手机号码', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  verificationCode: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '验证码为6位数字', trigger: 'blur' }
  ]
}
const countdown = ref(0)
let countdownTimer = null

// 地区选项（省市区级联选择）
const regionOptions = [
  {
    value: '110000',
    label: '北京市',
    children: [
      {
        value: '110100',
        label: '市辖区',
        children: [
          { value: '110101', label: '东城区' },
          { value: '110102', label: '西城区' },
          { value: '110105', label: '朝阳区' },
          { value: '110106', label: '丰台区' }
        ]
      }
    ]
  },
  {
    value: '320000',
    label: '江苏省',
    children: [
      {
        value: '320100',
        label: '南京市',
        children: [
          { value: '320102', label: '玄武区' },
          { value: '320104', label: '秦淮区' },
          { value: '320105', label: '建邺区' },
          { value: '320106', label: '鼓楼区' }
        ]
      }
    ]
  },
  {
    value: '330000',
    label: '浙江省',
    children: [
      {
        value: '330100',
        label: '杭州市',
        children: [
          { value: '330102', label: '上城区' },
          { value: '330103', label: '下城区' },
          { value: '330104', label: '江干区' },
          { value: '330105', label: '拱墅区' }
        ]
      }
    ]
  }
]

// 开始编辑
const startEditing = () => {
  // 保存原始数据，用于取消编辑时恢复
  originalData.value = JSON.parse(JSON.stringify(profileData))
  isEditing.value = true
}

// 取消编辑
const cancelEditing = () => {
  // 恢复原始数据
  Object.assign(profileData, originalData.value)
  isEditing.value = false
}

// 上传头像
const handleAvatarChange = (file) => {
  // 模拟上传头像
  const reader = new FileReader()
  reader.onload = (e) => {
    // 实际应用中，这里会上传文件到服务器，然后更新用户头像URL
    profileData.avatar = e.target.result
    ElMessage.success('头像上传成功')
  }
  reader.readAsDataURL(file.raw)
}

// 保存个人资料
const saveProfile = () => {
  profileForm.value.validate((valid) => {
    if (valid) {
      // 模拟保存个人资料
      setTimeout(() => {
        ElMessage.success('个人资料已保存')
        isEditing.value = false
      }, 1000)
    } else {
      ElMessage.warning('请填写正确的个人信息')
      return false
    }
  })
}

// 修改密码
const changePassword = () => {
  // 模拟修改密码
  setTimeout(() => {
    ElMessage.success('密码修改成功')
    showChangePasswordDialog.value = false
    // 重置表单
    passwordForm.currentPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
  }, 1000)
}

// 发送验证码
const sendVerificationCode = () => {
  if (!phoneForm.newPhone) {
    ElMessage.warning('请输入手机号码')
    return
  }
  
  // 模拟发送验证码
  ElMessage.success(`验证码已发送至手机: ${phoneForm.newPhone}`)
  countdown.value = 60
  
  // 倒计时
  countdownTimer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(countdownTimer)
    }
  }, 1000)
}

// 绑定新手机
const bindNewPhone = () => {
  // 模拟绑定新手机
  setTimeout(() => {
    profileData.phone = phoneForm.newPhone
    ElMessage.success('手机号码修改成功')
    showBindPhoneDialog.value = false
    // 重置表单
    phoneForm.newPhone = ''
    phoneForm.verificationCode = ''
  }, 1000)
}

// 手机号码脱敏处理
const maskPhone = (phone) => {
  if (!phone) return ''
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

// 组件卸载前清除定时器
onBeforeUnmount(() => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
})

// 获取用户资料
onMounted(() => {
  // 实际应用中，这里会从API获取用户资料
  console.log('用户资料组件已挂载')
})

// 添加用户统计数据
const userStats = reactive({
  visitedVillages: 12,
  favorites: 28,
  reviews: 15
})
</script>

<style scoped>
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

/* 英雄区域样式 */
.profile-hero {
  position: relative;
  margin-bottom: 30px;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 200px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  opacity: 0.9;
}

.profile-main {
  position: relative;
  background: white;
  margin-top: 120px;
  padding: 80px 40px 40px;
  border-radius: 20px;
}

.avatar-section {
  display: flex;
  align-items: flex-start;
  gap: 30px;
  margin-bottom: 30px;
}

.avatar-wrapper {
  position: relative;
  flex-shrink: 0;
}

.main-avatar {
  border: 4px solid white;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.avatar-upload-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 50%;
  cursor: pointer;
}

.upload-mask {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
  opacity: 0;
  transition: opacity 0.3s;
}

.avatar-upload-overlay:hover .upload-mask {
  opacity: 1;
}

.user-basic-info {
  flex: 1;
}

.username {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 8px;
  color: #2c3e50;
}

.user-title {
  font-size: 16px;
  color: #7f8c8d;
  margin: 0 0 20px;
  line-height: 1.5;
}

.user-stats {
  display: flex;
  gap: 30px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 24px;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #7f8c8d;
}

.action-buttons {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
}

.edit-btn, .save-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 25px;
  padding: 12px 30px;
}

.cancel-btn {
  border-radius: 25px;
  padding: 12px 30px;
}

/* 详细信息区域 */
.profile-details {
  display: grid;
  gap: 30px;
}

.info-card, .security-card {
  border-radius: 15px;
  border: none;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.header-icon {
  color: #667eea;
  font-size: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.profile-form :deep(.el-form-item__label) {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.profile-form :deep(.el-input__wrapper) {
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.profile-form :deep(.el-textarea__inner) {
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* 安全设置样式 */
.security-items {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.security-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  transition: all 0.3s;
}

.security-item:hover {
  background: #e9ecef;
  transform: translateY(-2px);
}

.security-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
}

.security-content {
  flex: 1;
}

.security-content h3 {
  margin: 0 0 5px;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
}

.security-content p {
  margin: 0;
  color: #7f8c8d;
  font-size: 14px;
}

.verification-code-input {
  display: flex;
  gap: 10px;
}

.verification-code-input .el-input {
  flex: 1;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile-container {
    padding: 10px;
  }
  
  .profile-main {
    padding: 60px 20px 30px;
  }
  
  .avatar-section {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .user-stats {
    justify-content: center;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    justify-content: center;
  }
}
</style>
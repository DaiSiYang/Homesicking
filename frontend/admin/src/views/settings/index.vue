<template>
  <div class="settings-container">
    <div class="page-header mb-4">
      <h2 class="text-xl font-bold">系统设置</h2>
    </div>

    <el-card>
      <el-tabs>
        <!-- 基础设置 -->
        <el-tab-pane label="基础设置">
          <el-form :model="basicSettings" label-width="120px" class="max-w-3xl">
            <el-form-item label="系统名称">
              <el-input v-model="basicSettings.systemName" />
            </el-form-item>
            
            <el-form-item label="系统Logo">
              <el-upload
                class="avatar-uploader"
                action="#"
                :http-request="uploadLogo"
                :show-file-list="false"
                :on-success="handleLogoSuccess"
              >
                <img v-if="basicSettings.logo" :src="basicSettings.logo" class="w-32 h-32 object-cover" />
                <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
              </el-upload>
              <div class="text-gray-500 text-sm mt-1">建议尺寸: 200px × 200px</div>
            </el-form-item>
            
            <el-form-item label="管理员联系电话">
              <el-input v-model="basicSettings.adminPhone" />
            </el-form-item>
            
            <el-form-item label="管理员邮箱">
              <el-input v-model="basicSettings.adminEmail" />
            </el-form-item>
            
            <el-form-item label="版权信息">
              <el-input v-model="basicSettings.copyright" />
            </el-form-item>
            
            <el-form-item label="备案信息">
              <el-input v-model="basicSettings.icp" />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveBasicSettings">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <!-- 支付设置 -->
        <el-tab-pane label="支付设置">
          <el-form :model="paymentSettings" label-width="120px" class="max-w-3xl">
            <el-form-item label="支付宝配置">
              <div class="border rounded p-4 mb-4">
                <el-form-item label="启用支付宝" label-width="120px">
                  <el-switch v-model="paymentSettings.alipayEnabled" />
                </el-form-item>
                <el-form-item label="APPID" label-width="120px">
                  <el-input v-model="paymentSettings.alipayAppId" />
                </el-form-item>
                <el-form-item label="商户私钥" label-width="120px">
                  <el-input v-model="paymentSettings.alipayPrivateKey" type="textarea" rows="3" />
                </el-form-item>
                <el-form-item label="支付宝公钥" label-width="120px">
                  <el-input v-model="paymentSettings.alipayPublicKey" type="textarea" rows="3" />
                </el-form-item>
              </div>
            </el-form-item>
            
            <el-form-item label="微信支付配置">
              <div class="border rounded p-4 mb-4">
                <el-form-item label="启用微信支付" label-width="120px">
                  <el-switch v-model="paymentSettings.wechatEnabled" />
                </el-form-item>
                <el-form-item label="商户ID" label-width="120px">
                  <el-input v-model="paymentSettings.wechatMchId" />
                </el-form-item>
                <el-form-item label="商户密钥" label-width="120px">
                  <el-input v-model="paymentSettings.wechatMchKey" />
                </el-form-item>
                <el-form-item label="APPID" label-width="120px">
                  <el-input v-model="paymentSettings.wechatAppId" />
                </el-form-item>
              </div>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="savePaymentSettings">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <!-- 短信设置 -->
        <el-tab-pane label="短信设置">
          <el-form :model="smsSettings" label-width="120px" class="max-w-3xl">
            <el-form-item label="短信服务商">
              <el-select v-model="smsSettings.provider" placeholder="请选择短信服务商">
                <el-option label="阿里云" value="aliyun" />
                <el-option label="腾讯云" value="tencent" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="AccessKey ID">
              <el-input v-model="smsSettings.accessKeyId" />
            </el-form-item>
            
            <el-form-item label="AccessKey Secret">
              <el-input v-model="smsSettings.accessKeySecret" show-password />
            </el-form-item>
            
            <el-form-item label="短信签名">
              <el-input v-model="smsSettings.signName" />
            </el-form-item>
            
            <el-form-item label="验证码模板ID">
              <el-input v-model="smsSettings.verificationTemplateId" />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveSmsSettings">保存设置</el-button>
              <el-button type="success" @click="testSms">发送测试短信</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <!-- 系统维护 -->
        <el-tab-pane label="系统维护">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <el-card shadow="hover" class="mb-4">
              <template #header>
                <div class="flex justify-between items-center">
                  <span>数据库备份</span>
                  <el-button type="primary" @click="backupDatabase">立即备份</el-button>
                </div>
              </template>
              <div>
                <p class="mb-2">上次备份时间: {{ maintenanceInfo.lastBackupTime || '从未备份' }}</p>
                <p class="mb-2">备份文件数量: {{ maintenanceInfo.backupCount || 0 }}</p>
                <el-table :data="maintenanceInfo.backupFiles" style="width: 100%" v-if="maintenanceInfo.backupFiles?.length">
                  <el-table-column prop="name" label="文件名" />
                  <el-table-column prop="size" label="大小" width="100" />
                  <el-table-column prop="time" label="时间" width="180" />
                  <el-table-column label="操作" width="120">
                    <template #default="scope">
                      <el-button type="primary" size="small" text @click="downloadBackup(scope.row)">下载</el-button>
                      <el-button type="danger" size="small" text @click="deleteBackup(scope.row)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </el-card>
            
            <el-card shadow="hover" class="mb-4">
              <template #header>
                <div class="flex justify-between items-center">
                  <span>缓存管理</span>
                  <el-button type="danger" @click="clearCache">清除缓存</el-button>
                </div>
              </template>
              <div>
                <p class="mb-2">当前缓存大小: {{ maintenanceInfo.cacheSize || '0 MB' }}</p>
                <p class="mb-2">上次清理时间: {{ maintenanceInfo.lastCacheClearTime || '从未清理' }}</p>
              </div>
            </el-card>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

// 基础设置数据
const basicSettings = ref({
  systemName: '觅乡记乡村旅游平台',
  logo: 'https://via.placeholder.com/200x200',
  adminPhone: '13800138000',
  adminEmail: 'admin@mixiangji.com',
  copyright: '© 2023 觅乡记 All Rights Reserved.',
  icp: '浙ICP备XXXXXXXX号'
})

// 支付设置数据
const paymentSettings = ref({
  alipayEnabled: true,
  alipayAppId: '2021000000000000',
  alipayPrivateKey: '',
  alipayPublicKey: '',
  wechatEnabled: true,
  wechatMchId: '1900000000',
  wechatMchKey: '',
  wechatAppId: 'wx1234567890'
})

// 短信设置数据
const smsSettings = ref({
  provider: 'aliyun',
  accessKeyId: '',
  accessKeySecret: '',
  signName: '觅乡记',
  verificationTemplateId: 'SMS_123456789'
})

// 系统维护信息
const maintenanceInfo = ref({
  lastBackupTime: '2023-11-20 15:30:45',
  backupCount: 5,
  backupFiles: [
    { name: 'backup_20231120_153045.sql', size: '2.5MB', time: '2023-11-20 15:30:45' },
    { name: 'backup_20231115_103022.sql', size: '2.4MB', time: '2023-11-15 10:30:22' },
    { name: 'backup_20231110_092135.sql', size: '2.3MB', time: '2023-11-10 09:21:35' }
  ],
  cacheSize: '156 MB',
  lastCacheClearTime: '2023-11-18 09:15:30'
})

// 保存基础设置
const saveBasicSettings = async () => {
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 500))
    ElMessage.success('基础设置保存成功')
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  }
}

// 保存支付设置
const savePaymentSettings = async () => {
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 500))
    ElMessage.success('支付设置保存成功')
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  }
}

// 保存短信设置
const saveSmsSettings = async () => {
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 500))
    ElMessage.success('短信设置保存成功')
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  }
}

// 上传Logo
const uploadLogo = async (options) => {
  try {
    // 模拟上传
    const file = options.file
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = (e) => {
      basicSettings.value.logo = e.target.result
      ElMessage.success('Logo上传成功')
    }
  } catch (error) {
    console.error('上传失败:', error)
    ElMessage.error('上传失败')
  }
}

// Logo上传成功处理
const handleLogoSuccess = (res) => {
  basicSettings.value.logo = res.url
}

// 发送测试短信
const testSms = async () => {
  ElMessageBox.prompt('请输入接收测试短信的手机号码', '发送测试短信', {
    confirmButtonText: '发送',
    cancelButtonText: '取消',
    inputPattern: /^1[3-9]\d{9}$/,
    inputErrorMessage: '请输入正确的手机号码'
  }).then(async ({ value }) => {
    try {
      // 模拟API请求
      await new Promise(resolve => setTimeout(resolve, 500))
      ElMessage.success(`测试短信已发送至 ${value}`)
    } catch (error) {
      console.error('发送失败:', error)
      ElMessage.error('发送失败')
    }
  }).catch(() => {})
}

// 备份数据库
const backupDatabase = async () => {
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const now = new Date()
    const timeString = now.toISOString().replace(/[-:T.]/g, '').substring(0, 14)
    const fileName = `backup_${timeString}.sql`
    const fileSize = '2.6MB'
    const fileTime = now.toISOString().replace('T', ' ').substring(0, 19)
    
    maintenanceInfo.value.lastBackupTime = fileTime
    maintenanceInfo.value.backupCount++
    maintenanceInfo.value.backupFiles.unshift({
      name: fileName,
      size: fileSize,
      time: fileTime
    })
    
    ElMessage.success('数据库备份成功')
  } catch (error) {
    console.error('备份失败:', error)
    ElMessage.error('备份失败')
  }
}

// 下载备份文件
const downloadBackup = (file) => {
  ElMessage.success(`开始下载备份文件: ${file.name}`)
}

// 删除备份文件
const deleteBackup = (file) => {
  ElMessageBox.confirm(`确定要删除备份文件 ${file.name} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    maintenanceInfo.value.backupFiles = maintenanceInfo.value.backupFiles.filter(item => item.name !== file.name)
    maintenanceInfo.value.backupCount--
    ElMessage.success(`备份文件 ${file.name} 已删除`)
  }).catch(() => {})
}

// 清除缓存
const clearCache = async () => {
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 800))
    
    maintenanceInfo.value.lastCacheClearTime = new Date().toISOString().replace('T', ' ').substring(0, 19)
    maintenanceInfo.value.cacheSize = '0 MB'
    
    ElMessage.success('缓存清除成功')
  } catch (error) {
    console.error('清除失败:', error)
    ElMessage.error('清除失败')
  }
}
</script>

<style scoped>
.settings-container {
  padding: 20px;
}

.avatar-uploader {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 128px;
  height: 128px;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  overflow: hidden;
}

.avatar-uploader:hover {
  border-color: #409eff;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 128px;
  height: 128px;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>

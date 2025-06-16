// 处理图片URL
export function getImageUrl(item) {
  // 优先使用cover_image，然后是coverImage，最后是image
  const imageUrl = item.cover_image || item.coverImage || item.image
  
  // 如果是相对路径，添加基础URL
  if (imageUrl && !imageUrl.startsWith('http')) {
    return `http://localhost:8000${imageUrl}`
  }
  
  return imageUrl || '/default-image.jpg' // 提供默认图片
}
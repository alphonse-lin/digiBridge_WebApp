// Helper function for handling image scaling needed for SAM
const handleImageScale = (image) => {
  // 输入到SAM的图像必须调整大小，以便最长的边是1024
  const LONG_SIDE_LENGTH = 1024
  const w = image.naturalWidth
  const h = image.naturalHeight
  const samScale = LONG_SIDE_LENGTH / Math.max(h, w)
  return { height: h, width: w, samScale }
}

export { handleImageScale }

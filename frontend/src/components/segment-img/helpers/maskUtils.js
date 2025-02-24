// Convert the onnx model mask prediction to ImageData
function arrayToImageData (input, width, height) {
  const [r, g, b, a] = [171, 127, 252, 255] // the masks's blue color
  const arr = new Uint8ClampedArray(4 * width * height).fill(0)
  for (let i = 0; i < input.length; i++) {
    // Threshold the onnx model mask prediction at 0.0
    // This is equivalent to thresholding the mask using predictor.model.mask_threshold
    // in python
    if (input[i] > 0.0) {
      arr[4 * i + 0] = r
      arr[4 * i + 1] = g
      arr[4 * i + 2] = b
      arr[4 * i + 3] = a
    }
  }
  return new ImageData(arr, height, width)
}

// Use a Canvas element to produce an image from ImageData
function imageDataToImage (imageData) {
  const canvas = imageDataToCanvas(imageData)
  const image = new Image()
  image.src = canvas.toDataURL()
  return image
}

// Canvas elements can be created from ImageData
function imageDataToCanvas (imageData) {
  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')
  canvas.width = imageData.width
  canvas.height = imageData.height
  ctx?.putImageData(imageData, 0, 0)
  return canvas
}

// Convert the onnx model mask output to an HTMLImageElement
export function onnxMaskToImage (input, width, height) {
  return imageDataToImage(arrayToImageData(input, width, height))
}

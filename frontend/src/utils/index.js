export function randomColor () {
  return '#' + Math.floor(Math.random() * 16777215).toString(16)
}

export function arrayToTree (arr, id = 'id', parentId = 'parentId', children = 'children') {
  const data = arr.reduce((acc, cur) => {
    cur[children] = []
    acc[cur[id]] = cur
    return acc
  }, {})
  return Object.values(data).filter(item => {
    if (item[parentId]) {
      data[item[parentId]][children].push(item)
      return false
    }
    return true
  })
}

// TODO
export function convertNodesToTree (nodes) {
  const objDict = {}

  // 创建一个字典，用于存储每个对象的引用
  for (const obj of nodes) {
    if ('mesh' in obj) {
      objDict[obj.mesh] = { children: [], data: obj }
    }
  }

  // 遍历每个对象
  for (const obj of nodes) {
    if ('children' in obj) {
      const children = obj.children

      // 遍历子对象的索引
      for (const childIndex of children) {
        // 获取子对象的引用
        const childObj = objDict[childIndex]

        // 将子对象添加到当前对象的子节点列表中
        objDict[obj.mesh].children.push(childObj)
      }
    }
  }

  // 返回根节点（没有父节点的对象）
  const root = Object.values(objDict).filter(obj => {
    return !Object.values(objDict).some(o => o.children.includes(obj))
  })
  return root
}

export function base64ToFile (base64, fileName) {
  const binaryString = atob(base64)
  const bytes = new Uint8Array(binaryString.length)
  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i)
  }
  const blob = new Blob([bytes], { type: 'image/png' })
  const blobUrl = URL.createObjectURL(blob)
  return {
    blobUrl,
    file: new File([blob], fileName, { type: 'image/png' })
  }
}

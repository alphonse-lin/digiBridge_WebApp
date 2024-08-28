<template>
  <div v-loading="loading === true"
       element-loading-text="please wait..."
       class="xz-chat-wrap">
    <div v-show="props.showBg === true"
         class="bg-1"></div>
    <div v-show="props.showBg === true"
         class="bg-2"></div>
    <div class="title">
      <div>
        <div class="img-wrap">
          <img :src="img2"
               alt="Robot">
        </div>
        <el-tag type="warning">Robot</el-tag>
      </div>
    </div>
    <div class="input">
      <el-input v-model="inputVal"
                size="large"
                placeholder="Input your question here..."
                clearable
                class="chat-input"
                style="width:100%;height: 100%;"
                @keyup.enter="onSend">
      </el-input>
      <svg-icon icon-class="send-plane-fill"
                style="width:20px;height:20px;position:absolute;top:15px;right: 17px;cursor:pointer"
                @click="onSend"></svg-icon>
    </div>
    <div class="content">
      <div ref="contentInner"
           class="content-inner">
        <div v-for="v in chatList"
             :key="v.id">
          <div v-if="v.side === 'left'">
            <div class="left">
              <div class="img-wrap">
                <img :src="img2"
                     alt="Robot">
              </div>
              <div class="text-content">
                <div class="text">
                  <div v-for="(t, i) in v.content.split('\n')"
                     :key="i"
                     v-html="marked.parse(t)"
                     class="row"></div>
                </div>
              </div>
            </div>
          </div>
          <div v-if="v.side === 'right'">
            <div class="right">
              <div class="text-content">
                <div class="text">
                <div v-for="(t, i) in v.content.split('\n')"
                     :key="i"
                     v-html="marked.parse(t)"
                     class="row"></div>
                </div>
              </div>
              <div class="img-wrap">
                <img :src="img1"
                     alt="Person">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// import Bus from '@/utils/bus.js'
import img1 from '@/assets/chat/user-line.png?url'
import img2 from '@/assets/chat/robot-2-line.png?url'
import { genUrl } from '@/api/config.js'
import { marked } from 'marked'

const props = defineProps({
  showBg: {
    type: Boolean,
    default: true
  }
})

const loading = ref(false)
const inputVal = ref('')
const hsahVal = 't0ucnfg9ae' + Math.random().toString(36).substring(2)
const chatList = ref([
  // { id: 1, time: dayjs().format('YYYY-MM-DD HH:mm:ss'), side: 'left', content: "Hello, I'm an intelligent assistant. How can I help you?" }
])

const contentInner = ref(null)
function onSend (showPrompt = true) {
  if (loading.value) return
  if (showPrompt && inputVal.value.trim() === '') {
    inputVal.value = ''
    return
  }
  let inputValBackup = ''
  if (showPrompt) {
    const obj = {
      id: hsahVal,
      side: 'right',
      content: inputVal.value
    }
    chatList.value.push(obj)
    inputValBackup = inputVal.value
    inputVal.value = ''
    setTimeout(() => {
      contentInner.value.scrollTop = contentInner.value.scrollHeight
    }, 0)
  }
  loading.value = true
  const param = {
    model: 'llama3:8b',
    prompt: inputValBackup,
    // prompt: 'hello, give me some markdown example.',
    stream: false
  }
  fetch(genUrl, {
    method: 'POST',
    mode: 'cors',
    body: JSON.stringify(param)
  })
    .then(response => {
      response.json()
        .then(res => {
          const obj = {
            id: hsahVal,
            side: 'left',
            content: res.response
          }
          chatList.value.push(obj)
          inputVal.value = ''
          // setTimeout(() => {
          //   contentInner.value.scrollTop = contentInner.value.scrollHeight
          // }, 0)
        })
    })
    .catch(err => {
      console.log('%c err: ', 'background-color: pink', err)
    })
    .finally(() => {
      loading.value = false
    })
}

onMounted(() => {
  contentInner.value.scrollTop = contentInner.value.scrollHeight

  // Bus.on('xz-qa-select', (v) => {
  //   inputVal.value = v.content
  //   questionListItem.value = v
  // })
})
onBeforeUnmount(() => { })
</script>

<style lang='scss'
       scoped>
      .xz-chat-wrap {
        width: 100%;
        height: 100%;
        position: relative;
        min-height: 600px;
        border-radius: 10px;

        .bg-1,
        .bg-2 {
          width: 190px;
          height: 800px;
          position: absolute;
          top: 50%;
          margin-top: -400px;
          z-index: 2;
          background-size: cover;
          background-repeat: no-repeat;
          background-position: center center;
        }

        .bg-1 {
          left: 0;
          background-image: url('../../../assets/img/zkfw/chat-bg-left.png');
        }

        .bg-2 {
          right: 0;
          background-image: url('../../../assets/img/zkfw/chat-bg-right.png');
        }

        .title {
          width: 482px;
          height: 56px;
          background: rgba(255, 255, 255, 0.01);
          box-shadow: var(--el-box-shadow-light);
          border-radius: 8px 8px 8px 8px;
          opacity: 1;
          position: absolute;
          left: 50%;
          top: 12px;
          margin-left: -241px;
          z-index: 100;

          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0 20px;
          color: var(--el-text-color);

          >div {
            &:first-child {
              display: flex;
              align-items: center;

              >div {
                margin-right: 12px;
              }

              .img-wrap {
                width: 40px;
                height: 40px;
                padding: 8px;
                opacity: 1;
                border: 1px solid var(--el-border-color);
                border-radius: 50%;
                overflow: hidden;
                display: flex;
                justify-content: center;
                align-items: flex-end;

                img {
                  width: 100%;
                  height: 100%;
                  object-fit: contain;
                }
              }
            }
          }
        }

        .content {
          width: 760px;
          height: 100%;
          margin: 0 auto;
          padding: 80px 0 100px;
          position: relative;
          z-index: 3;
          overflow-y: auto;

          .content-inner {
            width: 100%;
            height: 100%;
            overflow-y: auto;
            padding-right: 10px;
            border-radius: 8px;

            .left {
              display: flex;
              justify-content: flex-start;
              align-items: flex-start;
              margin-bottom: 20px;

              .img-wrap {
                width: 40px;
                height: 40px;
                padding: 8px;
                opacity: 1;
                border: 1px solid var(--el-border-color);
                border-radius: 50%;
                overflow: hidden;
                display: flex;
                justify-content: center;
                align-items: flex-end;

                img {
                  width: 100%;
                  height: 100%;
                  object-fit: contain;
                }
              }

              .text-content {
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                margin-left: 20px;

                .text {
                  max-width: 600px;
                  line-height: 26px;
                  padding: 10px 16px;
                  border-radius: 4px 12px 12px 12px;
                  opacity: 1;
                  border: 1px solid var(--el-border-color);
                }

                .time {
                  // color: var(--el-color-primary);
                  font-size: 12px;
                  margin-bottom: 6px;
                }
              }
            }

            .right {
              display: flex;
              justify-content: flex-end;
              align-items: flex-start;
              margin-bottom: 20px;

              .text-content {
                display: flex;
                flex-direction: column;
                align-items: flex-end;
                margin-right: 20px;

                .text {
                  // min-width: 100px;
                  max-width: 600px;
                  line-height: 26px;
                  padding: 10px 16px;
                  border-radius: 12px 4px 12px 12px;
                  opacity: 1;
                  border: 1px solid var(--el-border-color);
                }

                .time {
                  // color: var(--el-color-primary);
                  font-size: 12px;
                  margin-bottom: 6px;
                }
              }

              .img-wrap {
                width: 40px;
                height: 40px;
                padding: 8px;
                opacity: 1;
                border: 1px solid var(--el-border-color);
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: flex-end;

                img {
                  width: 100%;
                  height: 100%;
                  object-fit: contain;
                }
              }
            }
          }
        }

        .input {
          width: 760px;
          height: 50px;
          background: #FFFFFF;
          box-shadow: var(--el-box-shadow-light);
          border-radius: 8px 8px 8px 8px;
          opacity: 1;
          position: absolute;
          left: 50%;
          bottom: 20px;
          margin-left: -380px;
          z-index: 100;
          color: var(--el-color-primary);
        }
      }
    </style>

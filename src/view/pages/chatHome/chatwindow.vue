<template>
  <div class="chat-window">
    <div class="top">
      <div class="info-detail">
        <div class="detail">{{ frinedInfo.detail }}</div>
      </div>
      <div class="other-fun">
        <label for="docFile">
          <span class="iconfont icon-wenjian"></span>
        </label>
        <label for="imgFile">
          <span class="iconfont icon-tupian"></span>
        </label>
        <input
          type="file"
          name=""
          id="imgFile"
          @change="sendImg"
          accept="image/*"
        />
        <input
          type="file"
          name=""
          id="docFile"
          @change="sendFile"
          accept="application/*,text/*"
        />
        <!-- accept="application/*" -->
      </div>
    </div>
    <div class="botoom">
      <div class="chat-content" ref="chatContent">
        <div class="chat-wrapper" v-for="item in chatList" :key="item.id">
          <div class="chat-me">
            <div class="chat-text">
            {{ item.message.content }}
            </div>
            <div class="info-time">
              <span>{{ item.created_time }}</span>
            </div>
          </div>
          <div class="chat-friend" v-if="item.response">
            <div class="chat-text">
              {{ item.response }}
            </div>
            <div class="info-time">
              <span>{{ item.created_time }}</span>
            </div>
          </div>
        </div>
      </div>
      <div class="chatInputs">
        <input class="inputs" v-model="inputMsg" @keyup.enter="sendText" />
        <div class="send boxinput" @click="sendText">
          <img src="@/assets/img/emoji/rocket.png" alt="" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { animation } from "@/util/util";
import { getChatMsg } from "@/api/getData";
import { sendMessage } from "@/api/getData"
import HeadPortrait from "@/components/HeadPortrait";
import Emoji from "@/components/Emoji";
import FileCard from "@/components/FileCard.vue";
import {str} from "mockjs/src/mock/random/basic";
export default {
  components: {
    HeadPortrait,
    Emoji,
    FileCard,
  },
  props: {
    frinedInfo: Object,
    default() {
      return {};
    },
  },
  watch: {
    frinedInfo() {
      this.getFriendChatMsg();
    },
  },
  data() {
    return {
      isShow: true,
      chatList: [],
      inputMsg: "",
      showEmoji: false,
      friendInfo: {},
      srcImgList: [],
    };
  },
  mounted() {
    this.getFriendChatMsg();
  },
  methods: {
    //获取聊天记录
    getFriendChatMsg() {
      let params = {
        frinedId: this.frinedInfo.id,
      };
      getChatMsg(params).then((res) => {
        this.chatList = res;
        this.chatList.forEach((item) => {
          item.created_time = this.formatTime(item.created_time)
        });
        this.scrollBottom();
      });
    },
    //发送信息
    sendMsg(msgList) {
      this.chatList.push(msgList);
      sendMessage({"id":this.frinedInfo.id,"message":msgList.message.content}).then((res) => {
        msgList.response = res
        this.scrollBottom();
      });
      this.scrollBottom();
    },
    //获取窗口高度并滚动至最底层
    scrollBottom() {
      this.$nextTick(() => {
        const scrollDom = this.$refs.chatContent;
        animation(scrollDom, scrollDom.scrollHeight - scrollDom.offsetHeight);
      });
    },
    //关闭标签框
    clickEmoji() {
      this.showEmoji = !this.showEmoji;
    },
    //发送文字信息
    sendText() {
      if (this.inputMsg) {

        let chatMsg = {
          "chatbox":this.frinedInfo.id,
          "message":{"role": "user", "content": this.inputMsg},
          "response":"",
          "created_time":this.filterTime()
          };
        this.sendMsg(chatMsg);
        this.$emit('personCardSort', this.frinedInfo.id)
        this.inputMsg = "";
      } else {
        this.$message({
          message: "消息不能为空哦~",
          type: "warning",
        });
      }
    },
    //发送本地图片
    sendImg(e) {
      let _this = this;
      console.log(e.target.files);
      let chatMsg = {
        headImg: require("@/assets/img/head_portrait.jpg"),
        name: "大毛是小白",
        time: "09：12 AM",
        msg: "",
        chatType: 1, //信息类型，0文字，1图片, 2文件
        extend: {
          imgType: 2, //(1表情，2本地图片)
        },
        uid: "1001",
      };
      let files = e.target.files[0]; //图片文件名
      if (!e || !window.FileReader) return; // 看是否支持FileReader
      let reader = new FileReader();
      reader.readAsDataURL(files); // 关键一步，在这里转换的
      reader.onloadend = function() {
        chatMsg.msg = this.result; //赋值
        _this.srcImgList.push(chatMsg.msg);
      };
      this.sendMsg(chatMsg);
      e.target.files = null;
    },
    //发送文件
    sendFile(e) {
      let chatMsg = {
        headImg: require("@/assets/img/head_portrait.jpg"),
        name: "大毛是小白",
        time: "09：12 AM",
        msg: "",
        chatType: 2, //信息类型，0文字，1图片, 2文件
        extend: {
          fileType: "", //(1word，2excel，3ppt，4pdf，5zpi, 6txt)
        },
        uid: "1001",
      };
      let files = e.target.files[0]; //图片文件名
      chatMsg.msg = files;
      console.log(files);
      if (files) {
        switch (files.type) {
          case "application/msword":
          case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            chatMsg.extend.fileType = 1;
            break;
          case "application/vnd.ms-excel":
          case "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            chatMsg.extend.fileType = 2;
            break;
          case "application/vnd.ms-powerpoint":
          case "application/vnd.openxmlformats-officedocument.presentationml.presentation":
            chatMsg.extend.fileType = 3;
            break;
          case "application/pdf":
            chatMsg.extend.fileType = 4;
            break;
          case "application/zip":
          case "application/x-zip-compressed":
            chatMsg.extend.fileType = 5;
            break;
          case "text/plain":
            chatMsg.extend.fileType = 6;
            break;
          default:
            chatMsg.extend.fileType = 0;
        }
        this.sendMsg(chatMsg);
        e.target.files = null;
      }
    },
    // 发送语音
    telephone() {
      this.$message("该功能还没有开发哦，敬请期待一下吧~🥳");
    },
    //发送视频
    video() {
      this.$message("该功能还没有开发哦，敬请期待一下吧~🥳");
    },
    // 时间处理
    formatTime(timeString) {
      const date = new Date(timeString);
      const year = date.getFullYear();
      const month = date.getMonth() + 1;
      const day = date.getDate();
      const hour = date.getHours();
      const minute = date.getMinutes();
      const formattedTime = `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')} ${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
      return formattedTime;
    },
    filterTime() {
      var date = new Date();
      var y = date.getFullYear();
      var m = date.getMonth() + 1;
      m = m < 10 ? "0" + m : m;
      var d = date.getDate();
      d = d < 10 ? "0" + d : d;
      var h = date.getHours();
      h = h < 10 ? "0" + h : h;
      var minute = date.getMinutes();
      minute = minute < 10 ? "0" + minute : minute;
      var s = date.getSeconds();
      s = s < 10 ? "0" + s : s;
      return y + "-" + m + "-" + d + " " + h + ":" + minute;
    }
  },
};


</script>

<style lang="scss" scoped>
.chat-window {
  width: 100%;
  height: 100%;
  margin-left: 20px;
  position: relative;

  .top {
    margin-bottom: 50px;
    &::after {
      content: "";
      display: block;
      clear: both;
    }
    .head-pic {
      float: left;
    }
    .info-detail {
      float: left;
      margin: 5px 20px 0;
      .name {
        font-size: 20px;
        font-weight: 600;
        color: #fff;
      }
      .detail {
        color: #9e9e9e;
        font-size: 18px;
        margin-top: 2px;
      }
    }
    .other-fun {
      float: right;
      margin-top: 20px;
      span {
        margin-left: 30px;
        cursor: pointer;
      }
      // .icon-tupian {

      // }
      input {
        display: none;
      }
    }
  }
  .botoom {
    width: 100%;
    height: 70vh;
    background-color: rgb(50, 54, 68);
    border-radius: 20px;
    padding: 20px;
    box-sizing: border-box;
    position: relative;
    .chat-content {
      width: 100%;
      height: 85%;
      overflow-y: scroll;
      padding: 20px;
      box-sizing: border-box;
      &::-webkit-scrollbar {
        width: 0; /* Safari,Chrome 隐藏滚动条 */
        height: 0; /* Safari,Chrome 隐藏滚动条 */
        display: none; /* 移动端、pad 上Safari，Chrome，隐藏滚动条 */
      }
      .chat-wrapper {
        position: relative;
        word-break: break-all;
        .chat-friend {
          width: 100%;
          float: left;
          margin-bottom: 20px;
          display: flex;
          flex-direction: column;
          justify-content: flex-start;
          align-items: flex-start;
          .chat-text {
            width: 80%;
            max-width: 90%;
            padding: 20px;
            border-radius: 20px 20px 20px 5px;
            background-color: rgb(56, 60, 75);
            color: #fff;
            &:hover {
              background-color: rgb(39, 42, 55);
            }
          }
          .chat-img {
            img {
              width: 100px;
              height: 100px;
            }
          }
          .info-time {
            margin: 10px 0;
            color: #fff;
            font-size: 14px;
            img {
              width: 30px;
              height: 30px;
              border-radius: 50%;
              vertical-align: middle;
              margin-right: 10px;
            }
            span:last-child {
              color: rgb(101, 104, 115);
              margin-left: 10px;
              vertical-align: middle;
            }
          }
        }
        .chat-me {
          float: right;
          margin-bottom: 20px;
          position: relative;
          display: flex;
          flex-direction: column;
          justify-content: flex-end;
          align-items: flex-end;
          .chat-text {
            resize:none;
            width: 80%;
            float: right;
            max-width: 90%;
            padding: 20px;
            border-radius: 20px 20px 5px 20px;
            background-color: rgb(29, 144, 245);
            color: #fff;
            &:hover {
              background-color: rgb(26, 129, 219);
            }
          }
          .chat-img {
            img {
              max-width: 300px;
              max-height: 200px;
              border-radius: 10px;
            }
          }
          .info-time {
            margin: 10px 0;
            color: #fff;
            font-size: 14px;
            display: flex;
            justify-content: flex-end;

            img {
              width: 30px;
              height: 30px;
              border-radius: 50%;
              vertical-align: middle;
              margin-left: 10px;
            }
            span {
              line-height: 30px;
            }
            span:first-child {
              color: rgb(101, 104, 115);
              margin-right: 10px;
              vertical-align: middle;
            }
          }
        }
      }
    }
    .chatInputs {
      width: 90%;
      position: absolute;
      bottom: 0;
      margin: 3%;
      display: flex;
      .boxinput {
        width: 50px;
        height: 50px;
        background-color: rgb(66, 70, 86);
        border-radius: 15px;
        border: 1px solid rgb(80, 85, 103);
        position: relative;
        cursor: pointer;
        img {
          width: 30px;
          height: 30px;
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translate(-50%, -50%);
        }
      }
      .emoji {
        transition: 0.3s;
        &:hover {
          background-color: rgb(46, 49, 61);
          border: 1px solid rgb(71, 73, 82);
        }
      }

      .inputs {
        width: 90%;
        height: 50px;
        background-color: rgb(66, 70, 86);
        border-radius: 15px;
        border: 2px solid rgb(34, 135, 225);
        padding: 10px;
        box-sizing: border-box;
        transition: 0.2s;
        font-size: 20px;
        color: #fff;
        font-weight: 100;
        margin: 0 20px;
        &:focus {
          outline: none;
        }
      }
      .send {
        background-color: rgb(29, 144, 245);
        border: 0;
        transition: 0.3s;
        box-shadow: 0px 0px 5px 0px rgba(0, 136, 255);
        &:hover {
          box-shadow: 0px 0px 10px 0px rgba(0, 136, 255);
        }
      }
    }
  }
}
</style>

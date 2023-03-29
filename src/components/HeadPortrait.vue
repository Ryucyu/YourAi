<template>
  <div class="head-portrait">
    <button style="cursor: pointer" @click="dialogVisible = true">
    <img class="myinfo" :src="imgUrl" alt="">
    </button>
    <el-dialog
        title="作者信息"
        :visible.sync="dialogVisible"
        width="45%"
        :before-close="handleClose">
      <span class="iconfont" style="font-size: 18px">前端代码仓库</span><br />
      <a href="https://github.com/Ryucyu/YourAI-vue" class="iconfont" target="_blank" style="font-size: 16px;color: #DD4A68">YourAI-vue</a><br />
      <span class="iconfont" style="font-size: 18px">前端灵感来源</span><br />
      <a href="https://gitee.com/mao-yongyao/chatroom" class="iconfont" target="_blank" style="font-size: 16px;color: #DD4A68">chatroom</a><br />
      <span class="iconfont" style="font-size: 18px">个人博客</span><br />
      <a href="https://unexpected-macaroni-b94.notion.site/92a9c6c7c7214666a24fc411558ef482" target="_blank" class="iconfont" style="font-size: 16px;color: #DD4A68">Ryu的notion</a><br />
      <span slot="footer" class="dialog-footer" style=""></span><br />
      <span class="iconfont" style="font-size: 18px">请作者喝可乐</span><br />
      <img :src="require('@/assets/img/money.jpg')" alt="" style="display: inline;width: 100px;height: 100px"><br />
     <el-button @click="dialogVisible = false">取 消</el-button>
     <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
    </el-dialog>
  </div>
</template>

<script>
import MyInfo from '@/components/MyInfo.vue'

export default {
    props: {
        imgUrl:{ default:require('@/assets/img/mio.jpg')}
    },
    components: {
      MyInfo
    },
    data() {
      return {
        dialogVisible: false
      };
    },
    methods:{
      handleClose(done) {
        this.$confirm('确认关闭？')
            .then(_ => {
              done();
            })
            .catch(_ => {});
      },
    }
}
</script>

<style lang="scss" scoped>
.head-portrait {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    // border: 2px solid rgb(137,140,151);
    border: 2px solid rgb(255, 255, 255);
    position:relative;
    &::before {
        content: '';
        width: 15px;
        height: 15px;
        z-index: 1;
        display: block;
        border-radius: 50%;
        background-color: rgb(144,225,80);
        position: absolute;
        right: 0;
    }
  .myinfo {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        // padding: 2px;
        box-sizing: border-box;
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        vertical-align: middle;
    }
  .info{
    font-family: "iconfont" !important;
    font-style: normal;
    font-size: 25px;
    vertical-align: middle;
    color: rgb(117,120,137);
  }
}
</style>

<template>
  <div class="viewer-area">
    <el-tabs type="border-card" style="box-shadow: 0px 0 0px #FFFFFF;">
      <el-tab-pane :label="taskid">
        <div>
          <div style="padding: 14px">
            <el-table
              :data="resultData"
              stripe
              border
              style="width: 100%; color: #282828">
            <el-table-column
              label="Item"
              prop="Item"
              fixed
              width="180">
            </el-table-column>
            <el-table-column
              label="Value"
              prop="Value">
            </el-table-column>
          </el-table>
          <img :src="rocimgurl" style="width: 700px">
          <img :src="optimgurl" style="width: 700px">
        </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  mounted () {
    this.showResults()
    this.showResultImages()
  },
  methods: {
    showResultImages () {
      this.rocimgurl = 'http://127.0.0.1:8000/api/show_roc?task_id=' + this.taskid
      this.optimgurl = 'http://127.0.0.1:8000/api/show_opt?task_id=' + this.taskid
    },
    showResults () {
      axios.get('http://127.0.0.1:8000/api/show_results?task_id=' + this.taskid)
        .then(response => {
          var res = response.data
          console.log(res)
          if (res.error_num === 0) {
            console.log(res)
            this.resultData = res['list']
            console.log(this.resultData)
          } else {
            this.$message.error('Failed!')
            console.log(res['msg'])
          }
        })
    }
  },
  data () {
    return {
      taskid: this.$route.query.taskid,
      rocimgurl: '',
      optimgurl: '',
      resultData: []
    }
  }
}
</script>

<style lang="scss">
.viewer-area {
    padding: 14px;
}
</style>

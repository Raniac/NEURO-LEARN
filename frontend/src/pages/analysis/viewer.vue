<template>
  <div class="viewer-area">
    <el-tabs type="border-card" style="box-shadow: 0px 0 0px #FFFFFF;">
      <el-tab-pane :label="taskid">
        <div>
          <div style="padding: 14px">
          <div style="padding-bottom: 28px">
            <el-table
              class="taskinfo-table"
              :data="taskinfo"
              stripe
              border
              style="width: 100%; background-color: #E8E8E8; color: #282828">
              <el-table-column type="expand">
                <template slot-scope="props">
                  <el-form label-position="left" inline class="demo-table-expand">
                    <el-form-item label="Task Type">
                      <span>{{ props.row.fields.task_type }}</span>
                    </el-form-item>
                    <el-form-item label="Label">
                      <span>{{ props.row.fields.label }}</span>
                    </el-form-item>
                    <el-form-item label="Train Data">
                      <span>{{ props.row.fields.train_data }}</span>
                    </el-form-item>
                    <el-form-item label="Test Data">
                      <span>{{ props.row.fields.test_data }}</span>
                    </el-form-item>
                    <el-form-item label="Feat. Sel.">
                      <span>{{ props.row.fields.feat_sel }}</span>
                    </el-form-item>
                    <el-form-item label="Estimator">
                      <span>{{ props.row.fields.estimator }}</span>
                    </el-form-item>
                    <el-form-item label="CV Type">
                      <span>{{ props.row.fields.cv_type }}</span>
                    </el-form-item>
                    <el-form-item label="Note">
                      <span>{{ props.row.fields.note }}</span>
                    </el-form-item>
                  </el-form>
                </template>
              </el-table-column>
              <el-table-column
              label="Task Name"
              prop="fields.task_name">
              </el-table-column>
              <el-table-column
              label="Project Name"
              prop="fields.project_name">
              </el-table-column>
            </el-table>
            </div>
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
            <img class="result-image" :src="optimgurl">
            <img class="result-image" :src="pfmimgurl">
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
    console.log(this.taskSelections)
    // if (this.taskSelections) {
    //   this.showResults()
    //   this.showResultImages()
    // }
  },
  methods: {
    showResultImages () {
      if (this.tasktype === 'Classification') {
        this.pfmimgurl = 'http://127.0.0.1:8000/api/show_roc?task_id=' + this.taskid
      }
      this.optimgurl = 'http://127.0.0.1:8000/api/show_opt?task_id=' + this.taskid
    },
    showResults () {
      axios.get('http://127.0.0.1:8000/api/show_results?task_id=' + this.taskid)
        .then(response => {
          var res = response.data
          console.log(res)
          if (res.error_num === 0) {
            console.log(res)
            this.taskinfo = res['info']
            this.resultData = res['list']
            console.log(this.taskinfo)
            console.log(this.resultData)
          } else {
            this.$alert('Error: ' + res['msg'], 'Task Failed!', {
              confirmButtonText: 'Confirm',
              callback: action => {
                this.$router.replace({
                  path: '/analysis/submissions',
                  component: resolve => require(['@/pages/analysis/submissions'], resolve)
                })
              }
            })
          }
        })
    }
  },
  data () {
    return {
      taskSelections: this.$route.query.taskSelections,
      // taskid: this.$route.query.taskid,
      // tasktype: this.$route.query.tasktype,
      pfmimgurl: '',
      optimgurl: '',
      taskinfo: [],
      resultData: []
    }
  }
}
</script>

<style lang="scss">
.viewer-area {
    padding: 14px;
    .result-image {
      width: 700px;
    }
}
</style>

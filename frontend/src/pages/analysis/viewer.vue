<template>
  <div style="text-align: center">
    <div class="viewer-area" v-if="analysisType == 'Machine Learning'">
      <el-tabs type="border-card" style="box-shadow: 0px 0 0px #FFFFFF;" @tab-click="handleTabClick" stretch v-model="tabsValue">
        <el-tab-pane v-for="(taskSelection, key) in taskSelections" :label="taskSelection.fields.task_id" :name="taskSelection.fields.task_id" :key="key">
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
                      <el-form-item label="Project Name">
                        <span>{{ props.row.fields.project_name }}</span>
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
                label="Task Type"
                prop="fields.task_type"
                width="120">
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
              <el-button type="primary" style="margin-top: 28px" round @click="handleDownloadFeatureWeights" v-if="showDownloadButton">Download Feature Weights</el-button>
              <li v-for="(img_name, index) in resultImgList" :key="index" style="list-style: none; text-align: center">
                <img class="result-image" :src="'/api/show_img?task_id=' + taskid + '&img_name=' + img_name">
              </li>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
    <div class="viewer-area" v-else-if="analysisType == 'Statistical Analysis'">
      <el-tabs type="border-card" style="box-shadow: 0px 0 0px #FFFFFF;" @tab-click="handleTabClick" stretch v-model="tabsValue">
        <el-tab-pane v-for="(taskSelection, key) in taskSelections" :label="taskSelection.fields.task_id" :name="taskSelection.fields.task_id" :key="key">
          <div>
            <div style="padding: 14px">
            <div style="padding-bottom: 28px">
              <el-table
                class="taskinfo-table"
                :data="taskinfo"
                stripe
                default-expand-all="true"
                border
                style="width: 100%; background-color: #E8E8E8; color: #282828">
                <el-table-column type="expand">
                  <template slot-scope="props">
                    <el-form label-position="left" inline class="demo-table-expand">
                      <el-form-item label="Project Name">
                        <span>{{ props.row.fields.project_name }}</span>
                      </el-form-item>
                      <el-form-item label="Test Var. / Data X">
                        <span>{{ props.row.fields.test_var_data_x }}</span>
                      </el-form-item>
                      <el-form-item label="Group Var. / Data Y">
                        <span>{{ props.row.fields.group_var_data_y }}</span>
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
                label="Task Type"
                prop="fields.task_type"
                width="120">
                </el-table-column>
              </el-table>
              </div>
              <el-button type="primary" style="margin-top: 0px" round @click="handleDownloadSigValues" v-if="showDownloadButton">Download Significance Values</el-button>
              <li v-for="(img_name, index) in resultImgList" :key="index" style="list-style: none; text-align: center">
                <img class="result-image" :src="'/api/show_img?task_id=' + taskid + '&img_name=' + img_name">
              </li>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  mounted () {
    if (this.$route.query.taskSelections) {
      this.taskSelections = this.$route.query.taskSelections
      this.taskSelection = this.taskSelections[0]
      this.taskid = this.taskSelection.fields.task_id
      this.tasktype = this.taskSelection.fields.task_type
      this.tabsValue = this.taskid
      this.analysisType = this.$route.query.analysisType
      this.showResults()
    } else if (this.$route.query.taskid) {
      this.taskid = this.$route.query.taskid
      this.tasktype = this.$route.query.tasktype
      this.taskSelections = {0: {fields: {task_id: this.taskid}}}
      this.taskSelection = this.taskSelections[0]
      this.tabsValue = this.taskid
      this.analysisType = this.$route.query.analysisType
      this.showResults()
    } else {
      this.$alert('There is no report to view!', 'Error!', {
        confirmButtonText: 'Confirm',
        callback: action => {
          this.$router.replace({
            path: '/analysis/submissions',
            component: resolve => require(['@/pages/analysis/submissions'], resolve)
          })
        }
      })
    }
  },
  methods: {
    handleTabClick () {
      this.taskid = this.tabsValue
      this.showResults()
    },
    handleDownloadFeatureWeights () {
      console.log(this.taskid)
      window.location.href = '/api/download_feature_weights?task_id=' + this.taskid
    },
    handleDownloadSigValues () {
      window.location.href = '/api/download_significance_values?task_id=' + this.taskid
    },
    showResults () {
      axios.get('/api/show_results?analysis_type=' + this.analysisType + '&task_id=' + this.taskid)
        .then(response => {
          var res = response.data
          console.log(res)
          if (res.error_num === 0) {
            console.log(res)
            if (this.analysisType === 'Machine Learning') {
              this.taskinfo = res['info']
              this.resultData = res['list']
              this.resultImgList = res['img_list']
              console.log(this.taskinfo)
              console.log(this.resultData)
              console.log(this.resultImgList)
              if (res.got_weights === 1) {
                this.showDownloadButton = true
              } else {
                this.showDownloadButton = false
              }
            } else if (this.analysisType === 'Statistical Analysis') {
              this.taskinfo = res['info']
              this.showDownloadButton = true
            }
          } else {
            this.$alert('<div>' + res['msg'].slice(1, -1).replace(/\\n/g, '<br/>') + '</div>', 'Error!', {
              confirmButtonText: 'Confirm',
              dangerouslyUseHTMLString: true,
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
      taskid: '',
      tasktype: '',
      taskSelections: [],
      taskSelection: {},
      pfmimgurl: '',
      optimgurl: '',
      taskinfo: [],
      resultData: [],
      resultImgList: [],
      tabsValue: '',
      showDownloadButton: false,
      analysisType: ''
    }
  }
}
</script>

<style lang="scss">
.viewer-area {
  width: 800px;
  text-align: left;
  margin: 14px auto;
  .result-image {
    width: 700px;
  }
}
</style>

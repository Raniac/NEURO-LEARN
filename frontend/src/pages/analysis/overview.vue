<template>
  <div>
    <div style="padding: 14px; color: #282828">
    <h3>Overview</h3>
    <el-row>
  <el-col :span="4" :offset=".5">
    <el-card :body-style="{ padding: '0px' }" style="background-color: #FFFFFF; width: 90%">
      <div style="padding: 14px; color: #282828; text-align: center">
        <h4>Total</h4>
        <div>
          <h1>{{ total_num }}</h1>
        </div>
      </div>
    </el-card>
  </el-col>
  <el-col :span="4" :offset="1">
    <el-card :body-style="{ padding: '0px' }" style="background-color: #FFFFFF; width: 90%">
      <div style="padding: 14px; color: #006699; text-align: center">
        <h4>Submitted</h4>
        <div>
          <h1>{{ submitted_num }}</h1>
        </div>
      </div>
    </el-card>
  </el-col>
  <el-col :span="4" :offset="1">
    <el-card :body-style="{ padding: '0px' }" style="background-color: #FFFFFF; width: 90%">
      <div style="padding: 14px; color: #00CC99; text-align: center">
        <h4>Running</h4>
        <div>
          <h1>{{ running_num }}</h1>
        </div>
      </div>
    </el-card>
  </el-col>
  <el-col :span="4" :offset="1">
    <el-card :body-style="{ padding: '0px' }" style="background-color: #FFFFFF; width: 90%">
      <div style="padding: 14px; color: #00CCFF; text-align: center">
        <h4>Finished</h4>
        <div>
          <h1>{{ finished_num }}</h1>
        </div>
      </div>
    </el-card>
  </el-col>
  <el-col :span="4" :offset="1">
    <el-card :body-style="{ padding: '0px' }" style="background-color: #FFFFFF; width: 90%">
      <div style="padding: 14px; color: #FF3333; text-align: center">
        <h4>Failed</h4>
        <div>
          <h1>{{ failed_num }}</h1>
        </div>
      </div>
    </el-card>
  </el-col>
</el-row>
    </div>
    <div style="padding: 14px">
      <h3>Recent</h3>
      <el-table
        class="submissions-table"
        :data="submissions_table"
        stripe
        border
        @row-click="onRowClick"
        style="width: 100%; background-color: #E8E8E8; color: #282828"
        :default-sort = "{prop: 'fields.task_id', order: 'descending'}">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="Task Type">
                <span>{{ props.row.fields.task_type }}</span>
              </el-form-item>
              <el-form-item label="Train Data">
                <span>{{ props.row.fields.train_data }}</span>
              </el-form-item>
              <el-form-item label="Test Data">
                <span>{{ props.row.fields.test_data }}</span>
              </el-form-item>
              <el-form-item label="Label">
                <span>{{ props.row.fields.label }}</span>
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
        label="Task ID"
        prop="fields.task_id">
        </el-table-column>
        <el-table-column
        label="Task Name"
        prop="fields.task_name">
        </el-table-column>
        <el-table-column
        label="Status"
        prop="fields.task_status">
        </el-table-column>
      </el-table>
    </div>
</div>
</template>

<style>
  .clearfix:before,
  .clearfix:after {
      display: table;
      content: "";
  }
  .clearfix:after {
      clear: both
  }
  .el-carousel__item h3 {
    color: #3e4b5c;
    font-size: 14px;
    opacity: 0.75;
    line-height: 200px;
    margin: 0;
  }
  .el-carousel__item:nth-child(2n) {
    background-color: #8b9aaf;
  }
  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }
</style>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      total_num: 0,
      submitted_num: 0,
      running_num: 0,
      finished_num: 0,
      failed_num: 0,
      search_input: '',
      selected_status: '',
      submissions_table: []
    }
  },
  mounted: function () {
    this.showSubmissions()
  },
  methods: {
    showSubmissions () {
      axios.get('http://127.0.0.1:8000/api/overview_submissions')
        .then(response => {
          var res = response.data
          if (res.error_num === 0) {
            this.submissions_table = res['list']
            this.total_num = res['total_num']
            this.submitted_num = res['submitted_num']
            this.running_num = res['running_num']
            this.finished_num = res['finished_num']
            this.failed_num = res['failed_num']
            this.submissions_table = res['list']
          } else {
            this.$message.error('Failed!')
            console.log(res['msg'])
          }
        })
    },
    updateStats () {
      this.total_num = 0
      console.log(this.submissions_table)
      this.submitted_num = 0
      this.running_num = 0
      this.finished_num = 0
      this.failed_num = 0
    },
    onRowClick (row) {
      this.$router.push({
        path: '/analysis/viewer',
        query: {taskid: row.fields.task_id}
      })
    }
  }
}
</script>

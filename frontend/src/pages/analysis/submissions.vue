<template>
  <div>
    <div class="submissions-area">
    <div style="margin: 14px">
      <el-input placeholder="Search" v-model="search_input" class="input-with-select">
        <el-select v-model="selected_status" slot="prepend" placeholder="Status">
        <el-option label="Submitted" value="1"></el-option>
        <el-option label="Running" value="2"></el-option>
        <el-option label="Finished" value="3"></el-option>
        <el-option label="Failed" value="4"></el-option>
        </el-select>
        <el-button slot="append" icon="el-icon-search"></el-button>
      </el-input>
    </div>
    <div style="margin: 14px">
      <el-table
        class="submissions-table"
        :data="submissions_table"
        stripe
        border
        style="width: 100%; background-color: #E8E8E8; color: #282828"
        :default-sort = "{prop: 'fields.task_id', order: 'descending'}">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="Task Type">
                <span>{{ props.row.fields.task_type }}</span>
              </el-form-item>
              <el-form-item label="Proj. Name">
                <span>{{ props.row.fields.project_name }}</span>
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
    <div style="margin: 14px">
      <el-pagination
      background
      layout="prev, pager, next"
      :total="1000">
      </el-pagination>
    </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
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
      axios.get('http://127.0.0.1:8000/api/show_submissions')
        .then(response => {
          var res = response.data
          if (res.error_num === 0) {
            console.log(res)
            this.submissions_table = res['list']
            console.log(this.submissions_table)
          } else {
            this.$message.error('Failed!')
            console.log(res['msg'])
          }
        })
    }
  }
}
</script>

<style lang="scss">
.submissions-area {
  margin: 14px;
  padding: 14px;
  background-color: #FFFFFF;
}
.input-with-select .el-input-group__prepend {
  background-color: #FFFFFF;
  .el-select .el-input {
    width: 130px;
}
}
.demo-table-expand {
    font-size: 0;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
</style>

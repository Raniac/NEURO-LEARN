<template>
  <div style="text-align: center">
    <div class="data-area">
      <div>
        <el-input placeholder="Search data by name" v-model="search_input" class="input-with-select" style="width: 50%">
          <el-button slot="append" icon="el-icon-search"></el-button>
        </el-input>
        <el-upload
          class="upload-demo"
          action="/api/upload_data"
          name="datafile"
          style="float: right"
          :on-change="handleChange"
          :on-success="uploadSuccess"
          :file-list="fileList">
          <el-button size="large" type="primary">Upload</el-button>
        </el-upload>
      </div>
      <div style="margin-top: 14px">
        <el-table
          class="data-table"
          :data="data_table.filter(data => (!search_input || data.fields.data_name.toLowerCase().includes(search_input.toLowerCase()))).slice((currpage - 1) * pagesize, currpage * pagesize)"
          stripe
          border
          style="width: 100%; background-color: #E8E8E8; color: #282828"
          >
          <el-table-column
          label="Data ID"
          prop="fields.data_id"
          width="180px">
          </el-table-column>
          <el-table-column
          label="Data Name"
          prop="fields.data_name">
          </el-table-column>
        </el-table>
      </div>
      <div style="margin: 14px">
        <el-pagination
        background
        layout="prev, pager, next"
        :page-size="pagesize"
        :total="data_table.length"
        @current-change="handleCurrentChange"
        @size-change="handleSizeChange">
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
      data_table: [],
      fileList: [],
      pagesize: 10,
      currpage: 1,
      search_input: ''
    }
  },
  mounted: function () {
    console.log(this.$route.query.projectid)
    this.showData()
  },
  methods: {
    showData () {
      axios.get('/api/show_data')
        .then(response => {
          var res = response.data
          if (res.error_num === 0) {
            console.log(res)
            this.data_table = res['list']
            console.log(res['list'])
          } else {
            this.$message.error('Failed!')
            console.log(res['msg'])
          }
        })
    },
    handleChange (file, fileList) {
      this.fileList = fileList.slice(-4)
    },
    uploadSuccess (response) {
      if (response.msg === 'success') {
        this.$message({showClose: true, message: 'Successfully uploaded! Data ID: ' + response.dataid, type: 'success'})
        console.log(response)
      } else if (response.msg === 'existed') {
        this.$message({showClose: true, message: 'File existed!', type: 'warning'})
        console.log(response)
      }
    },
    handleCurrentChange (cpage) {
      this.currpage = cpage
    },
    handleSizeChange (psize) {
      this.pagesize = psize
    }
  }
}
</script>

<style lang="scss">
.data-area {
  width: 744px;
  text-align: left;
  margin: 14px auto;
  padding: 28px;
  background-color: #FFFFFF;
}
.input-with-select .el-input-group__prepend {
  background-color: #FFFFFF;
}
</style>

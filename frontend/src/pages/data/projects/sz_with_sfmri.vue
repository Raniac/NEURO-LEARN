<template>
  <div>
    <div class="sz-sfmri-data-area">
      <div>
        <el-upload
          class="upload-demo"
          action="http://127.0.0.1:8000/api/upload_data"
          name="datafile"
          :on-change="handleChange"
          :on-success="uploadSuccess"
          :file-list="fileList">
          <el-button size="large" type="primary">Upload</el-button>
        </el-upload>
      </div>
      <div style="margin-top: 14px">
        <el-table
          class="data-table"
          :data="data_table.slice((currpage - 1) * pagesize, currpage * pagesize)"
          @selection-change="handleSelectionChange"
          stripe
          border
          style="width: 100%; background-color: #E8E8E8; color: #282828"
          >
          <el-table-column
          label="Data ID"
          prop="fields.data_id">
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
      currpage: 1
    }
  },
  mounted: function () {
    this.showData()
  },
  methods: {
    showData () {
      axios.get('http://127.0.0.1:8000/api/show_data')
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
        this.$message({showClose: true, message: 'Successfully uploaded!', type: 'success'})
      } else if (response.msg === 'existed') {
        this.$message({showClose: true, message: 'File existed!', type: 'warning'})
      }
    },
    handleCurrentChange (cpage) {
      this.currpage = cpage
    },
    handleSizeChange (psize) {
      this.pagesize = psize
    },
    handleSelectionChange (val) {
      console.log(val)
    }
  }
}
</script>

<style lang="scss">
.sz-sfmri-data-area {
  margin: 14px;
  padding: 28px;
  background-color: #FFFFFF;
}
</style>

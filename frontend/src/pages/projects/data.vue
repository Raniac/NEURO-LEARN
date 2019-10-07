<template>
  <div style="text-align: center">
    <div class="data-area">
      <div>
        <el-upload
          class="upload-demo"
          :action="upload_url"
          name="datafile"
          style="float: left"
          :on-change="handleChange"
          :on-success="uploadSuccess"
          :file-list="fileList">
          <el-button size="large" type="primary">Upload</el-button>
        </el-upload>
        <el-input placeholder="Search data by name" v-model="search_input" class="input-with-select" style="width: 50%; float: right">
          <el-button slot="append" icon="el-icon-search"></el-button>
        </el-input>
      </div>
      <div style="margin-top: 60px">
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
          <el-table-column
            fixed="right"
            label="Action"
            width="100">
            <template slot-scope="scope" style="font-size: 20px">
              <el-button @click="handleDownload(scope.row)" size="small" icon="el-icon-download" circle></el-button>
              <el-button @click="handleDelete(scope.row)" type="danger" size="small" icon="el-icon-delete" circle></el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div style="margin-top: 14px; padding-bottom: 30px">
        <el-pagination
        background
        layout="prev, pager, next"
        :page-size="pagesize"
        :total="data_table.length"
        @current-change="handleCurrentChange"
        @size-change="handleSizeChange"
        style="float: left">
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
      search_input: '',
      proj_id: '',
      upload_url: '/api/v0/upload_data?proj_id='
    }
  },
  mounted: function () {
    if (this.$route.query.projectid) {
      this.proj_id = this.$route.query.projectid
      this.showData()
      this.upload_url += this.proj_id
    } else {
      this.$alert('Choose a project first!', 'Error!', {
        confirmButtonText: 'Confirm',
        callback: action => {
          this.$router.replace({
            path: '/projects/overview',
            component: resolve => require(['@/pages/projects/overview'], resolve)
          })
        }
      })
    }
  },
  methods: {
    showData () {
      axios.get('/api/v0/show_data?proj_id=' + this.proj_id)
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
        this.showData()
        console.log(response)
      } else if (response.msg === 'existed') {
        this.$message({showClose: true, message: 'File existed!', type: 'warning'})
        console.log(response)
      }
    },
    handleDelete (row) {
      console.log(row.fields.data_id)
      this.$confirm('Are you sure?', 'Attention!', {
        confirmButtonText: 'Yes',
        cancelButtonText: 'No'
      }).then(() => {
        axios.get('/api/v0/delete_data?proj_id=' + this.proj_id + '&data_id=' + row.fields.data_id)
          .then(response => {
            var res = response.data
            if (res.error_num === 0) {
              console.log(res)
              this.showData()
            } else {
              this.$message.error(res['msg'])
              console.log(res['msg'])
            }
          })
      }).catch(() => {})
    },
    handleDownload (row) {
      console.log(row.fields.data_id)
      // window.location.href = '/api/v0/download_data?data_id=' + row.fields.data_id
      axios.get('/api/v0/download_data?data_id=' + row.fields.data_id)
        .then(response => {
          var res = response.data
          if (res.error_num === 1) {
            this.$message.error(res['msg'])
            console.log(res['msg'])
          } else {
            window.location.href = '/api/v0/download_data?data_id=' + row.fields.data_id
          }
        })
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

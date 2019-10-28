<template>
  <div style="text-align: center">
    <div class="profile-area">
      <div class="profile-detail">
        <img style="float: left; height: auto; width: 200px" src="https://raw.githubusercontent.com/Raniac/NEURO-LEARN/master/doc/img/lby.png">
        <div style="line-height: 28px">
          <span style="padding-left: 20px; font-family: Arial; font-weight: 200; font-size: 40px; color: #282828">Benny Ray</span><br/>
          <span style="padding-left: 20px; font-family: Arial; font-weight: 100; font-size: 20px; color: #505050">Master of Engineering | SCUT</span><br/>
          <span style="padding-left: 20px; font-family: Arial; font-weight: 100; font-size: 20px; color: #505050">Interests:  Artificial Intelligence & Neuro-Informatics</span><br/>
        </div>
        <div style="margin-top: 16px; line-height: 28px">
          <a class="github-link" href="https://github.com/Raniac/NEURO-LEARN" target="_blank">NEURO-LEARN</a><br/>
          <a class="github-link" href="https://github.com/Raniac" target="_blank">GitHub/Raniac</a><br/>
          <a class="github-link" href="mailto:leibingye@outlook.com">leibingye@outlook.com</a>
        </div>
      </div>
    </div>
    <div class="projects-area">
      <div>
        <h1 style="padding-left: 20px; font-family: Arial; font-weight: 150; font-size: 30px; color: #505050">
          Joined Projects | <strong style="font-size: 18px; color: #505050">Logged in as <strong style="font-size: 30px; color: #00CCFF">{{ username }}</strong> (User ID: {{ user_id }})</strong>
        </h1>
      </div>
      <div style="margin: 14px">
        <el-table
          class="projects-table"
          :data="projects_table"
          stripe
          border
          style="width: 100%; background-color: #E8E8E8; color: #282828; ">
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" in-line class="projects-table-expand">
                <el-form-item label="Introduction">
                  <span>{{ props.row.fields.introduction }}</span>
                </el-form-item>
                <el-form-item label="Methods">
                  <span>{{ props.row.fields.methods }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column
          label="Project ID"
          prop="fields.proj_id"
          width="180px">
          </el-table-column>
          <el-table-column
          label="Project Title"
          prop="fields.title">
          </el-table-column>
          <el-table-column
          label="Project Label"
          prop="fields.label"
          width="120px">
          </el-table-column>
          <el-table-column
            fixed="right"
            label="Action"
            width="80px">
            <template slot-scope="scope" style="font-size: 20px">
              <el-button @click="handleQuit(scope.row)" type="danger" size="small">QUIT</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    <div class="projects-area">
      <div>
        <h1 style="float: left; padding-left: 20px; font-family: Arial; font-weight: 150; font-size: 30px; color: #505050">All Projects</h1>
      </div>
      <div style="margin: 14px">
        <el-input placeholder="Search projects by title or label" v-model="search_input" class="input-with-select" style="float: right; width: 50%">
          <el-button slot="append" icon="el-icon-search"></el-button>
        </el-input>
      </div>
      <div style="margin: 14px">
        <el-table
          class="projects-table"
          :data="all_projects_table.filter(data => (!search_input || data.fields.title.toLowerCase().includes(search_input.toLowerCase()) || data.fields.label.toLowerCase().includes(search_input.toLowerCase()))).slice((currpage - 1) * pagesize, currpage * pagesize)"
          stripe
          border
          style="width: 100%; background-color: #E8E8E8; color: #282828; ">
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" in-line class="projects-table-expand">
                <el-form-item label="Introduction">
                  <span>{{ props.row.fields.introduction }}</span>
                </el-form-item>
                <el-form-item label="Methods">
                  <span>{{ props.row.fields.methods }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column
          label="Project ID"
          prop="fields.proj_id"
          width="180px">
          </el-table-column>
          <el-table-column
          label="Project Title"
          prop="fields.title">
          </el-table-column>
          <el-table-column
          label="Project Label"
          prop="fields.label"
          width="120px">
          </el-table-column>
          <el-table-column
            fixed="right"
            label="Action"
            width="100px">
            <template slot-scope="scope" style="font-size: 20px">
              <!-- <el-button @click="handleJoin(scope.row)" type="primary" size="small">JOIN</el-button> -->
              <el-button @click="handleJoin(scope.row)" size="small" icon="el-icon-plus" circle></el-button>
              <el-button @click="handleDelete(scope.row)" type="danger" size="small" icon="el-icon-delete" circle></el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div style="margin: 14px; padding-bottom: 30px">
        <el-pagination
          background
          layout="prev, pager, next"
          :page-size="pagesize"
          :total="all_projects_table.length"
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
  mounted () {
    this.username = sessionStorage.getItem('Username')
    this.user_id = sessionStorage.getItem('UserID')
    this.showJoinedProjects()
    this.showAllProjects()
  },
  data () {
    return {
      search_input: '',
      pagesize: 4,
      currpage: 1,
      username: '',
      user_id: '',
      projects_table: [],
      all_projects_table: []
    }
  },
  methods: {
    showJoinedProjects () {
      axios.get('/api/v0/show_project_overview')
        .then(response => {
          var res = response.data
          if (res.error_num === 0) {
            console.log(res)
            this.projects_table = res['list']
            console.log(this.projects_table)
          } else {
            this.$message.error('Failed!')
            console.log(res['msg'])
          }
        })
    },
    showAllProjects () {
      axios.get('/api/v0/show_all_projects')
        .then(response => {
          var res = response.data
          if (res.error_num === 0) {
            console.log(res)
            this.all_projects_table = res['list']
            console.log(this.all_projects_table)
          } else {
            this.$message.error('Failed!')
            console.log(res['msg'])
          }
        })
    },
    handleJoin (row) {
      axios.get('/api/v0/join_project?proj_id=' + row.fields.proj_id)
        .then(response => {
          var res = response.data
          if (res.error_num === 0) {
            console.log(res)
            this.$message({showClose: true, message: 'Successfully joined ' + row.fields.proj_id, type: 'success'})
            this.showJoinedProjects()
          } else {
            this.$message.warning(res['msg'])
            console.log(res['msg'])
          }
        })
    },
    handleDelete (row) {
      console.log(row.fields.proj_id)
      this.$confirm('Are you sure?', 'Attention!', {
        confirmButtonText: 'Yes',
        cancelButtonText: 'No'
      }).then(() => {
        axios.get('/api/v0/delete_project?proj_id=' + row.fields.proj_id)
          .then(response => {
            var res = response.data
            if (res.error_num === 0) {
              console.log(res)
              this.showAllProjects()
              this.showJoinedProjects()
            } else {
              this.$message.error(res['msg'])
              console.log(res['msg'])
            }
          })
      }).catch(() => {})
    },
    handleQuit (row) {
      axios.get('/api/v0/quit_project?proj_id=' + row.fields.proj_id)
        .then(response => {
          var res = response.data
          if (res.error_num === 0) {
            console.log(res)
            this.$message({showClose: true, message: 'Successfully quitted ' + row.fields.proj_id, type: 'success'})
            this.showJoinedProjects()
          } else {
            this.$message.warning(res['msg'])
            console.log(res['msg'])
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
.profile-area {
  width: 772px;
  margin: 14px auto;
  text-align: left;
  padding: 14px;
  background-color: #FFFFFF;
  .profile-detail {
    padding: 14px;
    min-height: 200px;
    .github-link {
      padding-left: 20px;
      font-family: Arial;
      font-weight: 100;
      font-size: 20px;
      color: #282828;
      &:hover {
      color: #00CCFF;
      }
    }
  }
}
.projects-area {
  width: 772px;
  margin: 14px auto;
  padding: 14px;
  text-align: left;
  background-color: #FFFFFF;
}
.projects-table-expand {
  font-size: 0;
  width: 100%;
  }
  .projects-table-expand label {
    width: 140px;
    color: #505050;
  }
  .projects-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
  }
</style>

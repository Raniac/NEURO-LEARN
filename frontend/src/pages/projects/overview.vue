<template>
  <div style="text-align: center">
    <div class="data-overview-area">
      <div style="padding: 20px 0px">
        <div style="text-align: left">
          <el-select v-model="selected_project.title" style="margin: 0 20px; width: 300px" placeholder="Select Project" @change="handelSelectionChange">
            <el-option
              v-for="project_option in project_options"
              :key="project_option.fields.title"
              :label="project_option.fields.label"
              :value="project_option.fields.title">
            </el-option>
          </el-select>
        </div>
        <div style="line-height: 30px; font-family: 'Times New Roman'; text-align: left; width: 700px; margin: 0 auto; font-size: 18px; color: #000000">
          <h2>{{ selected_project.title }}</h2>
          <h3>Introduction</h3>
          <p>{{ selected_project.introduction }}</p>
          <h3>Methods</h3>
          <p>{{ selected_project.methods }}</p>
          <el-button round @click="handleDownloadWorkflows"><i class="el-icon-download"></i> Local Workflows</el-button>
          <el-button round :href="selected_project.templates_url" @click="handleDownloadTemplates"><i class="el-icon-download"></i> Dataset Templates</el-button>
          <el-button type="primary" round @click="handleUploadData"><i class="el-icon-upload2"></i> Upload Prepared Datasets</el-button>
          <h3>Flowchart</h3>
        </div>
        <div style="text-align: center">
          <img style="width: 700px; margin-top: -10px" :src="selected_project.flowchart_url">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      selected_project: {
        proj_id: '',
        label: '',
        title: '',
        introduction: '',
        methods: '',
        flowchart_url: '',
        workflows_url: '',
        templates_url: ''
      },
      project_options: []
    }
  },
  mounted () {
    this.showProjectOverview()
  },
  methods: {
    showProjectOverview () {
      axios.get('/api/v0/show_project_overview')
        .then(response => {
          var res = response.data
          if (res.error_num === 0) {
            console.log(res)
            this.project_options = res['list']
            console.log(this.project_options)
            this.selected_project.proj_id = this.project_options[0].fields.proj_id
            this.selected_project.label = this.project_options[0].fields.label
            this.selected_project.title = this.project_options[0].fields.title
            this.selected_project.introduction = this.project_options[0].fields.introduction
            this.selected_project.methods = this.project_options[0].fields.methods
            this.selected_project.flowchart_url = this.project_options[0].fields.flowchart_url
            this.selected_project.workflows_url = this.project_options[0].fields.workflows_url
            this.selected_project.templates_url = this.project_options[0].fields.templates_url
          } else {
            this.$message.error('Failed!')
            console.log(res['msg'])
          }
        })
    },
    handleUploadData () {
      this.$router.push({
        path: '/projects/data',
        query: {projectid: this.selected_project.proj_id}
      })
    },
    handleDownloadWorkflows () {
      window.location.href = this.selected_project.workflows_url
    },
    handleDownloadTemplates () {
      window.location.href = this.selected_project.templates_url
    },
    handelSelectionChange () {
      console.log(this.selected_project.title)
      var i
      for (i in this.project_options) {
        if (this.project_options[i].fields.title === this.selected_project.title) {
          this.selected_project.proj_id = this.project_options[i].fields.proj_id
          this.selected_project.label = this.project_options[i].fields.label
          this.selected_project.introduction = this.project_options[i].fields.introduction
          this.selected_project.methods = this.project_options[i].fields.methods
          this.selected_project.flowchart_url = this.project_options[i].fields.flowchart_url
          this.selected_project.workflows_url = this.project_options[i].fields.workflows_url
          this.selected_project.templates_url = this.project_options[i].fields.templates_url
        }
      }
      console.log(this.selected_project.proj_id)
    }
  }
}
</script>

<style lang="scss">
.data-overview-area {
  width: 760px;
  text-align: left;
  margin: 14px auto;
  padding: 14px 20px;
  background-color: #FFFFFF;
}
</style>

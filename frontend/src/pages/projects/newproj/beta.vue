<template>
  <div style="text-align: center">
    <div class="ml-task-form">
      <div style="text-align: left; width: 700px; margin: 0 auto; font-family: 'Arial', Times, serif; font-size: 18px; color: #505050">
        <h2>Create Your Own Project</h2>
      </div>
      <el-form ref="form" :model="form" label-width="120px" label-position="middle">
        <el-form-item label="Project Label">
          <el-input v-model="newform.label" placeholder="Specify Project Label. (e.g. 'SZ with sfMRI')"></el-input>
        </el-form-item>
        <el-form-item label="Project Title">
          <el-input
            type="textarea"
            v-model="newform.title"
            placeholder="Specify Project Title. (e.g. 'Study of Schizophrenia with Pattern Analysis of Structural/Functional MRI Data')">
          </el-input>
        </el-form-item>
        <el-form-item label="Introduction">
          <el-input
            type="textarea"
            v-model="newform.introduction"
            placeholder="Specify Introduction. (e.g. 'Fusing structural and functional MRI data, use DPABI on matlab to compute the features, and analyze SZ.')">
          </el-input>
        </el-form-item>
        <el-form-item label="Methods">
          <el-input
            type="textarea"
            v-model="newform.methods"
            placeholder="Specify Methods. (e.g. 'Compute gray matter volume, regional homogeneity, amplitude of low frequency fluctuations and degree centrality.')">
          </el-input>
        </el-form-item>
        <el-form-item label="Flowchart URL">
          <el-input v-model="newform.flowchart_url" placeholder="Specify the Flowchart Image Location."></el-input>
        </el-form-item>
        <el-form-item label="Workflows URL">
          <el-input v-model="newform.workflows_url" placeholder="Specify Where to Download the Workflows."></el-input>
        </el-form-item>
        <el-form-item label="Templates URL">
          <el-input v-model="newform.templates_url" placeholder="Specify Where to Download the Templates."></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onCreate">Create</el-button>
          <el-button @click="onCancel">Cancel</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      newform: {
        label: '',
        title: '',
        introduction: '',
        methods: '',
        flowchart_url: '',
        workflows_url: '',
        templates_url: ''
      }
    }
  },
  mounted () {},
  methods: {
    onCreate () {
      this.$confirm('Create this project now?', 'Attention!', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel'
      }).then(() => {
        this.newProj()
      }).catch(() => {})
    },
    onCancel () {
      this.$router.replace({
        path: '/profile',
        component: resolve => require(['@/pages/profile'], resolve)
      })
    },
    newProj () {
      console.log(JSON.stringify(this.newform))
      axios.post('/api/v0/new_proj', JSON.stringify(this.newform))
        .then(response => {
          var res = response.data
          if (res.error_num === 0) {
            this.$router.replace({
              path: '/profile',
              component: resolve => require(['@/pages/profile'], resolve)
            })
            console.log(res)
          } else {
            this.$message.error('Failed creation! Please retry!')
            console.log(res['msg'])
          }
        })
    }
  }
}
</script>

<style lang="scss">
.ml-task-form {
  background-color: #FFFFFF;
  width: 760px;
  margin: 14px auto;
  padding: 14px 20px;
  text-align: left;
  .select-data {
    width: 400px;
  }
  .select-label {
    width: 200px;
  }
  .select-model {
    width: 300px;
  }
  .select-cv-type {
    width: 200px;
  }
}
</style>

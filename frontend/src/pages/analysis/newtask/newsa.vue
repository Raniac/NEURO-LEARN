<template>
<div style="padding: 14px">
  <div class="tasks-form-area">
    <el-tabs type="border-card" stretch style="box-shadow: 0px 0 0px #FFFFFF;" v-model="tabsValue" @tab-click="handleTabClick">
      <el-tab-pane label="Difference Analysis" name="da">
        <div class="da-task-form">
          <el-form ref="form" :model="newform" label-width="90px" label-position="middle">
            <el-form-item label="Task Name">
              <el-input v-model="newform.task_name"></el-input>
            </el-form-item>
            <el-form-item label="Task Type">
              <el-radio-group v-model="taskType">
                <el-radio label="T-test">T-test</el-radio>
                <el-radio label="ANOVA">ANOVA</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="Proj. Name">
              <el-select class="select-label" v-model="newform.project_name" placeholder="Select Project">
                <el-option v-for="(project_option, key) in form.project_options" :label="project_option.name" :value="project_option.value" :key="key"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Test Var.">
              <el-select class="select-data" v-model="newform.test_var_data_x" placeholder="Select Test Variables">
              <el-option v-for="(data_option, key) in data_table" :label="data_option.fields.data_name" :value="data_option.fields.data_path" :key="key"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Group Var.">
              <el-select class="select-data" v-model="newform.group_var_data_y" placeholder="Select Group Variables">
              <el-option v-for="(group_variables_option, key) in form.group_variables_options" :label="group_variables_option.name" :value="group_variables_option.value" :key="key"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Note">
              <el-input type="textarea" v-model="newform.note"></el-input>
            </el-form-item>
            <el-form-item label="Verbose">
              <el-switch active-text="On" inactive-text="Off" v-model="newform.verbose"></el-switch>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit">Submit</el-button>
              <el-button @click="onCancel">Cancel</el-button>
            </el-form-item>
            </el-form>
        </div>
      </el-tab-pane>
      <el-tab-pane label="Correlation Analysis" name="ca">
        <div class="ca-task-form">
          <el-form ref="form" :model="newform" label-width="90px" label-position="middle">
            <el-form-item label="Task Name">
              <el-input v-model="newform.task_name"></el-input>
            </el-form-item>
            <el-form-item label="Task Type">
              <el-radio-group v-model="taskType">
                <el-radio label="Pearson">Pearson</el-radio>
                <el-radio label="Spearman">Spearman</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="Proj. Name">
              <el-select class="select-label" v-model="newform.project_name" placeholder="Select Project">
                <el-option v-for="(project_option, key) in form.project_options" :label="project_option.name" :value="project_option.value" :key="key"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Data X">
              <el-select class="select-data" v-model="newform.test_var_data_x" placeholder="Select Data X">
              <el-option v-for="(data_option, key) in data_table" :label="data_option.fields.data_name" :value="data_option.fields.data_path" :key="key"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Data Y">
              <el-select class="select-data" v-model="newform.group_var_data_y" placeholder="Select Data Y">
              <el-option v-for="(data_option, key) in data_table" :label="data_option.fields.data_name" :value="data_option.fields.data_path" :key="key"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Note">
              <el-input type="textarea" v-model="newform.note"></el-input>
            </el-form-item>
            <el-form-item label="Verbose">
              <el-switch active-text="On" inactive-text="Off" v-model="newform.verbose"></el-switch>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit">Submit</el-button>
              <el-button @click="onCancel">Cancel</el-button>
            </el-form-item>
            </el-form>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      data_table: [],
      tabsValue: 'da',
      taskType: '',
      newform: {
        project_name: '',
        task_name: '',
        task_type: '',
        test_var_data_x: [],
        group_var_data_y: [],
        note: '',
        verbose: false
      },
      form: {
        project_options: [
          {name: 'SZ with s/fMRI', value: 'sz_with_sfmri'},
          {name: 'AD with sMRI', value: 'ad_with_smri'},
          {name: 'SZ with fMRI', value: 'sz_with_fmri'}
        ],
        group_variables_options: [
          {name: 'GROUP', value: 'GROUP'}
        ]
      }
    }
  },
  mounted () {
    this.updateData()
  },
  methods: {
    handleTabClick () {
    },
    onSubmit () {
      this.$confirm('Submit this task now?', 'Attention!', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel'
      }).then(() => {
        console.log('New task!')
        this.newform.task_type = this.tabsValue + '-' + this.taskType
        console.log(this.newform.task_type)
      }).catch(() => {})
    },
    onCancel () {
      this.$router.replace({
        path: '/analysis/overview',
        component: resolve => require(['@/pages/analysis/overview'], resolve)
      })
    },
    updateData () {
      axios.get('/api/show_data')
        .then(response => {
          var res = response.data
          if (res.error_num === 0) {
            console.log(res)
            this.data_table = res['list']
            console.log(this.data_table[0].fields.data_name)
          } else {
            this.$message.error('Failed!')
            console.log(res['msg'])
          }
        })
    },
    newTask () {
      console.log(JSON.stringify(this.newform))
      axios.post('/api/new_sa_task', JSON.stringify(this.newform))
        .then(response => {
          var res = response.data
          if (res.error_num === 0) {
            this.$router.replace({
              path: '/analysis/overview',
              component: resolve => require(['@/pages/analysis/overview'], resolve)
            })
            console.log(res)
          } else {
            this.$message.error('Failed submission!')
            console.log(res['msg'])
          }
        })
    }
  }
}
</script>

<style lang="scss">
.select-data {
    width: 400px;
}
</style>

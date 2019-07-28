<template>
<div style="text-align: center">
  <div class="tasks-form-area" style="width: 800px; margin: 14px auto; text-align: left">
    <el-tabs type="border-card" stretch style="box-shadow: 0px 0 0px #FFFFFF" v-model="tabsValue" @tab-click="handleTabClick">
      <el-tab-pane label="Difference Analysis" name="DA">
        <div class="da-task-form">
          <el-form ref="form" :model="newform" label-width="100px" label-position="middle">
            <el-form-item label="Task Name">
              <el-input v-model="newform.task_name" placeholder="Specify Task Name. (e.g. 'Difference analysis t-test of SZ group with AAL90')"></el-input>
            </el-form-item>
            <el-form-item label="Task Type">
              <el-radio-group v-model="taskType">
                <el-radio label="T-test">T-test</el-radio>
                <el-radio label="ANOVA">ANOVA</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="Proj. Name">
              <el-select class="select-label" v-model="selected_project_label" placeholder="Select Project" @change="handelSelectionChange">
                <el-option v-for="(project_option, key) in form.project_options" :label="project_option.fields.label" :value="project_option.fields.label" :key="key"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Test Var.">
              <el-select class="select-data" v-model="newform.test_var_data_x" placeholder="Select Test Variables" filterable multiple>
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
      <el-tab-pane label="Correlation Analysis" name="CA">
        <div class="ca-task-form">
          <el-form ref="form" :model="newform" label-width="100px" label-position="middle">
            <el-form-item label="Task Name">
              <el-input v-model="newform.task_name" placeholder="Specify Task Name. (e.g. 'Correlation analysis Pearson of SZ group with AAL90')"></el-input>
            </el-form-item>
            <el-form-item label="Task Type">
              <el-radio-group v-model="taskType">
                <el-radio label="Pearson">Pearson</el-radio>
                <el-radio label="Spearman">Spearman</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="Proj. Name">
              <el-select class="select-label" v-model="selected_project_label" placeholder="Select Project" @change="handelSelectionChange">
                <el-option v-for="(project_option, key) in form.project_options" :label="project_option.fields.label" :value="project_option.fields.label" :key="key"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Data X">
              <el-select class="select-data" v-model="newform.test_var_data_x" placeholder="Select Data X" filterable multiple>
              <el-option v-for="(data_option, key) in data_table" :label="data_option.fields.data_name" :value="data_option.fields.data_path" :key="key"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Data Y">
              <el-select class="select-data" v-model="newform.group_var_data_y" placeholder="Select Data Y" filterable multiple>
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
      selected_project_label: '',
      selected_project_id: '',
      data_table: [],
      tabsValue: 'DA',
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
        project_options: [],
        group_variables_options: [
          {name: 'GROUP', value: 'GROUP'}
        ]
      }
    }
  },
  mounted () {
    this.updateProjects()
    // this.updateData()
  },
  methods: {
    handleTabClick () {
    },
    onSubmit () {
      this.$confirm('Submit this task now?', 'Attention!', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel'
      }).then(() => {
        this.newform.task_type = this.tabsValue + '-' + this.taskType
        this.newTask()
      }).catch(() => {})
    },
    onCancel () {
      this.$router.replace({
        path: '/analysis/overview',
        component: resolve => require(['@/pages/analysis/overview'], resolve)
      })
    },
    updateProjects () {
      axios.get('/api/show_project_overview')
        .then(response => {
          var res = response.data
          if (res.error_num === 0) {
            console.log(res)
            this.form.project_options = res['list']
            console.log(this.form.project_options)
            // this.selected_project_label = this.form.project_options[0].fields.label
            // this.selected_project_id = this.form.project_options[0].fields.project_id
          } else {
            this.$message.error('Failed!')
            console.log(res['msg'])
          }
        })
    },
    handelSelectionChange () {
      console.log(this.selected_project_label)
      var i
      for (i in this.form.project_options) {
        if (this.form.project_options[i].fields.label === this.selected_project_label) {
          this.selected_project_id = this.form.project_options[i].fields.project_id
        }
      }
      console.log(this.selected_project_id)
      this.updateData()
    },
    updateData () {
      axios.get('/api/show_data?project_id=' + this.selected_project_id)
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

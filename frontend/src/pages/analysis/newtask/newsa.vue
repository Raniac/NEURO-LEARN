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
                <el-radio label="sa_da_ttest">T-test</el-radio>
                <el-radio label="sa_da_anova">ANOVA</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="Proj. Name">
              <el-select class="select-label" v-model="selected_proj_label" placeholder="Select proj" @change="handelSelectionChange">
                <el-option v-for="(proj_option, key) in form.proj_options" :label="proj_option.fields.label" :value="proj_option.fields.label" :key="key"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Test Var.">
              <el-select class="select-data" v-model="newform.test_var_data_x" placeholder="Select Test Variables" filterable multiple>
              <el-option v-for="(data_option, key) in data_table" :label="data_option.fields.data_name" :value="data_option.fields.data_name" :key="key"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Group Var.">
              <el-select class="select-data" v-model="newform.group_var_data_y" placeholder="Select Group Variables">
              <el-option v-for="(group_variables_option, key) in form.group_variables_options" :label="group_variables_option.name" :value="group_variables_option.value" :key="key"></el-option>
              </el-select>
            </el-form-item>
            <!-- <el-form-item label="Note">
              <el-input type="textarea" v-model="newform.note"></el-input>
            </el-form-item>
            <el-form-item label="Verbose">
              <el-switch active-text="On" inactive-text="Off" v-model="newform.verbose"></el-switch>
            </el-form-item> -->
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
                <el-radio label="sa_ca_prson">Pearson</el-radio>
                <el-radio label="sa_ca_spman">Spearman</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="Proj. Name">
              <el-select class="select-label" v-model="selected_proj_label" placeholder="Select proj" @change="handelSelectionChange">
                <el-option v-for="(proj_option, key) in form.proj_options" :label="proj_option.fields.label" :value="proj_option.fields.label" :key="key"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Data X">
              <el-select class="select-data" v-model="newform.test_var_data_x" placeholder="Select Data X" filterable multiple>
              <el-option v-for="(data_option, key) in data_table" :label="data_option.fields.data_name" :value="data_option.fields.data_name" :key="key"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Data Y">
              <el-select class="select-data" v-model="newform.group_var_data_y" placeholder="Select Data Y" filterable multiple>
              <el-option v-for="(data_option, key) in data_table" :label="data_option.fields.data_name" :value="data_option.fields.data_name" :key="key"></el-option>
              </el-select>
            </el-form-item>
            <!-- <el-form-item label="Note">
              <el-input type="textarea" v-model="newform.note"></el-input>
            </el-form-item> -->
            <!-- <el-form-item label="Verbose">
              <el-switch active-text="On" inactive-text="Off" v-model="newform.verbose"></el-switch>
            </el-form-item> -->
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
      selected_proj_label: '',
      selected_proj_id: '',
      data_table: [],
      tabsValue: 'DA',
      taskType: '',
      newform: {
        proj_name: '',
        task_name: '',
        task_type: '',
        test_var_data_x: [],
        group_var_data_y: []
      },
      form: {
        proj_options: [],
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
        this.newform.task_type = this.taskType
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
      axios.get('/api/v0/show_project_overview')
        .then(response => {
          var res = response.data
          if (res.error_num === 0) {
            console.log(res)
            this.form.proj_options = res['list']
            console.log(this.form.proj_options)
          } else {
            this.$message.error('Failed!')
            console.log(res['msg'])
          }
        })
    },
    handelSelectionChange () {
      console.log(this.selected_proj_label)
      var i
      for (i in this.form.proj_options) {
        if (this.form.proj_options[i].fields.label === this.selected_proj_label) {
          this.selected_proj_id = this.form.proj_options[i].fields.proj_id
        }
      }
      console.log(this.selected_proj_id)
      this.updateData()
    },
    updateData () {
      axios.get('/api/v0/show_data?proj_id=' + this.selected_proj_id)
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
      this.newform.proj_name = this.selected_proj_label
      this.newform.proj_id = this.selected_proj_id
      console.log(JSON.stringify(this.newform))
      axios.post('/api/v0/new_task', JSON.stringify(this.newform))
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

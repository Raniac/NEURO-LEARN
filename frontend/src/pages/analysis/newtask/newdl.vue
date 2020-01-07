<template>
  <div style="text-align: center">
    <div class="ml-task-form">
      <div style="text-align: left; width: 700px; margin: 0 auto; font-family: 'Arial', Times, serif; font-size: 18px; color: #505050">
        <h2><i class="el-icon-edit-outline"></i> New Deep Learning Task</h2>
      </div>
      <el-form ref="form" :model="form" label-width="100px" label-position="middle">
        <el-form-item label="Task Name">
          <el-input v-model="newform.task_name" placeholder="Specify Task Name, Date_Model by Default."></el-input>
        </el-form-item>
        <el-form-item label="Task Type">
          <el-radio-group v-model="newform.task_type">
            <el-radio label="ts">Train from Scratch</el-radio>
            <el-radio label="ft">Fine Tune</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="Proj. Name">
          <el-select class="select-label" v-model="selected_proj_label" placeholder="Select Project" @change="handelSelectionChange">
            <el-option v-for="(proj_option, key) in form.proj_options" :label="proj_option.fields.label" :value="proj_option.fields.label" :key="key"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Train Data">
          <el-select class="select-data" v-model="newform.train_data" placeholder="Select Train Data" filterable multiple>
            <el-option v-for="(data_option, key) in data_table" :label="data_option.fields.data_name" :value="data_option.fields.data_name" :key="key"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Val. Data">
          <el-select class="select-data" v-model="newform.val_data" placeholder="Select Validation Data" filterable multiple>
            <el-option v-for="(data_option, key) in data_table" :label="data_option.fields.data_name" :value="data_option.fields.data_name" :key="key"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Model">
          <el-select class="select-model" v-model="newform.model" placeholder="Select Model" filterable multiple>
            <el-option v-for="(model_option, key) in form.model_options" :label="model_option.name" :value="model_option.value" :key="key"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Param. Set." style="color: #505050">
          Batch Size <el-input-number class="input-param" controls-position="right" size="small" min="0" max="1000" step="10" v-model="newform.param_set.batch_size"></el-input-number>
          &emsp;Learning Rate <el-input-number class="input-param" controls-position="right" size="small" min="0" max="1" v-model="newform.param_set.learning_rate"></el-input-number>
          &emsp;Epochs <el-input-number class="input-param" controls-position="right" size="small" min="0" max="1000" step="10" v-model="newform.param_set.epochs"></el-input-number>
          <br>
          Step Size <el-input-number class="input-param" controls-position="right" size="small" min="0" max="100" step="10" v-model="newform.param_set.step_size"></el-input-number>
          &emsp;Gamma <el-input-number class="input-param" controls-position="right" size="small" min="0" max="1" v-model="newform.param_set.gamma"></el-input-number>
          <br>
          <a style="color: #00CCFF" href="https://github.com/Raniac/NEURO-LEARN/wiki/" target="_blank">What are these?</a>
        </el-form-item>
        <el-form-item label="Enable Test">
          <el-switch
            v-model="newform.enable_test">
          </el-switch>
        </el-form-item>
        <el-form-item label="Test Data">
          <el-select class="select-data" v-model="newform.test_data" placeholder="Select Test Data" :disabled="!newform.enable_test" filterable multiple>
            <el-option v-for="(data_option, key) in data_table" :label="data_option.fields.data_name" :value="data_option.fields.data_name" :key="key"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">Submit</el-button>
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
      selected_proj_label: '',
      selected_proj_id: '',
      data_table: [],
      newform: {
        proj_id: '',
        proj_name: '',
        task_name: '',
        task_type: '',
        train_data: [],
        val_data: [],
        enable_test: false,
        test_data: [],
        model: [],
        param_set: {
          learning_rate: 5e-2,
          batch_size: 10,
          step_size: 60,
          gamma: 0.2,
          epochs: 200
        },
        cv_type: ''
      },
      form: {
        proj_options: [],
        model_options: []
      }
    }
  },
  mounted () {
    this.updateProjects()
    // this.updateData()
  },
  methods: {
    onSubmit () {
      this.$confirm('Submit this task now?', 'Attention!', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel'
      }).then(() => {
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
            this.$message.error('Failed submission! Please retry!')
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
  .input-param {
    width: 100px;
  }
  .second-label {
    font-size: 10px;
    padding: 0px 4px;
  }
}
</style>

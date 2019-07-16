<template>
  <div>
    <div class="ml-task-form">
      <el-form ref="form" :model="form" label-width="100px" label-position="middle">
        <el-form-item label="Task Name">
          <el-input v-model="newform.task_name" placeholder="Specify Task Name. (e.g. 'Classify SZ with ANOVA SVM on 246-template sfMRI data')"></el-input>
        </el-form-item>
        <el-form-item label="Task Type">
          <el-radio-group v-model="newform.task_type" @change="onRadioChange">
            <el-radio label="Classification">Classification</el-radio>
            <el-radio label="Regression">Regression</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="Proj. Name">
          <el-select class="select-label" v-model="newform.project_name" placeholder="Select Project">
            <el-option v-for="(project_option, key) in form.project_options" :label="project_option.name" :value="project_option.value" :key="key"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Train Data">
          <el-select class="select-data" v-model="newform.train_data" placeholder="Select Train Data" filterable multiple>
            <el-option v-for="(data_option, key) in data_table" :label="data_option.fields.data_name" :value="data_option.fields.data_path" :key="key"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Label">
          <el-select class="select-label" v-model="newform.label" placeholder="Select Label">
          <el-option v-for="(label_option, key) in form.label_options" :label="label_option.name" :value="label_option.value" :key="key"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Feat. Sel.">
          <el-select class="select-model" v-model="newform.feat_sel" placeholder="Select Model">
            <el-option v-for="(feat_sel_option, key) in form.feat_sel_options" :label="feat_sel_option.name" :value="feat_sel_option.value" :key="key"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Estimator">
          <el-select class="select-model" v-model="newform.estimator" placeholder="Select Model">
            <el-option v-for="(estimator_option, key) in form.estimator_options" :label="estimator_option.name" :value="estimator_option.value" :key="key"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="CV Type">
          <el-select class="select-cv-type" v-model="newform.cv_type" placeholder="Select CV Type">
          <el-option v-for="(cv_type_option, key) in form.cv_type_options" :label="cv_type_option.name" :value="cv_type_option.value" :key="key"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Enable Test">
          <el-switch
            v-model="newform.enable_test">
          </el-switch>
        </el-form-item>
        <el-form-item label="Test Data">
          <el-select class="select-data" v-model="newform.test_data" placeholder="Select Test Data" :disabled="!newform.enable_test" filterable multiple>
            <el-option v-for="(data_option, key) in data_table" :label="data_option.fields.data_name" :value="data_option.fields.data_path" :key="key"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Note">
          <el-input type="textarea" v-model="newform.note"></el-input>
        </el-form-item>
        <!-- <el-form-item label="Verbose">
          <el-switch v-model="newform.verbose"></el-switch>
        </el-form-item> -->
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
      data_table: [],
      newform: {
        project_name: '',
        task_name: '',
        task_type: '',
        train_data: [],
        enable_test: false,
        test_data: [],
        label: '',
        feat_sel: '',
        estimator: '',
        cv_type: '',
        note: '',
        verbose: false
      },
      form: {
        project_options: [
          {name: 'SZ with s/fMRI', value: 'sz_with_sfmri'},
          {name: 'AD with sMRI', value: 'ad_with_smri'},
          {name: 'SZ with fMRI', value: 'sz_with_fmri'}
        ],
        label_options: [],
        feat_sel_options: [],
        estimator_options: [],
        cv_type_options: [
          {name: '10-fold', value: '10-fold'},
          {name: '5-fold', value: '5-fold'},
          {name: '3-fold', value: '3-fold'},
          {name: 'Leave-One-Out', value: 'Leave-One-Out'}
        ]
      }
    }
  },
  mounted () {
    this.updateData()
  },
  methods: {
    onRadioChange () {
      if (this.newform.task_type === 'Classification') {
        this.form.estimator_options = [
          {name: 'Support Vector Machine', value: 'Support Vector Machine'},
          {name: 'Random Forest', value: 'Random Forest'},
          {name: 'Linear Discriminative Analysis', value: 'Linear Discriminative Analysis'},
          {name: 'Logistic Regression', value: 'Logistic Regression'},
          {name: 'K Nearest Neighbor', value: 'K Nearest Neighbor'}
        ]
        this.form.label_options = [
          {name: 'GROUP', value: 'GROUP'}
        ]
        this.form.feat_sel_options = [
          {name: 'Analysis of Variance', value: 'Analysis of Variance'},
          {name: 'Principal Component Analysis', value: 'Principal Component Analysis'},
          {name: 'Recursive Feature Elimination', value: 'Recursive Feature Elimination'},
          {name: 'None', value: 'None'}
        ]
      } else if (this.newform.task_type === 'Regression') {
        this.form.estimator_options = [
          {name: 'Support Vector Regression', value: 'Support Vector Regression'},
          {name: 'Elastic Net', value: 'Elastic Net'},
          {name: 'Ordinary Least Square', value: 'Ordinary Least Square'},
          {name: 'Lasso Regression', value: 'Lasso Regression'},
          {name: 'Ridge Regression', value: 'Ridge Regression'}
        ]
        this.form.label_options = [
          {name: 'PANSS_P', value: 'PANSS_P'},
          {name: 'PANSS_N', value: 'PANSS_N'},
          {name: 'PANSS_G', value: 'PANSS_G'},
          {name: 'PANSS_T', value: 'PANSS_T'}
        ]
        this.form.feat_sel_options = [
          {name: 'Analysis of Variance', value: 'Analysis of Variance'},
          {name: 'None', value: 'None'}
        ]
      }
    },
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
      axios.post('/api/new_task', JSON.stringify(this.newform))
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
.ml-task-form {
    background-color: #FFFFFF;
    margin: 14px;
    padding: 14px;
}
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
</style>

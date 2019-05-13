<template>
  <div>
    <div class="ml-task-form">
      <el-form ref="form" :model="form" label-width="90px" label-position="middle">
        <el-form-item label="Task Name">
          <el-input v-model="newform.task_name"></el-input>
        </el-form-item>
        <el-form-item label="Task Type">
          <el-radio-group v-model="newform.task_type">
            <el-radio label="Classification">Classification</el-radio>
            <el-radio label="Regression">Regression</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="Train Data">
          <el-select class="select-data" v-model="newform.train_data" placeholder="Select Train Data">
            <el-option v-for="(data_option, key) in form.data_options" :label="data_option.name" :value="data_option.value" :key="key"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Test Data">
          <el-select class="select-data" v-model="newform.test_data" placeholder="Select Test Data">
            <el-option v-for="(data_option, key) in form.data_options" :label="data_option.name" :value="data_option.value" :key="key"></el-option>
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
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      newform: {
        task_name: '',
        task_type: '',
        train_data: '',
        test_data: '',
        label: '',
        feat_sel: '',
        estimator: '',
        cv_type: '',
        note: '',
        verbose: false
      },
      form: {
        data_options: [
          {name: '363_fMRI', value: '363_fMRI'},
          {name: '345_sMRI', value: '345_sMRI'},
          {name: '110_DTI', value: '110_DTI'},
          {name: '168_Gut', value: '168_Gut'}
        ],
        label_options: [
          {name: 'Schizophrenia', value: 'Schizophrenia'},
          {name: 'Anxiety', value: 'Anxiety'},
          {name: 'Hallucination', value: 'Hallucination'},
          {name: 'Hostility', value: 'hs'}
        ],
        feat_sel_options: [
          {name: 'Principal Component Analysis', value: 'Principal Component Analysis'},
          {name: 'Independent Component Analysis', value: 'Independent Component Analysis'},
          {name: 'ANOVA', value: 'ANOVA'},
          {name: 'Recursive Feature Elimination', value: 'Recursive Feature Elimination'},
          {name: 'Canonical Correlation Analysis', value: 'Canonical Correlation Analysis'}
        ],
        estimator_options: [
          {name: 'Support Vector Machine', value: 'Support Vector Machine'},
          {name: 'Random Forest', value: 'Random Forest'},
          {name: 'Linear Discriminative Analysis', value: 'Linear Discriminative Analysis'},
          {name: 'Logistic Regression', value: 'Logistic Regression'},
          {name: 'K Nearest Neighbor', value: 'K Nearest Neighbor'}
        ],
        cv_type_options: [
          {name: '10-fold', value: '10-fold'},
          {name: '5-fold', value: '5-fold'},
          {name: '3-fold', value: '3-fold'},
          {name: 'Leave-One-Out', value: 'Leave-One-Out'}
        ]
      }
    }
  },
  methods: {
    onSubmit () {
      this.newTask()
    },
    onCancel () {
      this.$router.go(0)
    },
    newTask () {
      console.log(JSON.stringify(this.newform))
      axios.post('http://127.0.0.1:8000/api/new_task', JSON.stringify(this.newform))
        .then(response => {
          var res = response.data
          if (res.error_num === 0) {
            this.$router.replace({
              path: '/analysis/submissions',
              component: resolve => require(['@/pages/analysis/submissions'], resolve)
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

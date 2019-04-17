<template>
<div style="padding: 14px">
  <div class="tasks-form-area">
    <el-tabs type="border-card">
      <el-tab-pane label="Difference Analysis">
        <div class="da-task-form">
          <el-form ref="diff_form" :model="diff_form" label-width="90px" label-position="middle">
            <el-form-item label="Task Name">
              <el-input v-model="diff_form.task_name"></el-input>
            </el-form-item>
            <el-form-item label="Task Type">
              <el-radio-group v-model="diff_form.task_type">
              <el-radio label="ttest">T-test</el-radio>
              <el-radio label="anova">ANOVA</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="Test Var.">
              <el-select class="select-data" v-model="diff_form.test_variables" placeholder="Select Test Variables">
              <el-option v-for="(test_variables_option, key) in diff_form.test_variables_options" :label="test_variables_option.name" :value="test_variables_option.value" :key="key"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Group Var.">
              <el-select class="select-data" v-model="diff_form.group_variables" placeholder="Select Group Variables">
              <el-option v-for="(group_variables_option, key) in diff_form.group_variables_options" :label="group_variables_option.name" :value="group_variables_option.value" :key="key"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Note">
              <el-input type="textarea" v-model="diff_form.note"></el-input>
            </el-form-item>
            <el-form-item label="Verbose">
              <el-switch on-text="On" off-text="Off" v-model="diff_form.verbose"></el-switch>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit">Submit</el-button>
              <el-button>Cancel</el-button>
            </el-form-item>
            </el-form>
        </div>
      </el-tab-pane>
      <el-tab-pane label="Correlation Analysis">
        <div class="ca-task-form">
          <el-form ref="corr_form" :model="corr_form" label-width="90px" label-position="middle">
            <el-form-item label="Task Name">
              <el-input v-model="corr_form.task_name"></el-input>
            </el-form-item>
            <el-form-item label="Task Type">
              <el-radio-group v-model="corr_form.task_type">
              <el-radio label="pearson">Pearson</el-radio>
              <el-radio label="spearman">Spearman</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="Data X">
              <el-select class="select-data" v-model="corr_form.datax_variables" placeholder="Select Data X">
              <el-option v-for="(datax_variables_option, key) in corr_form.datax_variables_options" :label="datax_variables_option.name" :value="datax_variables_option.value" :key="key"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Data Y">
              <el-select class="select-data" v-model="corr_form.datay_variables" placeholder="Select Data Y">
              <el-option v-for="(datay_variables_option, key) in corr_form.datay_variables_options" :label="datay_variables_option.name" :value="datay_variables_option.value" :key="key"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Note">
              <el-input type="textarea" v-model="corr_form.note"></el-input>
            </el-form-item>
            <el-form-item label="Verbose">
              <el-switch on-text="On" off-text="Off" v-model="corr_form.verbose"></el-switch>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit">Submit</el-button>
              <el-button>Cancel</el-button>
            </el-form-item>
            </el-form>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</div>
</template>

<script>
export default {
  data () {
    return {
      diff_form: {
        task_name: '',
        task_type: 'ttest',
        test_variables: '',
        group_variables: '',
        note: '',
        verbose: false,
        test_variables_options: [
          {name: 'fMRI', value: 'fmri'},
          {name: 'sMRI', value: 'smri'},
          {name: 'DTI', value: 'dti'},
          {name: 'Gut', value: 'gut'}
        ],
        group_variables_options: [
          {name: 'fMRI', value: 'fmri'},
          {name: 'sMRI', value: 'smri'},
          {name: 'DTI', value: 'dti'},
          {name: 'Gut', value: 'gut'}
        ]
      },
      corr_form: {
        task_name: '',
        task_type: 'pearson',
        datax_variables: '',
        datay_variables: '',
        note: '',
        verbose: false,
        datax_variables_options: [
          {name: 'fMRI', value: 'fmri'},
          {name: 'sMRI', value: 'smri'},
          {name: 'DTI', value: 'dti'},
          {name: 'Gut', value: 'gut'}
        ],
        datay_variables_options: [
          {name: 'fMRI', value: 'fmri'},
          {name: 'sMRI', value: 'smri'},
          {name: 'DTI', value: 'dti'},
          {name: 'Gut', value: 'gut'}
        ]
      }
    }
  },
  methods: {
    onSubmit () {
      console.log('submit!')
    }
  }
}
</script>

<style lang="scss">
.select-data {
    width: 400px;
}
</style>

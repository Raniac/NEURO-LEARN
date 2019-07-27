<template>
  <div style="text-align: center">
    <div class="data-overview-area">
      <div style="padding: 20px 0px">
        <div style="text-align: left">
          <el-select v-model="selected_project.title" style="margin: 0 20px; width: 300px" placeholder="Select Project">
            <el-option
              v-for="project_option in project_options"
              :key="project_option.title"
              :label="project_option.label"
              :value="project_option.title">
            </el-option>
          </el-select>
        </div>
        <div style="line-height: 30px; font-family: 'Times New Roman'; text-align: left; width: 700px; margin: 0 auto; font-size: 18px; color: #000000">
          <h2>{{ selected_project.title }}</h2>
          <h3>Introduction</h3>
          <p>{{ selected_project.introduction }}</p>
          <h3>Methods</h3>
          <p>{{ selected_project.methods }}</p>
          <el-button type="primary" round @click="handleDownloadTemplates('workflow')">Download Workflow Templates</el-button>
          <el-button type="primary" round :href="selected_project.data_templates_url" @click="handleDownloadTemplates('workflow')">Download Data Templates</el-button>
          <el-button type="primary" round @click="handleUploadData">Upload Prepared Data</el-button>
          <h3>Flowchart</h3>
        </div>
        <div style="text-align: center">
          <img style="width: 700px; margin-top: -20px" :src="selected_project.flowchart_url">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      selected_project: {
        id: 'PROJ20190626040404',
        label: 'SZ with sfMRI',
        title: 'Study of Schizophrenia with Pattern Analysis of Structural/Functional MRI Data',
        introduction: 'Fusing structural and functional MRI data, we use DPABI on matlab to compute the features such as gray matter volume, regional homogeneity, amplitude of low frequency fluctuations and degree centrality. The brain template used for ROI extraction is Anatomical Automatic Labeling 90.',
        methods: 'To configure the DPASFA toolbox, you can download the workflow templates. The format and feature data arrangement of the dataset should be strictly the same as the dataset templates. If you have a dataset prepared, you can upload it for analysis.',
        flowchart_url: 'http://localhost:8000/api/show_img?task_id=TASK20190717211913&img_name=optimization_curve',
        workflow_templates_url: '/api/download_templates?template_type=workflow_templates',
        data_templates_url: '/api/download_templates?template_type=dataset_templates'
      },
      project_options: [
        {
          id: 'PROJ20190727040404',
          label: 'SZ with Brain FCN',
          title: 'Study of Schizophrenia with Pattern Analysis of Brain Functional Connectivity Network',
          introduction: '',
          methods: '',
          flowchart_url: 'http://localhost:8000/api/show_img?task_id=TASK20190717211913&img_name=optimization_curve',
          workflow_templates_url: '/api/download_templates?template_type=workflow_templates',
          data_templates_url: '/api/download_templates?template_type=dataset_templates'
        },
        {
          id: 'PROJ20190626040404',
          label: 'SZ with sfMRI',
          title: 'Study of Schizophrenia with Pattern Analysis of Structural/Functional MRI Data',
          introduction: 'Fusing structural and functional MRI data, we use DPABI on matlab to compute the features such as gray matter volume, regional homogeneity, amplitude of low frequency fluctuations and degree centrality. The brain template used for ROI extraction is Anatomical Automatic Labeling 90.',
          methods: 'To configure the DPASFA toolbox, you can download the workflow templates. The format and feature data arrangement of the dataset should be strictly the same as the dataset templates. If you have a dataset prepared, you can upload it for analysis.',
          flowchart_url: 'http://localhost:8000/api/show_img?task_id=TASK20190717211913&img_name=optimization_curve',
          workflow_templates_url: '/api/download_templates?template_type=workflow_templates',
          data_templates_url: '/api/download_templates?template_type=dataset_templates'
        }
      ]
    }
  },
  methods: {
    handleUploadData () {
      this.$router.push({
        path: '/projects/data',
        query: {projectid: this.selected_project.id}
      })
    },
    handleDownloadTemplates (templateType) {
      if (templateType === 'workflow') {
        window.location.href = this.selected_project.workflow_templates_url
      } else {
        window.location.href = this.selected_project.data_templates_url
      }
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

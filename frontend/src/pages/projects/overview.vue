<template>
  <div style="text-align: center">
    <div class="data-overview-area">
      <el-tabs type="border-card" style="box-shadow: 0px 0 0px #FFFFFF;" stretch>
        <el-tab-pane label="SZ with sfMRI">
          <div style="padding: 20px; line-height: 30px; font-family: Arial">
            <div>
              <h1>Analysis of Schizophrenia with s/fMRI Data</h1>
              <p>Fusing structural and functional MRI data, we use DPABI on matlab to compute the features
                such as <i>gray matter volume, regional homogeneity, amplitude of low frequency fluctuations
                and degree centrality</i>. The brain template used for ROI extraction is <i>Anatomical Automatic
                Labeling 90</i>.</p>
              <p>To configure the DPASFA toolbox, you can download the
                <a href="/api/download_templates?template_type=workflow_templates" target="_self" style="color: #00CCFF">workflow templates</a>.
                The format and feature data arrangement of the dataset should be strictly the same as the
                <a href="/api/download_templates?template_type=dataset_templates" target="_self" style="color: #00CCFF">dataset templates</a>.</p>
              <p>If you have a dataset prepared, you can <router-link to="/projects/data/sz_with_sfmri" style="color: #00CCFF">upload</router-link> it for analysis.</p>
            </div>
            <div style="text-align: center">
              <img style="height: 300px; width: 700px; margin: 10px" src="@/assets/img/sMRI_prep.png">
              <img style="height: 300px; width: 700px; margin: 10px" src="@/assets/img/fMRI_prep.png">
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="AD with sMRI">
          <div style="padding: 20px; line-height: 30px; font-family: Arial">
            <h1>Analysis of Alzheimer's Disease with sMRI Data</h1>
          </div>
        </el-tab-pane>
        <el-tab-pane label="SZ with fMRI">
          <div style="padding: 20px; line-height: 30px; font-family: Arial">
            <h1>Analysis of Schizophrenia with fMRI Data</h1>
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
    }
  },
  methods: {}
}
</script>

<style lang="scss">
.data-overview-area {
  width: 800px;
  text-align: left;
  margin: 14px auto;
}
</style>

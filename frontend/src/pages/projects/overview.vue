<template>
  <div class="data-overview-area">
    <el-tabs type="border-card" style="box-shadow: 0px 0 0px #FFFFFF;">
      <el-tab-pane label="SZ with s/fMRI">
        <div style="padding: 20px; line-height: 30px; font-family: Arial">
          <div>
            <h1>Analysis of Schizophrenia with s/fMRI Data</h1>
            <p>Fusing structural and functional MRI data, we use DPABI on matlab to compute the features
              such as <i>gray matter volume, regional homogeneity, amplitude of low frequency fluctuations
              and degree centrality</i>. The brain template used for ROI extraction is <i>Anatomical Automatic
              Labeling 90</i>.</p>
            <p>To configure the DPASFA toolbox, you can download the
              <a @click="downloadFile('workflow_templates')" style="color: #00CCFF">workflow templates</a>.
              The format and feature data arrangement of the dataset should be strictly the same as the
              <a @click="downloadFile('dataset_templates')" style="color: #00CCFF">dataset templates</a>.</p>
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
          <span style="font-size: 20px"><strong>Project Name:</strong> AD with sMRI</span><br/>
          <span style="font-size: 20px"><strong>Research Content:</strong> Using NiPype to calculate GMV, CT and CA, predict AD.</span><br/>
          <span style="font-size: 20px"><strong>Feature Types:</strong> Gray Matter Volume, Cortical Thickness, Cortical Area.</span><br/>
          <span style="font-size: 20px"><strong>Data Size:</strong> 1000</span><br/>
          <div style="text-align: center">
            <img style="height: 640px; width: 700px; margin: 10px; border: solid" src="@/assets/img/sMRI_prep.png">
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="SZ with fMRI">
        <div style="padding: 20px; line-height: 30px; font-family: Arial">
          <span style="font-size: 20px"><strong>Project Name:</strong> SZ with fMRI</span><br/>
          <span style="font-size: 20px"><strong>Research Content:</strong> Using NiLearn to calculate FC, DC and CC, predict SZ.</span><br/>
          <span style="font-size: 20px"><strong>Feature Types:</strong> Functional Connectivity, Degree Centrality, Clustering Coefficient.</span><br/>
          <span style="font-size: 20px"><strong>Data Size:</strong> 954</span><br/>
          <div style="text-align: center">
            <img style="height: 640px; width: 700px; margin: 10px" src="@/assets/img/fMRI_prep.png">
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  data () {
    return {
      downloadTemplatesUrl: 'http://127.0.0.1:8000/api/download_templates?template_type='
    }
  },
  methods: {
    downloadFile (templateType) {
      try {
        var elemIF = document.createElement('iframe')
        elemIF.src = this.downloadTemplatesUrl + templateType
        elemIF.style.display = 'none'
        document.body.appendChild(elemIF)
      } catch (e) {
        console.log(e)
      }
    }
  }
}
</script>

<style lang="scss">
.data-overview-area {
  padding: 14px;
}
</style>

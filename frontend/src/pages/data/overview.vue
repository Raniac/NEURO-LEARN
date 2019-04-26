<template>
  <div class="data-overview-area">
    <el-tabs type="border-card" style="box-shadow: 0px 0 0px #FFFFFF;">
      <el-tab-pane label="AD_with_sMRI">
        <div style="padding: 20px; line-height: 30px; font-family: Arial">
          <span style="font-size: 20px"><strong>Project Name:</strong> AD with sMRI</span><br/>
          <span style="font-size: 20px"><strong>Research Content:</strong> Using NiPype to calculate GMV, CT and CA, predict AD.</span><br/>
          <span style="font-size: 20px"><strong>Feature Types:</strong> Gray Matter Volume, Cortical Thickness, Cortical Area.</span><br/>
          <span style="font-size: 20px"><strong>Data Size:</strong> 1000</span><br/>
          <div style="text-align: center">
            <img style="height: auto; width: 700px; margin: 10px" src="@/assets/img/sMRI_prep.png">
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="SZ_with_fMRI">
        <div style="padding: 20px; line-height: 30px; font-family: Arial">
          <span style="font-size: 20px"><strong>Project Name:</strong> SZ with fMRI</span><br/>
          <span style="font-size: 20px"><strong>Research Content:</strong> Using NiLearn to calculate FC, DC and CC, predict SZ.</span><br/>
          <span style="font-size: 20px"><strong>Feature Types:</strong> Functional Connectivity, Degree Centrality, Clustering Coefficient.</span><br/>
          <span style="font-size: 20px"><strong>Data Size:</strong> 954</span><br/>
          <div style="text-align: center">
            <img style="height: auto; width: 700px; margin: 10px" src="@/assets/img/fMRI_prep.png">
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="SZ_with_s/fMRI">
        <div style="padding: 20px; line-height: 30px; font-family: Arial">
          <span style="font-size: 20px"><strong>Project Name:</strong> AD with sMRI</span><br/>
          <span style="font-size: 20px"><strong>Research Content:</strong> Fusing multi-modal data, using NiLearn to calculate GMV and FC, predict SZ.</span><br/>
          <span style="font-size: 20px"><strong>Feature Types:</strong> Gray Matter Volume, Functional Connectivity.</span><br/>
          <span style="font-size: 20px"><strong>Data Size:</strong> 675</span><br/>
          <div style="text-align: center">
            <img style="height: auto; width: 700px; margin: 10px" src="@/assets/img/sMRI_prep.png">
            <img style="height: auto; width: 700px; margin: 10px" src="@/assets/img/fMRI_prep.png">
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
    }
  }
}
</script>

<style lang="scss">
.data-overview-area {
  padding: 14px;
}
</style>

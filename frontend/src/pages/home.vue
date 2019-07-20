<template>
  <div style="text-align: center">
    <div style="margin: 14px auto">
      <img style="width: 800px" src="@/assets/img/NL.png">
    </div>
    <div class="home-content-area">
      <div style="padding: 20px">
        <div style="padding: 10px; font-size: 20px">
          <el-row>
            <el-col :span="6">
              <div class="grid-content">
                <router-link to="/projects/overview">
                <img class="feature-icon" src="@/assets/img/projects.png">
                <a class="feature-title">PROJECTS</a><br/>
                <a class="feature-item">Multi-Modal Data</a><br/>
                <a class="feature-item">Multi-Site Researches</a><br/>
                <a class="feature-item">Uniform Workflows</a><br/>
                </router-link>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="grid-content">
                <router-link to="/projects/data">
                <img class="feature-icon" src="@/assets/img/data.png">
                <a class="feature-title">DATA</a><br/>
                <a class="feature-item">Collaborative Sharing</a><br/>
                <a class="feature-item">Storage on Cloud</a><br/>
                <a class="feature-item">Efficient Management</a><br/>
                </router-link>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="grid-content">
                <router-link to="/analysis/overview">
                <img class="feature-icon" src="@/assets/img/analyses.png">
                <a class="feature-title">ANALYSES</a><br/>
                <a class="feature-item">Statistical Analysis</a><br/>
                <a class="feature-item">Machine Learning</a><br/>
                <a class="feature-item">Deep Learning</a><br/>
                </router-link>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="grid-content">
                <router-link to="/analysis/submissions">
                <img class="feature-icon" src="@/assets/img/reports.png">
                <a class="feature-title">REPORTS</a><br/>
                <a class="feature-item">Intuitive Plots</a><br/>
                <a class="feature-item">Sufficient Metrics</a><br/>
                <a class="feature-item">Detailed Illustration</a><br/>
                </router-link>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>
    </div>
    <div style="text-align: center">
      <div style="margin: 14px auto; padding:14px; width: 772px; background-color: #FFFFFF; color: #505050; text-align: center">
        <div style="text-align: left; width: 700px; margin: 0 auto; font-family: 'Times New Roman', Times, serif; font-size: 18px">
          <h1>About NEURO-LEARN</h1>
        </div>
        <hr style="width: 750px" />
        <div style="text-align: left; width: 700px; margin: 0 auto; font-family: 'Times New Roman', Times, serif; font-size: 18px">
          <p><a style="color: #00CCFF; font-weight: bold" href="https://github.com/Raniac/NEURO-LEARN/" target="_blank">NEURO-LEARN</a> is a decentralized solution for pattern analysis of neuroimaging data. Its decentralization scheme of data and workflow management consists of four parts: projects, data, analysis and reports. As data preparation workflows defined in projects reduce the high dimensionality of neuroimaging data by decentralized computation, collaborative sharing of data and analysis workflows along with visualization of generated reports on the Web enlarge the sample size and facilitate the validity, reliability, and reproducibility of pattern analyses. Incorporating this scheme, NEURO-LEARN provides an easy-to-use web platform for the decentralization of pattern analysis of neuroimaging data.</p>
          <p>Main functionalities of NEURO-LEARN was coded by Bingye Lei, who also wrote the first version of wiki. Should you encouter any problems when using NEURO-LEARN, please feel free to file an issue or contact <a style="color: #00CCFF; font-weight: bold" href="mailto:leibingye@outlook.com">leibingye@outlook.com</a>.</p>
          <p>The code of NEURO-LEARN is distributed under Apache License 2.0. If you find our work useful and want to publish a study using NEURO-LEARN, we would appreciate it if you cited our paper.</p>
          <p>More information about NEURO-LEARN can be found in <a style="color: #00CCFF; font-weight: bold" href="https://github.com/Raniac/NEURO-LEARN/wiki/" target="_blank">NEURO-LEARN Documentation</a>.</p>
        </div>
        <div>
          <hr style="width: 750px" />
            <p style="font-size: 14px; color: #505050">This application is part of NEURO-LEARN developed by Raniac from South China University of Technology.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style lang="scss">
  .home-content-area {
    margin: 14px auto;
    width: 800px;
    background-color: #FFFFFF;
    .el-row {
      margin-bottom: 20px;
      &:last-child {
        margin-bottom: 0;
      }
    }
    .el-col {
      border:1px solid #C8C8C8;
      border-style:none none none solid;
      &:last-child {
        border:1px solid #C8C8C8;
        border-style:none solid;
      }
    }
    .grid-content {
      padding: 0px 14px;
      min-height: 100px;
      .feature-icon {
        float: left;
        padding-left: 20px;
        padding-bottom: 8px;
        height: 90px;
        width: 120px;
      }
      .feature-title {
        color: #282828;
        font-size: 20px;
        padding-left: 15px;
      }
      .feature-item {
        color: #505050;
        font-size: 14px;
        padding-left: 15px;
      }
    }
  }
  // #icon {
  //   text-align: center;
  //   -webkit-background-size: 20px 20px;
  //   -moz-background-size: 20px 20px;
  //   background-size: 20px 20px;
  //   background-color: #00CCFF;
  //   background-image: -webkit-gradient(linear, 0 100%, 100% 0,
  //                             color-stop(.25, rgba(255, 255, 255, .2)), color-stop(.25, transparent),
  //                             color-stop(.5, transparent), color-stop(.5, rgba(255, 255, 255, .2)),
  //                             color-stop(.75, rgba(255, 255, 255, .2)), color-stop(.75, transparent),
  //                             to(transparent));
  //   background-image: -moz-linear-gradient(45deg, rgba(255, 255, 255, .2) 25%, transparent 25%,
  //                         transparent 50%, rgba(255, 255, 255, .2) 50%, rgba(255, 255, 255, .2) 75%,
  //                         transparent 75%, transparent);
  //   background-image: -o-linear-gradient(45deg, rgba(255, 255, 255, .2) 25%, transparent 25%,
  //                         transparent 50%, rgba(255, 255, 255, .2) 50%, rgba(255, 255, 255, .2) 75%,
  //                         transparent 75%, transparent);
  //   background-image: linear-gradient(45deg, rgba(255, 255, 255, .2) 25%, transparent 25%,
  //                         transparent 50%, rgba(255, 255, 255, .2) 50%, rgba(255, 255, 255, .2) 75%,
  //                         transparent 75%, transparent);
  // }
  #blue-title {
    color: #00CCFF;
    text-shadow:1px 1px 1px #282828;
  }
  #framework {
    text-align: center;
  }
</style>

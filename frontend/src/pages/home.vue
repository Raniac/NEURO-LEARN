<template>
  <div>
    <div class="home-content-area">
      <div id="icon">
        <img style="height: auto; width: 600px; margin: 10px" src="@/assets/img/neurolearn.png">
      </div>
    </div>
    <div class="home-content-area">
      <div style="padding: 20px">
        <h1 style="text-align: center; font-family: Arial; font-weight: 200; font-size: 40px; color: #282828">Welcome to <strong id="blue-title">NEURO-LEARN-WEB</strong>!:-)</h1>
        <div style="padding: 10px; font-size: 20px">
          <el-row>
            <el-col :span="6">
              <div class="grid-content">
                <router-link to="/profile">
                <img class="feature-icon" src="@/assets/img/projects.png">
                <a class="feature-title">PROJECTS</a><br/>
                <a class="feature-item">Multi-Modality Data</a><br/>
                <a class="feature-item">Various Researches</a><br/>
                <a class="feature-item">Uniform Pipelines</a><br/>
                </router-link>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="grid-content">
                <router-link to="/data/overview">
                <img class="feature-icon" src="@/assets/img/data.png">
                <a class="feature-title">DATA</a><br/>
                <a class="feature-item">Share & Collaboration</a><br/>
                <a class="feature-item">Stored on Cloud</a><br/>
                <a class="feature-item">Easy Access</a><br/>
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
                <router-link to="/analysis/overview">
                <img class="feature-icon" src="@/assets/img/reports.png">
                <a class="feature-title">REPORTS</a><br/>
                <a class="feature-item">Abundant Plots</a><br/>
                <a class="feature-item">Sufficient Metrics</a><br/>
                <a class="feature-item">Detailed Illustration</a><br/>
                </router-link>
              </div>
            </el-col>
          </el-row>
        </div>
        <div>
          <h2 style="text-align: center; font-family: Arial; font-weight: 150; font-size: 30px; color: #282828">What is it <strong style="color: #00CCFF; text-shadow:0.5px 0.5px 0.5px #282828;">capable</strong> of?</h2>
        </div>
        <div id="framework">
          <img style="height: auto; width: 700px; margin: 10px" src="@/assets/img/neurolearn_framework.png">
        </div>
        <div>
          <hr />
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
  margin: 14px;
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
#icon {
  text-align: center;
  -webkit-background-size: 20px 20px;
  -moz-background-size: 20px 20px;
  background-size: 20px 20px;
  background-color: #00CCFF;
  background-image: -webkit-gradient(linear, 0 100%, 100% 0,
                            color-stop(.25, rgba(255, 255, 255, .2)), color-stop(.25, transparent),
                            color-stop(.5, transparent), color-stop(.5, rgba(255, 255, 255, .2)),
                            color-stop(.75, rgba(255, 255, 255, .2)), color-stop(.75, transparent),
                            to(transparent));
  background-image: -moz-linear-gradient(45deg, rgba(255, 255, 255, .2) 25%, transparent 25%,
                        transparent 50%, rgba(255, 255, 255, .2) 50%, rgba(255, 255, 255, .2) 75%,
                        transparent 75%, transparent);
  background-image: -o-linear-gradient(45deg, rgba(255, 255, 255, .2) 25%, transparent 25%,
                        transparent 50%, rgba(255, 255, 255, .2) 50%, rgba(255, 255, 255, .2) 75%,
                        transparent 75%, transparent);
  background-image: linear-gradient(45deg, rgba(255, 255, 255, .2) 25%, transparent 25%,
                        transparent 50%, rgba(255, 255, 255, .2) 50%, rgba(255, 255, 255, .2) 75%,
                        transparent 75%, transparent);
}
#blue-title {
  color: #00CCFF;
  text-shadow:1px 1px 1px #282828;
}
#framework {
  text-align: center;
}
</style>

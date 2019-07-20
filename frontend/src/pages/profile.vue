<template>
  <div style="text-align: center">
    <div class="profile-area">
      <div class="profile-detail">
        <img style="float: left; height: auto; width: 200px" src="https://avatars2.githubusercontent.com/u/17725948?s=460&v=4">
        <div style="line-height: 30px">
          <span style="padding-left: 20px; font-family: Arial; font-weight: 200; font-size: 40px; color: #282828">{{ username }}</span><br/>
          <span style="padding-left: 20px; font-family: Arial; font-weight: 100; font-size: 20px; color: #505050">Master of Science from SCUT</span><br/>
          <span style="padding-left: 20px; font-family: Arial; font-weight: 100; font-size: 20px; color: #505050">Interests:  Artificial Intelligence & Neuro-Informatics</span><br/>
        </div>
        <div style="margin-top: 40px; line-height: 30px">
          <a class="github-link" href="https://github.com/Raniac" target="_blank">Paper: NEURO-LEARN</a><br/>
          <a class="github-link" href="https://github.com/Raniac" target="_blank">GitHub/Raniac</a><br/>
        </div>
      </div>
    </div>
    <div class="projects-area">
    <div>
      <h1 style="padding-left: 20px; font-family: Arial; font-weight: 150; font-size: 30px; color: #505050">Joined Projects</h1>
    </div>
    <div style="margin: 14px">
      <el-table
        class="projects-table"
        :data="projects_table"
        stripe
        border
        default-expand-all
        style="width: 100%; background-color: #E8E8E8; color: #282828; ">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" in-line class="projects-table-expand">
              <el-form-item label="Research Content">
                <span>{{ props.row.research_content }}</span>
              </el-form-item>
              <el-form-item label="Feature Types">
                <span>{{ props.row.feat_types }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column
        label="Project ID"
        prop="project_id">
        </el-table-column>
        <el-table-column
        label="Project Name"
        prop="project_name">
        </el-table-column>
        <el-table-column
        label="Status"
        prop="project_status">
        </el-table-column>
      </el-table>
    </div>
    </div>
  </div>
</template>

<script>
export default {
  mounted () {
    this.username = sessionStorage.getItem('Username')
  },
  data () {
    return {
      search_input: '',
      selected_status: '',
      username: '',
      projects_table: [{
        project_id: '2019050503',
        project_name: 'SZ with sfMRI',
        project_status: 'active',
        research_content: 'Fusing structural and functional MRI data, use DPABI on matlab to compute the features, and analyze SZ.',
        feat_types: 'Gray matter volume, regional homogeneity, amplitude of low frequency fluctuations and degree centrality.'
      }]
    }
  }
}
</script>

<style lang="scss">
.profile-area {
  width: 772px;
  margin: 14px auto;
  text-align: left;
  padding: 14px;
  background-color: #FFFFFF;
  .profile-detail {
    padding: 14px;
    min-height: 200px;
    .github-link {
      padding-left: 20px;
      font-family: Arial;
      font-weight: 100;
      font-size: 20px;
      color: #282828;
      &:hover {
      color: #00CCFF;
      }
    }
  }
}
.projects-area {
  width: 772px;
  margin: 14px auto;
  padding: 14px;
  text-align: left;
  background-color: #FFFFFF;
}
.projects-table-expand {
  font-size: 0;
  width: 100%;
  }
  .projects-table-expand label {
    width: 140px;
    color: #505050;
  }
  .projects-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
  }
</style>

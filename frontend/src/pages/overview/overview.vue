<template>
  <div>
    <div style="padding: 14px; color: #282828">
    <h3>Overview</h3>
    <el-row>
  <el-col :span="4" :offset=".5">
    <el-card :body-style="{ padding: '0px' }" style="background-color: #FFFFFF">
      <div style="padding: 14px; color: #282828; text-align: center">
        <h4>Total</h4>
        <div>
          <h1>45</h1>
        </div>
      </div>
    </el-card>
  </el-col>
  <el-col :span="4" :offset="1">
    <el-card :body-style="{ padding: '0px' }" style="background-color: #FFFFFF">
      <div style="padding: 14px; color: #006699; text-align: center">
        <h4>Submitted</h4>
        <div>
          <h1>5</h1>
        </div>
      </div>
    </el-card>
  </el-col>
  <el-col :span="4" :offset="1">
    <el-card :body-style="{ padding: '0px' }" style="background-color: #FFFFFF">
      <div style="padding: 14px; color: #00CC99; text-align: center">
        <h4>Running</h4>
        <div>
          <h1>5</h1>
        </div>
      </div>
    </el-card>
  </el-col>
  <el-col :span="4" :offset="1">
    <el-card :body-style="{ padding: '0px' }" style="background-color: #FFFFFF">
      <div style="padding: 14px; color: #00CCFF; text-align: center">
        <h4>Finished</h4>
        <div>
          <h1>25</h1>
        </div>
      </div>
    </el-card>
  </el-col>
  <el-col :span="4" :offset="1">
    <el-card :body-style="{ padding: '0px' }" style="background-color: #FFFFFF">
      <div style="padding: 14px; color: #FF3333; text-align: center">
        <h4>Failed</h4>
        <div>
          <h1>10</h1>
        </div>
      </div>
    </el-card>
  </el-col>
</el-row>
    </div>
    <div style="padding: 14px">
      <h3>Recent</h3>
      <el-table
    :data="tableData3"
    style="width: 99%; background-color: #FFFFFF; color: #282828">
    <el-table-column type="expand">
      <template slot-scope="props">
        <p>Task Name: {{ props.row.taskname }}</p>
        <p>Data Name: {{ props.row.dataname }}</p>
        <p>Data Size: {{ props.row.datasize }}</p>
        <p>Feature Name: {{ props.row.featurename }}</p>
      </template>
    </el-table-column>
    <el-table-column
      label="Task ID"
      prop="taskid">
    </el-table-column>
    <el-table-column
      label="Status"
      prop="status">
    </el-table-column>
  </el-table>
      </div>
</div>
</template>

<style>
  .clearfix:before,
  .clearfix:after {
      display: table;
      content: "";
  }
  .clearfix:after {
      clear: both
  }
  .el-carousel__item h3 {
    color: #3e4b5c;
    font-size: 14px;
    opacity: 0.75;
    line-height: 200px;
    margin: 0;
  }
  .el-carousel__item:nth-child(2n) {
    background-color: #8b9aaf;
  }
  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }
</style>

<script>
export default {
  data () {
    return {
      tableData3: [{
        taskid: '20190404161616',
        status: 'Submitted',
        taskname: 'Classify MCI and NC',
        dataname: 'fMRI',
        datasize: '200',
        featurename: 'Functional Connectivity'
      }, {
        taskid: '20190313231924',
        status: 'Running',
        taskname: 'Classify AD and NC',
        dataname: 'fMRI',
        datasize: '200',
        featurename: 'Functional Connectivity'
      }, {
        taskid: '20190304121536',
        status: 'Failed',
        taskname: 'Classify MCI and NC',
        dataname: 'fMRI',
        datasize: '200',
        featurename: 'Functional Connectivity'
      }, {
        taskid: '20190226121339',
        status: 'Finished',
        taskname: 'Regress FeSZ and PANSS',
        dataname: 'fMRI',
        datasize: '200',
        featurename: 'Functional Connectivity'
      }],
      currentDate: new Date()
    }
  }
}
</script>

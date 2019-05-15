<template>
  <div class="viewer-area">
    <el-tabs type="border-card" style="box-shadow: 0px 0 0px #FFFFFF;">
      <el-tab-pane :label="taskid">
        <div>
          <div style="padding: 14px">
            <el-table
              :data="resultData"
              stripe
              border
              style="width: 100%; color: #282828">
            <el-table-column
              label="Item"
              prop="item"
              fixed
              width="180">
            </el-table-column>
            <el-table-column
              label="Value"
              prop="value">
            </el-table-column>
          </el-table>
          <img :src="'http://127.0.0.1:8000/api/show_roc?task_id=' + this.taskid" style="width: 700px">
          <img :src="'http://127.0.0.1:8000/api/show_opt?task_id=' + this.taskid" style="width: 700px">
        </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  mounted () {
  },
  methods: {
  },
  data () {
    return {
      taskid: this.$route.query.taskid,
      resultData: [{
        item: 'Optimal Accuracy',
        value: '0.87'
      }, {
        item: 'Optimal Sensitivity',
        value: '0.82'
      }, {
        item: 'Optimal Specificity',
        value: '0.88'
      }, {
        item: 'Optimal Parameters',
        value: "'rfe__n_features_to_select': 500; 'svm__C': 0.001"
      }, {
        item: 'Optimal AUC',
        value: '0.89'
      }, {
        item: 'Optimal Features',
        value: "['GMV_2', 'GMV_4', 'GMV_5', 'GMV_7', 'GMV_8', 'GMV_11', 'GMV_13', 'GMV_15', 'GMV_16', 'GMV_17', 'GMV_18', 'GMV_23', 'GMV_26', 'GMV_33', 'GMV_34', 'GMV_38', 'GMV_40', 'GMV_42', 'GMV_43', 'GMV_44', 'GMV_46', 'GMV_47', 'GMV_50', 'GMV_52', 'GMV_54', 'GMV_62', 'GMV_64', 'GMV_68', 'GMV_69', 'GMV_70', 'GMV_71', 'GMV_76', 'GMV_77', 'GMV_78', 'GMV_79', 'GMV_80', 'GMV_82', 'GMV_85', 'GMV_87', 'GMV_90', 'GMV_91', 'GMV_92', 'GMV_94', 'GMV_95', 'GMV_99', 'GMV_101', 'GMV_102', 'GMV_103', 'GMV_104', 'GMV_105']"
      }]
    }
  }
}
</script>

<style lang="scss">
.viewer-area {
    padding: 14px;
}
</style>

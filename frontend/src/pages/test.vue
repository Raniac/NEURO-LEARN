<template>
  <div style="background-color: #FFFFFF; margin: 14px; padding: 14px">
    <el-upload
      class="upload-demo"
      action="http://127.0.0.1:8000/api/upload_data"
      name="test"
      :on-change="handleChange"
      :on-success="uploadSuccess"
      :file-list="fileList">
      <el-button size="small" type="primary">点击上传</el-button>
      <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
    </el-upload>
  </div>
</template>

<script>
export default {
  data () {
    return {
      fileList: []
    }
  },
  methods: {
    handleChange (file, fileList) {
      this.fileList = fileList.slice(-4)
    },
    uploadSuccess (response) {
      console.log(response.error_num, response.msg)
    }
  }
}
</script>

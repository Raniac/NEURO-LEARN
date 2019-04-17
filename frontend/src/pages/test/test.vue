<template>
  <div class="home" style="padding: 14px">
    <el-row display="margin-top:10px">
        <el-input v-model="input" placeholder="请输入书名" style="display:inline-table; width: 30%; float:left"></el-input>
        <el-button type="primary" @click="addBook()" style="float:left; margin: 2px;">新增</el-button>
    </el-row>
    <el-row>
        <el-table :data="bookList" style="width: 100%" border>
          <el-table-column prop="id" label="编号" min-width="100">
            <template slot-scope="scope"> {{ scope.row.pk }} </template>
          </el-table-column>
          <el-table-column prop="book_name" label="书名" min-width="100">
            <template slot-scope="scope"> {{ scope.row.fields.book_name }} </template>
          </el-table-column>
          <el-table-column prop="add_time" label="添加时间" min-width="100">
            <template slot-scope="scope"> {{ scope.row.fields.add_time }} </template>
          </el-table-column>
        </el-table>
    </el-row>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'home',
  data () {
    return {
      input: '',
      bookList: []
    }
  },
  mounted: function () {
    this.showBooks()
  },
  methods: {
    addBook () {
      axios.get('http://127.0.0.1:8000/api/add_book?book_name=' + this.input)
        .then(response => {
          this.showBooks()
        })
    },
    showBooks () {
      axios.get('http://127.0.0.1:8000/api/show_books')
        .then(response => {
          console.log(response.data)
          var res = response.data
          console.log(res)
          if (res.error_num === 0) {
            this.bookList = res['list']
          } else {
            this.$message.error('Failed!')
            console.log(res['msg'])
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>

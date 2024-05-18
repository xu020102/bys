<template>
  <div class="hello">
    <el-upload class="upload-demo" ref="upload" action="string"
      :on-preview="handlePreview" :on-remove="handleRemove" :on-change="handletwoChange" :file-list="fileList" :auto-upload="false" multiple="multiple" drag style="position: absolute;left: 200px;top: 30px;">
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      <div class="el-upload__tip" slot="tip">只能上传xlsx文件</div>
    </el-upload>
    <br/>
    <el-button style="position: absolute;left: 345px;top: 170px;" size="small" type="success" @click="onSubmit">提交数据</el-button>

    <el-button style="position: absolute;left: 60px;top: 40px;" size="small" type="primary"  @click="downloadFile">下载模板</el-button>

    <el-button style="position: absolute;left: 600px;top: 120px;" size="small" type="primary"  @click="downloadgoFile">下载结果</el-button>

    <!-- <el-upload
    class="read-excel"
    action=""
    :on-change="handleoneChange"
    :show-file-list="false"
    :auto-upload="false"> -->
    <el-button size="small" type="primary" style="position: absolute;left: 40px;top: 280px;margin-bottom:15px;" @click="loadxlsxData">刷新</el-button>
    <!-- </el-upload> -->
    <el-table :data="tableData" style="position: absolute;left: 40px;top: 330px;width: 50%; height: 400px; overflow: auto;" :header-cell-style="{ position: 'sticky', top: '0' }" height="400">
      <el-table-column v-for="(header, index) in tableHeader" :key="index" :prop="header" :label="header" :fixed="index === 0 ? 'left' : undefined">
    </el-table-column>
    </el-table>
    <el-button size="small" type="primary" style="position: absolute;left: 1100px;top: 280px;margin-bottom: 15px;" @click="loadCsvData">获取结果</el-button>
    <el-input style="position: absolute;left: 1200px;top: 275px;margin-bottom: 15px;width: 180px;height: 30px;" v-model="input" placeholder="请输入内容"></el-input>

    <div v-if="isLoading">
      模型尚在运行
    </div>
    <div v-else>
      <el-table :data="tableDatatwo" style="position: absolute;left: 800px;top: 330px;width: 43%;height: 400px; overflow: auto;" :header-cell-style="{ position: 'sticky', top: '0' }" height="400">
        <el-table-column v-for="(header, index) in tableHeaders" :key="index" :prop="header" :label="header" :fixed="index === 0 ? 'left' : undefined">
        </el-table-column>
      </el-table>
    </div>

    <!-- ... -->
    <el-button size="small" type="primary" style="position: absolute;left: 605px;top: 40px;margin-bottom: 15px;" @click="showImage">查看散点图</el-button>
    <img v-if="imageSrc" :src="imageSrc" alt="Image" style="position: absolute; top: 30px; left: 800px; max-width: 500px; max-height: 500px;">

    <!-- ... -->
    <el-button size="small" type="primary" style="position: absolute;left: 800px;top: 280px;margin-bottom: 15px;" @click="runScript">运行模型</el-button>
    <el-tooltip class="item" effect="dark" content="输入右边获得结果" style="position: absolute;left: 895px;top: 280px;margin-bottom: 15px;">
      <el-row >
        <el-col >
          <el-card class="card-game" shadow="hover" style="width: 180px;height: 30px;">
            <div class="card-content">
            <span class="key-label">key:</span>
            <span class="result-value">{{ result }}</span>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-tooltip>
    

  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data() {
      return {
        fileList: [],

        tableData: [],
        tableHeader: [],
        tableDatatwo:[],
        tableHeaders: [],

        multiple: false,
        formData: "",
        fileContent: '',
        file: '',

        data: '',
        imageSrc: null,

        result: '',
        input: '',
        
        isLoading: false,
      };
  },

  methods: {
      delFile () {
      this.fileList = [];
      },
      handletwoChange (file, fileList) {
      this.fileList = fileList;
      // console.log(this.fileList, "sb");
      },

      uploadFile (file) {
      this.formData.append("file", file.file);
      // console.log(file.file, "sb2");
      },
      onSubmit () {
        let formData = new FormData();
        formData.append("file", this.fileList[0].raw);//拿到存在fileList的文件存放到formData中
       //下面数据是我自己设置的数据,可自行添加数据到formData(使用键值对方式存储)
        formData.append("title", this.title);
        axios.post('http://localhost:8081/D/bysjcs', formData, {
        "Content-Type": "multipart/form-data;charset=utf-8"
      })
        .then(res => {
          if (res.data === "SUCCESS") {
            this.$notify({
              title: '成功',
              message: '提交成功',
              type: 'success',
              duration: 1000
            });
            axios.post('http://localhost:8081/xlsxgame')
        .then(response => {
        this.tableData = response.data.data;  // 假设后端返回的数据中的行数据存储在 "data" 字段中
        this.tableHeader = response.data.headers;  // 假设后端返回的数据中的列标题存储在 "headers" 字段中
      }).catch(error => {
        console.error(error);
      });
          }
        })
      },

      fetchData() {
      axios.get('http://localhost:8081/D/bysjsc') // 替换为实际的后端端点 URL
        .then(response => {
          this.tableDatatwo = response.data; // 将后端返回的数据赋值给 data
        })
        .catch(error => {
          console.error('请求错误:', error);
        });
      },
      loadxlsxData() {
      axios.post('http://localhost:8081/xlsxgame')
        .then(response => {
        this.tableData = response.data.data;  // 假设后端返回的数据中的行数据存储在 "data" 字段中
        this.tableHeader = response.data.headers;  // 假设后端返回的数据中的列标题存储在 "headers" 字段中
      }).catch(error => {
        console.error(error);
      });
      },
      loadCsvData() {
        this.isLoading = true;
      axios.post('http://localhost:8081/D/bysjsc', { input: this.input })
        .then(response => {
          const data = response.data;
          if (data.exists) {
            this.tableDatatwo = data.data;
            this.tableHeaders = data.headers;
          } else {
            // 文件不存在的处理逻辑
            this.isLoading = true;
            this.$notify({
              title: '失败',
              message: 'key错误或模型仍在运行',
              type: 'defeat',
              duration: 1000
            });
          }
          this.isLoading = false;
        })
        .catch(error => {
          console.error(error);
          this.isLoading = true;
        });
      },

      showImage() {
      const imageName = this.input + '.jpg'; // Replace with the actual image name
      axios.get(`http://localhost:8081/image/${imageName}`, { responseType: 'arraybuffer' })
      .then(response => {
        const imageBlob = new Blob([response.data], { type: response.headers['content-type'] });
        const imageUrl = URL.createObjectURL(imageBlob);
        this.imageSrc = imageUrl; // Assuming you have a data property called "imageSrc" to store the image URL
      })
      .catch(error => {
        console.error('Error fetching image:', error);
      });
      },
      
      async runScript() {
      try {
        const response = await axios.post('http://localhost:8081/gameon');
        this.result = response.data;
      } catch (error) {
        console.error(error);
      }
      },

      handleRemove(file, fileList) {
        console.log(file, fileList);
      },
      handlePreview(file) {
        console.log(file);
      },
      
      downloadFile() {
      const url = 'http://localhost:8081/D/bys-chen'; // 替换为实际的下载接口URL
      window.open(url, '_blank');
      },

      downloadgoFile() {
      window.location.href = `http://localhost:8081/D/bysjgo?input=${this.input}`;
      setTimeout(() => {
        if (window.location.href.includes('localhost:8081') && document.documentURI.includes('/D/bysjgo')) {
          this.$notify({
            title: '失败',
            message: '找不到对应文件',
            type: 'defeat',
            duration: 1000
          });
        }
      }, 3000);
    },

      // eslint-disable-next-line
      handleoneChange (file, fileList) {
        this.fileContent = file.raw
        const fileName = file.name
        const fileType = fileName.substring(fileName.lastIndexOf('.') + 1)
          if (this.fileContent) {
            if (fileType === 'xlsx' || fileType === 'xls') {
              this.importfile(this.fileContent)
            } else {
              this.$message({
                type: 'warning',
                message: '附件格式错误，请重新上传！'
              })
            }
          } else {
            this.$message({
              type: 'warning',
              message: '请上传附件！'
            })
          }
      },
      importfile (obj) {
  const reader = new FileReader()
  const _this = this
  reader.readAsArrayBuffer(obj)
  reader.onload = function () {
    const buffer = reader.result
    const bytes = new Uint8Array(buffer)
    const length = bytes.byteLength
    let binary = ''
    for (let i = 0; i < length; i++) {
      binary += String.fromCharCode(bytes[i])
    }
    const XLSX = require('xlsx')
    const wb = XLSX.read(binary, {
      type: 'binary'
    })
    const sheetName = wb.SheetNames[0]
    const worksheet = wb.Sheets[sheetName]
    const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 })

    // 忽略第一行数据
    const outdata = jsonData.slice(1)

    this.data = [...outdata]
    const arr = []
    this.data.map(v => {
      const obj = {}
      obj.ip = v[0] // 假设IP在第一列
      obj.canshu1 = v[1] // 假设CANSHU1在第二列
      obj.canshu2 = v[2] // 假设CANSHU2在第三列
      obj.canshu3 = v[3]
      obj.canshu4 = v[4]
      obj.canshu5 = v[5]
      obj.canshu6 = v[6]
      obj.canshu7 = v[7]
      obj.canshu8 = v[8]
      obj.canshu9 = v[9]
      obj.canshu10 = v[10]
      // 其他参数的处理
      obj.shiji = v[v.length - 1] // 假设SHIJI在最后一列
      arr.push(obj)
    })
    _this.tableData = _this.tableData.concat(arr)
  }
}
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.card-game {
  display: flex;
  justify-content: center;
  align-items: center;

}

.card-content {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}

.key-label {
  font-weight: bold;
  margin-right: 5px;
}

.result-value {
  margin-left: 5px;
}

h3 {
  margin: 40px 0 0;
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

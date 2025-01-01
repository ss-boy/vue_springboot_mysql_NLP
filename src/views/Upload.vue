<template>
  <div class="upload">
    <h2>上传文件</h2>

    <!-- 文件选择框 -->
    <input type="file" ref="fileInput" @change="handleFileChange" />

    <!-- 上传按钮 -->
    <button @click="uploadFile">上传文件</button>

    <!-- 预测按钮 -->
    <button v-if="uploadedFilePath" @click="predictFile">预测</button>

    <!-- 下载按钮 -->
    <button v-if="uploadedFilePath" @click="downloadFile">下载文件</button>

    <!-- 分析按钮 -->
    <button v-if="predictions.length > 0" @click="goToAnalysis">分析舆情</button>


    <!-- 文件内容显示 -->
    <div v-if="fileContent.length > 0">
      <h3>文件内容：</h3>
      <ul>
        <li v-for="(line, index) in fileContent" :key="index">{{ line }}</li>
      </ul>
    </div>

    <!-- 预测结果显示 -->
    <div v-if="predictions.length > 0">
      <h3>预测结果：</h3>
      <ul>
        <li v-for="(item, index) in predictions" :key="index">
          {{ item.comment }} -> {{ item.label }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      file: null,
      fileContent: [],
      uploadedFilePath: "",
      predictions: [],
    };
  },
  methods: {
    handleFileChange(event) {
      this.file = event.target.files[0];
    },
    async uploadFile() {
      const formData = new FormData();
      formData.append("file", this.file);

      const response = await axios.post("http://localhost:8080/upload", formData);
      this.fileContent = response.data.fileContent;
      this.uploadedFilePath = response.data.filePath;
    },
    async predictFile() {
      const response = await axios.post("http://localhost:8080/upload/predict", {
        filePath: this.uploadedFilePath,
      });

      // 对 predictions 数据进行处理
      this.predictions = response.data.predictions.map(item => {

        let label = "未知"; // 默认值
        if (item.prediction.includes("b'POS'")) {
          label = "正向";
        } else if (item.prediction.includes("b'NEG'")) {
          label = "负向";
        }

        // 返回新的结构
        return {
          comment: item.comment,
          label: label, // 显示正向/负向
        };
      });
    },
    downloadFile() {
      window.open(`http://localhost:8080/upload/download?path=${encodeURIComponent(this.uploadedFilePath)}`);
    },
    goToAnalysis() {
      // 使用 Vue Router 进行导航
      this.$router.push({
        name: 'sentiment-analysis',
        query: { filePath: this.uploadedFilePath },
      });
    },
  },
};
</script>

<style scoped>
.upload {
  text-align: center;
}
button {
  margin: 10px;
}
</style>

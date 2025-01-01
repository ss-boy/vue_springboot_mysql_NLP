<template>
  <div class="analysis-page">
    <h1>舆情分析</h1>
    <div class="charts-container">
      <!-- 第一张图：饼图 -->
      <div class="chart-item">
        <h2>情感分布饼图</h2>
        <canvas id="sentimentPieChart"></canvas>
      </div>
      <!-- 第二张图：表格 -->
      <div class="chart-item">
        <h2>正向负向评论统计表格</h2>
        <table class="sentiment-table">
          <thead>
          <tr>
            <th>类别</th>
            <th>数量</th>
          </tr>
          </thead>
          <tbody>
          <tr>
            <td>正向评论</td>
            <td>{{ positiveCount }}</td>
          </tr>
          <tr>
            <td>负向评论</td>
            <td>{{ negativeCount }}</td>
          </tr>
          </tbody>
        </table>
      </div>
      <!-- 第三张图:词云图 -->
      <div class="wordcloud-container">
        <h2>词云图</h2>
        <img v-if="wordCloudImagePath" :src="wordCloudImagePath" alt="词云图" class="wordcloud-image" />
      </div>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js/auto";
import axios from "axios";

export default {
  data() {
    return {
      predictions: [],
      positiveCount: 0,
      negativeCount: 0,
      wordCloudImagePath: "",
    };
  },
  async mounted() {
    const filePath = this.$route.query.filePath;
    if (filePath) {
      await this.fetchPredictions(filePath);
      await this.fetchWordCloud(filePath);
      this.createPieChart();
    }
  },
  methods: {
    async fetchPredictions(filePath) {
      try {
        const response = await axios.post("http://localhost:8080/upload/predict", { filePath });
        this.predictions = response.data.predictions.map((item) => {
          let label = "未知";
          if (item.prediction.includes("b'POS'")) label = "正向";
          else if (item.prediction.includes("b'NEG'")) label = "负向";
          return { comment: item.comment, label: label };
        });

        this.predictions.forEach((item) => {
          if (item.label === "正向") this.positiveCount++;
          else if (item.label === "负向") this.negativeCount++;
        });
      } catch (error) {
        console.error("获取预测数据失败", error);
      }
    },

    async fetchWordCloud(filePath) {
      try {
        const response = await axios.post("http://localhost:8080/wordcloud/generate", { filePath });
        this.wordCloudImagePath = `http://localhost:8080//wordcloud.png`;
      } catch (error) {
        console.error("词云图生成失败", error);
      }
    },

    createPieChart() {
      const ctx = document.getElementById("sentimentPieChart").getContext("2d");
      new Chart(ctx, {
        type: "pie",
        data: {
          labels: ["正向评论", "负向评论"],
          datasets: [
            {
              data: [this.positiveCount, this.negativeCount],
              backgroundColor: ["#4CAF50", "#F44336"],
            },
          ],
        },
      });
    },
  },
};
</script>

<style scoped>
.analysis-page {
  width: 100%;
  padding: 20px;
  box-sizing: border-box;
  text-align: center;
}

.charts-container {
  display: grid;
  grid-template-columns: 1fr 1fr; /* 两列布局 */
  gap: 20px;
  justify-items: center;
  align-items: start;
}

.chart-item {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 400px;
  height: auto; /* 取消固定高度，适应内容 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

/* 词云图容器单独一行 */
.wordcloud-container {
  grid-column: span 2; /* 让词云图占满整行 */
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.sentiment-table {
  width: 100%;
  border-collapse: collapse;
}

.sentiment-table th,
.sentiment-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

.sentiment-table th {
  background-color: #f0f0f0;
  font-weight: bold;
}

.sentiment-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.sentiment-table tr:hover {
  background-color: #f1f1f1;
}

.wordcloud-image {
  max-width: 100%;
  height: auto; /* 让词云图适应父容器 */
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
</style>

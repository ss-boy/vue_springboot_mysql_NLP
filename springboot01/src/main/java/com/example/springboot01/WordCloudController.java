package com.example.springboot01;


import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/wordcloud")
public class WordCloudController {

    @PostMapping("/generate")
    public ResponseEntity<String> generateWordCloud(@RequestBody Map<String, String> payload) {
        String filePath = payload.get("filePath"); // 接收文件路径

        // Python 脚本的路径
        String pythonScriptPath = "D:\\java\\vue01\\chinese_sentiment-master\\model\\lstm\\cloud.py"; // 请替换为实际路径

        // 生成的词云图保存路径
        String outputImagePath = "uploads/wordcloud.png"; // 请替换为实际路径

        try {
            // 构建命令
            ProcessBuilder processBuilder = new ProcessBuilder(
                    "C:/Users/ss/anaconda3/envs/chinese_sentiment-master/python.exe", pythonScriptPath, filePath, outputImagePath
            );
            processBuilder.redirectErrorStream(true);
            Process process = processBuilder.start();

            // 读取脚本执行结果
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }

            int exitCode = process.waitFor();
            if (exitCode == 0) {

                return ResponseEntity.ok(outputImagePath); // 返回图片路径
            } else {
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("词云图生成失败：" + output);
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("执行失败：" + e.getMessage());
        }
    }
}

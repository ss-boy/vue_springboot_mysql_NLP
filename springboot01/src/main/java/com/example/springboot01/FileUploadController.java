package com.example.springboot01;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.UrlResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/upload")
public class FileUploadController {

    @Autowired
    private FileUploadService fileUploadService;

    // 上传文件并返回内容
    @PostMapping
    public Map<String, Object> uploadFile(@RequestParam("file") MultipartFile file) {
        Map<String, Object> response = new HashMap<>();
        List<String> fileContent = new ArrayList<>();
        String filePath = "";

        try {
            // 保存文件
            filePath = fileUploadService.saveFile(file);

            // 读取文件内容
            Path path = Paths.get(filePath);
            BufferedReader reader = Files.newBufferedReader(path);
            String line;
            while ((line = reader.readLine()) != null) {
                fileContent.add(line);
            }

            response.put("filePath", filePath);
            response.put("fileContent", fileContent);
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException("文件处理失败：" + e.getMessage());
        }

        return response;
    }

    // 调用Python脚本进行预测
    @PostMapping("/predict")
    public Map<String, Object> predict(@RequestBody Map<String, String> request) {
        Map<String, Object> response = new HashMap<>();
        List<Map<String, String>> predictions = new ArrayList<>();

        String filePath = request.get("filePath");

        try {
            // 调用 Python 脚本
            ProcessBuilder processBuilder = new ProcessBuilder(
                    "C:/Users/ss/anaconda3/envs/chinese_sentiment-master/python.exe",
                    "D:/java/vue01/chinese_sentiment-master/model/lstm/txt-serve.py",
                    filePath
            );

            processBuilder.redirectErrorStream(true);
            Process process = processBuilder.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), "UTF-8"));
            String line;


            while ((line = reader.readLine()) != null) {
                if (line.startsWith("评论:")) {
                    String comment = line.substring(3).trim();
                    String prediction = ""; // 默认值

                    while ((line = reader.readLine()) != null) { // 继续读取直到找到预测结果
                        if (line.startsWith("预测结果:")) {
                            prediction = line.substring(5).trim();
                            break; // 找到结果后退出循环
                        }
                    }

                    if (!prediction.isEmpty()) {
                        Map<String, String> result = new HashMap<>();
                        result.put("comment", comment);
                        result.put("prediction", prediction);
                        predictions.add(result);
                    }

                }
            }




            int exitCode = process.waitFor();
            if (exitCode != 0) {
                throw new RuntimeException("Python 脚本执行失败，退出码：" + exitCode);
            }

            response.put("predictions", predictions);
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException("预测失败：" + e.getMessage());
        }

        return response;
    }

    // 下载文件
    @GetMapping("/download")
    public ResponseEntity<UrlResource> downloadFile(@RequestParam String path) {
        try {
            Path filePath = Paths.get(path);
            UrlResource resource = new UrlResource(filePath.toUri());

            if (!resource.exists()) {
                throw new RuntimeException("文件未找到");
            }

            return ResponseEntity.ok()
                    .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + filePath.getFileName().toString() + "\"")
                    .body(resource);
        } catch (Exception e) {
            throw new RuntimeException("文件下载失败：" + e.getMessage());
        }
    }
}

package com.example.springboot01;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

@Service
public class FileUploadService {

    @Autowired
    private FileMetadataRepository fileMetadataRepository;

    private static String UPLOAD_DIR = "uploads/";

    public String saveFile(MultipartFile file) throws IOException {
        // 获取文件名
        String fileName = file.getOriginalFilename();
        Path path = Paths.get(UPLOAD_DIR + fileName);
        Files.createDirectories(path.getParent());

        // 将文件保存到服务器
        file.transferTo(path);

        return path.toString();
    }
}

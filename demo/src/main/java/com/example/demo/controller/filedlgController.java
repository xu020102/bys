package com.example.demo.controller;

import org.springframework.core.io.FileSystemResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestParam;
import java.io.File;

@RestController
public class filedlgController {

    @GetMapping("/D/bysjgo")
    public ResponseEntity<FileSystemResource> downloadFile(@RequestParam("input") String input) {
        // 根据输入的文件名获取文件路径
        String filePath = "//D:/bysjxt/restlt/" + input + ".csv";
        File file = new File(filePath);

        if (!file.exists()) {
            // 文件不存在时返回404 Not Found状态码和提示信息
            return ResponseEntity.notFound().build();
        }

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);
        headers.setContentDispositionFormData("attachment", file.getName());
        System.out.println("success");
        return ResponseEntity
                .ok()
                .headers(headers)
                .body(new FileSystemResource(file));
    }
}

package com.example.demo.controller;

import org.springframework.core.io.FileSystemResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.File;

@RestController
public class filedlController {

    @GetMapping("/D/bys-chen")
    public ResponseEntity<FileSystemResource> downloadFile() {
        // 替换为你要下载的文件路径
        String filePath = "//D:/bysjxt/data/template.xlsx/";
        File file = new File(filePath);

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

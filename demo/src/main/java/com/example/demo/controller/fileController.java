package com.example.demo.controller;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;


@RestController
@CrossOrigin
@RequestMapping("/D/bysjcs")
public class fileController {
    @PostMapping()
    public String saveVue(String title,@RequestParam("file") MultipartFile file) throws Exception {
        // 保存文件
        String originalFilename = file.getOriginalFilename();
        String savePath = "D:/bysjxt/data";
        Path filePath = Paths.get(savePath, originalFilename);
        file.transferTo(filePath);

        // 执行 Python 脚本
        String pythonScriptPath = "D:/bysjxt/bys-chen/dataConcatenate.py";  // 替换为 Python 脚本路径

        try {
            System.out.println(pythonScriptPath);
            String command = "python " + pythonScriptPath + " " + filePath.toString();
            Runtime.getRuntime().exec(command);
            Thread.sleep(10000);  // 等待py文件运行结束
            return "SUCCESS";
        } catch (Exception e) {
            e.printStackTrace();
            return "ERROR";
        }
    }
}

//    @GetMapping()
//    public String upLoad(){
//        System.out.println("upload");
//        return "upLoad";
//    }


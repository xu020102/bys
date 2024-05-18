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
import java.util.Date;


@RestController
@CrossOrigin
@RequestMapping("/gameon")
public class gameonController {
    @PostMapping()
    public String saveVue() throws Exception {
        // 执行 Python 脚本
        String pythonScriptPath = "D:/bysjxt/bys-chen/BBO.py";  // 替换为 Python 脚本路径
        Date now = new Date();
        long seconds = now.getTime();
        String file_name = String.valueOf(seconds);

        try {

            String command = "python " + pythonScriptPath + " " + file_name;;
            Runtime.getRuntime().exec(command);
            return file_name;
        } catch (Exception e) {
            e.printStackTrace();
            return "error";
        }

    }
}


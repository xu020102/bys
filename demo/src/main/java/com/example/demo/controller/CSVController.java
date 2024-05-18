package com.example.demo.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;
import java.io.FileReader;
import java.io.IOException;
import java.text.DecimalFormat;
import java.time.Duration;
import java.time.LocalDateTime;
import java.util.*;
import org.springframework.web.bind.annotation.RequestBody;
import java.io.File;
import com.opencsv.CSVReader;
import org.springframework.web.bind.annotation.RequestMapping;

import java.io.Reader;

import org.springframework.web.bind.annotation.CrossOrigin;

@CrossOrigin(origins = "http://localhost:8080")
@RestController
@RequestMapping("/D/bysjsc")
public class CSVController {
    private static final String CSV_DIRECTORY = "//D:/bysjxt/result/";

    @PostMapping
    public Map<String, Object> getCsvData(@RequestBody Map<String, String> request) throws IOException {
        String input = request.get("input");

        Map<String, Object> csvData = new HashMap<>();
        // 检查CSV文件是否存在
        File csvFile = new File(CSV_DIRECTORY + input + ".csv");
        if (!csvFile.exists() || csvFile.isDirectory()) {
            csvData.put("exists", false);
            return csvData;
        }
        // 读取 CSV 文件的内容，假设文件路径为 "/path/to/csv/file.csv"
        try (FileReader reader = new FileReader(csvFile);
             CSVReader csvReader = new CSVReader(reader)) {
            String[] headers = csvReader.readNext();  // CSV 文件的列标题
            List<String> res_headers = new ArrayList<>();
            res_headers.add("序号");
            for (String h : headers) {
                if (!Objects.equals(h, "")) {
                    res_headers.add(h);
                }
            }
            List<Map<String, String>> rows = new ArrayList<>();
            String[] row;
            int t = 1;
            while ((row = csvReader.readNext()) != null) {
                Map<String, String> rowData = new HashMap<>();
                rowData.put("序号", String.valueOf(t++));
                for (int i = 1; i < headers.length-1; i++) {
                    rowData.put(headers[i], row[i]);
                }
                DecimalFormat decimalFormat = new DecimalFormat("0.00");
                rowData.put(headers[headers.length-1], decimalFormat.format(Double.valueOf(row[headers.length - 1])));
                rows.add(rowData);
            }
            csvData.put("exists", true);
            csvData.put("headers", res_headers);
            csvData.put("data", rows);
        }
        System.out.println("success");
        return csvData;
    }
}

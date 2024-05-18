package com.example.demo.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;
import java.io.FileReader;
import java.io.IOException;
import java.text.DecimalFormat;
import java.util.*;

import com.opencsv.CSVReader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import java.io.Reader;
import java.io.FileInputStream;
import org.springframework.web.bind.annotation.CrossOrigin;

@CrossOrigin(origins = "http://localhost:8080")
@RestController
@RequestMapping("/xlsxgame")
public class xlsxController {
    @PostMapping()
    public Map<String, Object> getCsvData() throws IOException {
        Map<String, Object> xlsxData = new HashMap<>();
        // 读取 XLSX 文件的内容，假设文件路径为 "/path/to/xlsx/file.xlsx"
        try (Workbook workbook = new XSSFWorkbook(new FileInputStream("D:/bysjxt/data/test4.xlsx"))) {
            Sheet sheet = workbook.getSheetAt(0); // 获取第一个工作表
            Row headerRow = sheet.getRow(0); // 获取标题行
            List<String> headers = new ArrayList<>();
            headers.add("序号");
            for (int j = 1; j < headerRow.getLastCellNum(); j++) {
                headers.add(headerRow.getCell(j).getStringCellValue());
//                System.out.println(headers);
            }

            List<Map<String, String>> rows = new ArrayList<>();
            int t = 1;
            System.out.println(sheet.getLastRowNum());
            for (int i = 1; i <= sheet.getLastRowNum(); i++) {
                Row dataRow = sheet.getRow(i);

                if (dataRow != null) {
                    Map<String, String> rowData = new HashMap<>();
                    rowData.put("序号", String.valueOf(t++));

                    for (int j = 1; j < headerRow.getLastCellNum()-1; j++) {
                        Cell cell = dataRow.getCell(j);
                        if (cell != null) {
                            rowData.put(headerRow.getCell(j).getStringCellValue(), String.valueOf(cell.getNumericCellValue()));
                        }
                    }
                    DecimalFormat decimalFormat = new DecimalFormat("0.00");
                    rowData.put(headerRow.getCell(headerRow.getLastCellNum()-1).getStringCellValue(),
                            String.valueOf(decimalFormat.format(dataRow.getCell(headerRow.getLastCellNum()-1).getNumericCellValue())));
                    rows.add(rowData);
                }
            }

            xlsxData.put("headers", headers);
            xlsxData.put("data", rows);
        }
        System.out.println("success");
        return xlsxData;
    }
}

# 基于贝叶斯优化的微藻培养交互系统设计
## 基本介绍
该系统是基于**贝叶斯优化技术**的用于辅助测定微藻最佳培养环境的工具。本系统是使用Vue2.0+springboot框架的前后端分离项目，代码已经于`Python 3.8.8`下进行测试，以下为相关依赖包或组件库：

* tensorflow==2.13.0
* gpflow==2.9.1
* numpy==1.22.4
* pandas==1.3.2
* Vue2.0
* element-ui
* springboot2.6.13

## 目录树
该项目目录树如下：

```
.
├── data
├── result
├── README.md
├── vuegame
├── demo
├── BBO.py
├── dataConcatenate.py
├── acquisitionFunction.py
└── black_box_f.py
```
其中，data:用于存放上传数据文件与模板文件。result：用于存放贝叶斯优化得到的添加剂参数与对应评价值结果，降维后散点图。vuegame：用于存放前端项目文件代码。demo：用于存放响应前端的对应后端方法代码。BBO.py：用于对实验数据进行贝叶斯优化与对结果进行MDS降维与保存。dataConcatenate.py：用于对上传数据与原有数据进行数据拼接。acquisitionFuntion.py：效用函数，权衡当前已有的结果以及探索的可能。black_box_f.py：黑盒函数。

## 首次部署
### 1. 安装前后端框架
安装前端框架Vue2.0，详细教程参考https://blog.csdn.net/Javachichi/article/details/132868889。安装后端框架springboot，官网https://spring.io/projects/spring-boot/。

### 2. 安装前后端依赖

* 安装python依赖

        pip install tensorflow==2.13.0
        pip install gpflow==2.9.1
        pip install numpy==1.22.4
        pip install pandas==1.3.2
       
## 部署步骤

### 1. 安装框架与依赖
按照上一步首次部署中的过程安装项目所用的前后端框架vue、springboot与依赖element-ui、tensorflow、gpflow、numpy、pandas等。
### 2. 启动后端
将后端代码demo\src\main\java\com\example\demo\controller中的所有方法中文件路径修改为当前本机路径
运行springboot后端文件".\demo\src\main\java\com\example\demo\DemoApplication.java"开启接收前端传来的请求的服务。
### 3. 启动前端
移动到前端文件根目录下，输入下方命令：

       npm run serve
运行命令成功给出下列反应：

     > game1@0.1.0 serve
     > vue-cli-service serve
      INFO  Starting development server...
     DONE  Compiled successfully in 4135ms                                                                                                                       23:13:07
      App running at:
     - Local:   http://l....../
     - Network: http://....../
4. 进入系统界面
在浏览器输入 Local: http://....../即可进入基于贝叶斯优化的微藻培养交互系统界面，进行后续操作。

## 系统操作流程

### 1. 下载模板
点击系统界面上的“下载模板”按钮，前端文件会调用方法“downloadFile()”，方法downloadFile()会向后端filedlController方法发出get请求，filedlController方法接收到请求后，会将固定路径下的下载模板文件信息返回给前端，前端根据返回信息，打开一个新的窗口对文件进行下载。
### 2. 上传数据
将实验数据文件拖拽到对应位置，点击系统界面上的“提交数据“按钮，前端文件会调用方法“onSubmit ()”，方法onSubmit ()会将文件作为参数向后端fileController方法发出post请求，filedController方法接收到请求后，会将文件保存到data中，并运行python文件dataConcatenate.py将上传数据与原有数据拼接起来。然后方法onSubmit ()会向后端xlsxController方法发出post请求，xlsxController方法会读取拼接后的数据并将其以list的形式返回前端，前端在接收到传回信息后会将其以表格形式展示在网页。
### 3.运行模型
点击系统界面上的“运行模型“按钮，前端文件会调用方法“runScript()”，方法runScript()会向后端gameonController方法发出post请求，gameonController方法接收到请求后，会读取当前时间并以此生成一组独特的key，将其作为参数运行python文件BBO.py，BBO.py会对拼接后的数据进行贝叶斯优化，并以key为名将结果保存，并对结果降维生成散点图key为名保存。gameonController方法会将key传回前端，前端将key展示在网页。
### 4. 查看结果
在网页上输入key，点击系统界面上的“获取结果“按钮，前端文件会调用方法“loadCsvData()”，方法loadCsvData()会将key作为参数向后端CSVController方法发出post请求，CSVController方法接收到请求后，会查询key文件是否存在，若不存在则直接返回"exists"，否则读取key文件并将结果以map形式返回前端。前端在收到返回后会根据返回内容中是否有exists来进行判断，若存在exists，则在网页给出错误提示，否则将返回内容以表格的形式展示在网页。
### 5. 查看散点图
在网页上输入key，点击系统界面上的“查看散点图“按钮，前端文件会调用方法“showImage()”，方法showImage()会将key作为参数向后端ImageController方法发出get请求，ImageController方法接收到请求后，会将降维后的图片文件返回前端，前端接到返回后将图片展示在网页。
### 6. 下载结果
在网页上输入key，点击系统界面上的“下载结果“按钮，前端文件会调用方法“downloadgoFile()”，方法downloadgoFile()会将key作为参数向后端filedlgController方法发出get请求，filedlgController方法接收到请求后，会检查是否存在key文件，若不存在则返回错误原因，若存在，则将result路径下的结果文件信息返回给前端，前端根据返回信息，打开一个新的窗口对文件进行下载。
-- 项目描述：
这是一个由我描述需求，由AI编写代码的项目

-- 数据库设计

sql  
CREATE DATABASE myapp;  
USE myapp;  

CREATE TABLE records (  
    id INT AUTO_INCREMENT PRIMARY KEY,  
    date DATE,  -- 日期  
    name VARCHAR(255) -- 人名    
);


-- 执行步骤：
1. 执行 python3 views.py ，启动程序
2. 执行 mysql.server start，启动本地数据库
3. 访问 对应地址

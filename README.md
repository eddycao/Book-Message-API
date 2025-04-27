# Book & Message API

本项目基于 **Python + Flask**，提供两个简单的 REST 接口：

1. **图书管理** `/books`
2. **留言板** `/messages`

## 快速开始
# Linux / macOS
```bash
git clone <repo-url>
cd Python_book_and_message_project
python3 -m venv venv
source venv/bin/activate      
pip install -r requirements.txt
python app.py                  
```
# Windows (PowerShell)
```bash
git clone <repo-url>
cd Python_book_and_message_project
python -m venv venv
.\venv\Scripts\Activate.ps1      
pip install -r requirements.txt
python app.py                 
```

服务默认运行在 <http://localhost:5000>。

## 目录结构

```
controllers/   路由 + 统一响应
services/      业务逻辑
models/        模型
data/          数据文件（必须初始均为 []）
```

## APIs

| 方法     | 路径                                  | 说明          |
|--------|-------------------------------------|-------------|
| GET    | /books                              | 获取全部图书      |
| POST   | /books                              | 创建单本 / 批量导入 |
| GET    | /books/id={id}                      | 按 ID 查询图书   |
| PUT    | /books/id={id}                      | 按 ID 更新图书   |
| DELETE | /books/id={id}                      | 按 ID 删除图书   |
| POST   | /messages                           | 发布留言        |
| GET    | /messages?page={page}&limit={limit} | 分页获取留言      |

> **批量导入示例**  
> ```json
> [
>   {"title":"红楼梦","author":"Xueqin Cao","year":1923},
>   {"title":"三国演义","author":"Guanzhong Luo","year":2014}
> ]
> ```

## Postman

导入根目录的 `postman_collection.json`，并设置变量

```
base_url = http://localhost:5000
```

即可进行所有接口的测试。

---

谢谢！~
# 书店API

一个简单的书店后端API，使用Python/Flask框架开发。

## 功能

- 获取所有图书
- 按作者名字搜索图书
- 获取单本图书详情
- 添加新图书
- 更新图书信息
- 删除图书

## 安装

```bash
pip install -r requirements.txt
```

## 运行

```bash
python run.py
```

## 测试

```bash
# 确保API服务器已启动
python test_api.py
```

## API端点

- `GET /api/books` - 获取所有图书
- `GET /api/books?author=作者名` - 按作者名字搜索图书
- `POST /api/books` - 添加新图书
- `GET /api/books/<id>` - 获取单本图书详情
- `PUT /api/books/<id>` - 更新图书信息
- `DELETE /api/books/<id>` - 删除图书

## 示例请求

### 获取所有图书

```
GET /api/books
```

### 按作者名字搜索图书

```
GET /api/books?author=刘慈欣
```

### 添加新图书

```
POST /api/books
Content-Type: application/json

{
    "title": "新书名称",
    "author": "作者名",
    "price": 45.00,
    "isbn": "9787XXXXXXXXX",
    "stock": 5
}
```

### 更新图书

```
PUT /api/books/1
Content-Type: application/json

{
    "price": 49.99,
    "stock": 20
}
```

### 删除图书

```
DELETE /api/books/1
```
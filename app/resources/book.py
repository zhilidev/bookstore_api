from flask import request
from flask_restful import Resource

# 模拟数据库
books = [
    {
        'id': 1,
        'title': '三体',
        'author': '刘慈欣',
        'price': 59.00,
        'isbn': '9787536692930',
        'stock': 10
    },
    {
        'id': 2,
        'title': '活着',
        'author': '余华',
        'price': 39.50,
        'isbn': '9787506365437',
        'stock': 15
    },
    {
        'id': 3,
        'title': '百年孤独',
        'author': '加西亚·马尔克斯',
        'price': 55.00,
        'isbn': '9787544253994',
        'stock': 8
    },
    {
        'id': 4,
        'title': '围城',
        'author': '钱钟书',
        'price': 36.00,
        'isbn': '9787020090006',
        'stock': 12
    },
    {
        'id': 5,
        'title': '平凡的世界',
        'author': '路遥',
        'price': 68.00,
        'isbn': '9787530216781',
        'stock': 20
    }
]

class BookListResource(Resource):
    def get(self):
        """获取所有图书，支持按作者名字进行搜索和过滤"""
        author = request.args.get('author')
        
        if author:
            # 如果提供了作者参数，按作者名字过滤图书
            filtered_books = [book for book in books if author in book['author']]
            return {'books': filtered_books}, 200
        else:
            # 否则返回所有图书
            return {'books': books}, 200
    
    def post(self):
        """添加新图书"""
        data = request.get_json()
        
        # 简单验证
        if not data or not all(key in data for key in ['title', 'author', 'price']):
            return {'message': '缺少必要的字段'}, 400
        
        # 生成新ID
        new_id = max(book['id'] for book in books) + 1 if books else 1
        
        # 创建新书
        new_book = {
            'id': new_id,
            'title': data['title'],
            'author': data['author'],
            'price': data['price'],
            'isbn': data.get('isbn', ''),
            'stock': data.get('stock', 0)
        }
        
        books.append(new_book)
        return {'book': new_book}, 201

class BookResource(Resource):
    def get(self, book_id):
        """获取单本图书"""
        book = next((book for book in books if book['id'] == book_id), None)
        if book:
            return {'book': book}, 200
        return {'message': '图书不存在'}, 404
    
    def put(self, book_id):
        """更新图书信息"""
        book = next((book for book in books if book['id'] == book_id), None)
        if not book:
            return {'message': '图书不存在'}, 404
            
        data = request.get_json()
        if not data:
            return {'message': '无效的数据'}, 400
            
        # 更新图书信息
        for key in data:
            if key in book:
                book[key] = data[key]
                
        return {'book': book}, 200
    
    def delete(self, book_id):
        """删除图书"""
        global books
        book = next((book for book in books if book['id'] == book_id), None)
        if not book:
            return {'message': '图书不存在'}, 404
            
        books = [book for book in books if book['id'] != book_id]
        return {'message': '图书已删除'}, 200
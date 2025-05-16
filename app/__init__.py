from flask import Flask
from flask_restful import Api

def create_app():
    app = Flask(__name__)
    api = Api(app)
    
    from app.resources.book import BookResource, BookListResource
    
    # 注册API路由
    api.add_resource(BookListResource, '/api/books')
    api.add_resource(BookResource, '/api/books/<int:book_id>')
    
    return app
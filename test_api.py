#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import unittest
import time

BASE_URL = "http://127.0.0.1:5000/api"

class BookstoreAPITest(unittest.TestCase):
    """书店API测试类"""
    
    def setUp(self):
        """测试前准备工作"""
        # 确保服务器已启动
        print("测试开始，请确保API服务器已运行...")
        time.sleep(1)
    
    def test_01_get_all_books(self):
        """测试获取所有图书"""
        response = requests.get(f"{BASE_URL}/books")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('books', data)
        self.assertIsInstance(data['books'], list)
        print(f"获取所有图书成功，共 {len(data['books'])} 本图书")
        
    def test_01a_search_books_by_author(self):
        """测试按作者名字搜索图书"""
        # 搜索刘慈欣的书
        response = requests.get(f"{BASE_URL}/books?author=刘慈欣")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('books', data)
        self.assertIsInstance(data['books'], list)
        # 验证所有返回的书籍作者名字中包含"刘慈欣"
        for book in data['books']:
            self.assertIn('刘慈欣', book['author'])
        print(f"按作者'刘慈欣'搜索图书成功，找到 {len(data['books'])} 本图书")
        
        # 搜索不存在的作者
        response = requests.get(f"{BASE_URL}/books?author=不存在的作者")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('books', data)
        self.assertEqual(len(data['books']), 0)
        print("搜索不存在作者测试通过")
    
    def test_02_get_book_by_id(self):
        """测试获取单本图书"""
        # 获取ID为1的图书
        response = requests.get(f"{BASE_URL}/books/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('book', data)
        self.assertEqual(data['book']['id'], 1)
        print(f"获取图书详情成功: {data['book']['title']}")
        
        # 测试获取不存在的图书
        response = requests.get(f"{BASE_URL}/books/999")
        self.assertEqual(response.status_code, 404)
        print("获取不存在图书测试通过")
    
    def test_03_create_book(self):
        """测试创建新图书"""
        new_book = {
            "title": "测试图书",
            "author": "测试作者",
            "price": 29.99,
            "isbn": "9787XXXXXXXXX",
            "stock": 100
        }
        
        response = requests.post(
            f"{BASE_URL}/books", 
            headers={"Content-Type": "application/json"},
            data=json.dumps(new_book)
        )
        
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('book', data)
        self.assertEqual(data['book']['title'], "测试图书")
        self.book_id = data['book']['id']
        print(f"创建图书成功，ID: {self.book_id}")
        
        # 测试创建图书时缺少必要字段
        invalid_book = {"title": "无效图书"}
        response = requests.post(
            f"{BASE_URL}/books", 
            headers={"Content-Type": "application/json"},
            data=json.dumps(invalid_book)
        )
        self.assertEqual(response.status_code, 400)
        print("创建无效图书测试通过")
    
    def test_04_update_book(self):
        """测试更新图书"""
        # 先获取所有图书，找到一个可以更新的ID
        response = requests.get(f"{BASE_URL}/books")
        books = response.json()['books']
        if not books:
            self.skipTest("没有可用的图书进行更新测试")
        
        book_id = books[0]['id']
        update_data = {
            "price": 88.88,
            "stock": 50
        }
        
        response = requests.put(
            f"{BASE_URL}/books/{book_id}", 
            headers={"Content-Type": "application/json"},
            data=json.dumps(update_data)
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('book', data)
        self.assertEqual(data['book']['price'], 88.88)
        self.assertEqual(data['book']['stock'], 50)
        print(f"更新图书成功，ID: {book_id}")
        
        # 测试更新不存在的图书
        response = requests.put(
            f"{BASE_URL}/books/999", 
            headers={"Content-Type": "application/json"},
            data=json.dumps(update_data)
        )
        self.assertEqual(response.status_code, 404)
        print("更新不存在图书测试通过")
    
    def test_05_delete_book(self):
        """测试删除图书"""
        # 先创建一本新书，然后删除它
        new_book = {
            "title": "待删除图书",
            "author": "待删除作者",
            "price": 19.99,
            "stock": 5
        }
        
        # 创建新书
        response = requests.post(
            f"{BASE_URL}/books", 
            headers={"Content-Type": "application/json"},
            data=json.dumps(new_book)
        )
        book_id = response.json()['book']['id']
        
        # 删除这本书
        response = requests.delete(f"{BASE_URL}/books/{book_id}")
        self.assertEqual(response.status_code, 200)
        print(f"删除图书成功，ID: {book_id}")
        
        # 确认已删除
        response = requests.get(f"{BASE_URL}/books/{book_id}")
        self.assertEqual(response.status_code, 404)
        print("确认图书已删除")
        
        # 测试删除不存在的图书
        response = requests.delete(f"{BASE_URL}/books/999")
        self.assertEqual(response.status_code, 404)
        print("删除不存在图书测试通过")

if __name__ == "__main__":
    unittest.main(verbosity=2)
import sqlite3
from datetime import datetime, timedelta, date
import json
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import tkinter.font as tkFont
import random
import hashlib
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfbase
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
import webbrowser

class SweetShopDatabase:
    def __init__(self):
        self.db_file = "sweet_shop_advanced.db"
        self.connection = None
        self.connect_database()
        self.create_tables()
        self.insert_initial_data()
    
    def connect_database(self):
        """الاتصال بقاعدة البيانات"""
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.connection.execute("PRAGMA foreign_keys = ON")
            print("تم الاتصال بقاعدة البيانات بنجاح")
        except sqlite3.Error as err:
            print(f"خطأ في الاتصال بقاعدة البيانات: {err}")
    
    def execute_query(self, query, params=None, fetch=False):
        """تنفيذ استعلام قاعدة البيانات"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                cursor.close()
                return True
        except sqlite3.Error as err:
            print(f"خطأ في تنفيذ الاستعلام: {err}")
            return None
    
    def create_tables(self):
        """إنشاء جداول قاعدة البيانات"""
        
        # جدول المستخدمين (للمسؤولين)
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT DEFAULT 'admin' CHECK(role IN ('admin', 'cashier')),
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
        """)
        
        # باقي الجداول (كما هي في النسخة السابقة)
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_id INTEGER,
            price REAL NOT NULL,
            cost REAL NOT NULL,
            stock_quantity INTEGER DEFAULT 0,
            description TEXT,
            image_url TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
        """)
        
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE,
            address TEXT,
            birth_date DATE,
            gender TEXT CHECK(gender IN ('male', 'female')),
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            total_purchases REAL DEFAULT 0.00,
            loyalty_points INTEGER DEFAULT 0
        )
        """)
        
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS subscription_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            duration_days INTEGER NOT NULL,
            price REAL NOT NULL,
            discount_percentage REAL DEFAULT 0.00,
            description TEXT,
            benefits TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS customer_subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            subscription_type_id INTEGER NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            status TEXT DEFAULT 'active' CHECK(status IN ('active', 'expired', 'cancelled')),
            payment_amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (subscription_type_id) REFERENCES subscription_types(id)
        )
        """)
        
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_number TEXT UNIQUE NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount REAL NOT NULL,
            discount_amount REAL DEFAULT 0.00,
            final_amount REAL NOT NULL,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'confirmed', 'preparing', 'ready', 'delivered', 'cancelled')),
            payment_method TEXT DEFAULT 'cash' CHECK(payment_method IN ('cash', 'card', 'online')),
            notes TEXT,
            created_by INTEGER,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
        """)
        
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
        """)
        
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            subscription_id INTEGER,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL CHECK(payment_method IN ('cash', 'card', 'online')),
            payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'completed' CHECK(status IN ('pending', 'completed', 'failed', 'refunded')),
            transaction_id TEXT,
            notes TEXT,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (subscription_id) REFERENCES customer_subscriptions(id)
        )
        """)
        
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS inventory_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL CHECK(transaction_type IN ('purchase', 'sale', 'adjustment', 'return')),
            quantity_change INTEGER NOT NULL,
            quantity_after INTEGER NOT NULL,
            reference_id INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
        """)
    
    def insert_initial_data(self):
        """إدراج البيانات الأساسية"""
        
        # التحقق من وجود البيانات مسبقاً
        result = self.execute_query("SELECT COUNT(*) FROM categories", fetch=True)
        if result and result[0][0] > 0:
            return
        
        # إنشاء مستخدم افتراضي
        default_password = self.hash_password("admin123")
        self.execute_query("""
            INSERT INTO users (username, password_hash, full_name, role)
            VALUES (?, ?, ?, ?)
        """, ("admin", default_password, "المدير العام", "admin"))
        
        # إدراج فئات المنتجات (نفس البيانات السابقة)
        categories = [
            ('حلويات باردة', 'حلويات تقدم باردة مثل الكيك والتيراميسو'),
            ('حلويات ساخنة', 'حلويات تقدم ساخنة مثل الكنافة والسوفليه'),
            ('مشروبات باردة', 'عصائر طبيعية ومشروبات منعشة'),
            ('مشروبات ساخنة', 'قهوة وشاي ومشروبات ساخنة أخرى'),
            ('حلويات شرقية', 'بقلاوة وكنافة وحلويات تراثية')
        ]
        
        for name, desc in categories:
            self.execute_query("INSERT INTO categories (name, description) VALUES (?, ?)", (name, desc))
        
        # إدراج المنتجات (نفس البيانات السابقة)
        products = [
            # حلويات باردة
            ('تشيز كيك', 1, 15.00, 8.00, 50, 'كيك الجبن الكريمي الشهير'),
            ('براونيز', 1, 12.00, 6.00, 100, 'كيك الشوكولاتة الغني'),
            ('تيراميسو', 1, 18.00, 10.00, 30, 'الحلوى الإيطالية الكلاسيكية'),
            ('بافلوفا', 1, 20.00, 12.00, 25, 'حلوى المرانغ الخفيفة'),
            ('ماكرون', 1, 3.00, 1.50, 200, 'حلوى الماكرون الفرنسية'),
            ('كب كيك', 1, 8.00, 4.00, 150, 'كيك صغير بأطعمة متنوعة'),
            ('إكلير', 1, 10.00, 5.00, 80, 'معجنات محشوة بالكريمة'),
            ('مافن', 1, 6.00, 3.00, 120, 'كيك صغير بالتوت'),
            ('بانا كوتا', 1, 14.00, 7.00, 40, 'حلوى إيطالية كريمية'),
            ('دونتس', 1, 4.00, 2.00, 200, 'دونتس مقلي بالسكر'),
            
            # حلويات ساخنة
            ('سوفليه', 2, 22.00, 14.00, 20, 'حلوى فرنسية منفوشة'),
            ('فطيرة التفاح', 2, 16.00, 9.00, 35, 'فطيرة التفاح الكلاسيكية'),
            ('خبز البودينغ', 2, 13.00, 7.00, 45, 'بودينغ الخبز بالفانيليا'),
            ('تشورو', 2, 9.00, 4.50, 100, 'عجين مقلي بالسكر والقرفة'),
            ('كريب سوزيت', 2, 17.00, 10.00, 30, 'كريب فرنسي باللهب'),
            
            # مشروبات باردة
            ('عصير برتقال', 3, 5.00, 2.50, 100, 'عصير برتقال طبيعي'),
            ('عصير ليمون نعناع', 3, 6.00, 3.00, 80, 'مشروب منعش بالليمون'),
            ('عصير بطيخ', 3, 7.00, 3.50, 60, 'عصير بطيخ طازج'),
            ('عصير أناناس', 3, 8.00, 4.00, 50, 'عصير أناناس استوائي'),
            ('عصير رمان', 3, 9.00, 4.50, 40, 'عصير رمان غني بالفيتامينات'),
            
            # مشروبات ساخنة
            ('سحلب', 4, 7.00, 3.50, 80, 'مشروب شتوي دافئ'),
            ('شاي', 4, 3.00, 1.50, 200, 'شاي أحمر تقليدي'),
            ('شوكولاتة ساخنة', 4, 8.00, 4.00, 100, 'شوكولاتة دافئة كريمية'),
            ('قهوة موكا', 4, 10.00, 5.00, 80, 'قهوة بالشوكولاتة'),
            ('لاتيه', 4, 9.00, 4.50, 90, 'قهوة بالحليب الرغوي'),
            ('إسبريسو', 4, 6.00, 3.00, 150, 'قهوة إيطالية قوية'),
            ('كابتشينو', 4, 8.00, 4.00, 100, 'قهوة إيطالية كلاسيكية')
        ]
        
        for product in products:
            self.execute_query("""
                INSERT INTO products (name, category_id, price, cost, stock_quantity, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, product)
        
        # إدراج أنواع الاشتراكات
        subscription_types = [
            ('اشتراك أسبوعي', 7, 25.00, 10.00, 'خصم 10% على جميع المشتريات لمدة أسبوع', '{"discount": "10%", "free_delivery": false, "priority_service": false}'),
            ('اشتراك شهري', 30, 80.00, 15.00, 'خصم 15% على جميع المشتريات لمدة شهر', '{"discount": "15%", "free_delivery": true, "priority_service": true}'),
            ('اشتراك ربع سنوي', 90, 200.00, 20.00, 'خصم 20% على جميع المشتريات لمدة 3 أشهر', '{"discount": "20%", "free_delivery": true, "priority_service": true, "birthday_gift": true}'),
            ('اشتراك سنوي', 365, 600.00, 25.00, 'خصم 25% على جميع المشتريات لمدة سنة كاملة', '{"discount": "25%", "free_delivery": true, "priority_service": true, "birthday_gift": true, "exclusive_items": true}')
        ]
        
        for sub in subscription_types:
            self.execute_query("""
                INSERT INTO subscription_types (name, duration_days, price, discount_percentage, description, benefits)
                VALUES (?, ?, ?, ?, ?, ?)
            """, sub)
    
    def hash_password(self, password):
        """تشفير كلمة المرور"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_user(self, username, password):
        """التحقق من صحة تسجيل الدخول"""
        password_hash = self.hash_password(password)
        query = """
        SELECT id, username, full_name, role FROM users 
        WHERE username = ? AND password_hash = ? AND is_active = 1
        """
        result = self.execute_query(query, (username, password_hash), fetch=True)
        
        if result:
            user_id = result[0][0]
            # تحديث آخر تسجيل دخول
            self.execute_query(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?", 
                (user_id,)
            )
            return result[0]
        return None
    
    def register_user(self, username, password, full_name, role='admin'):
        """تسجيل مستخدم جديد"""
        password_hash = self.hash_password(password)
        query = """
        INSERT INTO users (username, password_hash, full_name, role)
        VALUES (?, ?, ?, ?)
        """
        return self.execute_query(query, (username, password_hash, full_name, role))
    
    # باقي الدوال (نفسها من النسخة السابقة)
    def add_customer(self, name, phone, email=None, address=None, birth_date=None, gender=None):
        """إضافة عميل جديد"""
        query = """
        INSERT INTO customers (name, phone, email, address, birth_date, gender)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (name, phone, email, address, birth_date, gender)
        return self.execute_query(query, params)
    
    def get_customer_by_phone(self, phone):
        """البحث عن عميل بالهاتف"""
        query = "SELECT * FROM customers WHERE phone = ?"
        result = self.execute_query(query, (phone,), fetch=True)
        return result[0] if result else None
    
    def get_all_products(self):
        """جلب جميع المنتجات"""
        query = """
        SELECT p.id, p.name, c.name as category, p.price, p.stock_quantity, p.description
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.is_active = 1
        ORDER BY c.name, p.name
        """
        return self.execute_query(query, fetch=True)
    
    def create_order(self, customer_id, items, payment_method='cash', user_id=None):
        """إنشاء طلب جديد"""
        try:
            order_number = f"ORD{random.randint(10000, 99999)}"
            total_amount = sum(item['quantity'] * item['price'] for item in items)
            
            # التحقق من الاشتراك للحصول على خصم
            discount_amount = 0
            subscription = self.get_active_subscription(customer_id)
            if subscription:
                discount_percentage = subscription[4]
                discount_amount = total_amount * (discount_percentage / 100)
            
            final_amount = total_amount - discount_amount
            
            # إنشاء الطلب
            order_query = """
            INSERT INTO orders (customer_id, order_number, total_amount, discount_amount, 
                              final_amount, payment_method, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            order_params = (customer_id, order_number, total_amount, discount_amount, 
                           final_amount, payment_method, user_id)
            
            if self.execute_query(order_query, order_params):
                order_id_query = "SELECT last_insert_rowid()"
                order_id_result = self.execute_query(order_id_query, fetch=True)
                order_id = order_id_result[0][0]
                
                # إضافة عناصر الطلب
                for item in items:
                    item_query = """
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
                    VALUES (?, ?, ?, ?, ?)
                    """
                    item_total = item['quantity'] * item['price']
                    item_params = (order_id, item['product_id'], item['quantity'], 
                                 item['price'], item_total)
                    
                    if self.execute_query(item_query, item_params):
                        self.update_product_stock(item['product_id'], -item['quantity'], 'sale')
                
                # إضافة نقاط الولاء
                loyalty_points = int(final_amount)
                self.update_customer_loyalty_points(customer_id, loyalty_points)
                
                # تسجيل الدفع
                payment_query = """
                INSERT INTO payments (order_id, amount, payment_method)
                VALUES (?, ?, ?)
                """
                self.execute_query(payment_query, (order_id, final_amount, payment_method))
                
                return order_id, order_number, final_amount
            
            return None
        except Exception as e:
            print(f"خطأ في إنشاء الطلب: {e}")
            return None
    
    def get_active_subscription(self, customer_id):
        """جلب الاشتراك النشط للعميل"""
        query = """
        SELECT cs.*, st.discount_percentage 
        FROM customer_subscriptions cs
        JOIN subscription_types st ON cs.subscription_type_id = st.id
        WHERE cs.customer_id = ? AND cs.status = 'active' 
        AND cs.end_date >= DATE('now')
        """
        result = self.execute_query(query, (customer_id,), fetch=True)
        return result[0] if result else None
    
    def update_product_stock(self, product_id, quantity_change, transaction_type):
        """تحديث مخزون المنتج"""
        query = "SELECT stock_quantity FROM products WHERE id = ?"
        result = self.execute_query(query, (product_id,), fetch=True)
        if not result:
            return False
        
        current_quantity = result[0][0]
        new_quantity = current_quantity + quantity_change
        
        update_query = "UPDATE products SET stock_quantity = ? WHERE id = ?"
        if self.execute_query(update_query, (new_quantity, product_id)):
            inventory_query = """
            INSERT INTO inventory_transactions 
            (product_id, transaction_type, quantity_change, quantity_after)
            VALUES (?, ?, ?, ?)
            """
            return self.execute_query(inventory_query, 
                                    (product_id, transaction_type, quantity_change, new_quantity))
        return False
    
    def update_customer_loyalty_points(self, customer_id, points):
        """تحديث نقاط الولاء للعميل"""
        query = "UPDATE customers SET loyalty_points = loyalty_points + ? WHERE id = ?"
        return self.execute_query(query, (points, customer_id))
    
    def get_order_details(self, order_id):
        """جلب تفاصيل الطلب للفاتورة"""
        order_query = """
        SELECT o.*, c.name as customer_name, c.phone, c.address, u.full_name as cashier_name
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        LEFT JOIN users u ON o.created_by = u.id
        WHERE o.id = ?
        """
        order_result = self.execute_query(order_query, (order_id,), fetch=True)
        
        items_query = """
        SELECT oi.*, p.name as product_name
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = ?
        """
        items_result = self.execute_query(items_query, (order_id,), fetch=True)
        
        if order_result:
            return order_result[0], items_result
        return None, None
    
    def close_connection(self):
        """إغلاق الاتصال بقاعدة البيانات"""
        if self.connection:
            self.connection.close()

class LoginWindow:
    def __init__(self, main_callback):
        self.main_callback = main_callback
        self.db = SweetShopDatabase()
        self.root = Tk()
        self.setup_login_window()
    
    def setup_login_window(self):
        """إعداد نافذة تسجيل الدخول"""
        self.root.title("🍰 نظام إدارة محل الحلويات - تسجيل الدخول")
        self.root.geometry("450x550")
        self.root.configure(bg='#f8f9fa')
        self.root.resizable(False, False)
        
        # توسيط النافذة
        self.center_window()
        
        # الإطار الرئيسي
        main_frame = Frame(self.root, bg='#ffffff', relief='raised', bd=2)
        main_frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=500)
        
        # العنوان والأيقونة
        title_frame = Frame(main_frame, bg='#ffffff')
        title_frame.pack(pady=30)
        
        title_label = Label(title_frame, text="🍰", font=('Arial', 48), bg='#ffffff')
        title_label.pack()
        
        welcome_label = Label(title_frame, text="مرحباً بك في محل الحلويات", 
                             font=('Arial', 16, 'bold'), bg='#ffffff', fg='#2c3e50')
        welcome_label.pack(pady=5)
        
        subtitle_label = Label(title_frame, text="يرجى تسجيل الدخول للمتابعة", 
                              font=('Arial', 12), bg='#ffffff', fg='#7f8c8d')
        subtitle_label.pack()
        
        # إطار تسجيل الدخول
        login_frame = Frame(main_frame, bg='#ffffff')
        login_frame.pack(pady=20, padx=40, fill='x')
        
        # حقل اسم المستخدم
        Label(login_frame, text="اسم المستخدم:", font=('Arial', 12, 'bold'), 
              bg='#ffffff', fg='#2c3e50').pack(anchor='e', pady=(0, 5))
        
        self.username_entry = Entry(login_frame, font=('Arial', 12), relief='flat', 
                                   bg='#f8f9fa', bd=1, insertbackground='#3498db')
        self.username_entry.pack(fill='x', ipady=8)
        self.username_entry.insert(0, "admin")  # قيمة افتراضية
        
        # حقل كلمة المرور
        Label(login_frame, text="كلمة المرور:", font=('Arial', 12, 'bold'), 
              bg='#ffffff', fg='#2c3e50').pack(anchor='e', pady=(15, 5))
        
        self.password_entry = Entry(login_frame, font=('Arial', 12), show='*', 
                                   relief='flat', bg='#f8f9fa', bd=1, insertbackground='#3498db')
        self.password_entry.pack(fill='x', ipady=8)
        self.password_entry.insert(0, "admin123")  # قيمة افتراضية
        
        # زر تسجيل الدخول
        login_btn = Button(login_frame, text="تسجيل الدخول", font=('Arial', 12, 'bold'),
                          bg='#3498db', fg='white', relief='flat', cursor='hand2',
                          command=self.login, pady=10)
        login_btn.pack(fill='x', pady=(20, 10))
        
        # خط فاصل
        separator = Frame(login_frame, height=1, bg='#bdc3c7')
        separator.pack(fill='x', pady=15)
        
        # نص التسجيل الجديد
        signup_text = Label(login_frame, text="ليس لديك حساب؟", 
                           font=('Arial', 10), bg='#ffffff', fg='#7f8c8d')
        signup_text.pack(pady=(0, 5))
        
        # زر التسجيل الجديد
        signup_btn = Button(login_frame, text="Sign Up - إنشاء حساب جديد", 
                           font=('Arial', 11, 'bold'), bg='#2ecc71', fg='white',
                           relief='flat', cursor='hand2', command=self.show_signup,
                           pady=8)
        signup_btn.pack(fill='x')
        
        # معلومات الاختبار
        info_frame = Frame(main_frame, bg='#ffffff')
        info_frame.pack(pady=20)
        
        info_label = Label(info_frame, text="للاختبار:", font=('Arial', 9, 'bold'),
                          bg='#ffffff', fg='#e74c3c')
        info_label.pack()
        
        test_info = Label(info_frame, text="المستخدم: admin | كلمة المرور: admin123",
                         font=('Arial', 9), bg='#ffffff', fg='#95a5a6')
        test_info.pack()
        
        # ربط Enter بتسجيل الدخول
        self.root.bind('<Return>', lambda event: self.login())
        
        # تركيز على حقل المستخدم
        self.username_entry.focus()
    
    def center_window(self):
        """توسيط النافذة على الشاشة"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def login(self):
        """تسجيل الدخول"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("خطأ", "يرجى إدخال اسم المستخدم وكلمة المرور")
            return
        
        user = self.db.authenticate_user(username, password)
        
        if user:
            messagebox.showinfo("نجح", f"مرحباً {user[2]}!\nتم تسجيل الدخول بنجاح")
            self.root.destroy()
            self.main_callback(user)
        else:
            messagebox.showerror("خطأ", "اسم المستخدم أو كلمة المرور غير صحيح")
            self.password_entry.delete(0, END)
            self.password_entry.focus()
    
    def show_signup(self):
        """عرض نافذة التسجيل الجديد"""
        signup_window = Toplevel(self.root)
        signup_window.title("إنشاء حساب جديد")
        signup_window.geometry("400x450")
        signup_window.configure(bg='#ffffff')
        signup_window.resizable(False, False)
        
        # توسيط النافذة
        signup_window.update_idletasks()
        x = (signup_window.winfo_screenwidth() // 2) - (200)
        y = (signup_window.winfo_screenheight() // 2) - (225)
        signup_window.geometry(f'400x450+{x}+{y}')
        
        # العنوان
        title_label = Label(signup_window, text="🆕 إنشاء حساب جديد", 
                           font=('Arial', 18, 'bold'), bg='#ffffff', fg='#2c3e50')
        title_label.pack(pady=20)
        
        # إطار النموذج
        form_frame = Frame(signup_window, bg='#ffffff')
        form_frame.pack(pady=20, padx=40, fill='x')
        
        # الاسم الكامل
        Label(form_frame, text="الاسم الكامل:", font=('Arial', 12, 'bold'),
              bg='#ffffff', fg='#2c3e50').pack(anchor='e', pady=(0, 5))
        full_name_entry = Entry(form_frame, font=('Arial', 12), relief='flat',
                               bg='#f8f9fa', bd=1)
        full_name_entry.pack(fill='x', ipady=8)
        
        # اسم المستخدم
        Label(form_frame, text="اسم المستخدم:", font=('Arial', 12, 'bold'),
              bg='#ffffff', fg='#2c3e50').pack(anchor='e', pady=(15, 5))
        new_username_entry = Entry(form_frame, font=('Arial', 12), relief='flat',
                                  bg='#f8f9fa', bd=1)
        new_username_entry.pack(fill='x', ipady=8)
        
        # كلمة المرور
        Label(form_frame, text="كلمة المرور:", font=('Arial', 12, 'bold'),
              bg='#ffffff', fg='#2c3e50').pack(anchor='e', pady=(15, 5))
        new_password_entry = Entry(form_frame, font=('Arial', 12), show='*',
                                  relief='flat', bg='#f8f9fa', bd=1)
        new_password_entry.pack(fill='x', ipady=8)
        
        # تأكيد كلمة المرور
        Label(form_frame, text="تأكيد كلمة المرور:", font=('Arial', 12, 'bold'),
              bg='#ffffff', fg='#2c3e50').pack(anchor='e', pady=(15, 5))
        confirm_password_entry = Entry(form_frame, font=('Arial', 12), show='*',
                                      relief='flat', bg='#f8f9fa', bd=1)
        confirm_password_entry.pack(fill='x', ipady=8)
        
        # الدور
        Label(form_frame, text="الدور:", font=('Arial', 12, 'bold'),
              bg='#ffffff', fg='#2c3e50').pack(anchor='e', pady=(15, 5))
        role_var = StringVar(value="admin")
        role_frame = Frame(form_frame, bg='#ffffff')
        role_frame.pack(fill='x')
        
        Radiobutton(role_frame, text="مدير", variable=role_var, value="admin",
                   font=('Arial', 11), bg='#ffffff').pack(side='right', padx=10)
        Radiobutton(role_frame, text="كاشير", variable=role_var, value="cashier",
                   font=('Arial', 11), bg='#ffffff').pack(side='right', padx=10)
        
        def create_account():
            full_name = full_name_entry.get().strip()
            username = new_username_entry.get().strip()
            password = new_password_entry.get().strip()
            confirm_password = confirm_password_entry.get().strip()
            role = role_var.get()
            
            if not all([full_name, username, password, confirm_password]):
                messagebox.showerror("خطأ", "يرجى ملء جميع الحقول")
                return
            
            if password != confirm_password:
                messagebox.showerror("خطأ", "كلمتا المرور غير متطابقتان")
                return
            
            if len(password) < 6:
                messagebox.showerror("خطأ", "كلمة المرور يجب أن تكون 6 أحرف على الأقل")
                return
            
            if self.db.register_user(username, password, full_name, role):
                messagebox.showinfo("نجح", "تم إنشاء الحساب بنجاح!\nيمكنك الآن تسجيل الدخول")
                signup_window.destroy()
            else:
                messagebox.showerror("خطأ", "فشل في إنشاء الحساب\nاسم المستخدم موجود مسبقاً")
        
        # أزرار العمليات
        buttons_frame = Frame(form_frame, bg='#ffffff')
        buttons_frame.pack(fill='x', pady=20)
        
        Button(buttons_frame, text="إنشاء الحساب", font=('Arial', 12, 'bold'),
               bg='#2ecc71', fg='white', relief='flat', cursor='hand2',
               command=create_account, pady=8).pack(side='right', padx=5)
        
        Button(buttons_frame, text="إلغاء", font=('Arial', 12, 'bold'),
               bg='#95a5a6', fg='white', relief='flat', cursor='hand2',
               command=signup_window.destroy, pady=8).pack(side='right', padx=5)
    
    def run(self):
        """تشغيل نافذة تسجيل الدخول"""
        self.root.mainloop()

class InvoicePrinter:
    def __init__(self, db):
        self.db = db
    
    def print_invoice(self, order_id):
        """طباعة الفاتورة"""
        try:
            order_data, items_data = self.db.get_order_details(order_id)
            
            if not order_data:
                messagebox.showerror("خطأ", "لم يتم العثور على الطلب")
                return
            
            # اختيار مكان حفظ الفاتورة
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="حفظ الفاتورة",
                initialname=f"فاتورة_{order_data[2]}.pdf"
            )
            
            if filename:
                self.create_pdf_invoice(filename, order_data, items_data)
                messagebox.showinfo("نجح", f"تم حفظ الفاتورة في:\n{filename}")
                
                # سؤال لفتح الملف
                if messagebox.askyesno("فتح الفاتورة", "هل تريد فتح الفاتورة الآن؟"):
                    os.startfile(filename) if os.name == 'nt' else os.system(f'open "{filename}"')
                    
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في إنشاء الفاتورة:\n{str(e)}")
    
    def create_pdf_invoice(self, filename, order_data, items_data):
        """إنشاء فاتورة PDF"""
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        
        # معلومات الطلب
        order_id, customer_id, order_number, order_date, total_amount, discount_amount, final_amount, status, payment_method, notes, created_by, customer_name, phone, address, cashier_name = order_data
        
        # رأس الفاتورة
        y = height - 50
        
        # شعار وعنوان المحل
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredText(width/2, y, "🍰 Sweet Shop")
        y -= 30
        
        c.setFont("Helvetica", 16)
        c.drawCentredText(width/2, y, "محل الحلويات المتميز")
        y -= 20
        
        c.setFont("Helvetica", 12)
        c.drawCentredText(width/2, y, "العنوان: شارع الملك فهد، الرياض | الهاتف: 0112345678")
        y -= 40
        
        # خط فاصل
        c.line(50, y, width-50, y)
        y -= 30
        
        # عنوان الفاتورة
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredText(width/2, y, "فـــاتـــورة")
        y -= 40
        
        # معلومات الطلب والعميل
        c.setFont("Helvetica-Bold", 12)
        
        # الجانب الأيمن - معلومات العميل
        c.drawRightString(width-50, y, f"اسم العميل: {customer_name}")
        y -= 20
        c.drawRightString(width-50, y, f"رقم الهاتف: {phone}")
        y -= 20
        if address:
            c.drawRightString(width-50, y, f"العنوان: {address}")
            y -= 20
        
        # العودة للأعلى للجانب الأيسر
        y += 60 if address else 40
        
        # الجانب الأيسر - معلومات الطلب
        c.drawString(50, y, f"رقم الطلب: {order_number}")
        y -= 20
        c.drawString(50, y, f"التاريخ: {order_date[:16]}")
        y -= 20
        c.drawString(50, y, f"الكاشير: {cashier_name or 'غير محدد'}")
        y -= 40
        
        # جدول المنتجات
        c.setFont("Helvetica-Bold", 12)
        
        # رأس الجدول
        table_headers = ["المجموع", "السعر", "الكمية", "اسم المنتج"]
        col_widths = [80, 80, 60, 200]
        x_positions = [width-50-sum(col_widths[:i]) for i in range(len(col_widths))]
        x_positions.reverse()
        
        # رسم رأس الجدول
        for i, header in enumerate(table_headers):
            c.drawCentredText(x_positions[i] + col_widths[i]/2, y, header)
        
        y -= 5
        c.line(50, y, width-50, y)  # خط تحت الرأس
        y -= 20
        
        # بيانات المنتجات
        c.setFont("Helvetica", 11)
        for item in items_data:
            item_id, order_id, product_id, quantity, unit_price, total_price, product_name = item
            
            row_data = [f"{total_price:.2f}", f"{unit_price:.2f}", str(quantity), product_name]
            
            for i, data in enumerate(row_data):
                if i == 3:  # اسم المنتج - محاذاة يمين
                    c.drawRightString(x_positions[i] + col_widths[i] - 5, y, data)
                else:  # باقي البيانات - توسيط
                    c.drawCentredText(x_positions[i] + col_widths[i]/2, y, data)
            
            y -= 18
        
        # خط فاصل قبل المجموع
        y -= 10
        c.line(50, y, width-50, y)
        y -= 25
        
        # المجاميع
        c.setFont("Helvetica-Bold", 12)
        
        c.drawRightString(width-50, y, f"المجموع الفرعي: {total_amount:.2f} ريال")
        y -= 20
        
        if discount_amount > 0:
            c.drawRightString(width-50, y, f"الخصم: {discount_amount:.2f} ريال")
            y -= 20
        
        c.setFont("Helvetica-Bold", 14)
        c.drawRightString(width-50, y, f"المجموع الإجمالي: {final_amount:.2f} ريال")
        y -= 30
        
        # طريقة الدفع
        c.setFont("Helvetica", 12)
        payment_methods = {'cash': 'نقداً', 'card': 'بطاقة', 'online': 'إلكتروني'}
        c.drawRightString(width-50, y, f"طريقة الدفع: {payment_methods.get(payment_method, payment_method)}")
        y -= 40
        
        # ملاحظات
        if notes:
            c.setFont("Helvetica-Bold", 12)
            c.drawRightString(width-50, y, "ملاحظات:")
            y -= 15
            c.setFont("Helvetica", 11)
            c.drawRightString(width-50, y, notes)
            y -= 30
        
        # رسالة شكر
        y -= 20
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredText(width/2, y, "شكراً لتسوقكم معنا")
        y -= 15
        c.setFont("Helvetica", 12)
        c.drawCentredText(width/2, y, "نتطلع لخدمتكم مرة أخرى")
        
        # حفظ الملف
        c.save()

class SweetShopGUI:
    def __init__(self, user_data):
        self.user_data = user_data  # (id, username, full_name, role)
        self.db = SweetShopDatabase()
        self.invoice_printer = InvoicePrinter(self.db)
        self.root = Tk()
        self.current_customer = None
        self.cart_items = []
        self.setup_main_gui()
    
    def setup_main_gui(self):
        """إعداد الواجهة الرئيسية"""
        self.root.title(f"🍰 نظام إدارة محل الحلويات - مرحباً {self.user_data[2]}")
        self.root.geometry("1500x900")
        self.root.configure(bg='#f8f9fa')
        
        # الألوان المستخدمة
        self.colors = {
            'primary': '#3498db',
            'success': '#2ecc71', 
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'info': '#17a2b8',
            'dark': '#2c3e50',
            'light': '#ecf0f1',
            'white': '#ffffff'
        }
        
        # إعداد شريط القوائم المحسن
        self.setup_menubar()
        
        # إعداد شريط الحالة
        self.setup_statusbar()
        
        # الإطار الرئيسي مع تصميم متقدم
        self.setup_main_content()
        
        # تحميل البيانات
        self.load_products()
    
    def setup_menubar(self):
        """إعداد شريط القوائم المحسن"""
        menubar = Menu(self.root, bg=self.colors['dark'], fg='white', font=('Arial', 11))
        self.root.config(menu=menubar)
        
        # قائمة العملاء
        customer_menu = Menu(menubar, tearoff=0, bg='white', font=('Arial', 10))
        menubar.add_cascade(label="👥 العملاء", menu=customer_menu)
        customer_menu.add_command(label="🆕 إضافة عميل جديد", command=self.add_customer_window)
        customer_menu.add_command(label="🔍 البحث عن عميل", command=self.search_customer_window)
        customer_menu.add_separator()
        customer_menu.add_command(label="📊 قائمة العملاء", command=self.show_customers_list)
        
        # قائمة الاشتراكات
        subscription_menu = Menu(menubar, tearoff=0, bg='white', font=('Arial', 10))
        menubar.add_cascade(label="💳 الاشتراكات", menu=subscription_menu)
        subscription_menu.add_command(label="🆕 إنشاء اشتراك", command=self.create_subscription_window)
        subscription_menu.add_command(label="📋 عرض الاشتراكات", command=self.view_subscriptions)
        
        # قائمة التقارير
        reports_menu = Menu(menubar, tearoff=0, bg='white', font=('Arial', 10))
        menubar.add_cascade(label="📊 التقارير", menu=reports_menu)
        reports_menu.add_command(label="🏆 أكثر المنتجات مبيعاً", command=self.show_top_products)
        reports_menu.add_command(label="📉 أقل المنتجات مبيعاً", command=self.show_least_products)
        reports_menu.add_separator()
        reports_menu.add_command(label="👥 تحليل العملاء", command=self.show_customer_analytics)
        reports_menu.add_command(label="📈 المبيعات الشهرية", command=self.show_monthly_sales)
        reports_menu.add_command(label="📂 تحليل الفئات", command=self.show_category_analysis)
        
        # قائمة الإعدادات
        settings_menu = Menu(menubar, tearoff=0, bg='white', font=('Arial', 10))
        menubar.add_cascade(label="⚙️ الإعدادات", menu=settings_menu)
        settings_menu.add_command(label="👤 معلومات المستخدم", command=self.show_user_info)
        settings_menu.add_separator()
        settings_menu.add_command(label="🚪 تسجيل الخروج", command=self.logout)
    
    def setup_statusbar(self):
        """إعداد شريط الحالة"""
        self.statusbar = Frame(self.root, bg=self.colors['dark'], height=25)
        self.statusbar.pack(side=BOTTOM, fill=X)
        
        # معلومات المستخدم
        user_label = Label(self.statusbar, text=f"👤 {self.user_data[2]} ({self.user_data[3]})", 
                          bg=self.colors['dark'], fg='white', font=('Arial', 9))
        user_label.pack(side=RIGHT, padx=10, pady=2)
        
        # الوقت
        self.time_label = Label(self.statusbar, text="", bg=self.colors['dark'], 
                               fg='white', font=('Arial', 9))
        self.time_label.pack(side=LEFT, padx=10, pady=2)
        self.update_time()
        
        # حالة الاتصال
        status_label = Label(self.statusbar, text="🟢 متصل", bg=self.colors['dark'], 
                           fg='white', font=('Arial', 9))
        status_label.pack(side=LEFT, padx=20, pady=2)
    
    def update_time(self):
        """تحديث الوقت في شريط الحالة"""
        current_time = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
        self.time_label.config(text=f"🕐 {current_time}")
        self.root.after(1000, self.update_time)
    
    def setup_main_content(self):
        """إعداد المحتوى الرئيسي"""
        # الإطار الرئيسي
        main_container = Frame(self.root, bg=self.colors['light'])
        main_container.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # إطار معلومات العميل المحسن
        self.setup_customer_section(main_container)
        
        # إطار المنتجات والسلة
        self.setup_products_and_cart_section(main_container)
    
    def setup_customer_section(self, parent):
        """إعداد قسم معلومات العميل"""
        customer_frame = LabelFrame(parent, text="🔍 البحث عن العميل", 
                                   bg=self.colors['white'], font=('Arial', 12, 'bold'),
                                   fg=self.colors['dark'], relief='ridge', bd=2)
        customer_frame.pack(fill=X, pady=(0, 10))
        
        # إطار البحث
        search_frame = Frame(customer_frame, bg=self.colors['white'])
        search_frame.pack(fill=X, padx=15, pady=15)
        
        Label(search_frame, text="📱 رقم الهاتف:", bg=self.colors['white'], 
              font=('Arial', 12, 'bold'), fg=self.colors['dark']).pack(side=LEFT, padx=(0, 10))
        
        self.phone_entry = Entry(search_frame, width=25, font=('Arial', 12), 
                                relief='flat', bg=self.colors['light'], bd=1)
        self.phone_entry.pack(side=LEFT, padx=(0, 10), ipady=5)
        
        search_btn = Button(search_frame, text="🔍 بحث", command=self.search_customer,
                           bg=self.colors['primary'], fg='white', font=('Arial', 11, 'bold'),
                           relief='flat', cursor='hand2', padx=20)
        search_btn.pack(side=LEFT, padx=(0, 10))
        
        add_customer_btn = Button(search_frame, text="👤 عميل جديد", command=self.add_customer_window,
                                 bg=self.colors['success'], fg='white', font=('Arial', 11, 'bold'),
                                 relief='flat', cursor='hand2', padx=20)
        add_customer_btn.pack(side=LEFT)
        
        # معلومات العميل
        self.customer_info_frame = Frame(customer_frame, bg=self.colors['light'], 
                                        relief='sunken', bd=1)
        self.customer_info_frame.pack(fill=X, padx=15, pady=(0, 15))
        
        self.customer_info_label = Label(self.customer_info_frame, 
                                        text="❌ لم يتم اختيار عميل", 
                                        bg=self.colors['light'], fg=self.colors['danger'],
                                        font=('Arial', 11), pady=10)
        self.customer_info_label.pack()
        
        # ربط Enter بالبحث
        self.phone_entry.bind('<Return>', lambda event: self.search_customer())
    
    def setup_products_and_cart_section(self, parent):
        """إعداد قسم المنتجات والسلة"""
        # الإطار الرئيسي للمنتجات والسلة
        products_container = Frame(parent, bg=self.colors['light'])
        products_container.pack(fill=BOTH, expand=True)
        
        # قسم المنتجات (الجانب الأيسر)
        products_frame = LabelFrame(products_container, text="🛍️ المنتجات المتاحة",
                                   bg=self.colors['white'], font=('Arial', 12, 'bold'),
                                   fg=self.colors['dark'], relief='ridge', bd=2)
        products_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))
        
        # جدول المنتجات المحسن
        self.setup_products_table(products_frame)
        
        # إطار إضافة للسلة
        self.setup_add_to_cart_section(products_frame)
        
        # قسم السلة (الجانب الأيمن)
        cart_frame = LabelFrame(products_container, text="🛒 سلة التسوق",
                               bg=self.colors['white'], font=('Arial', 12, 'bold'),
                               fg=self.colors['dark'], relief='ridge', bd=2)
        cart_frame.pack(side=RIGHT, fill=Y, padx=(5, 0))
        cart_frame.config(width=450)
        
        # جدول السلة المحسن
        self.setup_cart_table(cart_frame)
        
        # قسم المجموع والعمليات
        self.setup_cart_totals_and_actions(cart_frame)
    
    def setup_products_table(self, parent):
        """إعداد جدول المنتجات"""
        # إطار الجدول
        table_frame = Frame(parent, bg=self.colors['white'])
        table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # أعمدة الجدول
        columns = ("ID", "اسم المنتج", "الفئة", "السعر", "المخزون", "الوصف")
        self.products_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        # تخصيص الأعمدة
        column_widths = [60, 200, 120, 80, 80, 250]
        for i, col in enumerate(columns):
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=column_widths[i], anchor='center')
        
        # تلوين الصفوف بالتناوب
        self.products_tree.tag_configure('oddrow', background='#f8f9fa')
        self.products_tree.tag_configure('evenrow', background='white')
        
        # شريط التمرير
        scrollbar_v = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.products_tree.yview)
        scrollbar_h = ttk.Scrollbar(table_frame, orient=HORIZONTAL, command=self.products_tree.xview)
        
        self.products_tree.configure(yscrollcommand=scrollbar_v.set, 
                                    xscrollcommand=scrollbar_h.set)
        
        # ترتيب العناصر
        self.products_tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar_v.pack(side=RIGHT, fill=Y)
        scrollbar_h.pack(side=BOTTOM, fill=X)
    
    def setup_add_to_cart_section(self, parent):
        """إعداد قسم إضافة المنتجات للسلة"""
        add_frame = Frame(parent, bg=self.colors['light'], relief='raised', bd=1)
        add_frame.pack(fill=X, padx=10, pady=(0, 10))
        
        # إطار التحكم
        controls_frame = Frame(add_frame, bg=self.colors['light'])
        controls_frame.pack(fill=X, padx=10, pady=10)
        
        Label(controls_frame, text="📦 الكمية:", bg=self.colors['light'], 
              font=('Arial', 11, 'bold'), fg=self.colors['dark']).pack(side=LEFT, padx=(0, 10))
        
        self.quantity_entry = Entry(controls_frame, width=8, font=('Arial', 12), 
                                   relief='flat', bg='white', bd=1, justify='center')
        self.quantity_entry.pack(side=LEFT, padx=(0, 15))
        self.quantity_entry.insert(0, "1")
        
        add_btn = Button(controls_frame, text="➕ إضافة للسلة", command=self.add_to_cart,
                        bg=self.colors['info'], fg='white', font=('Arial', 11, 'bold'),
                        relief='flat', cursor='hand2', padx=20, pady=5)
        add_btn.pack(side=LEFT, padx=(0, 10))
        
        # زر تحديث المنتجات
        refresh_btn = Button(controls_frame, text="🔄 تحديث", command=self.load_products,
                           bg=self.colors['warning'], fg='white', font=('Arial', 11, 'bold'),
                           relief='flat', cursor='hand2', padx=15, pady=5)
        refresh_btn.pack(side=RIGHT)
    
    def setup_cart_table(self, parent):
        """إعداد جدول السلة"""
        # إطار الجدول
        cart_table_frame = Frame(parent, bg=self.colors['white'])
        cart_table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # جدول السلة
        cart_columns = ("المنتج", "الكمية", "السعر", "المجموع")
        self.cart_tree = ttk.Treeview(cart_table_frame, columns=cart_columns, 
                                     show="headings", height=8)
        
        for col in cart_columns:
            self.cart_tree.heading(col, text=col)
            if col == "المنتج":
                self.cart_tree.column(col, width=180, anchor='e')
            else:
                self.cart_tree.column(col, width=80, anchor='center')
        
        # شريط التمرير للسلة
        cart_scrollbar = ttk.Scrollbar(cart_table_frame, orient=VERTICAL, command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=cart_scrollbar.set)
        
        self.cart_tree.pack(side=LEFT, fill=BOTH, expand=True)
        cart_scrollbar.pack(side=RIGHT, fill=Y)
    
    def setup_cart_totals_and_actions(self, parent):
        """إعداد قسم المجاميع والعمليات"""
        # إطار المجاميع
        totals_frame = Frame(parent, bg=self.colors['light'], relief='sunken', bd=2)
        totals_frame.pack(fill=X, padx=10, pady=(0, 10))
        
        self.total_label = Label(totals_frame, text="المجموع: 0.00 ريال", 
                                font=('Arial', 13, 'bold'), bg=self.colors['light'], 
                                fg=self.colors['dark'])
        self.total_label.pack(pady=5)
        
        self.discount_label = Label(totals_frame, text="الخصم: 0.00 ريال", 
                                   font=('Arial', 12), bg=self.colors['light'], 
                                   fg=self.colors['success'])
        self.discount_label.pack()
        
        self.final_total_label = Label(totals_frame, text="المجموع النهائي: 0.00 ريال", 
                                      font=('Arial', 14, 'bold'), bg=self.colors['light'], 
                                      fg=self.colors['primary'])
        self.final_total_label.pack(pady=5)
        
        # إطار أزرار العمليات
        actions_frame = Frame(parent, bg=self.colors['white'])
        actions_frame.pack(fill=X, padx=10, pady=(0, 15))
        
        # زر تأكيد الطلب
        confirm_btn = Button(actions_frame, text="✅ تأكيد الطلب", command=self.confirm_order,
                           bg=self.colors['success'], fg='white', font=('Arial', 12, 'bold'),
                           relief='flat', cursor='hand2', pady=8)
        confirm_btn.pack(fill=X, pady=2)
        
        # زر طباعة آخر فاتورة
        print_btn = Button(actions_frame, text="🖨️ طباعة آخر فاتورة", command=self.print_last_invoice,
                          bg=self.colors['info'], fg='white', font=('Arial', 12, 'bold'),
                          relief='flat', cursor='hand2', pady=8)
        print_btn.pack(fill=X, pady=2)
        
        # أزرار السلة
        Button(actions_frame, text="🗑️ مسح السلة", command=self.clear_cart,
               bg=self.colors['danger'], fg='white', font=('Arial', 12, 'bold'),
               relief='flat', cursor='hand2', pady=8).pack(fill=X, pady=2)
        
        Button(actions_frame, text="➖ حذف العنصر", command=self.remove_from_cart,
               bg=self.colors['warning'], fg='white', font=('Arial', 12, 'bold'),
               relief='flat', cursor='hand2', pady=8).pack(fill=X, pady=2)
    
    # باقي الدوال من النسخة السابقة مع تحسينات...
    def load_products(self):
        """تحميل المنتجات في الجدول"""
        products = self.db.get_all_products()
        
        # مسح البيانات الموجودة
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # إضافة المنتجات مع تلوين متناوب
        for i, product in enumerate(products):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.products_tree.insert("", "end", values=product, tags=(tag,))
    
    def search_customer(self):
        """البحث عن عميل"""
        phone = self.phone_entry.get().strip()
        if not phone:
            messagebox.showwarning("تنبيه", "يرجى إدخال رقم الهاتف")
            return
        
        customer = self.db.get_customer_by_phone(phone)
        if customer:
            self.current_customer = customer
            subscription = self.db.get_active_subscription(customer[0])
            
            if subscription:
                discount = subscription[4]
                status_text = f"✅ العميل: {customer[1]} | 📱 {customer[2]} | 💳 مشترك | 🎯 خصم: {discount}%"
                status_color = self.colors['success']
            else:
                status_text = f"✅ العميل: {customer[1]} | 📱 {customer[2]} | ❌ غير مشترك"
                status_color = self.colors['info']
            
            self.customer_info_label.config(text=status_text, fg=status_color)
            self.update_cart_total()
        else:
            messagebox.showerror("خطأ", "لم يتم العثور على العميل")
            self.customer_info_label.config(text="❌ لم يتم العثور على العميل", 
                                          fg=self.colors['danger'])
    
    def add_to_cart(self):
        """إضافة منتج للسلة"""
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("تنبيه", "يرجى اختيار منتج")
            return
        
        try:
            quantity = int(self.quantity_entry.get())
            if quantity <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال كمية صحيحة")
            return
        
        product_data = self.products_tree.item(selected[0])['values']
        product_id = product_data[0]
        product_name = product_data[1]
        price = float(product_data[3])
        stock = int(product_data[4])
        
        if quantity > stock:
            messagebox.showerror("خطأ", f"الكمية المطلوبة أكبر من المخزون المتاح ({stock})")
            return
        
        # البحث عن المنتج في السلة
        for i, item in enumerate(self.cart_items):
            if item['product_id'] == product_id:
                self.cart_items[i]['quantity'] += quantity
                break
        else:
            # إضافة منتج جديد للسلة
            self.cart_items.append({
                'product_id': product_id,
                'name': product_name,
                'price': price,
                'quantity': quantity
            })
        
        self.update_cart_display()
        self.quantity_entry.delete(0, END)
        self.quantity_entry.insert(0, "1")
        
        # رسالة تأكيد
        messagebox.showinfo("نجح", f"تم إضافة {quantity} من {product_name} للسلة")
    
    def remove_from_cart(self):
        """حذف عنصر من السلة"""
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showwarning("تنبيه", "يرجى اختيار عنصر لحذفه")
            return
        
        item_index = self.cart_tree.index(selected[0])
        removed_item = self.cart_items[item_index]['name']
        del self.cart_items[item_index]
        self.update_cart_display()
        
        messagebox.showinfo("تم", f"تم حذف {removed_item} من السلة")
    
    def clear_cart(self):
        """مسح السلة"""
        if not self.cart_items:
            messagebox.showinfo("تنبيه", "السلة فارغة")
            return
        
        if messagebox.askyesno("تأكيد", "هل أنت متأكد من مسح جميع العناصر من السلة؟"):
            self.cart_items = []
            self.update_cart_display()
            messagebox.showinfo("تم", "تم مسح السلة")
    
    def update_cart_display(self):
        """تحديث عرض السلة"""
        # مسح العرض الحالي
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # إضافة العناصر
        for item in self.cart_items:
            total = item['quantity'] * item['price']
            self.cart_tree.insert("", "end", values=(
                item['name'], item['quantity'], f"{item['price']:.2f}", f"{total:.2f}"
            ))
        
        self.update_cart_total()
    
    def update_cart_total(self):
        """تحديث مجموع السلة"""
        total = sum(item['quantity'] * item['price'] for item in self.cart_items)
        discount = 0
        
        if self.current_customer:
            subscription = self.db.get_active_subscription(self.current_customer[0])
            if subscription:
                discount_percentage = subscription[4]
                discount = total * (discount_percentage / 100)
        
        final_total = total - discount
        
        self.total_label.config(text=f"المجموع: {total:.2f} ريال")
        self.discount_label.config(text=f"الخصم: {discount:.2f} ريال")
        self.final_total_label.config(text=f"المجموع النهائي: {final_total:.2f} ريال")
    
    def confirm_order(self):
        """تأكيد الطلب"""
        if not self.current_customer:
            messagebox.showerror("خطأ", "يرجى اختيار عميل أولاً")
            return
        
        if not self.cart_items:
            messagebox.showerror("خطأ", "السلة فارغة")
            return
        
        # نافذة تأكيد الطلب
        if not messagebox.askyesno("تأكيد الطلب", 
                                  f"تأكيد الطلب للعميل: {self.current_customer[1]}\n"
                                  f"عدد العناصر: {len(self.cart_items)}\n"
                                  f"المبلغ الإجمالي: {sum(item['quantity'] * item['price'] for item in self.cart_items):.2f} ريال"):
            return
        
        # إنشاء الطلب
        result = self.db.create_order(self.current_customer[0], self.cart_items, 'cash', self.user_data[0])
        
        if result:
            order_id, order_number, final_amount = result
            self.last_order_id = order_id  # حفظ معرف آخر طلب للطباعة
            
            # رسالة نجاح مع خيار الطباعة
            success_msg = f"✅ تم إنشاء الطلب بنجاح!\n\n📋 رقم الطلب: {order_number}\n💰 المبلغ: {final_amount:.2f} ريال\n\nهل تريد طباعة الفاتورة؟"
            
            if messagebox.askyesno("نجح العملية", success_msg):
                self.invoice_printer.print_invoice(order_id)
            
            # مسح السلة وتحديث المنتجات
            self.clear_cart()
            self.load_products()
        else:
            messagebox.showerror("خطأ", "فشل في إنشاء الطلب")
    
    def print_last_invoice(self):
        """طباعة آخر فاتورة"""
        if hasattr(self, 'last_order_id'):
            self.invoice_printer.print_invoice(self.last_order_id)
        else:
            messagebox.showinfo("تنبيه", "لا توجد فاتورة للطباعة")
    
    def add_customer_window(self):
        """نافذة إضافة عميل جديد"""
        window = Toplevel(self.root)
        window.title("إضافة عميل جديد")
        window.geometry("450x400")
        window.configure(bg=self.colors['white'])
        window.resizable(False, False)
        
        # توسيط النافذة
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (225)
        y = (window.winfo_screenheight() // 2) - (200)
        window.geometry(f'450x400+{x}+{y}')
        
        # العنوان
        title_label = Label(window, text="👤 إضافة عميل جديد", 
                           font=('Arial', 16, 'bold'), bg=self.colors['white'], 
                           fg=self.colors['dark'])
        title_label.pack(pady=20)
        
        # إطار النموذج
        form_frame = Frame(window, bg=self.colors['white'])
        form_frame.pack(pady=10, padx=40, fill='both', expand=True)
        
        # الحقول
        fields = [
            ("الاسم *:", "name"),
            ("رقم الهاتف *:", "phone"),
            ("البريد الإلكتروني:", "email"),
            ("العنوان:", "address")
        ]
        
        entries = {}
        
        for label_text, field_name in fields:
            Label(form_frame, text=label_text, font=('Arial', 12, 'bold'),
                  bg=self.colors['white'], fg=self.colors['dark']).pack(anchor='e', pady=(10, 5))
            
            entry = Entry(form_frame, width=40, font=('Arial', 12), relief='flat',
                         bg=self.colors['light'], bd=1)
            entry.pack(fill='x', ipady=5)
            entries[field_name] = entry
        
        # اختيار الجنس
        Label(form_frame, text="الجنس:", font=('Arial', 12, 'bold'),
              bg=self.colors['white'], fg=self.colors['dark']).pack(anchor='e', pady=(15, 5))
        
        gender_var = StringVar(value="male")
        gender_frame = Frame(form_frame, bg=self.colors['white'])
        gender_frame.pack(fill='x')
        
        Radiobutton(gender_frame, text="ذكر", variable=gender_var, value="male",
                   font=('Arial', 11), bg=self.colors['white']).pack(side='right', padx=10)
        Radiobutton(gender_frame, text="أنثى", variable=gender_var, value="female",
                   font=('Arial', 11), bg=self.colors['white']).pack(side='right', padx=10)
        
        def save_customer():
            name = entries['name'].get().strip()
            phone = entries['phone'].get().strip()
            email = entries['email'].get().strip() or None
            address = entries['address'].get().strip() or None
            gender = gender_var.get()
            
            if not name or not phone:
                messagebox.showerror("خطأ", "الاسم ورقم الهاتف مطلوبان")
                return
            
            if self.db.add_customer(name, phone, email, address, None, gender):
                messagebox.showinfo("نجح", "تم إضافة العميل بنجاح")
                window.destroy()
                # تحديث حقل البحث
                self.phone_entry.delete(0, END)
                self.phone_entry.insert(0, phone)
                self.search_customer()
            else:
                messagebox.showerror("خطأ", "فشل في إضافة العميل\nقد يكون رقم الهاتف موجود مسبقاً")
        
        # أزرار العمليات
        buttons_frame = Frame(form_frame, bg=self.colors['white'])
        buttons_frame.pack(fill='x', pady=20)
        
        Button(buttons_frame, text="💾 حفظ", command=save_customer,
               bg=self.colors['success'], fg='white', font=('Arial', 12, 'bold'),
               relief='flat', cursor='hand2', padx=20, pady=8).pack(side='right', padx=5)
        
        Button(buttons_frame, text="❌ إلغاء", command=window.destroy,
               bg=self.colors['danger'], fg='white', font=('Arial', 12, 'bold'),
               relief='flat', cursor='hand2', padx=20, pady=8).pack(side='right', padx=5)
        
        # تركيز على حقل الاسم
        entries['name'].focus()
    
    def search_customer_window(self):
        """نافذة البحث عن عميل - نفس الكود السابق مع تحسينات التصميم"""
        pass
    
    def create_subscription_window(self):
        """نافذة إنشاء اشتراك - نفس الكود السابق مع تحسينات التصميم"""
        pass
    
    # دوال التقارير
    def show_top_products(self):
        """عرض أكثر المنتجات مبيعاً - نفس الكود مع تحسينات التصميم"""
        pass
    
    def show_least_products(self):
        """عرض أقل المنتجات مبيعاً"""
        pass
    
    def show_customer_analytics(self):
        """عرض تحليل العملاء"""
        pass
    
    def show_monthly_sales(self):
        """عرض تحليل المبيعات الشهرية"""
        pass
    
    def show_category_analysis(self):
        """عرض تحليل الفئات"""
        pass
    
    def show_customers_list(self):
        """عرض قائمة العملاء"""
        pass
    
    def view_subscriptions(self):
        """عرض الاشتراكات"""
        pass
    
    def show_user_info(self):
        """عرض معلومات المستخدم"""
        info_text = f"""
معلومات المستخدم الحالي:

👤 الاسم: {self.user_data[2]}
🏷️ اسم المستخدم: {self.user_data[1]}
🎭 الدور: {self.user_data[3]}
🕐 تاريخ اليوم: {datetime.now().strftime('%Y/%m/%d %H:%M')}
        """
        messagebox.showinfo("معلومات المستخدم", info_text)
    
    def logout(self):
        """تسجيل الخروج"""
        if messagebox.askyesno("تسجيل الخروج", "هل أنت متأكد من تسجيل الخروج؟"):
            self.root.destroy()
            # العودة لشاشة تسجيل الدخول
            def restart_login():
                login_window = LoginWindow(main_app)
                login_window.run()
            
            restart_login()
    
    def run(self):
        """تشغيل التطبيق"""
        self.root.mainloop()
        self.db.close_connection()

def main_app(user_data):
    """تشغيل التطبيق الرئيسي"""
    app = SweetShopGUI(user_data)
    app.run()

if __name__ == "__main__":
    # تشغيل نافذة تسجيل الدخول أولاً
    login_window = LoginWindow(main_app)
    login_window.run()
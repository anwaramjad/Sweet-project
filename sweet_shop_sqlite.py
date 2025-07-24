import sqlite3
from datetime import datetime, timedelta, date
import json
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import *
from tkinter import ttk, messagebox
import random
import os

class SweetShopDatabase:
    def __init__(self):
        self.db_file = "sweet_shop.db"
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
            messagebox.showerror("خطأ", f"فشل في الاتصال بقاعدة البيانات: {err}")
    
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
        
        # جدول فئات المنتجات
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # جدول المنتجات
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
        
        # جدول العملاء
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
        
        # جدول أنواع الاشتراكات
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
        
        # جدول اشتراكات العملاء
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
        
        # جدول الطلبات
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
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
        """)
        
        # جدول تفاصيل الطلبات
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
        
        # جدول المدفوعات
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
        
        # جدول تقييمات المنتجات
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS product_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            rating INTEGER CHECK (rating >= 1 AND rating <= 5),
            review_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
        """)
        
        # جدول تتبع المخزون
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
            return  # البيانات موجودة مسبقاً
        
        # إدراج فئات المنتجات
        categories = [
            ('حلويات باردة', 'حلويات تقدم باردة مثل الكيك والتيراميسو'),
            ('حلويات ساخنة', 'حلويات تقدم ساخنة مثل الكنافة والسوفليه'),
            ('مشروبات باردة', 'عصائر طبيعية ومشروبات منعشة'),
            ('مشروبات ساخنة', 'قهوة وشاي ومشروبات ساخنة أخرى'),
            ('حلويات شرقية', 'بقلاوة وكنافة وحلويات تراثية')
        ]
        
        for name, desc in categories:
            self.execute_query("INSERT INTO categories (name, description) VALUES (?, ?)", (name, desc))
        
        # إدراج المنتجات
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
    
    # ===== إدارة العملاء =====
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
    
    def update_customer_loyalty_points(self, customer_id, points):
        """تحديث نقاط الولاء للعميل"""
        query = "UPDATE customers SET loyalty_points = loyalty_points + ? WHERE id = ?"
        return self.execute_query(query, (points, customer_id))
    
    # ===== إدارة المنتجات =====
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
    
    def update_product_stock(self, product_id, quantity_change, transaction_type):
        """تحديث مخزون المنتج"""
        # جلب الكمية الحالية
        query = "SELECT stock_quantity FROM products WHERE id = ?"
        result = self.execute_query(query, (product_id,), fetch=True)
        if not result:
            return False
        
        current_quantity = result[0][0]
        new_quantity = current_quantity + quantity_change
        
        # تحديث المخزون
        update_query = "UPDATE products SET stock_quantity = ? WHERE id = ?"
        if self.execute_query(update_query, (new_quantity, product_id)):
            # تسجيل الحركة في جدول المخزون
            inventory_query = """
            INSERT INTO inventory_transactions 
            (product_id, transaction_type, quantity_change, quantity_after)
            VALUES (?, ?, ?, ?)
            """
            return self.execute_query(inventory_query, 
                                    (product_id, transaction_type, quantity_change, new_quantity))
        return False
    
    # ===== إدارة الطلبات =====
    def create_order(self, customer_id, items, payment_method='cash'):
        """إنشاء طلب جديد"""
        try:
            # إنشاء رقم الطلب
            order_number = f"ORD{random.randint(10000, 99999)}"
            
            # حساب إجمالي الطلب
            total_amount = sum(item['quantity'] * item['price'] for item in items)
            
            # التحقق من الاشتراك للحصول على خصم
            discount_amount = 0
            subscription = self.get_active_subscription(customer_id)
            if subscription:
                discount_percentage = subscription[4]  # discount_percentage from subscription_types join
                discount_amount = total_amount * (discount_percentage / 100)
            
            final_amount = total_amount - discount_amount
            
            # إنشاء الطلب
            order_query = """
            INSERT INTO orders (customer_id, order_number, total_amount, discount_amount, 
                              final_amount, payment_method)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            order_params = (customer_id, order_number, total_amount, discount_amount, 
                           final_amount, payment_method)
            
            if self.execute_query(order_query, order_params):
                # جلب معرف الطلب
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
                        # تحديث المخزون
                        self.update_product_stock(item['product_id'], -item['quantity'], 'sale')
                
                # إضافة نقاط الولاء (نقطة واحدة لكل ريال)
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
    
    # ===== إدارة الاشتراكات =====
    def get_subscription_types(self):
        """جلب أنواع الاشتراكات"""
        query = "SELECT * FROM subscription_types WHERE is_active = 1"
        return self.execute_query(query, fetch=True)
    
    def create_subscription(self, customer_id, subscription_type_id):
        """إنشاء اشتراك جديد"""
        # جلب تفاصيل نوع الاشتراك
        query = "SELECT duration_days, price FROM subscription_types WHERE id = ?"
        result = self.execute_query(query, (subscription_type_id,), fetch=True)
        
        if result:
            duration_days, price = result[0]
            start_date = date.today()
            end_date = start_date + timedelta(days=duration_days)
            
            subscription_query = """
            INSERT INTO customer_subscriptions 
            (customer_id, subscription_type_id, start_date, end_date, payment_amount)
            VALUES (?, ?, ?, ?, ?)
            """
            params = (customer_id, subscription_type_id, start_date, end_date, price)
            
            if self.execute_query(subscription_query, params):
                # تسجيل دفع الاشتراك
                subscription_id_query = "SELECT last_insert_rowid()"
                subscription_id_result = self.execute_query(subscription_id_query, fetch=True)
                subscription_id = subscription_id_result[0][0]
                
                payment_query = """
                INSERT INTO payments (subscription_id, amount, payment_method)
                VALUES (?, ?, 'cash')
                """
                self.execute_query(payment_query, (subscription_id, price))
                
                return subscription_id
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
    
    # ===== التحليلات والتقارير =====
    def get_top_selling_products(self, limit=10):
        """جلب أكثر المنتجات مبيعاً"""
        query = f"""
        SELECT 
            p.id,
            p.name,
            c.name as category_name,
            COUNT(oi.id) as total_orders,
            SUM(oi.quantity) as total_quantity_sold,
            SUM(oi.total_price) as total_revenue,
            AVG(COALESCE(pr.rating, 0)) as average_rating
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN order_items oi ON p.id = oi.product_id
        LEFT JOIN orders o ON oi.order_id = o.id
        LEFT JOIN product_reviews pr ON p.id = pr.product_id
        WHERE o.status != 'cancelled' OR o.status IS NULL
        GROUP BY p.id, p.name, c.name
        ORDER BY total_quantity_sold DESC
        LIMIT {limit}
        """
        return self.execute_query(query, fetch=True)
    
    def get_least_selling_products(self, limit=10):
        """جلب أقل المنتجات مبيعاً"""
        query = f"""
        SELECT 
            p.id,
            p.name,
            c.name as category_name,
            COALESCE(COUNT(oi.id), 0) as total_orders,
            COALESCE(SUM(oi.quantity), 0) as total_quantity_sold,
            COALESCE(SUM(oi.total_price), 0) as total_revenue
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN order_items oi ON p.id = oi.product_id
        LEFT JOIN orders o ON oi.order_id = o.id AND o.status != 'cancelled'
        GROUP BY p.id, p.name, c.name
        ORDER BY total_quantity_sold ASC, p.id ASC
        LIMIT {limit}
        """
        return self.execute_query(query, fetch=True)
    
    def get_customer_analytics(self):
        """جلب تحليلات العملاء"""
        query = """
        SELECT 
            c.id,
            c.name,
            c.phone,
            c.registration_date,
            COUNT(o.id) as total_orders,
            COALESCE(SUM(o.final_amount), 0) as total_spent,
            COALESCE(AVG(o.final_amount), 0) as average_order_value,
            c.loyalty_points,
            CASE 
                WHEN COUNT(cs.id) > 0 THEN 'مشترك'
                ELSE 'غير مشترك'
            END as subscription_status,
            MAX(o.order_date) as last_order_date
        FROM customers c
        LEFT JOIN orders o ON c.id = o.customer_id AND o.status != 'cancelled'
        LEFT JOIN customer_subscriptions cs ON c.id = cs.customer_id AND cs.status = 'active'
        GROUP BY c.id, c.name, c.phone, c.registration_date, c.loyalty_points
        ORDER BY total_spent DESC
        """
        return self.execute_query(query, fetch=True)
    
    def get_monthly_sales_analysis(self, year=None):
        """جلب تحليل المبيعات الشهرية"""
        if year:
            query = f"""
            SELECT 
                strftime('%Y', o.order_date) as year,
                strftime('%m', o.order_date) as month,
                strftime('%Y-%m', o.order_date) as month_name,
                COUNT(o.id) as total_orders,
                SUM(o.final_amount) as total_revenue,
                AVG(o.final_amount) as average_order_value,
                COUNT(DISTINCT o.customer_id) as unique_customers
            FROM orders o
            WHERE o.status != 'cancelled' AND strftime('%Y', o.order_date) = '{year}'
            GROUP BY strftime('%Y', o.order_date), strftime('%m', o.order_date)
            ORDER BY year DESC, month DESC
            """
        else:
            query = """
            SELECT 
                strftime('%Y', o.order_date) as year,
                strftime('%m', o.order_date) as month,
                strftime('%Y-%m', o.order_date) as month_name,
                COUNT(o.id) as total_orders,
                SUM(o.final_amount) as total_revenue,
                AVG(o.final_amount) as average_order_value,
                COUNT(DISTINCT o.customer_id) as unique_customers
            FROM orders o
            WHERE o.status != 'cancelled'
            GROUP BY strftime('%Y', o.order_date), strftime('%m', o.order_date)
            ORDER BY year DESC, month DESC
            """
        return self.execute_query(query, fetch=True)
    
    def get_category_analysis(self):
        """جلب تحليل الفئات"""
        query = """
        SELECT 
            c.id,
            c.name as category_name,
            COUNT(DISTINCT p.id) as total_products,
            COUNT(oi.id) as total_orders,
            SUM(oi.quantity) as total_quantity_sold,
            SUM(oi.total_price) as total_revenue,
            AVG(oi.unit_price) as average_price
        FROM categories c
        LEFT JOIN products p ON c.id = p.category_id
        LEFT JOIN order_items oi ON p.id = oi.product_id
        LEFT JOIN orders o ON oi.order_id = o.id AND o.status != 'cancelled'
        GROUP BY c.id, c.name
        ORDER BY total_revenue DESC
        """
        return self.execute_query(query, fetch=True)
    
    def close_connection(self):
        """إغلاق الاتصال بقاعدة البيانات"""
        if self.connection:
            self.connection.close()

class SweetShopGUI:
    def __init__(self):
        self.db = SweetShopDatabase()
        self.root = Tk()
        self.root.title("نظام إدارة محل الحلويات")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f0f0')
        
        # متغيرات
        self.current_customer = None
        self.cart_items = []
        
        self.setup_gui()
    
    def setup_gui(self):
        """إعداد واجهة المستخدم"""
        # شريط القوائم
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # قائمة العملاء
        customer_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="العملاء", menu=customer_menu)
        customer_menu.add_command(label="إضافة عميل جديد", command=self.add_customer_window)
        customer_menu.add_command(label="البحث عن عميل", command=self.search_customer_window)
        
        # قائمة الاشتراكات
        subscription_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="الاشتراكات", menu=subscription_menu)
        subscription_menu.add_command(label="إنشاء اشتراك", command=self.create_subscription_window)
        subscription_menu.add_command(label="عرض الاشتراكات", command=self.view_subscriptions)
        
        # قائمة التقارير
        reports_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="التقارير", menu=reports_menu)
        reports_menu.add_command(label="أكثر المنتجات مبيعاً", command=self.show_top_products)
        reports_menu.add_command(label="أقل المنتجات مبيعاً", command=self.show_least_products)
        reports_menu.add_command(label="تحليل العملاء", command=self.show_customer_analytics)
        reports_menu.add_command(label="تحليل المبيعات الشهرية", command=self.show_monthly_sales)
        reports_menu.add_command(label="تحليل الفئات", command=self.show_category_analysis)
        
        # الإطار الرئيسي
        main_frame = Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # إطار معلومات العميل
        customer_frame = LabelFrame(main_frame, text="معلومات العميل", bg='#e0e0e0', font=('Arial', 12, 'bold'))
        customer_frame.pack(fill=X, pady=5)
        
        Label(customer_frame, text="رقم الهاتف:", bg='#e0e0e0').grid(row=0, column=0, padx=5, pady=5)
        self.phone_entry = Entry(customer_frame, width=20)
        self.phone_entry.grid(row=0, column=1, padx=5, pady=5)
        
        Button(customer_frame, text="بحث", command=self.search_customer, bg='#4CAF50', fg='white').grid(row=0, column=2, padx=5, pady=5)
        
        self.customer_info_label = Label(customer_frame, text="لم يتم اختيار عميل", bg='#e0e0e0', fg='red')
        self.customer_info_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        
        # إطار المنتجات والسلة
        products_frame = Frame(main_frame)
        products_frame.pack(fill=BOTH, expand=True, pady=5)
        
        # إطار المنتجات
        products_list_frame = LabelFrame(products_frame, text="المنتجات", font=('Arial', 12, 'bold'))
        products_list_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))
        
        # جدول المنتجات
        columns = ("ID", "اسم المنتج", "الفئة", "السعر", "المخزون")
        self.products_tree = ttk.Treeview(products_list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=100)
        
        scrollbar_products = ttk.Scrollbar(products_list_frame, orient=VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=scrollbar_products.set)
        
        self.products_tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar_products.pack(side=RIGHT, fill=Y)
        
        # إطار إضافة للسلة
        add_frame = Frame(products_list_frame)
        add_frame.pack(fill=X, pady=5)
        
        Label(add_frame, text="الكمية:").pack(side=LEFT, padx=5)
        self.quantity_entry = Entry(add_frame, width=10)
        self.quantity_entry.pack(side=LEFT, padx=5)
        self.quantity_entry.insert(0, "1")
        
        Button(add_frame, text="إضافة للسلة", command=self.add_to_cart, bg='#2196F3', fg='white').pack(side=LEFT, padx=5)
        
        # إطار السلة
        cart_frame = LabelFrame(products_frame, text="السلة", font=('Arial', 12, 'bold'))
        cart_frame.pack(side=RIGHT, fill=Y, padx=(5, 0))
        cart_frame.config(width=400)
        
        # جدول السلة
        cart_columns = ("المنتج", "الكمية", "السعر", "المجموع")
        self.cart_tree = ttk.Treeview(cart_frame, columns=cart_columns, show="headings", height=10)
        
        for col in cart_columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=80)
        
        self.cart_tree.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        # إطار المجموع والدفع
        total_frame = Frame(cart_frame)
        total_frame.pack(fill=X, padx=5, pady=5)
        
        self.total_label = Label(total_frame, text="المجموع: 0.00 ريال", font=('Arial', 14, 'bold'))
        self.total_label.pack()
        
        self.discount_label = Label(total_frame, text="الخصم: 0.00 ريال", font=('Arial', 12), fg='green')
        self.discount_label.pack()
        
        self.final_total_label = Label(total_frame, text="المجموع النهائي: 0.00 ريال", font=('Arial', 14, 'bold'), fg='blue')
        self.final_total_label.pack()
        
        # أزرار العمليات
        buttons_frame = Frame(cart_frame)
        buttons_frame.pack(fill=X, padx=5, pady=5)
        
        Button(buttons_frame, text="تأكيد الطلب", command=self.confirm_order, bg='#4CAF50', fg='white', font=('Arial', 12)).pack(fill=X, pady=2)
        Button(buttons_frame, text="مسح السلة", command=self.clear_cart, bg='#f44336', fg='white', font=('Arial', 12)).pack(fill=X, pady=2)
        Button(buttons_frame, text="حذف العنصر", command=self.remove_from_cart, bg='#FF9800', fg='white', font=('Arial', 12)).pack(fill=X, pady=2)
        
        # تحميل المنتجات
        self.load_products()
    
    def load_products(self):
        """تحميل المنتجات في الجدول"""
        products = self.db.get_all_products()
        
        # مسح البيانات الموجودة
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # إضافة المنتجات
        for product in products:
            self.products_tree.insert("", "end", values=product)
    
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
            subscription_status = "مشترك" if subscription else "غير مشترك"
            
            info_text = f"العميل: {customer[1]} | الهاتف: {customer[2]} | الحالة: {subscription_status}"
            if subscription:
                discount = subscription[4]
                info_text += f" | خصم: {discount}%"
            
            self.customer_info_label.config(text=info_text, fg='green')
            self.update_cart_total()
        else:
            messagebox.showerror("خطأ", "لم يتم العثور على العميل")
            self.customer_info_label.config(text="لم يتم العثور على العميل", fg='red')
    
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
    
    def remove_from_cart(self):
        """حذف عنصر من السلة"""
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showwarning("تنبيه", "يرجى اختيار عنصر لحذفه")
            return
        
        item_index = self.cart_tree.index(selected[0])
        del self.cart_items[item_index]
        self.update_cart_display()
    
    def clear_cart(self):
        """مسح السلة"""
        self.cart_items = []
        self.update_cart_display()
    
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
        
        # إنشاء الطلب
        result = self.db.create_order(self.current_customer[0], self.cart_items)
        
        if result:
            order_id, order_number, final_amount = result
            messagebox.showinfo("نجح", f"تم إنشاء الطلب بنجاح\nرقم الطلب: {order_number}\nالمبلغ: {final_amount:.2f} ريال")
            
            # مسح السلة وتحديث المنتجات
            self.clear_cart()
            self.load_products()
        else:
            messagebox.showerror("خطأ", "فشل في إنشاء الطلب")
    
    def add_customer_window(self):
        """نافذة إضافة عميل جديد"""
        window = Toplevel(self.root)
        window.title("إضافة عميل جديد")
        window.geometry("400x300")
        window.configure(bg='#f0f0f0')
        
        # الحقول
        Label(window, text="الاسم:", bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=5, sticky=W)
        name_entry = Entry(window, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        Label(window, text="رقم الهاتف:", bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=5, sticky=W)
        phone_entry = Entry(window, width=30)
        phone_entry.grid(row=1, column=1, padx=10, pady=5)
        
        Label(window, text="البريد الإلكتروني:", bg='#f0f0f0').grid(row=2, column=0, padx=10, pady=5, sticky=W)
        email_entry = Entry(window, width=30)
        email_entry.grid(row=2, column=1, padx=10, pady=5)
        
        Label(window, text="العنوان:", bg='#f0f0f0').grid(row=3, column=0, padx=10, pady=5, sticky=W)
        address_entry = Entry(window, width=30)
        address_entry.grid(row=3, column=1, padx=10, pady=5)
        
        Label(window, text="الجنس:", bg='#f0f0f0').grid(row=4, column=0, padx=10, pady=5, sticky=W)
        gender_var = StringVar()
        gender_combo = ttk.Combobox(window, textvariable=gender_var, values=["male", "female"], state="readonly")
        gender_combo.grid(row=4, column=1, padx=10, pady=5)
        
        def save_customer():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            email = email_entry.get().strip() or None
            address = address_entry.get().strip() or None
            gender = gender_var.get() or None
            
            if not name or not phone:
                messagebox.showerror("خطأ", "الاسم ورقم الهاتف مطلوبان")
                return
            
            if self.db.add_customer(name, phone, email, address, None, gender):
                messagebox.showinfo("نجح", "تم إضافة العميل بنجاح")
                window.destroy()
            else:
                messagebox.showerror("خطأ", "فشل في إضافة العميل")
        
        Button(window, text="حفظ", command=save_customer, bg='#4CAF50', fg='white').grid(row=5, column=0, columnspan=2, pady=20)
    
    def search_customer_window(self):
        """نافذة البحث عن عميل"""
        window = Toplevel(self.root)
        window.title("البحث عن عميل")
        window.geometry("600x400")
        
        # حقل البحث
        search_frame = Frame(window)
        search_frame.pack(fill=X, padx=10, pady=5)
        
        Label(search_frame, text="رقم الهاتف:").pack(side=LEFT, padx=5)
        search_entry = Entry(search_frame, width=20)
        search_entry.pack(side=LEFT, padx=5)
        
        def search():
            phone = search_entry.get().strip()
            if phone:
                customer = self.db.get_customer_by_phone(phone)
                if customer:
                    info = f"الاسم: {customer[1]}\nالهاتف: {customer[2]}\nالبريد: {customer[3] or 'غير محدد'}\nالعنوان: {customer[4] or 'غير محدد'}"
                    messagebox.showinfo("تفاصيل العميل", info)
                else:
                    messagebox.showerror("خطأ", "لم يتم العثور على العميل")
        
        Button(search_frame, text="بحث", command=search, bg='#4CAF50', fg='white').pack(side=LEFT, padx=5)
    
    def create_subscription_window(self):
        """نافذة إنشاء اشتراك"""
        if not self.current_customer:
            messagebox.showerror("خطأ", "يرجى اختيار عميل أولاً")
            return
        
        window = Toplevel(self.root)
        window.title("إنشاء اشتراك")
        window.geometry("500x300")
        
        Label(window, text=f"العميل: {self.current_customer[1]}", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # أنواع الاشتراكات
        subscription_types = self.db.get_subscription_types()
        
        selected_subscription = IntVar()
        
        for subscription in subscription_types:
            text = f"{subscription[1]} - {subscription[3]:.2f} ريال - خصم {subscription[4]}%"
            Radiobutton(window, text=text, variable=selected_subscription, value=subscription[0]).pack(pady=5)
        
        def create_subscription():
            if selected_subscription.get():
                result = self.db.create_subscription(self.current_customer[0], selected_subscription.get())
                if result:
                    messagebox.showinfo("نجح", "تم إنشاء الاشتراك بنجاح")
                    window.destroy()
                    self.search_customer()  # تحديث معلومات العميل
                else:
                    messagebox.showerror("خطأ", "فشل في إنشاء الاشتراك")
            else:
                messagebox.showwarning("تنبيه", "يرجى اختيار نوع الاشتراك")
        
        Button(window, text="إنشاء الاشتراك", command=create_subscription, bg='#4CAF50', fg='white').pack(pady=20)
    
    def show_top_products(self):
        """عرض أكثر المنتجات مبيعاً"""
        products = self.db.get_top_selling_products()
        
        window = Toplevel(self.root)
        window.title("أكثر المنتجات مبيعاً")
        window.geometry("800x400")
        
        columns = ("المنتج", "الفئة", "عدد الطلبات", "إجمالي الكمية", "إجمالي الإيرادات")
        tree = ttk.Treeview(window, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        for product in products:
            tree.insert("", "end", values=(product[1], product[2], product[3], product[4], f"{product[5] or 0:.2f}"))
        
        tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    def show_least_products(self):
        """عرض أقل المنتجات مبيعاً"""
        products = self.db.get_least_selling_products()
        
        window = Toplevel(self.root)
        window.title("أقل المنتجات مبيعاً")
        window.geometry("800x400")
        
        columns = ("المنتج", "الفئة", "عدد الطلبات", "إجمالي الكمية", "إجمالي الإيرادات")
        tree = ttk.Treeview(window, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        for product in products:
            tree.insert("", "end", values=(product[1], product[2], product[3], product[4], f"{product[5] or 0:.2f}"))
        
        tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    def show_customer_analytics(self):
        """عرض تحليل العملاء"""
        customers = self.db.get_customer_analytics()
        
        window = Toplevel(self.root)
        window.title("تحليل العملاء")
        window.geometry("1000x500")
        
        columns = ("العميل", "الهاتف", "عدد الطلبات", "إجمالي المبلغ", "متوسط الطلب", "نقاط الولاء", "حالة الاشتراك")
        tree = ttk.Treeview(window, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        for customer in customers:
            tree.insert("", "end", values=(
                customer[1], customer[2], customer[4], f"{customer[5]:.2f}",
                f"{customer[6]:.2f}", customer[7], customer[8]
            ))
        
        tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    def show_monthly_sales(self):
        """عرض تحليل المبيعات الشهرية"""
        sales = self.db.get_monthly_sales_analysis()
        
        window = Toplevel(self.root)
        window.title("تحليل المبيعات الشهرية")
        window.geometry("800x400")
        
        columns = ("السنة", "الشهر", "عدد الطلبات", "إجمالي الإيرادات", "متوسط الطلب", "عدد العملاء")
        tree = ttk.Treeview(window, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        for sale in sales:
            tree.insert("", "end", values=(
                sale[0], sale[2], sale[3], f"{sale[4]:.2f}", f"{sale[5]:.2f}", sale[6]
            ))
        
        tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    def show_category_analysis(self):
        """عرض تحليل الفئات"""
        categories = self.db.get_category_analysis()
        
        window = Toplevel(self.root)
        window.title("تحليل الفئات")
        window.geometry("800x400")
        
        columns = ("الفئة", "عدد المنتجات", "عدد الطلبات", "إجمالي الكمية", "إجمالي الإيرادات", "متوسط السعر")
        tree = ttk.Treeview(window, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        for category in categories:
            tree.insert("", "end", values=(
                category[1], category[2], category[3] or 0, category[4] or 0,
                f"{category[5] or 0:.2f}", f"{category[6] or 0:.2f}"
            ))
        
        tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    def view_subscriptions(self):
        """عرض الاشتراكات"""
        messagebox.showinfo("قريباً", "هذه الميزة ستكون متاحة قريباً")
    
    def run(self):
        """تشغيل التطبيق"""
        self.root.mainloop()
        self.db.close_connection()

if __name__ == "__main__":
    app = SweetShopGUI()
    app.run()
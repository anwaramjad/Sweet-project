import mysql.connector
from datetime import datetime, timedelta, date
import json
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import *
from tkinter import ttk, messagebox
import random

class SweetShopDatabase:
    def __init__(self):
        self.connection = None
        self.connect_database()
    
    def connect_database(self):
        """الاتصال بقاعدة البيانات"""
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="sweet_shop_db",
                charset='utf8mb4'
            )
            print("تم الاتصال بقاعدة البيانات بنجاح")
        except mysql.connector.Error as err:
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
        except mysql.connector.Error as err:
            print(f"خطأ في تنفيذ الاستعلام: {err}")
            return None
    
    # ===== إدارة العملاء =====
    def add_customer(self, name, phone, email=None, address=None, birth_date=None, gender=None):
        """إضافة عميل جديد"""
        query = """
        INSERT INTO customers (name, phone, email, address, birth_date, gender)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (name, phone, email, address, birth_date, gender)
        return self.execute_query(query, params)
    
    def get_customer_by_phone(self, phone):
        """البحث عن عميل بالهاتف"""
        query = "SELECT * FROM customers WHERE phone = %s"
        result = self.execute_query(query, (phone,), fetch=True)
        return result[0] if result else None
    
    def update_customer_loyalty_points(self, customer_id, points):
        """تحديث نقاط الولاء للعميل"""
        query = "UPDATE customers SET loyalty_points = loyalty_points + %s WHERE id = %s"
        return self.execute_query(query, (points, customer_id))
    
    # ===== إدارة المنتجات =====
    def get_all_products(self):
        """جلب جميع المنتجات"""
        query = """
        SELECT p.id, p.name, c.name as category, p.price, p.stock_quantity, p.description
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.is_active = TRUE
        ORDER BY c.name, p.name
        """
        return self.execute_query(query, fetch=True)
    
    def update_product_stock(self, product_id, quantity_change, transaction_type):
        """تحديث مخزون المنتج"""
        # جلب الكمية الحالية
        query = "SELECT stock_quantity FROM products WHERE id = %s"
        result = self.execute_query(query, (product_id,), fetch=True)
        if not result:
            return False
        
        current_quantity = result[0][0]
        new_quantity = current_quantity + quantity_change
        
        # تحديث المخزون
        update_query = "UPDATE products SET stock_quantity = %s WHERE id = %s"
        if self.execute_query(update_query, (new_quantity, product_id)):
            # تسجيل الحركة في جدول المخزون
            inventory_query = """
            INSERT INTO inventory_transactions 
            (product_id, transaction_type, quantity_change, quantity_after)
            VALUES (%s, %s, %s, %s)
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
                discount_percentage = subscription[3]  # discount_percentage from subscription_types
                discount_amount = total_amount * (discount_percentage / 100)
            
            final_amount = total_amount - discount_amount
            
            # إنشاء الطلب
            order_query = """
            INSERT INTO orders (customer_id, order_number, total_amount, discount_amount, 
                              final_amount, payment_method)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            order_params = (customer_id, order_number, total_amount, discount_amount, 
                           final_amount, payment_method)
            
            if self.execute_query(order_query, order_params):
                # جلب معرف الطلب
                order_id_query = "SELECT LAST_INSERT_ID()"
                order_id_result = self.execute_query(order_id_query, fetch=True)
                order_id = order_id_result[0][0]
                
                # إضافة عناصر الطلب
                for item in items:
                    item_query = """
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    item_total = item['quantity'] * item['price']
                    item_params = (order_id, item['product_id'], item['quantity'], 
                                 item['price'], item_total)
                    
                    if self.execute_query(item_query, item_params):
                        # تحديث المخزون
                        self.update_product_stock(item['product_id'], -item['quantity'], 'sale')
                
                # إضافة نقاط الولاء (نقطة واحدة لكل دولار)
                loyalty_points = int(final_amount)
                self.update_customer_loyalty_points(customer_id, loyalty_points)
                
                # تسجيل الدفع
                payment_query = """
                INSERT INTO payments (order_id, amount, payment_method)
                VALUES (%s, %s, %s)
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
        query = "SELECT * FROM subscription_types WHERE is_active = TRUE"
        return self.execute_query(query, fetch=True)
    
    def create_subscription(self, customer_id, subscription_type_id):
        """إنشاء اشتراك جديد"""
        # جلب تفاصيل نوع الاشتراك
        query = "SELECT duration_days, price FROM subscription_types WHERE id = %s"
        result = self.execute_query(query, (subscription_type_id,), fetch=True)
        
        if result:
            duration_days, price = result[0]
            start_date = date.today()
            end_date = start_date + timedelta(days=duration_days)
            
            subscription_query = """
            INSERT INTO customer_subscriptions 
            (customer_id, subscription_type_id, start_date, end_date, payment_amount)
            VALUES (%s, %s, %s, %s, %s)
            """
            params = (customer_id, subscription_type_id, start_date, end_date, price)
            
            if self.execute_query(subscription_query, params):
                # تسجيل دفع الاشتراك
                subscription_id_query = "SELECT LAST_INSERT_ID()"
                subscription_id_result = self.execute_query(subscription_id_query, fetch=True)
                subscription_id = subscription_id_result[0][0]
                
                payment_query = """
                INSERT INTO payments (subscription_id, amount, payment_method)
                VALUES (%s, %s, 'cash')
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
        WHERE cs.customer_id = %s AND cs.status = 'active' 
        AND cs.end_date >= CURDATE()
        """
        result = self.execute_query(query, (customer_id,), fetch=True)
        return result[0] if result else None
    
    # ===== التحليلات والتقارير =====
    def get_top_selling_products(self, limit=10):
        """جلب أكثر المنتجات مبيعاً"""
        query = f"SELECT * FROM top_selling_products LIMIT {limit}"
        return self.execute_query(query, fetch=True)
    
    def get_least_selling_products(self, limit=10):
        """جلب أقل المنتجات مبيعاً"""
        query = f"SELECT * FROM least_selling_products LIMIT {limit}"
        return self.execute_query(query, fetch=True)
    
    def get_customer_analytics(self):
        """جلب تحليلات العملاء"""
        query = "SELECT * FROM customer_analytics ORDER BY total_spent DESC"
        return self.execute_query(query, fetch=True)
    
    def get_monthly_sales_analysis(self, year=None):
        """جلب تحليل المبيعات الشهرية"""
        if year:
            query = f"SELECT * FROM monthly_sales_analysis WHERE year = {year}"
        else:
            query = "SELECT * FROM monthly_sales_analysis"
        return self.execute_query(query, fetch=True)
    
    def get_category_analysis(self):
        """جلب تحليل الفئات"""
        query = "SELECT * FROM category_analysis"
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
                discount = subscription[3]
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
                discount_percentage = subscription[3]
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
            tree.insert("", "end", values=(product[1], product[2], product[3], product[4], f"{product[5]:.2f}"))
        
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
            tree.insert("", "end", values=(product[1], product[2], product[3], product[4], f"{product[5]:.2f}"))
        
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
                category[1], category[2], category[3], category[4] or 0,
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
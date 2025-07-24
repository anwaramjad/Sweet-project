#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime, timedelta, date
import random

def add_test_customers():
    """إضافة عملاء وطلبات تجريبية لاختبار النظام"""
    
    # الاتصال بقاعدة البيانات
    conn = sqlite3.connect("sweet_shop.db")
    cursor = conn.cursor()
    
    # إضافة عملاء تجريبيين
    test_customers = [
        ('أحمد محمد علي', '0501234567', 'ahmed@email.com', 'الرياض، حي النخيل', '1985-03-15', 'male'),
        ('فاطمة علي أحمد', '0509876543', 'fatima@email.com', 'جدة، حي الصفا', '1990-07-22', 'female'),
        ('سعد الأحمد محمد', '0551234567', 'saad@email.com', 'الدمام، حي الفيصلية', '1988-12-10', 'male'),
        ('نورا السالم خالد', '0559876543', 'nora@email.com', 'الرياض، حي العليا', '1992-05-18', 'female'),
        ('خالد البترجي عبدالله', '0561234567', 'khalid@email.com', 'مكة، حي الشوقية', '1987-09-25', 'male'),
        ('مريم الخالد سعد', '0569876543', 'mariam@email.com', 'الرياض، حي السليمانية', '1995-01-30', 'female'),
        ('عبدالله النصر علي', '0571234567', 'abdullah@email.com', 'جدة، حي الروضة', '1983-11-12', 'male'),
        ('سارة القحطاني أحمد', '0579876543', 'sara@email.com', 'الرياض، حي الملز', '1991-08-20', 'female'),
        ('محمد الفايز سعد', '0581234567', 'mohammed@email.com', 'الخبر، حي الثقبة', '1989-04-03', 'male'),
        ('هند الرشيد محمد', '0589876543', 'hind@email.com', 'الرياض، حي الورود', '1993-12-14', 'female')
    ]
    
    print("جاري إضافة العملاء التجريبيين...")
    
    customer_ids = []
    for customer in test_customers:
        try:
            cursor.execute("""
                INSERT INTO customers (name, phone, email, address, birth_date, gender)
                VALUES (?, ?, ?, ?, ?, ?)
            """, customer)
            customer_ids.append(cursor.lastrowid)
            print(f"تم إضافة العميل: {customer[0]}")
        except sqlite3.IntegrityError:
            # العميل موجود مسبقاً
            cursor.execute("SELECT id FROM customers WHERE phone = ?", (customer[1],))
            customer_ids.append(cursor.fetchone()[0])
            print(f"العميل موجود مسبقاً: {customer[0]}")
    
    # إضافة اشتراكات للعملاء
    print("\nجاري إضافة اشتراكات للعملاء...")
    
    subscription_data = [
        (customer_ids[0], 2, 80.00),  # أحمد - اشتراك شهري
        (customer_ids[1], 3, 200.00), # فاطمة - اشتراك ربع سنوي
        (customer_ids[2], 1, 25.00),  # سعد - اشتراك أسبوعي
        (customer_ids[3], 4, 600.00), # نورا - اشتراك سنوي
        (customer_ids[4], 2, 80.00),  # خالد - اشتراك شهري
    ]
    
    for customer_id, subscription_type_id, price in subscription_data:
        # جلب مدة الاشتراك
        cursor.execute("SELECT duration_days FROM subscription_types WHERE id = ?", (subscription_type_id,))
        duration = cursor.fetchone()[0]
        
        start_date = date.today() - timedelta(days=random.randint(1, 30))
        end_date = start_date + timedelta(days=duration)
        
        cursor.execute("""
            INSERT INTO customer_subscriptions 
            (customer_id, subscription_type_id, start_date, end_date, payment_amount)
            VALUES (?, ?, ?, ?, ?)
        """, (customer_id, subscription_type_id, start_date, end_date, price))
        
        print(f"تم إضافة اشتراك للعميل ID: {customer_id}")
    
    # إضافة طلبات تجريبية
    print("\nجاري إضافة طلبات تجريبية...")
    
    # جلب قائمة المنتجات
    cursor.execute("SELECT id, price FROM products WHERE is_active = 1")
    products = cursor.fetchall()
    
    for i, customer_id in enumerate(customer_ids[:8]):  # إضافة طلبات لأول 8 عملاء
        num_orders = random.randint(1, 4)  # عدد الطلبات لكل عميل
        
        for order_num in range(num_orders):
            # إنشاء رقم طلب
            order_number = f"ORD{random.randint(10000, 99999)}"
            
            # اختيار منتجات عشوائية
            selected_products = random.sample(products, random.randint(1, 5))
            
            total_amount = 0
            order_items = []
            
            for product_id, price in selected_products:
                quantity = random.randint(1, 3)
                item_total = quantity * price
                total_amount += item_total
                order_items.append((product_id, quantity, price, item_total))
            
            # حساب الخصم إذا كان للعميل اشتراك
            discount_amount = 0
            cursor.execute("""
                SELECT st.discount_percentage 
                FROM customer_subscriptions cs
                JOIN subscription_types st ON cs.subscription_type_id = st.id
                WHERE cs.customer_id = ? AND cs.status = 'active' 
                AND cs.end_date >= DATE('now')
            """, (customer_id,))
            
            subscription = cursor.fetchone()
            if subscription:
                discount_percentage = subscription[0]
                discount_amount = total_amount * (discount_percentage / 100)
            
            final_amount = total_amount - discount_amount
            
            # إنشاء الطلب
            order_date = datetime.now() - timedelta(days=random.randint(1, 60))
            
            cursor.execute("""
                INSERT INTO orders (customer_id, order_number, order_date, total_amount, 
                                  discount_amount, final_amount, status, payment_method)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (customer_id, order_number, order_date, total_amount, 
                  discount_amount, final_amount, 'delivered', 'cash'))
            
            order_id = cursor.lastrowid
            
            # إضافة عناصر الطلب
            for product_id, quantity, price, item_total in order_items:
                cursor.execute("""
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
                    VALUES (?, ?, ?, ?, ?)
                """, (order_id, product_id, quantity, price, item_total))
                
                # تسجيل حركة المخزون
                cursor.execute("SELECT stock_quantity FROM products WHERE id = ?", (product_id,))
                current_stock = cursor.fetchone()[0]
                new_stock = current_stock - quantity
                
                cursor.execute("UPDATE products SET stock_quantity = ? WHERE id = ?", (new_stock, product_id))
                
                cursor.execute("""
                    INSERT INTO inventory_transactions 
                    (product_id, transaction_type, quantity_change, quantity_after, reference_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (product_id, 'sale', -quantity, new_stock, order_id))
            
            # تحديث نقاط الولاء
            loyalty_points = int(final_amount)
            cursor.execute("""
                UPDATE customers SET 
                    loyalty_points = loyalty_points + ?,
                    total_purchases = total_purchases + ?
                WHERE id = ?
            """, (loyalty_points, final_amount, customer_id))
            
            # تسجيل الدفع
            cursor.execute("""
                INSERT INTO payments (order_id, amount, payment_method, payment_date)
                VALUES (?, ?, ?, ?)
            """, (order_id, final_amount, 'cash', order_date))
            
            print(f"تم إضافة طلب {order_number} للعميل ID: {customer_id}")
    
    # إضافة تقييمات للمنتجات
    print("\nجاري إضافة تقييمات للمنتجات...")
    
    for customer_id in customer_ids[:5]:  # أول 5 عملاء يقيمون منتجات
        # اختيار منتجات عشوائية للتقييم
        reviewed_products = random.sample(products[:10], random.randint(2, 5))
        
        for product_id, _ in reviewed_products:
            rating = random.randint(3, 5)  # تقييمات إيجابية
            reviews = [
                "منتج ممتاز وطعم رائع",
                "أعجبني كثيراً وأنصح به",
                "جودة عالية وطعم مميز",
                "منتج جيد جداً",
                "طعم لذيذ ومميز",
                "أفضل حلويات في المنطقة",
                "جودة ممتازة وخدمة رائعة"
            ]
            
            review_text = random.choice(reviews)
            
            cursor.execute("""
                INSERT INTO product_reviews (product_id, customer_id, rating, review_text)
                VALUES (?, ?, ?, ?)
            """, (product_id, customer_id, rating, review_text))
    
    print("تم إضافة التقييمات بنجاح")
    
    # حفظ التغييرات
    conn.commit()
    conn.close()
    
    print("\n✅ تم إضافة جميع البيانات التجريبية بنجاح!")
    print("\n📊 ملخص البيانات المضافة:")
    print(f"• {len(test_customers)} عملاء")
    print(f"• {len(subscription_data)} اشتراكات")
    print(f"• طلبات متعددة مع عناصر مختلفة")
    print("• تقييمات للمنتجات")
    print("• تحديث نقاط الولاء والمخزون")
    
    print("\n🎯 العملاء الجاهزين للاختبار:")
    for i, customer in enumerate(test_customers[:5]):
        print(f"• {customer[0]}: {customer[1]}")

if __name__ == "__main__":
    add_test_customers()
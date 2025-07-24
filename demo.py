#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
عرض توضيحي لنظام إدارة محل الحلويات
يعرض أهم وظائف النظام بطريقة تفاعلية
"""

import sqlite3
from datetime import datetime
import sys

def print_header(title):
    """طباعة عنوان مع تنسيق جميل"""
    print("\n" + "="*60)
    print(f"📊 {title}")
    print("="*60)

def print_separator():
    """فاصل بين الأقسام"""
    print("-" * 60)

def show_customers():
    """عرض العملاء وحالة اشتراكاتهم"""
    print_header("العملاء المسجلين في النظام")
    
    conn = sqlite3.connect("sweet_shop.db")
    cursor = conn.cursor()
    
    query = """
    SELECT 
        c.name,
        c.phone,
        c.loyalty_points,
        CASE 
            WHEN cs.id IS NOT NULL THEN st.name || ' (خصم ' || st.discount_percentage || '%)'
            ELSE 'غير مشترك'
        END as subscription_status,
        COUNT(o.id) as total_orders,
        COALESCE(SUM(o.final_amount), 0) as total_spent
    FROM customers c
    LEFT JOIN customer_subscriptions cs ON c.id = cs.customer_id AND cs.status = 'active'
    LEFT JOIN subscription_types st ON cs.subscription_type_id = st.id
    LEFT JOIN orders o ON c.id = o.customer_id AND o.status != 'cancelled'
    GROUP BY c.id, c.name, c.phone, c.loyalty_points, cs.id, st.name, st.discount_percentage
    ORDER BY total_spent DESC
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print(f"{'الاسم':<20} {'الهاتف':<15} {'النقاط':<8} {'الاشتراك':<25} {'الطلبات':<8} {'المبلغ':<10}")
    print("-" * 95)
    
    for row in results:
        name, phone, points, subscription, orders, spent = row
        print(f"{name:<20} {phone:<15} {points:<8} {subscription:<25} {orders:<8} {spent:<10.2f}")
    
    conn.close()

def show_top_products():
    """عرض أكثر المنتجات مبيعاً"""
    print_header("أكثر المنتجات مبيعاً")
    
    conn = sqlite3.connect("sweet_shop.db")
    cursor = conn.cursor()
    
    query = """
    SELECT 
        p.name,
        c.name as category,
        COALESCE(SUM(oi.quantity), 0) as total_sold,
        COALESCE(SUM(oi.total_price), 0) as total_revenue,
        p.price,
        p.stock_quantity
    FROM products p
    LEFT JOIN categories c ON p.category_id = c.id
    LEFT JOIN order_items oi ON p.id = oi.product_id
    LEFT JOIN orders o ON oi.order_id = o.id AND o.status != 'cancelled'
    GROUP BY p.id, p.name, c.name, p.price, p.stock_quantity
    ORDER BY total_sold DESC
    LIMIT 10
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print(f"{'المنتج':<20} {'الفئة':<15} {'المباع':<8} {'الإيرادات':<12} {'السعر':<8} {'المخزون':<10}")
    print("-" * 85)
    
    for row in results:
        name, category, sold, revenue, price, stock = row
        print(f"{name:<20} {category:<15} {sold:<8} {revenue:<12.2f} {price:<8.2f} {stock:<10}")
    
    conn.close()

def show_sales_summary():
    """عرض ملخص المبيعات"""
    print_header("ملخص المبيعات")
    
    conn = sqlite3.connect("sweet_shop.db")
    cursor = conn.cursor()
    
    # إجمالي الإحصائيات
    cursor.execute("""
    SELECT 
        COUNT(DISTINCT c.id) as total_customers,
        COUNT(DISTINCT o.id) as total_orders,
        COALESCE(SUM(o.final_amount), 0) as total_revenue,
        COUNT(DISTINCT cs.id) as active_subscriptions
    FROM customers c
    LEFT JOIN orders o ON c.id = o.customer_id AND o.status != 'cancelled'
    LEFT JOIN customer_subscriptions cs ON c.id = cs.customer_id AND cs.status = 'active'
    """)
    
    stats = cursor.fetchone()
    customers, orders, revenue, subscriptions = stats
    
    print(f"📊 إجمالي العملاء: {customers}")
    print(f"📦 إجمالي الطلبات: {orders}")
    print(f"💰 إجمالي الإيرادات: {revenue:.2f} ريال")
    print(f"📋 الاشتراكات النشطة: {subscriptions}")
    
    if orders > 0:
        avg_order = revenue / orders
        print(f"📈 متوسط قيمة الطلب: {avg_order:.2f} ريال")
    
    print_separator()
    
    # أداء الفئات
    print("📊 أداء الفئات:")
    cursor.execute("""
    SELECT 
        c.name,
        COUNT(oi.id) as total_items_sold,
        COALESCE(SUM(oi.total_price), 0) as category_revenue
    FROM categories c
    LEFT JOIN products p ON c.id = p.category_id
    LEFT JOIN order_items oi ON p.id = oi.product_id
    LEFT JOIN orders o ON oi.order_id = o.id AND o.status != 'cancelled'
    GROUP BY c.id, c.name
    ORDER BY category_revenue DESC
    """)
    
    categories = cursor.fetchall()
    for name, items, cat_revenue in categories:
        print(f"  • {name}: {items} عنصر مباع، {cat_revenue:.2f} ريال")
    
    conn.close()

def show_recent_orders():
    """عرض آخر الطلبات"""
    print_header("آخر 5 طلبات")
    
    conn = sqlite3.connect("sweet_shop.db")
    cursor = conn.cursor()
    
    query = """
    SELECT 
        o.order_number,
        c.name as customer_name,
        o.order_date,
        o.total_amount,
        o.discount_amount,
        o.final_amount,
        o.status
    FROM orders o
    JOIN customers c ON o.customer_id = c.id
    ORDER BY o.order_date DESC
    LIMIT 5
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    for row in results:
        order_num, customer, date, total, discount, final, status = row
        print(f"🛍️  الطلب: {order_num}")
        print(f"   العميل: {customer}")
        print(f"   التاريخ: {date}")
        print(f"   المبلغ: {total:.2f} ريال")
        if discount > 0:
            print(f"   الخصم: {discount:.2f} ريال ({discount/total*100:.1f}%)")
        print(f"   النهائي: {final:.2f} ريال")
        print(f"   الحالة: {status}")
        print()
    
    conn.close()

def interactive_search():
    """بحث تفاعلي عن عميل"""
    print_header("البحث عن عميل")
    
    phone = input("أدخل رقم الهاتف للبحث (أو اضغط Enter للعودة): ").strip()
    
    if not phone:
        return
    
    conn = sqlite3.connect("sweet_shop.db")
    cursor = conn.cursor()
    
    # البحث عن العميل
    cursor.execute("""
    SELECT 
        c.*,
        CASE 
            WHEN cs.id IS NOT NULL THEN st.name || ' (خصم ' || st.discount_percentage || '%)'
            ELSE 'غير مشترك'
        END as subscription_status
    FROM customers c
    LEFT JOIN customer_subscriptions cs ON c.id = cs.customer_id AND cs.status = 'active'
    LEFT JOIN subscription_types st ON cs.subscription_type_id = st.id
    WHERE c.phone = ?
    """, (phone,))
    
    result = cursor.fetchone()
    
    if result:
        print(f"\n✅ تم العثور على العميل:")
        print(f"   الاسم: {result[1]}")
        print(f"   الهاتف: {result[2]}")
        print(f"   البريد: {result[3] or 'غير محدد'}")
        print(f"   العنوان: {result[4] or 'غير محدد'}")
        print(f"   نقاط الولاء: {result[9]}")
        print(f"   حالة الاشتراك: {result[11]}")
        
        # عرض آخر الطلبات
        cursor.execute("""
        SELECT order_number, order_date, final_amount, status
        FROM orders 
        WHERE customer_id = ? 
        ORDER BY order_date DESC 
        LIMIT 3
        """, (result[0],))
        
        orders = cursor.fetchall()
        if orders:
            print(f"\n📦 آخر الطلبات:")
            for order in orders:
                print(f"   • {order[0]}: {order[2]:.2f} ريال ({order[1]})")
        else:
            print(f"\n📦 لا توجد طلبات سابقة")
            
    else:
        print(f"\n❌ لم يتم العثور على عميل بالرقم: {phone}")
    
    conn.close()

def main():
    """الدالة الرئيسية للعرض التوضيحي"""
    
    # التحقق من وجود قاعدة البيانات
    try:
        conn = sqlite3.connect("sweet_shop.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM customers")
        customer_count = cursor.fetchone()[0]
        conn.close()
        
        if customer_count == 0:
            print("⚠️  قاعدة البيانات فارغة. يرجى تشغيل:")
            print("python3 add_test_customers.py")
            return
            
    except sqlite3.Error:
        print("❌ لم يتم العثور على قاعدة البيانات. يرجى تشغيل:")
        print("python3 sweet_shop_sqlite.py")
        return
    
    print("🍰 مرحباً بك في نظام إدارة محل الحلويات")
    print("📊 عرض توضيحي للإمكانيات المتاحة")
    
    while True:
        print("\n" + "="*60)
        print("اختر ما تريد عرضه:")
        print("1. العملاء والاشتراكات")
        print("2. أكثر المنتجات مبيعاً") 
        print("3. ملخص المبيعات")
        print("4. آخر الطلبات")
        print("5. البحث عن عميل")
        print("0. الخروج")
        print("="*60)
        
        choice = input("اختيارك (0-5): ").strip()
        
        if choice == "1":
            show_customers()
        elif choice == "2":
            show_top_products()
        elif choice == "3":
            show_sales_summary()
        elif choice == "4":
            show_recent_orders()
        elif choice == "5":
            interactive_search()
        elif choice == "0":
            print("\n🍰 شكراً لاستخدام نظام إدارة محل الحلويات!")
            print("🎯 للحصول على الواجهة الكاملة، شغل: python3 sweet_shop_sqlite.py")
            break
        else:
            print("❌ اختيار غير صحيح. يرجى المحاولة مرة أخرى.")
        
        input("\nاضغط Enter للمتابعة...")

if __name__ == "__main__":
    main()
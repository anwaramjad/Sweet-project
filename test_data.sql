-- بيانات تجريبية لاختبار نظام محل الحلويات
USE sweet_shop_db;

-- إضافة عملاء تجريبيين
INSERT INTO customers (name, phone, email, address, birth_date, gender) VALUES
('أحمد محمد', '0501234567', 'ahmed@email.com', 'الرياض، حي النخيل', '1985-03-15', 'male'),
('فاطمة علي', '0509876543', 'fatima@email.com', 'جدة، حي الصفا', '1990-07-22', 'female'),
('سعد الأحمد', '0551234567', 'saad@email.com', 'الدمام، حي الفيصلية', '1988-12-10', 'male'),
('نورا السالم', '0559876543', 'nora@email.com', 'الرياض، حي العليا', '1992-05-18', 'female'),
('خالد البترجي', '0561234567', 'khalid@email.com', 'مكة، حي الشوقية', '1987-09-25', 'male'),
('مريم الخالد', '0569876543', 'mariam@email.com', 'الرياض، حي السليمانية', '1995-01-30', 'female'),
('عبدالله النصر', '0571234567', 'abdullah@email.com', 'جدة، حي الروضة', '1983-11-12', 'male'),
('سارة القحطاني', '0579876543', 'sara@email.com', 'الرياض، حي الملز', '1991-04-08', 'female'),
('محمد الزهراني', '0581234567', 'mohammed@email.com', 'الطائف، حي السداد', '1986-08-14', 'male'),
('هند العتيبي', '0589876543', 'hind@email.com', 'الرياض، حي الياسمين', '1994-02-28', 'female');

-- إضافة اشتراكات للعملاء
INSERT INTO customer_subscriptions (customer_id, subscription_type_id, start_date, end_date, payment_amount) VALUES
(1, 2, '2024-01-01', '2024-01-31', 80.00),  -- أحمد - اشتراك شهري
(2, 3, '2024-01-15', '2024-04-15', 200.00), -- فاطمة - اشتراك ربع سنوي  
(3, 1, '2024-01-20', '2024-01-27', 25.00),  -- سعد - اشتراك أسبوعي
(4, 4, '2024-01-01', '2024-12-31', 600.00), -- نورا - اشتراك سنوي
(5, 2, '2024-01-10', '2024-02-10', 80.00);  -- خالد - اشتراك شهري

-- إضافة طلبات تجريبية
INSERT INTO orders (customer_id, order_number, total_amount, discount_amount, final_amount, payment_method, status) VALUES
(1, 'ORD12345', 50.00, 7.50, 42.50, 'cash', 'delivered'),
(2, 'ORD12346', 80.00, 16.00, 64.00, 'card', 'delivered'),
(3, 'ORD12347', 25.00, 2.50, 22.50, 'cash', 'delivered'),
(4, 'ORD12348', 120.00, 30.00, 90.00, 'card', 'delivered'),
(5, 'ORD12349', 60.00, 9.00, 51.00, 'cash', 'delivered'),
(6, 'ORD12350', 35.00, 0.00, 35.00, 'cash', 'delivered'),
(7, 'ORD12351', 75.00, 0.00, 75.00, 'card', 'delivered'),
(8, 'ORD12352', 45.00, 0.00, 45.00, 'cash', 'delivered'),
(9, 'ORD12353', 90.00, 0.00, 90.00, 'card', 'delivered'),
(10, 'ORD12354', 55.00, 0.00, 55.00, 'cash', 'delivered');

-- إضافة تفاصيل الطلبات
INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
-- الطلب الأول (أحمد)
(1, 1, 2, 15.00, 30.00),  -- تشيز كيك
(1, 5, 4, 3.00, 12.00),   -- ماكرون
(1, 22, 1, 8.00, 8.00),   -- شاي

-- الطلب الثاني (فاطمة)
(2, 3, 3, 18.00, 54.00),  -- تيراميسو
(2, 7, 2, 10.00, 20.00),  -- إكلير
(2, 21, 1, 6.00, 6.00),   -- عصير برتقال

-- الطلب الثالث (سعد)
(3, 2, 1, 12.00, 12.00),  -- براونيز
(3, 23, 2, 6.50, 13.00),  -- شوكولاتة ساخنة

-- الطلب الرابع (نورا)
(4, 11, 2, 22.00, 44.00), -- سوفليه
(4, 4, 1, 20.00, 20.00),  -- بافلوفا
(4, 16, 4, 14.00, 56.00), -- عصير ليمون نعناع

-- الطلب الخامس (خالد)
(5, 6, 3, 8.00, 24.00),   -- كب كيك
(5, 12, 2, 16.00, 32.00), -- فطيرة التفاح
(5, 20, 1, 4.00, 4.00),   -- سحلب

-- الطلب السادس
(6, 8, 2, 6.00, 12.00),   -- مافن
(6, 25, 3, 7.67, 23.00),  -- لاتيه

-- الطلب السابع
(7, 13, 1, 13.00, 13.00), -- خبز البودينغ
(7, 14, 3, 9.00, 27.00),  -- تشورو
(8, 24, 4, 8.75, 35.00),  -- قهوة موكا

-- الطلب الثامن
(8, 9, 2, 14.00, 28.00),  -- بانا كوتا
(8, 17, 2, 8.50, 17.00),  -- عصير بطيخ

-- الطلب التاسع
(9, 15, 1, 17.00, 17.00), -- كريب سوزيت
(9, 18, 3, 8.00, 24.00),  -- عصير أناناس
(9, 26, 5, 9.80, 49.00),  -- إسبريسو

-- الطلب العاشر
(10, 10, 4, 4.00, 16.00), -- دونتس
(10, 19, 2, 9.00, 18.00), -- عصير رمان
(10, 27, 3, 7.00, 21.00); -- كابتشينو

-- إضافة تقييمات للمنتجات
INSERT INTO product_reviews (product_id, customer_id, rating, review_text) VALUES
(1, 1, 5, 'تشيز كيك رائع جداً، طعم مميز ونكهة غنية'),
(3, 2, 5, 'أفضل تيراميسو جربته في حياتي'),
(2, 3, 4, 'براونيز لذيذ ولكن يحتاج لمزيد من الشوكولاتة'),
(11, 4, 5, 'سوفليه خفيف ولذيذ، يستحق السعر'),
(6, 5, 4, 'كب كيك جميل ومناسب للأطفال'),
(8, 6, 3, 'مافن عادي، يمكن تحسينه'),
(13, 7, 4, 'خبز البودينغ تقليدي ولذيذ'),
(9, 8, 5, 'بانا كوتا إيطالية أصيلة'),
(15, 9, 5, 'كريب سوزيت مذهل، تحضير احترافي'),
(10, 10, 4, 'دونتس طازج ومقرمش');

-- تحديث نقاط الولاء للعملاء بناء على مشترياتهم
UPDATE customers SET 
    loyalty_points = 43,
    total_purchases = 42.50
WHERE id = 1;

UPDATE customers SET 
    loyalty_points = 64,
    total_purchases = 64.00
WHERE id = 2;

UPDATE customers SET 
    loyalty_points = 23,
    total_purchases = 22.50
WHERE id = 3;

UPDATE customers SET 
    loyalty_points = 90,
    total_purchases = 90.00
WHERE id = 4;

UPDATE customers SET 
    loyalty_points = 51,
    total_purchases = 51.00
WHERE id = 5;

UPDATE customers SET 
    loyalty_points = 35,
    total_purchases = 35.00
WHERE id = 6;

UPDATE customers SET 
    loyalty_points = 75,
    total_purchases = 75.00
WHERE id = 7;

UPDATE customers SET 
    loyalty_points = 45,
    total_purchases = 45.00
WHERE id = 8;

UPDATE customers SET 
    loyalty_points = 90,
    total_purchases = 90.00
WHERE id = 9;

UPDATE customers SET 
    loyalty_points = 55,
    total_purchases = 55.00
WHERE id = 10;

-- إضافة مدفوعات الطلبات
INSERT INTO payments (order_id, amount, payment_method, status) VALUES
(1, 42.50, 'cash', 'completed'),
(2, 64.00, 'card', 'completed'),
(3, 22.50, 'cash', 'completed'),
(4, 90.00, 'card', 'completed'),
(5, 51.00, 'cash', 'completed'),
(6, 35.00, 'cash', 'completed'),
(7, 75.00, 'card', 'completed'),
(8, 45.00, 'cash', 'completed'),
(9, 90.00, 'card', 'completed'),
(10, 55.00, 'cash', 'completed');

-- إضافة مدفوعات الاشتراكات
INSERT INTO payments (subscription_id, amount, payment_method, status) VALUES
(1, 80.00, 'cash', 'completed'),
(2, 200.00, 'card', 'completed'),
(3, 25.00, 'cash', 'completed'),
(4, 600.00, 'card', 'completed'),
(5, 80.00, 'cash', 'completed');

-- تحديث حركات المخزون بناء على المبيعات
INSERT INTO inventory_transactions (product_id, transaction_type, quantity_change, quantity_after) VALUES
-- تشيز كيك
(1, 'sale', -2, 48),
-- براونيز  
(2, 'sale', -1, 99),
-- تيراميسو
(3, 'sale', -3, 27),
-- بافلوفا
(4, 'sale', -1, 24),
-- ماكرون
(5, 'sale', -4, 196),
-- كب كيك
(6, 'sale', -3, 147),
-- إكلير
(7, 'sale', -2, 78),
-- مافن
(8, 'sale', -2, 118),
-- بانا كوتا
(9, 'sale', -2, 38),
-- دونتس
(10, 'sale', -4, 196),
-- سوفليه
(11, 'sale', -2, 18),
-- فطيرة التفاح
(12, 'sale', -2, 33),
-- خبز البودينغ
(13, 'sale', -1, 44),
-- تشورو
(14, 'sale', -3, 97),
-- كريب سوزيت
(15, 'sale', -1, 29);

-- تحديث كميات المنتجات في جدول المنتجات
UPDATE products SET stock_quantity = 48 WHERE id = 1;  -- تشيز كيك
UPDATE products SET stock_quantity = 99 WHERE id = 2;  -- براونيز
UPDATE products SET stock_quantity = 27 WHERE id = 3;  -- تيراميسو
UPDATE products SET stock_quantity = 24 WHERE id = 4;  -- بافلوفا
UPDATE products SET stock_quantity = 196 WHERE id = 5; -- ماكرون
UPDATE products SET stock_quantity = 147 WHERE id = 6; -- كب كيك
UPDATE products SET stock_quantity = 78 WHERE id = 7;  -- إكلير
UPDATE products SET stock_quantity = 118 WHERE id = 8; -- مافن
UPDATE products SET stock_quantity = 38 WHERE id = 9;  -- بانا كوتا
UPDATE products SET stock_quantity = 196 WHERE id = 10; -- دونتس
UPDATE products SET stock_quantity = 18 WHERE id = 11; -- سوفليه
UPDATE products SET stock_quantity = 33 WHERE id = 12; -- فطيرة التفاح
UPDATE products SET stock_quantity = 44 WHERE id = 13; -- خبز البودينغ
UPDATE products SET stock_quantity = 97 WHERE id = 14; -- تشورو
UPDATE products SET stock_quantity = 29 WHERE id = 15; -- كريب سوزيت

-- إضافة طلبات إضافية لجعل البيانات أكثر واقعية
INSERT INTO orders (customer_id, order_number, total_amount, discount_amount, final_amount, payment_method, status, order_date) VALUES
(1, 'ORD12355', 35.00, 5.25, 29.75, 'cash', 'delivered', '2024-01-05'),
(2, 'ORD12356', 60.00, 12.00, 48.00, 'card', 'delivered', '2024-01-10'),
(4, 'ORD12357', 95.00, 23.75, 71.25, 'card', 'delivered', '2024-01-15'),
(1, 'ORD12358', 40.00, 6.00, 34.00, 'cash', 'delivered', '2024-01-20'),
(3, 'ORD12359', 30.00, 3.00, 27.00, 'cash', 'delivered', '2024-01-22');

SELECT 'تم إدراج البيانات التجريبية بنجاح!' as message;
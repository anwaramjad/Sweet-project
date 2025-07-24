-- قاعدة بيانات محل الحلويات
CREATE DATABASE sweet_shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sweet_shop_db;

-- جدول فئات المنتجات
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول المنتجات
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category_id INT,
    price DECIMAL(10,2) NOT NULL,
    cost DECIMAL(10,2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    description TEXT,
    image_url VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- جدول العملاء
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    address TEXT,
    birth_date DATE,
    gender ENUM('male', 'female'),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    total_purchases DECIMAL(10,2) DEFAULT 0.00,
    loyalty_points INT DEFAULT 0
);

-- جدول أنواع الاشتراكات
CREATE TABLE subscription_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    duration_days INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    discount_percentage DECIMAL(5,2) DEFAULT 0.00,
    description TEXT,
    benefits JSON,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول اشتراكات العملاء
CREATE TABLE customer_subscriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    subscription_type_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status ENUM('active', 'expired', 'cancelled') DEFAULT 'active',
    payment_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (subscription_type_id) REFERENCES subscription_types(id)
);

-- جدول الطلبات
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_number VARCHAR(20) UNIQUE NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0.00,
    final_amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'confirmed', 'preparing', 'ready', 'delivered', 'cancelled') DEFAULT 'pending',
    payment_method ENUM('cash', 'card', 'online') DEFAULT 'cash',
    notes TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- جدول تفاصيل الطلبات
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- جدول المدفوعات
CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    subscription_id INT,
    amount DECIMAL(10,2) NOT NULL,
    payment_method ENUM('cash', 'card', 'online') NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'completed',
    transaction_id VARCHAR(100),
    notes TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (subscription_id) REFERENCES customer_subscriptions(id)
);

-- جدول تقييمات المنتجات
CREATE TABLE product_reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    customer_id INT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- جدول تتبع المخزون
CREATE TABLE inventory_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    transaction_type ENUM('purchase', 'sale', 'adjustment', 'return') NOT NULL,
    quantity_change INT NOT NULL,
    quantity_after INT NOT NULL,
    reference_id INT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- إدراج البيانات الأساسية

-- إدراج فئات المنتجات
INSERT INTO categories (name, description) VALUES
('حلويات باردة', 'حلويات تقدم باردة مثل الكيك والتيراميسو'),
('حلويات ساخنة', 'حلويات تقدم ساخنة مثل الكنافة والسوفليه'),
('مشروبات باردة', 'عصائر طبيعية ومشروبات منعشة'),
('مشروبات ساخنة', 'قهوة وشاي ومشروبات ساخنة أخرى'),
('حلويات شرقية', 'بقلاوة وكنافة وحلويات تراثية');

-- إدراج المنتجات
INSERT INTO products (name, category_id, price, cost, stock_quantity, description) VALUES
-- حلويات باردة
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

-- حلويات ساخنة
('سوفليه', 2, 22.00, 14.00, 20, 'حلوى فرنسية منفوشة'),
('فطيرة التفاح', 2, 16.00, 9.00, 35, 'فطيرة التفاح الكلاسيكية'),
('خبز البودينغ', 2, 13.00, 7.00, 45, 'بودينغ الخبز بالفانيليا'),
('تشورو', 2, 9.00, 4.50, 100, 'عجين مقلي بالسكر والقرفة'),
('كريب سوزيت', 2, 17.00, 10.00, 30, 'كريب فرنسي باللهب'),

-- مشروبات باردة
('عصير برتقال', 3, 5.00, 2.50, 100, 'عصير برتقال طبيعي'),
('عصير ليمون نعناع', 3, 6.00, 3.00, 80, 'مشروب منعش بالليمون'),
('عصير بطيخ', 3, 7.00, 3.50, 60, 'عصير بطيخ طازج'),
('عصير أناناس', 3, 8.00, 4.00, 50, 'عصير أناناس استوائي'),
('عصير رمان', 3, 9.00, 4.50, 40, 'عصير رمان غني بالفيتامينات'),

-- مشروبات ساخنة
('سحلب', 4, 7.00, 3.50, 80, 'مشروب شتوي دافئ'),
('شاي', 4, 3.00, 1.50, 200, 'شاي أحمر تقليدي'),
('شوكولاتة ساخنة', 4, 8.00, 4.00, 100, 'شوكولاتة دافئة كريمية'),
('قهوة موكا', 4, 10.00, 5.00, 80, 'قهوة بالشوكولاتة'),
('لاتيه', 4, 9.00, 4.50, 90, 'قهوة بالحليب الرغوي'),
('إسبريسو', 4, 6.00, 3.00, 150, 'قهوة إيطالية قوية'),
('كابتشينو', 4, 8.00, 4.00, 100, 'قهوة إيطالية كلاسيكية');

-- إدراج أنواع الاشتراكات
INSERT INTO subscription_types (name, duration_days, price, discount_percentage, description, benefits) VALUES
('اشتراك أسبوعي', 7, 25.00, 10.00, 'خصم 10% على جميع المشتريات لمدة أسبوع', 
 '{"discount": "10%", "free_delivery": false, "priority_service": false}'),
('اشتراك شهري', 30, 80.00, 15.00, 'خصم 15% على جميع المشتريات لمدة شهر', 
 '{"discount": "15%", "free_delivery": true, "priority_service": true}'),
('اشتراك ربع سنوي', 90, 200.00, 20.00, 'خصم 20% على جميع المشتريات لمدة 3 أشهر', 
 '{"discount": "20%", "free_delivery": true, "priority_service": true, "birthday_gift": true}'),
('اشتراك سنوي', 365, 600.00, 25.00, 'خصم 25% على جميع المشتريات لمدة سنة كاملة', 
 '{"discount": "25%", "free_delivery": true, "priority_service": true, "birthday_gift": true, "exclusive_items": true}');

-- إنشاء الفهارس لتحسين الأداء
CREATE INDEX idx_customer_phone ON customers(phone);
CREATE INDEX idx_customer_email ON customers(email);
CREATE INDEX idx_order_date ON orders(order_date);
CREATE INDEX idx_order_customer ON orders(customer_id);
CREATE INDEX idx_product_category ON products(category_id);
CREATE INDEX idx_subscription_customer ON customer_subscriptions(customer_id);
CREATE INDEX idx_subscription_dates ON customer_subscriptions(start_date, end_date);

-- إنشاء مشاهد للتحليلات
-- مشهد أكثر المنتجات مبيعاً
CREATE VIEW top_selling_products AS
SELECT 
    p.id,
    p.name,
    c.name as category_name,
    COUNT(oi.id) as total_orders,
    SUM(oi.quantity) as total_quantity_sold,
    SUM(oi.total_price) as total_revenue,
    AVG(pr.rating) as average_rating
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN order_items oi ON p.id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.id
LEFT JOIN product_reviews pr ON p.id = pr.product_id
WHERE o.status != 'cancelled'
GROUP BY p.id, p.name, c.name
ORDER BY total_quantity_sold DESC;

-- مشهد أقل المنتجات مبيعاً
CREATE VIEW least_selling_products AS
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
ORDER BY total_quantity_sold ASC, p.id ASC;

-- مشهد تحليل العملاء
CREATE VIEW customer_analytics AS
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
GROUP BY c.id, c.name, c.phone, c.registration_date, c.loyalty_points;

-- مشهد تحليل المبيعات الشهرية
CREATE VIEW monthly_sales_analysis AS
SELECT 
    YEAR(o.order_date) as year,
    MONTH(o.order_date) as month,
    MONTHNAME(o.order_date) as month_name,
    COUNT(o.id) as total_orders,
    SUM(o.final_amount) as total_revenue,
    AVG(o.final_amount) as average_order_value,
    COUNT(DISTINCT o.customer_id) as unique_customers
FROM orders o
WHERE o.status != 'cancelled'
GROUP BY YEAR(o.order_date), MONTH(o.order_date), MONTHNAME(o.order_date)
ORDER BY year DESC, month DESC;

-- مشهد تحليل الفئات
CREATE VIEW category_analysis AS
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
ORDER BY total_revenue DESC;
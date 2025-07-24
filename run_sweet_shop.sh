#!/bin/bash

echo ""
echo "🍰 نظام إدارة محل الحلويات"
echo "========================"
echo ""
echo "جاري تشغيل التطبيق..."
echo ""

# التحقق من وجود Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 غير مثبت! يرجى تثبيت Python 3.7 أو أحدث"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "macOS: brew install python3"
    exit 1
fi

# التحقق من وجود الملفات المطلوبة
if [ ! -f "sweet_shop_sqlite.py" ]; then
    echo "❌ لم يتم العثور على ملف sweet_shop_sqlite.py"
    echo "تأكد من وجود جميع ملفات المشروع في هذا المجلد"
    exit 1
fi

if [ ! -f "sweet_shop.db" ]; then
    echo "⚠️  لم يتم العثور على قاعدة البيانات"
    echo "جاري إنشاء قاعدة البيانات الجديدة..."
    if [ -f "add_test_customers.py" ]; then
        python3 add_test_customers.py
    else
        echo "❌ لم يتم العثور على ملف add_test_customers.py"
        exit 1
    fi
fi

# تثبيت tkinter إذا لم يكن متوفراً
echo "التحقق من المكتبات المطلوبة..."

# Ubuntu/Debian
if command -v apt &> /dev/null; then
    if ! python3 -c "import tkinter" 2>/dev/null; then
        echo "جاري تثبيت tkinter..."
        sudo apt update > /dev/null 2>&1
        sudo apt install -y python3-tk > /dev/null 2>&1
    fi
fi

# تثبيت المكتبات المطلوبة
echo "جاري تثبيت المكتبات المطلوبة..."
pip3 install pandas matplotlib > /dev/null 2>&1

# تشغيل التطبيق
echo ""
echo "✅ جاري تشغيل نظام إدارة محل الحلويات..."
echo ""

if python3 sweet_shop_sqlite.py; then
    echo "تم إغلاق التطبيق بنجاح"
else
    echo ""
    echo "❌ حدث خطأ في تشغيل التطبيق"
    echo "جرب تشغيل العرض التوضيحي بدلاً من ذلك:"
    echo "python3 demo.py"
    echo ""
    echo "أو تحقق من المكتبات المطلوبة:"
    echo "pip3 install pandas matplotlib"
    echo "sudo apt install python3-tk  # لنظام Ubuntu/Debian"
fi
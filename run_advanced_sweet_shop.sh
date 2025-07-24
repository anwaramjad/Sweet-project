#!/bin/bash

echo ""
echo "🍰 نظام إدارة محل الحلويات - النسخة المتطورة"
echo "============================================="
echo ""
echo "جاري تشغيل التطبيق المحدث..."
echo ""

# التحقق من وجود Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 غير مثبت! يرجى تثبيت Python 3.7 أو أحدث"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip python3-tk"
    echo "macOS: brew install python3 python-tk"
    exit 1
fi

# التحقق من وجود الملفات المطلوبة
if [ ! -f "sweet_shop_advanced.py" ]; then
    echo "❌ لم يتم العثور على ملف sweet_shop_advanced.py"
    echo "تأكد من وجود جميع ملفات المشروع في هذا المجلد"
    exit 1
fi

# تثبيت tkinter إذا لم يكن متوفراً
echo "التحقق من المكتبات المطلوبة..."
if command -v apt &> /dev/null; then
    if ! python3 -c "import tkinter" 2>/dev/null; then
        echo "جاري تثبيت tkinter..."
        sudo apt update > /dev/null 2>&1
        sudo apt install -y python3-tk > /dev/null 2>&1
    fi
fi

# تثبيت المكتبات المطلوبة
echo "جاري تثبيت المكتبات المطلوبة..."
echo ""
pip3 install pandas matplotlib reportlab Pillow

# التحقق من نجاح التثبيت
if [ $? -ne 0 ]; then
    echo "⚠️  حدث خطأ في تثبيت بعض المكتبات"
    echo "سيتم المحاولة بطريقة أخرى..."
    pip3 install --user pandas matplotlib reportlab Pillow
fi

echo ""
echo "✅ تم تثبيت المكتبات بنجاح"
echo ""
echo "🚀 جاري تشغيل نظام إدارة محل الحلويات المتطور..."
echo ""
echo "المميزات الجديدة:"
echo "✓ نظام تسجيل دخول آمن"
echo "✓ تصميم جميل ومتجاوب"
echo "✓ طباعة الفواتير بصيغة PDF"
echo "✓ واجهة مستخدم محسنة"
echo ""

# تشغيل التطبيق
if python3 sweet_shop_advanced.py; then
    echo ""
    echo "تم إغلاق التطبيق بنجاح"
else
    echo ""
    echo "❌ حدث خطأ في تشغيل التطبيق"
    echo ""
    echo "تأكد من:"
    echo "1. تثبيت Python 3.7 أو أحدث"
    echo "2. تثبيت جميع المكتبات المطلوبة"
    echo "3. وجود جميع ملفات المشروع"
    echo ""
    echo "أو جرب التشغيل اليدوي:"
    echo "python3 sweet_shop_advanced.py"
    echo ""
fi

echo ""
echo "شكراً لاستخدام نظام إدارة محل الحلويات! 🍰"
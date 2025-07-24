@echo off
chcp 65001
echo.
echo 🍰 نظام إدارة محل الحلويات
echo ========================
echo.
echo جاري تشغيل التطبيق...
echo.

REM التحقق من وجود Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت! يرجى تثبيت Python 3.7 أو أحدث
    echo يمكنك تحميله من: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM التحقق من وجود الملفات المطلوبة
if not exist "sweet_shop_sqlite.py" (
    echo ❌ لم يتم العثور على ملف sweet_shop_sqlite.py
    echo تأكد من وجود جميع ملفات المشروع في هذا المجلد
    pause
    exit /b 1
)

if not exist "sweet_shop.db" (
    echo ⚠️  لم يتم العثور على قاعدة البيانات
    echo جاري إنشاء قاعدة البيانات الجديدة...
    if exist "add_test_customers.py" (
        python add_test_customers.py
    ) else (
        echo ❌ لم يتم العثور على ملف add_test_customers.py
        pause
        exit /b 1
    )
)

REM تثبيت المكتبات المطلوبة
echo جاري تثبيت المكتبات المطلوبة...
pip install pandas matplotlib >nul 2>&1

REM تشغيل التطبيق
echo.
echo ✅ جاري تشغيل نظام إدارة محل الحلويات...
echo.
python sweet_shop_sqlite.py

REM في حالة فشل التشغيل
if errorlevel 1 (
    echo.
    echo ❌ حدث خطأ في تشغيل التطبيق
    echo جرب تشغيل العرض التوضيحي بدلاً من ذلك:
    echo python demo.py
    echo.
    pause
)
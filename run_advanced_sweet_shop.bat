@echo off
chcp 65001 >nul
echo.
echo 🍰 نظام إدارة محل الحلويات - النسخة المتطورة
echo =============================================
echo.
echo جاري تشغيل التطبيق المحدث...
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
if not exist "sweet_shop_advanced.py" (
    echo ❌ لم يتم العثور على ملف sweet_shop_advanced.py
    echo تأكد من وجود جميع ملفات المشروع في هذا المجلد
    pause
    exit /b 1
)

REM تثبيت المكتبات المطلوبة
echo جاري تثبيت المكتبات المطلوبة...
echo.
pip install pandas matplotlib reportlab Pillow

REM التحقق من نجاح التثبيت
if errorlevel 1 (
    echo ⚠️  حدث خطأ في تثبيت بعض المكتبات
    echo سيتم المحاولة بطريقة أخرى...
    pip install --user pandas matplotlib reportlab Pillow
)

echo.
echo ✅ تم تثبيت المكتبات بنجاح
echo.
echo 🚀 جاري تشغيل نظام إدارة محل الحلويات المتطور...
echo.
echo المميزات الجديدة:
echo ✓ نظام تسجيل دخول آمن
echo ✓ تصميم جميل ومتجاوب  
echo ✓ طباعة الفواتير بصيغة PDF
echo ✓ واجهة مستخدم محسنة
echo.

REM تشغيل التطبيق
python sweet_shop_advanced.py

REM في حالة فشل التشغيل
if errorlevel 1 (
    echo.
    echo ❌ حدث خطأ في تشغيل التطبيق
    echo.
    echo تأكد من:
    echo 1. تثبيت Python 3.7 أو أحدث
    echo 2. تثبيت جميع المكتبات المطلوبة
    echo 3. وجود جميع ملفات المشروع
    echo.
    echo أو جرب التشغيل اليدوي:
    echo python sweet_shop_advanced.py
    echo.
    pause
)

echo.
echo شكراً لاستخدام نظام إدارة محل الحلويات! 🍰
pause
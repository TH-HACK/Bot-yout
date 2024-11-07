# استخدام صورة PHP
FROM php:8.1-cli

# تثبيت مكتبة cURL المطلوبة
RUN apt-get update && apt-get install -y curl

# تعيين المجلد الافتراضي للتطبيق
WORKDIR /app

# نسخ كافة ملفات المشروع إلى المجلد
COPY . /app

# فتح المنفذ 8000
EXPOSE 8000

# تشغيل خادم PHP
CMD ["php", "-S", "0.0.0.0:8000", "-t", "/app"]

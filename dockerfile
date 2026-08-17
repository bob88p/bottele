FROM python:3.12-slim

WORKDIR /app

# 1. نزل المكتبات الأساسية بس
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. انسخ كود البوت
COPY src/ ./src/

# 3. متغيرات البيئة
ENV PYTHONUNBUFFERED=1

# 4. شغل البوت
CMD ["python", "-m", "src.bot"]
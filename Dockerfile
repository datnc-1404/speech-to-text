# Sử dụng image Python chính thức làm base
FROM python:3.9-slim

# Thiết lập thư mục làm việc bên trong container
WORKDIR /app

# Sao chép file requirements.txt vào container và cài các package
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Expose cổng 7026 để ứng dụng Flask có thể lắng nghe
EXPOSE 7026

# Chạy ứng dụng Flask
CMD ["python", "app.py"]

# Bắt đầu từ image chính thức của Python
FROM python:3.9-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy tất cả các file từ thư mục hiện tại vào thư mục /app trong container
COPY . /app

# Cài đặt các thư viện cần thiết từ file requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mở cổng (nếu ứng dụng sử dụng web, ví dụ như Flask sẽ mặc định chạy trên cổng 5000)
EXPOSE 5000

# Lệnh chạy ứng dụng
CMD ["python", "main.py"]

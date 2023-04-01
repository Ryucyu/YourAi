FROM node:latest as builder
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build
FROM nginx:latest
COPY nginx.conf /etc/nginx
COPY --from=builder /app/dist  /usr/share/nginx/html

FROM python:3.9.5
# 设置工作目录
WORKDIR /app
# 复制 requirements.txt 文件并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# 复制项目代码
COPY . .
# 数据库迁移
RUN python manage.py makemigrations
# 设置环境变量
ENV PYTHONUNBUFFERED=1
CMD ["python", "manage.py", "runserver", "0.0.0.0:7999" ]
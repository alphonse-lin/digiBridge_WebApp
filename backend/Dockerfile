FROM python:3.9.7-slim

WORKDIR /app

# 安装系统依赖和 Java
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    openjdk-11-jdk \
    && rm -rf /var/lib/apt/lists/*

# 设置 JAVA_HOME 环境变量
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ENV PATH $JAVA_HOME/bin:$PATH

# 复制并安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 验证 Java 安装（可选，用于调试）
RUN java -version

CMD ["flask", "run"]
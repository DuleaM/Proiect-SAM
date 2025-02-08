FROM python:3.13-slim

WORKDIR /app

COPY . /app
COPY requirements.txt /app

RUN apt-get update && \
    apt-get install -y default-mysql-server pkg-config default-libmysqlclient-dev build-essential curl python3-dev gcc wget unzip \
    fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcairo2 libcups2 libdbus-1-3 libgbm1 libgtk-3-0 libgtk-4-1 \
    libnspr4 libnss3 libpango-1.0-0 libvulkan1 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils \
    python3 python3-pip

# Install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -f -y

RUN apt-get install -f

# Install ChromeDriver
RUN wget https://chromedriver.storage.googleapis.com/92.0.4515.107/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver

RUN pip3 install --upgrade pip && \
    pip3 install --upgrade setuptools && \
    pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

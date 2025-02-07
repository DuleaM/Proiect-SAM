FROM ubuntu:22.04

WORKDIR /app

COPY requirements.txt /app/


RUN apt-get update && \
    apt-get install -y default-mysql-server pkg-config default-libmysqlclient-dev build-essential curl python3-dev gcc wget unzip

# Install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN sudo apt-get install -f

# Install ChromeDriver
RUN wget https://chromedriver.storage.googleapis.com/92.0.4515.107/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver

RUN pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "python webScrapper/manage.py makemigrations && python webScrapper/manage.py migrate && python webScrapper/manage.py runserver 0.0.0.0:8000"]
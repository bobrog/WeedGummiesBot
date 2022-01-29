FROM python:3.10.2
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY *.txt ./
COPY *.py ./
ENV VERSION=latest
ENTRYPOINT ["python", "-u", "./bot.py"]

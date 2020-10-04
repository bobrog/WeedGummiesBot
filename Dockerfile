FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY *.txt ./
COPY *.py ./
ENTRYPOINT ["python", "-u", "./bot.py"]

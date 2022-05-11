FROM python:3.9

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY assets aux bot.py extensions config.yaml /

CMD [ "python", "bot.py" ]

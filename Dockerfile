FROM python:3.9

COPY requirements.txt .
RUN pip install -r requirements.txt

ADD src/ config.yaml .

CMD [ "python", "bot.py" ]

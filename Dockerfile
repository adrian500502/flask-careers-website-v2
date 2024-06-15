FROM python:3.12-slim
ENV APP_HOME=/app
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p $APP_HOME/instance

EXPOSE 8111
ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=8111"]

FROM python:3.13.3-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY "URL Redirection Service" ./

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]

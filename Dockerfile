FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt ./

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install -r requirements.txt

COPY . .

ENV PORT=8080

EXPOSE 8080

CMD ["uvicorn", "server:app", "--port", "8080", "--host", "0.0.0.0"]
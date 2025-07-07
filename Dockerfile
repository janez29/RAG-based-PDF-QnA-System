FROM python:3.9-slim
RUN apt-get update && apt-get install -y git
WORKDIR /app
cd /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
CMD ['uvicorn','app.main:app','--host','0.0.0.0','--port','8000']

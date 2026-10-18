FROM python:3.8-slim
WORKDIR /app
COPY app.py /app/app.py
RUN pip install --no-cache-dir Flask==2.0.3 Werkzeug==2.0.3
EXPOSE 5000
CMD ["python", "app.py"]


FROM python:3.10-slim
WORKDIR /app
COPY app.py .
COPY templates ./templates
RUN pip install flask
EXPOSE 80
CMD ["python", "app.py"]

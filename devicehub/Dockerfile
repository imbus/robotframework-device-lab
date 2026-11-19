# Der Mock als Container, nur für Jenkins (lokal reicht: just sim). Versionen wie in uv.lock.
FROM python:3.14-slim
RUN pip install --no-cache-dir fastapi==0.163.2 fastapi-offline==1.7.7 uvicorn==0.54.0
WORKDIR /app
COPY *.py devicehub/
CMD ["uvicorn", "devicehub.app:app", "--host", "0.0.0.0", "--port", "8080"]

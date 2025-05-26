FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install flask requests

EXPOSE 6789

CMD ["python", "sample_app.py"]

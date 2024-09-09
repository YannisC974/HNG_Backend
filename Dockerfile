FROM python:3.10
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
# Create directories for media
RUN mkdir -p /app/media
COPY . /code 

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
FROM python:3.10
WORKDIR /app
COPY . /app
VOLUME /app//download
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
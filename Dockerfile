FROM python:3.10
WORKDIR /app
COPY . /app
VOLUME /app//download
RUN pip install flask
EXPOSE 5000
CMD ["python", "app.py"]

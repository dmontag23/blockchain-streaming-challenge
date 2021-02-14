FROM python:3.7.9-slim-stretch
WORKDIR /app
COPY . /app
RUN mkdir -p db
ENTRYPOINT ["python"]
CMD ["main.py"]
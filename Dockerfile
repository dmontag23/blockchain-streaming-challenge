FROM python:3.7.9-slim-stretch
COPY src /src
WORKDIR /src
ENTRYPOINT ["python"]
CMD ["main.py"]
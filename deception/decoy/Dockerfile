FROM python:3.11-slim

WORKDIR /decoy

COPY . /decoy

EXPOSE 8080

CMD ["python", "-m", "http.server", "8080", "--directory", "/decoy"]
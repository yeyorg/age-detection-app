FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir uv

CMD ["uv", "run", "python", "-c", "print('Backend scaffold ready')"]

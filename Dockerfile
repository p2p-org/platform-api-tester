FROM python:3.10

WORKDIR /platform-api-tester
ENV TESTNET_API_KEY=${TESTNET_API_KEY}
ENV MAINNET_API_KEY=${MAINNET_API_KEY}
ENV METRICS_PREFIX="platform_api_tester_"
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY config ./config

EXPOSE 8080

CMD ["python", "src/main.py"]

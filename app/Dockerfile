ARG PYTHON_VERSION=3.9-alpine
FROM python:${PYTHON_VERSION} AS builder
LABEL stage=builder
WORKDIR /app
COPY pyproject.toml requirements.txt /app/

RUN pip install --no-cache-dir wheel
RUN pip wheel --no-cache-dir -r requirements.txt -w /wheels

FROM python:${PYTHON_VERSION} AS runner
LABEL stage=runner

WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels
COPY app.py /app/
EXPOSE 8000
ENTRYPOINT ["uvicorn", "app:app"]
CMD ["--host", "0.0.0.0", "--port", "8000"]

FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (for layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY src/ ./src/

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

EXPOSE 8080

CMD ["python", "-m", "src.bot"]
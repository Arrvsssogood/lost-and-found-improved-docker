# ─── Finders Keepers — Dockerfile ───────────────────
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Create uploads folder if it doesn't exist
RUN mkdir -p app/static/uploads

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]

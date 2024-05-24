# Start with official python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements.txt file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set PYTHONPATH
ENV PYTHONPATH="/app/src"

# Expose port where application is running
EXPOSE 8000

# Execute the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

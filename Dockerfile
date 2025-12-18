FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Copy application files
COPY server.py .
COPY .env .

# Run the server with stdio transport
CMD ["python3", "server.py"]

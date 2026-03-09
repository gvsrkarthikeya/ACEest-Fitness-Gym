# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy app files
COPY app.py ./
COPY program_data.py ./
COPY templates ./templates
COPY tests ./tests

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]

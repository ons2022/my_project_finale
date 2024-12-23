# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system-level dependencies for psycopg2
RUN apt-get update && apt-get install -y gcc libpq-dev

# Copy requirements.txt into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Debug: Show installed Python packages
RUN pip list

# Copy the rest of the application files
COPY . .

# Expose the Django development server port
EXPOSE 8000

# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

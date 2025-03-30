# FROM python:3-slim
# WORKDIR /usr/src/app
# COPY requirements.txt ./
# RUN python -m pip install --no-cache-dir -r requirements.txt
# COPY . .
# CMD [ "python", "./main.py" ]

# Dockerfile for the Flask App
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy files to the container
COPY /requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]

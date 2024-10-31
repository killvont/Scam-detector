# Use the official Ubuntu image
FROM ubuntu:latest

# Install Python, pip, and venv
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Set the working directory
WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt ./

# Create a virtual environment and install requirements
RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 5000

# Command to run the application
CMD ["venv/bin/python", "app.py"]

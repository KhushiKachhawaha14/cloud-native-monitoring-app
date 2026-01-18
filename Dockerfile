# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# 1. Update package lists
RUN apt-get update 

# 2. Install the C compiler (gcc) and Python development files (python3-dev)
RUN apt-get install -y gcc python3-dev 

# 3. Install any needed packages specified in requirements.txt (including gunicorn)
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
# This includes app.py and the 'templates' directory
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Run the application using Gunicorn (Production WSGI Server)
# This replaces 'CMD ["python", "app.py"]'
# -w 4: 4 worker processes (a standard starting point)
# -b 0.0.0.0:5000: binds to all interfaces on port 5000
# app:app: targets the Flask application instance named 'app' inside the 'app.py' file
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
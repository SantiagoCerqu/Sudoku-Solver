# Use the official Python image from Docker Hub
FROM python:3

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Specify the port number the container should expose
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the bot code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Command to run your bot
CMD python bot.py
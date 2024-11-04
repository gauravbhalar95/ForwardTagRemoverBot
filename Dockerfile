# Use the official Python image from Docker Hub
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file first for caching
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Set environment variables
ENV PORT=8080
ENV BOT_TOKEN=7268627071:AAHJXah9jXlZW_4hfzzs9JpY8j8J2ypDNjc
ENV WEBHOOK_URL=https://residential-renelle-telegrambotsearch-f9fa463c.koyeb.app/

# Expose the port the app runs on
EXPOSE 8080

# Command to run the bot
CMD python bot.py

# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /var/www/html/humanize

# Copy the current directory contents into the container at /app
COPY src/ /var/www/html/humanize/src
COPY main.py /var/www/html/humanize
COPY requirements.txt /var/www/html/humanize
COPY .env /var/www/html/humanize
#COPY generate_selfsigned.sh /var/www/html/humanize

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


#SSL generation, maybe change to certbot
# RUN chmod +x generate_selfsigned.sh
# RUN ./generate_selfsigned.sh

# Make port 80 available to the world outside this container
EXPOSE 8000

# Define environment variable
# ENV SECRET_KEY secret1

# Run app.py when the container launches
CMD ["python", "main.py"]

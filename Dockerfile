# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /humanize

# Copy the current directory contents into the container at /app
COPY . /humanize

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV SECRET_KEY 0349u,qgf[p0jtfp4903e[uj
ENV WS_URL http://localhost:5000/chat
ENV OPENAI_API_KEY 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 
ENV DATABASE_URI sqlite:///humanize.db

# Run app.py when the container launches
CMD ["python", "main.py"]

# Use an official Python runtime as a parent image
FROM python:3.10

# Update the package list and install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV DEBUG=False
ENV DB_HOST=192.168.211.10
ENV DB_PORT=3306
ENV DB_NAME=bengomall
ENV DB_USER=root
ENV DB_PASSWORD=root

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE ecommerce.settings

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

#COPY wait-for.py /bin/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

#collect static
RUN python manage.py collectstatic --noinput

# Expose the port that the application will run on
EXPOSE 8001

# Define the command to run your application
CMD ["gunicorn", "ecommerce.wsgi:application", "--bind", "0.0.0.0:8001"]

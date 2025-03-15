# Use Ubuntu as the base image
FROM ubuntu:latest

# Install required packages
RUN apt update && apt install -y python3 python3-pip python3-venv net-tools curl

# Set working directory
WORKDIR /app

# Create and activate virtual environment
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Upgrade pip and install dependencies
COPY requirements.txt /app/
COPY . /app/

RUN /app/venv/bin/pip install --upgrade pip && /app/venv/bin/pip install -r requirements.txt

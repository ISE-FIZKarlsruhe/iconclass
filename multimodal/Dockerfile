# Sets the base image for subsequent instructions
FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-dev
# Copies the files to the working directory
WORKDIR /app
COPY . /app
# Install dependencies
RUN pip3 install -r requirements.txt
# Command to run on container start    
CMD [ "python3" , "app.py" ]

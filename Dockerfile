# Build an debian image
FROM python:3.6

# Remove o delay do log
ENV PYTHONUNBUFFERED 1

# Install SO dependecies
RUN apt-get update && apt-get install -y vim && pip3 install --upgrade pip

# Create project folder
RUN mkdir /software

# Make /software main directory
WORKDIR /software

# Add requirements into /software folder
ADD ./project/requirements.txt /software

# Install dependencies
RUN pip3 install -r requirements.txt

# Insert everything into /software
ADD ./project/ /software

# Expose the port 8000
EXPOSE 8000

# Run the production script before and after any command
RUN chmod +x ./start.sh
ENTRYPOINT ["./start.sh"]
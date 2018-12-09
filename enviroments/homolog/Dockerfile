# Build an debian image
FROM python:3.6

# Update, Upgrade and configure locale
RUN apt-get update

# Install SO dependecies
RUN apt-get install -y python3-dev \
    python3-pip \
    libpq-dev \
    vim \
    build-essential

# Install pip dependecies
COPY requirements requirements
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements/requirements-dev.txt

ADD . /software
WORKDIR /software

# Insert Enviroment variable
ENV MODE_ENVIROMENT=development

# Run the dev script before and after any command
RUN chmod +x enviroments/homolog/homolog.sh
ENTRYPOINT ["enviroments/homolog/homolog.sh"]

# Expose 8000 port
EXPOSE 8080

# Run the server
CMD ["python3", "project/manage.py", "runserver", "0.0.0.0:8080"]
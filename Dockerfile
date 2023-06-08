# set the base image
FROM python:3.11.3

# specify a working directory
WORKDIR /webapp

# Set the following environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP app
ENV FLASK_ENV development

# install the necessary python modules
# inside the container
# this is where the requirements.txt
# comes in handy
RUN pip install --upgrade pip
COPY requirements.txt /webapp
RUN pip install -r requirements.txt

# now, we copy the contents of our
# Django project directory over to the container

COPY . /webapp/

# venv is not required in the container
# so we remove the venv directory
# NB: in Docker, no way to copy everything except venv dir

RUN rm -r venv/

# set the authors label
LABEL authors="mmbil"

# finally, run the server for our project
# inside the container
# note: need to specify 0.0.0.0
# as our host (0.0.0.0 = wildcard address; matches any host)

CMD python -m flask run -h 0.0.0.0 -p 8080
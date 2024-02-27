# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.9.0

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1


# Set the working directory to /drf
# NOTE: all the directives that follow in the Dockerfile will be executed in
# that directory.
WORKDIR /usr/src/hiker

RUN ls .
COPY requirements.txt /usr/src/req.txt
# Install any needed packages specified in requirements.txt
RUN pip install -r /usr/src/req.txt

COPY . /usr/src/hiker

VOLUME /drf_src

#EXPOSE 8080

#CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
# CMD ["%%CMD%%"]
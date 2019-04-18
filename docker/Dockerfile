# Set Base image
FROM python:3.6.5-slim

# Set Maintainer
LABEL maintainer="Victor Nwokeocha"

# Python unbuffered env and python dont write byte code variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Upgrade and install pipenv
RUN pip install --upgrade pip && pip install pipenv

# Make and cd into a dir to store app source code
RUN mkdir /api-trixbuy
WORKDIR /api-trixbuy

# Copy the pipfiles to the work directory.
COPY ./Pipfile /api-trixbuy
COPY ./Pipfile.lock /api-trixbuy

# Install dependencies
RUN pipenv install --system --deploy --ignore-pipfile

# Copy all the other files/folders to airtech-api
COPY . /api-trixbuy

RUN chmod +x /api-trixbuy/docker/start.sh

# Create a user to run the app on docker
# Necessary for security reasons
RUN useradd -r -u 1234 -U docker-user

USER docker-user

EXPOSE 9000

CMD sh docker/start.sh

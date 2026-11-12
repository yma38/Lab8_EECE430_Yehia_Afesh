# Image 1 - Lab 5 "Postman and APIs" (CRUD on users) running on port 5000

# start by pulling the python image
FROM python:3.12-alpine

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# copy every content from the local folder to the image
COPY . /app

# document the port the Flask app listens on inside the container
EXPOSE 5000

# start the app
CMD ["python3", "app.py"]
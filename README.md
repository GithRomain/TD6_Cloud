# TD6

Created: February 24, 2023 3:06 PM
Person: Romain Pasquier
Tags: Dockerfile, bind, docker, docker-compose, flask, mount, python, volumes

# Creating a Simple Docker App with Python and Flask

In this tutorial, we will create a simple Docker app using Python and Flask. Docker is a popular platform for containerization, which allows developers to package and run their applications in a self-contained environment.

## Prerequisites

Before we begin, make sure you have the following installed on your system:

- Docker
- Python
- Flask

## Creating the Flask App

Let's start by creating a simple Flask app. Open your favorite text editor and create a new file called `app.py`. Add the following code to the file:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

# Start the Flask application if this file is being executed as the main script
if __name__ == "__main__":
    # Start the Flask application, listening on all available interfaces
    app.run(host="0.0.0.0"
```

This code creates a new Flask app and defines a single route that returns a "Hello, World!" message.

## Creating the Dockerfile

Next, we need to create a Dockerfile that will define our app's environment. In the same directory as `app.py`, create a new file called `Dockerfile`. Add the following code to the file:

```docker
FROM python:latest
WORKDIR /app
COPY . ./
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
```

This Dockerfile starts from the official Python 3.8 image, sets the working directory to `/app`, copies the `requirements.txt` file to the container, installs the dependencies, copies the rest of the files to the container, and finally runs the `app.py` script.

Here is the content of the `requirements.txt` file:

```
Flask
```

This file specifies the dependencies required by our Flask app, which in this case is just Flask itself.

## Building the Docker Image

Now that we have our app and Dockerfile ready, we can build the Docker image. Open your terminal and navigate to the directory where your `app.py` and `Dockerfile` files are located. Run the following command:

```
docker build -t my-flask-app .
```

This command tells Docker to build a new image based on the `Dockerfile` in the current directory and tag it as `my-flask-app`.

## Running the Docker Container

To run the Docker container, execute the following command:

```
docker run -p 5000:5000 my-flask-app
```

This command tells Docker to run a new container based on the `my-flask-app` image and map port `5000` from the container to port `5000` on the host machine.

## Accessing the App

Open your web browser and navigate to `http://localhost:5000/`. You should see the "Hello, World!" message displayed.

Congratulations! You have created a simple Docker app using Python and Flask.

## Part 1: Without using docker-compose

### Step 1:

To add the feature of reading a text file on your host and showing the content on a web page, you'll need to modify the Flask app in `app.py`

Next, modify the `hello()` function to read the contents of a text file and render it in an HTML template. Here's the updated code:

```python
@app.route('/')
def hello():
    with open('file.txt', 'r') as f:
        content = f.read()
    return content
```

This code opens a file called `file.txt`, reads its contents, and write on the web page the content.

### Step 2:

Finally, we need to modify our Dockerfile to include the `file.txt` file as a bind mount. Add the following line to the end of your Dockerfile:

```docker
VOLUME /app
```

This line creates a volume called `/app` in the container.

Now, when we run the Docker container, we need to mount the `file.txt` file to the `/app` volume. Modify the `docker run` command to include the `-v` flag:

```
docker run -d -p 5000:5000 -v /Users/romainpasquier/Documents/ESILV/CloudComputing/TD6/file.txt:/app/file.txt my-flask-app
```

This command tells Docker to mount the `file.txt` file on the host machine to the `/app/file.txt` file inside the container.

Now, any changes to the `file.txt` file on the host machine will be reflected in the Flask app when you refresh the web page.

Congratulations! You have added a feature to your Docker app that reads a text file on the host and displays its contents on a web page.

## Adding MongoDB to the Docker App

To add MongoDB to our Docker app, we will need to modify our `app.py` file, `Dockerfile`, and `requirements.txt` file.

### Modifying DockerFile with env variable

```python
FROM python:latest
WORKDIR /app
COPY app.py .
COPY requirements.txt .
RUN pip3 install -r requirements.txt
EXPOSE 5000
VOLUME /app
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
```

### Modifying `app.py`

First, let's modify our Flask app to connect to a MongoDB database. Add the following code to the top of your `app.py` file:

```python
from flask import Flask
from pymongo import MongoClient

# Create a Flask application instance
app = Flask(__name__)

# Connect the database
client = MongoClient("mongodb://mongodb:27017/")

db = client.td6db

collection = db.td6_collection

app = Flask(__name__)

# Insert data in mongodb
documents = [{"name": "Jane Doe", "age": 25}, {"name": "Jim Smith", "age": 35}]
collection.insert_many(documents)

@app.route('/')
def hello():
    # Fetch all document from the test_collection
    data = list(collection.find({}))
    with open('file.txt', 'r') as f:
        content = f.read()
#    return content
    return str(data) + "\n" + content

# Start the Flask application if this file is being executed as the main script
if __name__ == "__main__":
    # Start the Flask application, listening on all available interfaces
    app.run(debug=True, host="0.0.0.0")
```

This code imports the `MongoClient` class from the `pymongo` package, creates a new client connected to a MongoDB container called `mongo` on port `27017`

### Modifying `requirements.txt`

Next, we need to add the `pymongo` package to our `requirements.txt` file. Add the following line to the file:

```
Flask
Pymongo
```

# Create network

The next step is to create a network to connect the Flask app to the MongoDB container. In the terminal, run the following command to create a network:

```
docker network create my-network
```

This command creates a new Docker network called `my-network`.

Add the following line to your Dockerfile to specify that the container should be connected to the network:

Now, you can build and run the Docker image as described in the tutorial to add MongoDB to your Docker app.

# Create mongo container and volumes

```bash
docker run -d --name mongodb --network my-network -p -v /Users/romainpasquier/Documents/ESILV/CloudComputing/TD6/db:/data/db mongo:latest
```

# Run app :

```bash
docker run -d --network my-network -p 5000:5000 -v /Users/romainpasquier/Documents/ESILV/CloudComputing/TD6/file.txt:/app/file.txt tp6-flask
```

All works :

![Untitled](Export-b29d5315-125c-49e0-a380-8aac36ad513a/TD6 f0bca9de8eeb4dcd858f3200239693c7/Untitled.png)

And if I modify the txt file it modify the end of the string

# Migration

To migrate a MongoDB container with an existing volume, you can use the `docker export` command to export the container's data as a tar archive, and then use the `docker import` command to import the data into a new container.

If you want to migrate in local you can just bind the previous db volume to your new mongo container.

Here are the steps to migrate a MongoDB container properly:

1. Stop the MongoDB container: `docker stop mongodb`
2. Export the container's data as a tar archive:

```
docker export mongodb > mongodb.tar
```

1. Create a new MongoDB container with the same volume:

```
docker run -d --name mongodb-new -v db:/data/db mongo:latest
```

1. Import the data from the tar archive into the new container:

```
cat mongodb.tar | docker import - mongodb-new
```

1. Verify that the new container has the data:

```
docker run -it --rm --volumes-from mongodb-new busybox ls /data/db
```

To share the migrated MongoDB container with another instance of the same database engine, you can push the container to a Docker registry and then pull it on the other instance.

Here are the steps to share the migrated MongoDB container:

1. Push the container to a Docker registry:

```
docker tag mongodb-new myregistry.com/mongodb-new
docker push myregistry.com/mongodb-new
```

1. On the other instance of the database engine, pull the container from the Docker registry:

```
docker pull myregistry.com/mongodb-new
```

1. Start the container:

```
docker run -d --name mongodb-new -v db:/data/db myregistry.com/mongodb-new
```

## Part 2: Using docker-compose

### Step 1:

Create a new file in the same directory as `app.py` and `Dockerfile` called `docker-compose.yaml`. Add the following code to the file:

```docker
version: '3'
services:
    web:
        build: .
        ports:
            - "5000:5000"
        volumes:
            - ./file.txt:/app/file.txt
    mongodb:
        image: mongo:latest
        volumes:
            - ./db:/data/db
```

This code defines two services: `web` and `mongo`. The `web` service builds the Docker image defined in the current directory (`.`) and maps port `5000` from the container to port `5000` on the host machine. It also mounts the `file.txt` file on the host machine to the `/app/file.txt` file inside the container. The `mongo` service uses the official `mongo` image and maps port `27017` from the container to port `27017` on the host machine. It also creates a new volume called `td6db-data` to store the MongoDB data.

### Step 2:

Now, run the following command to start the Docker containers:

```bash
docker-compose up -d
```

This command tells Docker Compose to start the containers defined in the `docker-compose.yaml` file. The `-d` flag can be added to run the containers in the background.

You should now be able to access the Flask app by navigating to `http://localhost:5000/` in your web browser.

Congratulations! You have created a Docker app using Python, Flask, and MongoDB, and used Docker Compose to simplify the process of running multiple containers.
# DevOps Web Test App

## Project Overview
This is a simple Flask web application designed as a DevOps test project. It demonstrates:

- Displaying a static message: "Hello World"
- Showing current date & time
- Showing current CPU and RAM usage
- Dynamic background color, based on user-selected colors
- Runtime configuration without rebuilding the Docker image

The project is **Dockerized** and can be run via **Docker Compose**. User-selected colors are persisted in a config file (`config/colors.json`) and can be modified at runtime.

## how to run Web App
$ sudo apt install docker.io
$ sudo apt install docker-compose
$ chmod +x run.sh
$ sudo ./run.sh

warning: this app use port 5000 to serving Web so port 5000 must be free or change the app port

## auther
Mohammad Mahdi Kharaghani


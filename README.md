# Container Deployment for Redis & Mysql

## Requirement
Deploy Redis locally using a Docker container

Create a docker image based on the official mysql docker image which creates a table with columns ID-int, Key-varchar, Value-varchar

Develop a small python CLI and put in a docker image. The CLI must:

    - connect to Redis database and write keys in it
    Example run:
        python program.py write_keys --redis-addr <addr to redis deployment> - this needs to write 100 keys in Redis
        Keys example:
            key = test_key_0
            value = test_value_0
            key = test_key_1
            value = test_value_1
            .
            .
            .
    - Read keys from Redis and save them in a mysql db
        python program.py move_keys --redis-addr <addr to redis deployment> --mysql-addr <addr to mysql deployment> - this needs to get all redis keys and save them in a mysql table as
        ID | Key | Value
        0  | test_key_0 | test_value_0
        1  | test_key_1 | test_value_1
        2  | test_key_2 | test_value_2
        .
        .
        .
    - Must use Redis and Mysql deployed in docker containers
    - Must be in python 3.8+

## Tech

Application is using following libraries:

* **Typer** - library for building CLI applications Based on Python type hints.
* **Redis** - in-memory data structure store, used as a distributed, in-memory key–value database, cache and message broker, with optional durability. 
* **MySql** - relational database management system. 

## Installation
Once cloned on your local machine. Use to following commands to run the application.
```sh
$ cd redis_mysql_deployment
$ docker compose up -d
```
Now the containers is all set. All you have to do is run the app inside myapp container

make sure redis and mysql container is already running using `docker ps`

this will show something like this
```sh
CONTAINER ID   IMAGE                          COMMAND                  CREATED         STATUS         PORTS                                                  NAMES
e43262873769   redis_mysql_deployment_myapp   "tail -f /dev/null"      2 minutes ago   Up 2 minutes                                                          deployment_myapp
fdabcc82f724   redis_mysql_deployment_mysql   "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes   0.0.0.0:3306->3306/tcp, :::3306->3306/tcp, 33060/tcp   deployment_mysql
a612c884b1b8   redis_mysql_deployment_redis   "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes   0.0.0.0:6379->6379/tcp, :::6379->6379/tcp              deployment_redis
```

## Running the app

Write key into Redis
```sh
docker exec deployment_myapp python program.py write-keys --redis-addr deployment_redis:6379
```

Retrieve key and value from redis, then save it into mysql
```sh
docker exec deployment_myapp python program.py move-keys --redis-addr deployment_redis:6379 --mysql-addr deployment_mysql
```

This directory contains the necessary configurations to deploy a PostgreSQL database container that comes pre-populated with the OMDB movie dataset.

## Docker Compose Setup

We use Docker Compose to define and run multi-container Docker applications. In this case, we'll run a PostgreSQL database container.

To start the PostgreSQL container, you need Docker installed on your machine. If you don't have it already, you can download Docker from here: [Docker Downloads](https://www.docker.com/products/docker-desktop)

Once you have Docker installed and running, navigate to this directory (`database`) in your terminal and run the following command:

```bash
docker-compose up -d
```

This command will pull the necessary Docker images (if they aren't already on your machine), create the container, and start the PostgreSQL service.

## OMDB Dataset

The database is populated with the Open Movie Database (OMDB) dataset, which provides a comprehensive list of movie-related data. For further details about this dataset, you can visit the official OMDB repository here: [OMDB on GitHub](https://github.com/credativ/omdb-postgresql)

The PostgreSQL container comes pre-configured with this dataset, meaning you don't need to manually load the data. Once the container is up and running, you can start querying the database to retrieve the data.

## Connecting to the Database

To connect to the PostgreSQL container from your application or for testing, use the following credentials:

```bash
Host: localhost
Port: 5432
User: postgres
Password: password
Database: omdb
```

**Note**: These are default credentials for local development. For any production use, please ensure to follow best security practices, including using secure passwords and managing them safely.


# Dozer Authorization Sample - Movie Ticket Booking App

This repository contains a sample application demonstrating the power of Dozer's data API authorization capabilities. Dozer simplifies the task of adding an authorization layer to your data APIs. One method it employs is the use of JSON Web Tokens (JWT), a widely accepted industry standard for secure claim representation between two parties.

In this sample, we are building a straightforward movie ticket booking app, which defines two roles: user (public) and admin. The user can book tickets and view their bookings, while the admin has complete access to all APIs.

## Getting Started

1. Clone the `dozer-samples` repository and change the directory to the project directory:

 ```bash
git clone git@github.com:getdozer/dozer-samples.git && cd dozer-samples/usecases/api-auth/
 ```

2. Start the PostgreSQL database which contains the movie dataset. The Docker Compose file is under the `database` folder:

```bash
cd database
docker-compose up -d
cd ..
```

3. Generate a master token for auth by running the command from the project root directory where `dozer-config.yaml` is located:
```bash
dozer api generate-token
```

4. Copy the `MASTER_TOKEN` generated from the previous step and export the `MASTER_TOKEN` as an environment variable
```bash
export MASTER_TOKEN=your_token_here
```

5. Start the Dozer app. Dozer will start running, handling the data operations and APIs authorization as defined in your configuration. To do this, simply run the command:

```bash
dozer
```

6. Open the new terminal and change the directory to the `server` folder and install required package dependencies:
```bash
cd server && yarn install
```


7. Run the server app:
```bash
 node index.js
```
 The server app takes care of the user login feature and passes the auto-generated auth token with the master token to subsequent requests to the client app while communicating

8. In a new terminal, navigate to the `client` directory, install client dependencies and start the app:
    ```bash
    cd ../client && yarn install && yarn start
    ```
Go to [localhost:3000](localhost:3000) to see the user side view of the app that lets you book the ticket.
To see the admin dashboard go to [localhost:3000/admin/dashboard](localhost:3000/admin/dashboard). Enter username and password as "admin" to see the real-time updates on ticket sales.

> Note: Always ensure that your `MASTER_TOKEN` is kept secure. Do not commit this information to your version control system.

## About JWT

JWT is a compact, URL-safe means of representing claims to be transferred between two parties. You can find more about JWT [here](https://jwt.io/introduction/).



## Additional Information

If you encounter any issues or have suggestions, please file an issue in the [issue tracker](https://github.com/getdozer/dozer-samples/issues) on our Github page or reach out to us on [discord](https://discord.com/invite/3eWXBgJaEQ).

Happy coding with Dozer!

## Contributing

We love contributions! Please check our [Contributing Guidelines](../../community-samples/README.md) if you're interested in helping!

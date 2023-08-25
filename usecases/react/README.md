# Getting Started with Dozer React Cloud example

## Prerequisites

Before you start, ensure you have the following:

- Node.js and npm installed.
- Yarn package manager.
- An account and credentials for your chosen cloud platform (replace `<cloud-provider>`).

## Cloud Deployment Steps

1. Navigate to the `usecases/pg-flights` directory in your terminal:

    ```bash
    cd ../pg-flights
    ```

2. Run the following command to deploy the default configuration dozer-config.yaml to the cloud:

    ```bash
    dozer cloud deploy
    ```
    
This command will deploy the config file to the cloud, and a new config file named dozer-config.cloud.yaml will be generated. This new config file contains the application ID.

3. Open the newly generated dozer-config.cloud.yaml file and locate the app_id field. Copy the value of the app_id.

4. In the src directory of your this project, find the config.js file and paste the copied app_id value in place of DOZER_APP_ID. This will connect your React app to the cloud-deployed application.

5. Navigate back to the root directory of your project, and run the following command to start the React app in development mode:

    ```bash
    yarn start
    ```

6. Open your browser and visit [http://localhost:3000](http://localhost:3000) to view the React app.

7. The React UI is now linked with the cloud-deployed application. As you make changes to the project code, the page will automatically reload to reflect those changes. Any lint errors will also be displayed in the console.

## Data Sources and Endpoints

The project utilizes various data sources and endpoints defined in the `dozer-config.yaml` file. These include:

- `tickets`: Endpoint for booking tickets.
- `flights`: Endpoint for flight information.
- `airports`: Endpoint for airport details.
- `airports_flights_schema`: Endpoint for airport and flight schema.
- `ticket_flights`: Endpoint for ticket-flight associations.
- `airports_count`: Endpoint for counting airports and their coordinates.
- `departures_count`: Endpoint for counting flight departures.

You can access these endpoints in your React app to display relevant information.

Remember to keep the `dozer-config.yaml` file and the project directory structure consistent to ensure proper functionality.

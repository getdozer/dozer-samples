## Dozer Samples

This repository will contain a variety of samples showcasing [Dozer](https://github.com/getdozer/dozer).

#### Installing Dozer

Refer to the [Installation section](https://getdozer.io/docs/installation) for installing on different operating systems.

## Samples

| Type             | Sample                                                  | Notes                                                        |
| ---------------- | ------------------------------------------------------- | ------------------------------------------------------------ |
| Connectors       | [Postgres](./connectors/postgres)                       | Load data using Postgres CDC                                 |
|                  | [Local Storage](/connectors/local-storage)              | Load data from local files                                   |
|                  | [Snowflake](./connectors/snowflake)                     | Load data using Snowflake table streams                      |
| SQL              | [Using JOINs](./sql/join)                               | Dozer APIs over multiple sources using JOIN                  |
|                  | [Using Aggregations](/sql/aggregrations)                | How to aggregate using Dozer                                 |
|                  | [Using Window Functions](./sql/window-functions)        | Use `Hop` and `Tumble` Windows                               |
| Use Cases        | [Flight Microservices](./usecases/pg-flights)           | Build APIs over multiple microservices.                      |
|                  | [Use Dozer to Instrument](./usecases/instrument)        | Combine Log data to get real time insights                   |
|                  | [Real Time Model Scoring](./usecases/model-scoring)     | Deploy trained models to get real time insights as APIs      |
| Client Libraries | [Dozer React Starter](./clients/react-sample)           | Instantly start building real time views using Dozer and React |
|                  | [Python Ingestion Using Arrow](./clients/python-sample) | Use Python to instantly ingest arrow dataframes into Dozer   |
|                  | [Real Time Model Scoring](./usecases/model-scoring)     | Deploy trained models to get real time insights as APIs      |
| Authorization    | [Dozer Authorziation](./authorization/auth-sample)      | How to apply JWT Auth on Dozer APIs                          |



## Refeference

Refer to the following section on the main repository for the following references.
| Reference  | Notes                               |
| ---------- | ----------------------------------- |
| Connectors | Sample connnector config references |
| SQL        | Sample SQL using Dozer              |


## Contributing
Please refer to [Contributing](https://getdozer.io/docs/contributing/overview) for more details.


## Links

- [Documentation](https://getdozer.io/docs/dozer/)
- [Architecture](https://getdozer.io/docs/dozer/architecture)
- [Discord channel](https://discord.gg/3eWXBgJaEQ)


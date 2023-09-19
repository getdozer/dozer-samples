<div align="center">
    <a target="_blank" href="https://getdozer.io/">
        <br><img src="https://dozer-assets.s3.ap-southeast-1.amazonaws.com/logo-blue.svg" width=40%><br>
    </a>
</div>

<p align="center">
    <br />
    <b>
    Connect any data source, combine them in real-time and instantly get low-latency gRPC and REST APIs.<br>
    ⚡ All with just a simple configuration! ⚡️
    </b>
</p>
<br />

## Dozer Samples

This repository will contain a variety of samples showcasing [Dozer](https://github.com/getdozer/dozer).

#### Installing Dozer

Refer to the [Installation section](https://getdozer.io/docs/installation) for installing on different operating systems.

## Samples

| Type             | Sample                                                                   | Notes                                                                        |
| ---------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| Connectors       | [Postgres](./connectors/postgres)                                        | Load data using Postgres CDC                                                 |
|                  | [Local Storage](./connectors/local-storage)                              | Load data from local files                                                   |
|                  | [AWS S3](./connectors/aws-s3)                                            | Load data from AWS S3 bucket                                                 |
|                  | [Ethereum](./connectors/ethereum)                                        | Load data from Ethereum                                                      |
|                  | [Kafka](./connectors/kafka)                                              | Load data from kafka stream                                                  |
|                  | [Snowflake](./connectors/snowflake)                                                  | Load data using Snowflake table streams                                      |
| SQL              | [Using JOINs](./sql/join)                                                | Dozer APIs over multiple sources using JOIN                                  |
|                  | [Using Aggregations](./sql/aggregations)                                 | How to aggregate using Dozer                                                 |
|                  | [Using Window Functions](./sql/window-functions)                         | Use `Hop` and `Tumble` Windows                                               |
| Use Cases        | [Flight Microservices](./usecases/pg-flights)                            | Build APIs over multiple microservices.                                      |
|                  | [Scaling Ecommerce](./usecases/scaling-ecommerce)                        | Profile and benchmark Dozer using an ecommerce data set                      |
|                  | Use Dozer to Instrument (Coming soon)                                    | Combine Log data to get real time insights                                   |
|                  | Real Time Model Scoring (Coming soon)                                    | Deploy trained models to get real time insights as APIs                      |
| Client Libraries | [Dozer React Starter](./usecases/react/)                                 | Instantly start building real time views using Dozer and React               |
|                  | [Ingest Polars/Pandas Dataframes](./client-samples/ingest-python-sample) | Instantly ingest Polars/Pandas dataframes using Arrow format and deploy APIs |
| Authorization    | [Dozer Authorziation](./usecases/api-auth/README.md)                     | How to apply JWT Auth on Dozer APIs                                          |



## Reference

Refer to the following for an exhaustive list of configuration samples.
| Reference                                                       | Notes                              |
| --------------------------------------------------------------- | ---------------------------------- |
| [Connectors](https://getdozer.io/docs/configuration/connectors) | Sample connector config references |
| [SQL](https://getdozer.io/docs/sql/introduction)                | Sample SQL using Dozer             |


## Contributing
Please refer to [Contributing](https://getdozer.io/docs/contributing/overview) for more details.


## Links

- [Documentation](https://getdozer.io/docs/dozer/)
- [Architecture](https://getdozer.io/docs/dozer/architecture)
- [Discord channel](https://discord.gg/3eWXBgJaEQ)



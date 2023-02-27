## Dozer Samples

This repository will contain a variety of samples showcasing [Dozer](https://github.com/getdozer/dozer).


Each of the samples provide a `dozer-config.yaml` that could be used to start Dozer. 
Each folder also optionally contains a `docker-compose.yaml` for any data source support.

## Running Dozer
```bash
docker run -it \
  -v "$PWD":/usr/dozer \
  -p 8080:8080 \
  -p 50051:50051 \
  public.ecr.aws/k7k6x1d4/dozer \
  dozer -c dozer-config.yaml
```


## Samples

[Flight Booking Service and Postgres ](./pg-flights/README.md) 

This sample describes a pattern to deploy fast APIs out of multiple micro services taking the example of a flight booking service powered by Postgres.



## Contributing
Please refer to [Contributing](https://getdozer.io/docs/contributing/overview) for more details.


## Links

- [Documentation](https://getdozer.io/docs/dozer/)
- [Architecture](https://getdozer.io/docs/dozer/architecture)
- [Discord channel](https://discord.gg/3eWXBgJaEQ)


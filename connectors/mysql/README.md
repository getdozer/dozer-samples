## Dozer Cloud

1. Setup MYSQL database
2. Pass in the credentials in the config file
3. Run the following command to deploy the app on Dozer Cloud

```bash
dozer cloud deploy
```

### Deploy with environment variables

```bash
 dozer cloud deploy -s EC2_INSTANCE_DNS=$EC2_INSTANCE_DNS 
 ```


##  Query data on cloud

```bash
curl -H "x-dozer-app-id: <app-id" https://data.dev.getdozer.io:443 ```

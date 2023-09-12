# Ingesting data from AWS S3

This README provides a brief guide on how to set up Dozer for real-time data ingestion from an AWS S3 bucket. For a more comprehensive tutorial, please refer to our [blog post](https://getdozer.io/blog/Real-Time-Data-Ingestion-from-AWS-S3-using-Dozer-A-Comprehensive-Tutorial).

## Prerequisites
- AWS account with access to S3 services
- AWS CLI installed and configured
- Python installed
- Dozer installed

## Steps

1. **Generate and Upload Data to S3**: Use a Python script to generate a dataset and upload it to an S3 bucket.
 ```bash
 python create_dataset_and_upload_to_s3.py
 ```
If you already have a dataset in your S3 bucket, you can skip this step.

2. **Configure Dozer**: Create a YAML configuration file that defines the data sources, transformations, and APIs.
Checkout the sample Dozer configuration file  [dozer-config.yaml](dozer-config.yaml) that uses AWS S3 connector.

```yaml
connections:
  - config : !S3Storage
      details:
        access_key_id: {{YOUR_ACCESS_KEY}}
        secret_access_key: {{YOUR_SECRET_KEY}}
        region: {{YOUR_REGION}}
        bucket_name: aws-s3-sample-stock-data-dozer
      tables:
        - !Table
          name: stocks
          config: !CSV
            path: . # path to files or folder inside a bucket
            extension: .csv
    name: s3
```

3. **Running Dozer**: Start Dozer by running the following command in the terminal:

   ```bash
   dozer -c dozer-config.yaml
   ```

4. **Querying the Dozer APIs**: Query the Dozer endpoints to get the results of your SQL queries. You can query the cache using gRPC or REST.

   Example queries:
   ```bash
   # REST
   curl -X GET http://localhost:8080/analysis/ticker
   ```

5. **Append New Data & Query**: Dozer automatically detects and ingests new data files added to the bucket. This allows you to process recurring data without changing any configuration. You can upload a new file to the bucket and can see the dozer ingesting the newly uploaded files in console log.

## Dozer Cloud

```bash
dozer cloud`deploy -c dozer-config.yaml
```

### To use environment variables in the config file

```bash
dozer cloud deploy -s AWS_ACCESS_KEY=$AWS_ACCESS_KEY -s AWS_SECRET_KEY=$AWS_SECRET_KEY -s AWS_REGION_S3=$AWS_REGION_S3 -s AWS_BUCKET_NAME=$AWS_BUCKET_NAME
```

## Querying data

```bash
curl -H "x-dozer-app-id: <app-id" https://data.dev.getdozer.io:443  ```

## Additional Information

If you encounter any issues or have suggestions, please file an issue in the [issue tracker](https://github.com/getdozer/dozer-samples/issues) on our Github page or reach out to us on [discord](https://discord.com/invite/3eWXBgJaEQ).

Happy coding with Dozer!

## Contributing

We love contributions! Please check our [Contributing Guidelines](../../community-samples/README.md) if you're interested in helping!

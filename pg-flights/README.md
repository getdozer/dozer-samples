### Dozer Sample - Flight bookings
In this example, Dozer fetches data from multiple Postgres tables and combines them in real time based on the queries and produces fast READ APIs to be used in a flight booking application. 


This pattern is very much applicable even when the data is being fetched across micro services and even from different types of data stores. Check out Dozer documentation for all supported data sources. 

Please check out our blog for a [full explanation](https://getdozer.io/blog/microservices)

### Running 

```
docker-compose up
```

**NOTE**: [Git LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage) is needed when cloning this sample.

### Schema

![Image](images/schema.png)

### APIs 
| Path                  | Source  | Notes                                                                                          |
| --------------------- | ------- | ---------------------------------------------------------------------------------------------- |
| GET /bookings         | Derived | Booking Listing API. Filters are automatically generated on single columns. Eg: `passenger_id` |
| GET /bookings/details | Derived | Detailed information about a booking including flight information across several stops         |
| GET /routes           | Derived | All routes per day of the week based on all ticket bookings made                               |

### Configuration
Dozer generates end to end date pipeline + APIs just via configuration. Refer to the configuration for [this example here](./dozer-config.yaml)

###  Notes
[Sample data is from here](https://postgrespro.com/docs/postgrespro/10/demodb-bookings-installation)

You can download a bigger data set following the instructions on the above page. 

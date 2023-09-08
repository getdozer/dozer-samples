#IMDB - Analytics

## Experiment 2

Finding the actors or actresses with the most movies.

We run 2 cascading JOINs and a COUNT aggregation on the data source. The sql can be found in [`join-config.yaml`](../join-config.yaml).

![Experiement 2](../images/experiment_2_diagram.png)

```sql
 select p.name, c.category, count(1) as titles
 into endpoint1
 from people p 
 join crew c on p.person_id = c.person_id  
 join titles t on t.title_id = c.title_id  
 where category = 'actor' or category = 'actress' 
 group by p.name,c.category;
```

### Instructions
```
dozer clean -c exp2-config.yaml
dozer build -c exp2-config.yaml
dozer run app -c exp2-config.yaml
```

### Findings

![Insights](../images/exp2_source.png)

 - Roughly took `2 mins` to process all the records. 
 - Exp 2 took less time than Exp 1 even with a sql operation. This can be attributed to two reasons,
  - Less store operations due to one endpoint and less data outputted `103734` to be exact.
  - Less read operations from source due to data read from three tables. 
 - Pipeline latency stays under `0.25s` even with 2 joins and an aggregation.
 
| Start Time | End Time   | Elapsed   |
| ---------- | ---------- | --------- |
| 1:20:36 PM | 1:22:12 PM | ~ 2 mins  |
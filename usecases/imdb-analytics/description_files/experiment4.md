#IMDB - Analytics

## Experiment 3 lorem ipsum

Running `dozer` with multiple cte defined as well as multiple aggregation and join operations.

We run 3 cascading JOINs and a COUNT aggregation on the data source. The sql can be found in [`cte-config.yaml`](../cte-config.yaml).

```sql
select c.customer_id, c.name, c.email,  o.order_id, o.order_date, o.total_amount, COUNT(*)
  into customer_orders 
  from customers c
  inner join orders o on c.customer_id = o.customer_id
  join order_items i on o.order_id = i.order_id
  join products p on i.product_id = p.product_id
  group by c.customer_id, c.name, c.email, o.order_id, o.order_date, o.total_amount
```

### Instructions
```
dozer clean -c cte-config.yaml
dozer build -c cte-config.yaml
dozer run app -c cte-config.yaml
```

### Findings

![Experiement 2](../images/experiment_2.png)

 - Roughly took `12 mins` to process all the records. 
 - Note that here total number of `order_items` increases in conjunction with `products`. This is to due to the dependency of the join. 
 - Pipeline latency stays under `1s` even with 4 joins and an aggregation.
 
| Start Time | End Time   | Elapsed   |
| ---------- | ---------- | --------- |
| 2:32:48 PM | 2:44:51 PM | ~ 12 mins |
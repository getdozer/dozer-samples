from temporalio import workflow, activity
from dataclasses import dataclass
from uuid import UUID, uuid4
from datetime import timedelta
from decimal import Decimal
import asyncio
import psycopg

TIMEOUT = timedelta(minutes=5)


@dataclass
class OrderProduct:
    product_id: str
    amount: int
    price: float


@dataclass
class PlaceOrderParams:
    products: list[OrderProduct]
    customer_id: UUID


@workflow.defn(name="PlaceOrderWorkflow")
class PlaceOrderWorkflow:
    @workflow.run
    async def run(self, params: PlaceOrderParams):
        print(f"Placing order for customer {params.customer_id}")
        await workflow.execute_activity(
            record_order, params, start_to_close_timeout=TIMEOUT
        )
        print(f"Order placed for customer {params.customer_id}")

@activity.defn(name="RecordOrderActivity")
async def record_order(order: PlaceOrderParams):
    print(f"Recording order for customer {order.customer_id}")
    async with await psycopg.AsyncConnection.connect(
        "postgresql://postgres:pgpass@localhost:5432/orders"
    ) as conn:
        cur = conn.cursor()
        await cur.execute(
            "INSERT INTO orders (customer) VALUES (%s) RETURNING id",
            (order.customer_id,),
        )
        order_id = (await cur.fetchone())[0]
        await cur.executemany(
            "INSERT INTO order_items (order_id, item_id, amount, price) VALUES (%s, %s, %s, %s)",
            [
                (order_id, prod.product_id, prod.amount, prod.price)
                for prod in order.products
            ],
        )
    pass


if __name__ == "__main__":
    asyncio.run(
        record_order(
            PlaceOrderParams(
                customer_id=uuid4(), products=[OrderProduct("item1", 2, 3.14)]
            )
        )
    )

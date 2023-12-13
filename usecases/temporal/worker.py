import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from workflows.place_order import PlaceOrderWorkflow, record_order


async def main():
    print("Starting worker...")
    client = await Client.connect("localhost:7233")
    print("Worker connected to Temporal server successfully")
    worker = Worker(
        client,
        task_queue="task-queue",
        workflows=[PlaceOrderWorkflow],
        activities=[record_order],
    )
    print("Worker created successfully")
    await worker.run()
    print("Worker exited successfully")

if __name__ == "__main__":
    asyncio.run(main())

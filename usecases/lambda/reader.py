import os

import pydozer_log
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = ""
auth_token = ""
client = Client(account_sid, auth_token)


def message():
    message = client.messages.create(
        body="from Dozer Assistant:\nThe temperature of the room is too high 🥵",
        from_='',
        to=''
    )
    print(message.sid)


async def main():
    reader = await pydozer_log.LogReader.new("http://127.0.0.1:50053", "events")
    while True:
        data = await reader.next_op()
        if "op" in data.keys():
            op = data["op"]
            record = op["new"]
            temperature = record["temperature"]
            if temperature >= 22.9:
                print("ALERT!")
                message()
                break


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

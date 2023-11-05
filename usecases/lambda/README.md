# Dozer Lambda Runtime Example

This example demonstrates how to use the Dozer Lambda Runtime to execute Lambda functions based on data change conditions in Dozer. In this specific case, we will create a React app that generates a real-time graph based on room temperature data (room temperature monitoring). We will use the `pydozer_log` module to react to data change conditions and trigger a Twilio message if the room temperature goes above 22.9°C.

## Prerequisites

- Python 3.9 or higher
- Node.js 14.x or higher
- Yarn (optional, but recommended)
- A Twilio account

## Setup and Run the App

Follow these steps to set up and run the example app:

### Step 1: Clone the Dozer repository and install dependencies

```bash
git clone https://github.com/getdozer/dozer-samples.git
cd dozer-samples/usecases/lambda/
pip install -r requirements.txt
```

### Step 2: Remove any existing Dozer configuration and start the Dozer process

```bash
rm -rf ./.dozer && dozer run -c config/dozer-config.yaml
```

### Step 3: Run the Python scripts to read data from the pipeline

*Note: Make sure to replace the Twilio configuration in `reader.py`, with your account id and auth token. To learn more about Twilio SMS setup, check out this [getting started guide](https://www.twilio.com/docs/sms/quickstart/python).*

```bash
python reader.py
python main.py
```

### Step 4: Navigate to the React app folder, install the necessary packages, and start the development server

```bash
cd react
yarn install && yarn start
```

You should now see a real-time graph of the room temperature data in your browser:

![React app showing a graph of room temperature monitoring](https://i.imgur.com/2IhoM5C.png)

If the room temperature exceeds 22.9°C, a Twilio message will be triggered, notifying the relevant parties of the situation:

![Twilio message after temperature exceeds 22.9°C](https://i.imgur.com/WIpnpPc.png)

🎉 Congratulations! 🎉 You've successfully set up and run the Dozer Lambda Runtime example with a React app to monitor room temperature data and trigger Twilio messages based on data change conditions.

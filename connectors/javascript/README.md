# Deno Connector And Lambda Functions

This folder contains the sample for Deno connector and the lambda functions that are used to trigger notification in response to changes in data.

## Prerequisites

1. Slack Webhooks URL, to your Slack Channel. 
2. Dozer installed. 

## Setup Instructions

### Step 1: Run App To Start Ingestion

Execute the following command: 

```bash
dozer run app
```

### Step 2: Run Lambda Functions To Trigger Notifications

Execute the following command: 

```bash
dozer run lambda
```

That's all to it. Head over to your Slack alerts channel to see the notifications triggered by Dozer Lambda Function.
const SLACK_WEBHOOK_URL = 'xxxxx'; // Set this to your Slack Webhook URL
function log(op) {
    if (op.typ === "insert") {
        const message = `ALERT: Price Drop ! Ready to Buy: ${op.new.Name}, current price ${op.new.Price} USD`;


        const payload = {
            text: message,
        };


        fetch(SLACK_WEBHOOK_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        })
            .then(() => {
                console.log('Slack notification sent.');
            })
            .catch((error) => {
                console.error('Error sending Slack notification:', error);
            });
    }
}

export default log;




from prometheus_client import start_http_server, Gauge
import requests
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the environment variables
ZENDESK_DOMAIN = os.getenv('ZENDESK_DOMAIN')
ZENDESK_EMAIL = os.getenv('ZENDESK_EMAIL')
ZENDESK_API_TOKEN = os.getenv('ZENDESK_API_TOKEN')
ZENDESK_API_URL = f'https://{ZENDESK_DOMAIN}.zendesk.com/api/v2'

# Define Prometheus metrics
zendesk_ticket_count = Gauge(
    'zendesk_ticket_count', 'Total number of Zendesk tickets')


def fetch_tickets():
    response = requests.get(f'{ZENDESK_API_URL}/tickets.json', auth=(
        f'{ZENDESK_EMAIL}/token', ZENDESK_API_TOKEN))

    if response.status_code == 200:
        tickets = response.json()['tickets']
        return len(tickets)
    else:
        print(f"Failed to fetch data from Zendesk: {response.status_code}")
        return 0


def collect_metrics():
    ticket_count = fetch_tickets()
    zendesk_ticket_count.set(ticket_count)


if __name__ == '__main__':
    start_http_server(8000)
    print("Prometheus exporter started on port 8000")
    while True:
        collect_metrics()
        time.sleep(60)

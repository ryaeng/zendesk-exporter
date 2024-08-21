from dotenv import load_dotenv
from prometheus_client import start_http_server, Gauge
from zenpy import Zenpy, ZenpyException
import logging
import time
import os

# Load environment variables from .env file
load_dotenv()

# Configure logging to stdout (default behavior)
logging.basicConfig(level=logging.ERROR)

# Get the environment variables
ZENDESK_DOMAIN = os.getenv('ZENDESK_DOMAIN')
ZENDESK_EMAIL = os.getenv('ZENDESK_EMAIL')
ZENDESK_API_TOKEN = os.getenv('ZENDESK_API_TOKEN')

# Zenpy API token
creds = {
    'email': ZENDESK_EMAIL,
    'token': ZENDESK_API_TOKEN,
    'subdomain': ZENDESK_DOMAIN,
}

zenpy_client = Zenpy(**creds)

# Define Prometheus metrics
zendesk_ticket_total = Gauge(
    'zendesk_ticket_total', 'Total number of Zendesk tickets')


def get_zendesk_ticket_total():
    '''
    This function returns the total number of tickets within Zendesk.
    '''

    try:
        ticket_count = zenpy_client.search(type='ticket').count
    except ZenpyException as e:
        # Handle Zenpy-specific exceptions
        logging.error(
            f'An error occurred while fetching the ticket count: {str(e)}')
    except Exception as e:
        # Handle any other exception
        logging.error(f'An unexpected error occurred: {str(e)}')

    return ticket_count


def collect_metrics():
    ticket_total = get_zendesk_ticket_total()

    zendesk_ticket_total.set(ticket_total)


if __name__ == '__main__':
    start_http_server(8000)
    print("Prometheus exporter started on port 8000")
    while True:
        collect_metrics()
        time.sleep(60)

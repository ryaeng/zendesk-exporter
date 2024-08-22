from dotenv import load_dotenv
from enum import Enum
from zenpy import Zenpy, ZenpyException
import datetime
import logging
import prometheus_client
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

# Prometheus metrics
zendesk_ticket_total = prometheus_client.Gauge('zendesk_ticket_total',
                                               'Zendesk tickets over the last month (30 days)',
                                               ['status'])


def zenpy_error_handler(exception, zenpy_type):
    e = exception

    # Handle Zenpy-specific exceptions
    if e == 'ZenpyException':
        msg = f'An error occurred while fetching {zenpy_type}: {str(e)}'
    # Handle any other exception
    else:
        msg = f'An unexpected error occurred: {str(e)}'

    logging.error(msg)


def get_zendesk_ticket_total(status_category):
    '''
    This function sets the Zendesk ticket totals over the last
    month (30 days).
    '''

    status_name = status_category.name.lower()
    one_mo_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    today = datetime.datetime.now()

    try:
        ticket_search = zenpy_client.search('', created_between=[one_mo_ago, today],
                                            status=f'{status_name}', type='ticket', minus='negated')
    except (ZenpyException, Exception) as e:
        zenpy_error_handler(e, 'tickets')

    zendesk_ticket_total.labels(status=f'{status_name}').set(len(ticket_search))


def collect_metrics():
    class TicketStatusCategories(Enum):
        NEW = 1
        OPEN = 2
        PENDING = 3
        HOLD = 4
        SOLVED = 5

    for status_category in TicketStatusCategories:
        get_zendesk_ticket_total(status_category)


if __name__ == '__main__':
    prometheus_client.start_http_server(8000)
    print("Prometheus exporter started on port 8000")
    while True:
        collect_metrics()
        time.sleep(60)

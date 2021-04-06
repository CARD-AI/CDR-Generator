import random
import json
import datetime
import numpy as np
from scipy.stats import truncnorm

from cdr import CallRecord


def get_truncated_normal(mean = 5, standard_deviation = 1, low = 0, upp = 10):
    return truncnorm((low - mean) / standard_deviation,
                    (upp - mean) / standard_deviation,
                    loc = mean,
                    scale = standard_deviation)


def read_params():
    with open('./resources/situation1params.json') as file:
        params = json.load(file)
    return params


def fill_event_contacts(customers, params):
    for customer in customers:
        people_count = len(customer.friends) + len(customer.acquaintances)
        event_calls_count = int(get_truncated_normal(mean = people_count / 2,
                                upp = people_count).rvs())
        for _ in range(event_calls_count):
            probability = random.randint(1, 10)
            if probability <= params['probFriend']:
                possible_contact = random.choice(customer.friends)
                customer.call_contacts.append(possible_contact)
            elif probability <= params['probFriend'] + params['probAcqaint']:
                possible_contact = random.choice(customer.acquaintances)
                customer.call_contacts.append(possible_contact)
            else:
                possible_contact = random.choice(customers)
                if possible_contact.customerid!=customer.customerid:
                    customer.call_contacts.append(possible_contact)
    return customers


def random_event_timestamp(params):
    start = datetime.datetime.strptime(params['dateTimeFrom'], "%Y-%m-%d %H:%M")
    end = datetime.datetime.strptime(params['dateTimeTo'], "%Y-%m-%d %H:%M")

    duration = end - start
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    rand_hour = get_truncated_normal(mean = hours / 2, standard_deviation = 2, upp = hours)
    if days != 0:
        start += datetime.timedelta(days = random.randrange(days))
    start += datetime.timedelta(minutes = random.randrange(minutes))
    start += datetime.timedelta(hours = int(rand_hour.rvs()))

    return start


def random_duration():
    return int(np.random.weibull(0.61) * 413.62)


def fill_cdr(customers, params):
    event_cdr = []
    for customer in customers:
        for contact in customer.call_contacts:
            random_event_timestamp(params)
            timestamp = random_event_timestamp(params)
            duration = random_duration()
            cdr = CallRecord(caller = customer,
                            called = contact,
                            timestamp = timestamp.strftime("%Y-%m-%d %H:%M"),
                            duration = duration)

            customer.call_records.append(cdr)
            event_cdr.append(cdr)

    return event_cdr


def situation1(customers):
    params = read_params()
    customers = fill_event_contacts(customers, params)
    call_detail_records = fill_cdr(customers, params)
    return call_detail_records

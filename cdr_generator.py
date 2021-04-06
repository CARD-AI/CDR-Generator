import datetime
import operator
import random
import json
import csv
from random import randrange, randint
import numpy as np

from customers import LocalCustomer, InternationalCustomer
from operators import LocalOperator, InternationalOperator
from cdr import CallRecord

from situation_1 import situation1
from situation_2 import situation2

def weibull_call_count():
    return int(np.random.weibull(0.74) * 11.13)


def weibull_duration(call_number):
    return np.random.weibull(0.61, call_number) * 413.62


def normal(call_number):
    return np.random.normal(15.74, 4.21, call_number)


def load_npy_file(path):
    with open(path, 'rb') as file:
        loaded_file = np.load(file)
    return loaded_file


def read_params():
    with open('./resources/params.json') as file:
        params = json.load(file)

    id_list = load_npy_file('./resources/id.npy')
    int_list = load_npy_file('./resources/intls.npy')

    return params, id_list, int_list


def create_operator(operator_num):
    operators = []
    last_marketshare = 0

    for i in range(operator_num):
        if i == 0:
            market_sh = random.randint(0, 70)
            last_marketshare += market_sh
            oper = LocalOperator(f"Kompanija{i + 1}", (market_sh / 100))
            operators.append(oper)
        elif i == operator_num - 1:
            oper = LocalOperator(f"Kompanija{i + 1}", ((100 - last_marketshare) / 100))
            operators.append(oper)

        else:
            market_sh = random.randint(0, (100 - last_marketshare))
            oper = LocalOperator(f"Kompanija{i + 1}", (market_sh / 100))
            operators.append(oper)
            last_marketshare += market_sh
    return operators


def create_international_operator(operator_num):
    international_operators = []
    for _ in range(operator_num):
        operator_name = randint(10000,1000000)
        intoper = InternationalOperator(operator_name)
        international_operators.append(intoper)
    return international_operators


def create_customer(customer_num, id_list):
    customers = []
    for i in range(customer_num):
        customerid = id_list[i]
        customer = LocalCustomer(customerid)
        customers.append(customer)
    return customers


def create_international(international_num, int_list, int_op):
    internationals = []
    for i in range(international_num):
        internationalid = int_list[i]
        international_operator = int_op[i]
        intc = InternationalCustomer(internationalid, international_operator)
        internationals.append(intc)
    return internationals


def fill_operators(operators, customers4op, customer_num):
    for oper in operators:
        for _ in range(int(oper.marketshare*customer_num)):
            customer = customers4op.pop()
            customer.operator = oper
            oper.customers.append(customer)


def fill_int_operators(international_operators, internationals):
    for index, intop in enumerate(international_operators):
        customer = internationals[index]
        customer.operator = intop
        intop.customers.append(customer)


def fill_possible_contacts(customers, max_friends, max_acquaintances, internationals):
    for _, customer in enumerate(customers):
        # Append friends
        for _ in range(random.randint(2, max_friends)):
            if np.random.binomial(1, 0.9):
                possible_contact = random.choice(customers)
                if possible_contact.customerid != customer.customerid:
                    customer.friends.append(possible_contact)
                    possible_contact.friends.append(customer)
            else:
                possible_contact = random.choice(internationals)
                customer.friends.append(possible_contact)

        # Append acquaintances
        for _ in range(random.randint(2, max_acquaintances)):
            if np.random.binomial(1, 0.9):
                possible_contact = random.choice(customers)
                if possible_contact.customerid != customer.customerid:
                    customer.acquaintances.append(possible_contact)
                    possible_contact.acquaintances.append(customer)
            else:
                possible_contact = random.choice(internationals)
                customer.acquaintances.append(possible_contact)


def fill_calls(customers):
    for customer in customers:
        call_count = weibull_call_count()
        for _ in range(call_count):
            probability = random.randint(1, 10)
            if probability <= 5:
                possible_contact = random.choice(customer.friends)
                customer.call_contacts.append(possible_contact)
            elif probability <= 8:
                possible_contact = random.choice(customer.acquaintances)
                customer.call_contacts.append(possible_contact)
            else:
                possible_contact = random.choice(customers)
                if possible_contact.customerid!=customer.customerid:
                    customer.call_contacts.append(possible_contact)


def random_hour(call_number):
    normal_list = normal(call_number)
    normal_rounded = np.array([round(normal_list[i]) for i in range(call_number)])
    sample_hours = normal_rounded[normal_rounded <= 24]
    random.shuffle(sample_hours)
    return sample_hours


def random_date(rand_hour, start_date_str):
    start_date = start_date_str.split('-')
    start = datetime.datetime(int(start_date[0]), int(start_date[1]), int(start_date[2]), 0, 0)
    start += datetime.timedelta(minutes=randrange(60))
    start += datetime.timedelta(hours=int(random.choice(rand_hour)))
    start += datetime.timedelta(days=randrange(0, 30))
    return start


def random_duration(call_number):
    weibull_list = weibull_duration(call_number)
    duration_sample = [round(weibull_list[i]) for i in range(call_number)]
    random.shuffle(duration_sample)
    return duration_sample


def generate_cdr(customers, start_date, rand_h, rand_duration):
    call_detail_records = []
    for customer in customers:
        for contact in customer.call_contacts:
            call_success = np.random.binomial(1, 0.7)
            duration = random.choice(rand_duration) if bool(call_success) else call_success
            cdr = CallRecord(caller=customer,
                            called=contact,
                            timestamp=random_date(rand_h, start_date).strftime("%Y-%m-%d %H:%M"),
                            duration=duration)

            customer.call_records.append(cdr)
            call_detail_records.append(cdr)
    return call_detail_records


def write_situation1(data):
    with open('./results/cdr_situation1.csv', mode='w') as cdr_file:
        cdr_write = csv.writer(cdr_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        cdr_write.writerow(['Caller id',
                            'Caller company',
                            'Receiver id',
                            'Receiver company',
                            'Timestamp',
                            'Duration s.'])

        for row in data:
            cdr_write.writerow([row.caller.customerid,
                                row.caller.operator.name,
                                row.called.customerid,
                                row.called.operator.name,
                                row.timestamp,
                                row.duration])


def write2file(cdr_data):
    with open('./results/cdr_data.csv', mode='w') as cdr_file:
        cdr_write = csv.writer(cdr_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        cdr_write.writerow(['Caller id',
                            'Caller company',
                            'Receiver id',
                            'Receiver company',
                            'Timestamp',
                            'Duration s.'])

        for row in cdr_data:
            cdr_write.writerow([row.caller.customerid,
                                row.caller.operator.name,
                                row.called.customerid,
                                row.called.operator.name,
                                row.timestamp,
                                row.duration])


def run_generator():
    parameters, local_ids, international_ids = read_params()

    operators_obj = create_operator(parameters['operatorNum'])
    international_operators_obj = create_international_operator(parameters['customerNum'])

    customers_obj = create_customer(parameters['customerNum'],
                                    local_ids)
    internationals_obj = create_international(parameters['customerNum'],
                                              international_ids,
                                              international_operators_obj)
    customers4op_obj = customers_obj.copy()

    random_h = random_hour(parameters['callNum'])
    random_dur = random_duration(parameters['callNum'])
    random_h = random_hour(parameters['callNum'])

    fill_operators(operators_obj,
                  customers4op_obj,
                  parameters['customerNum'])

    fill_int_operators(international_operators_obj,
                      internationals_obj)

    fill_possible_contacts(customers_obj,
                          parameters['maxFriends'],
                          parameters['maxAcquaintances'],
                          internationals_obj)

    fill_calls(customers_obj)

    call_detail_records = generate_cdr(customers_obj, parameters['startDate'], random_h, random_dur)

    if parameters['situation'] == 1:
        event_cdr = situation1(customers_obj)
        event_cdr = sorted(event_cdr, key=operator.attrgetter('timestamp'))
        write_situation1(event_cdr)
        call_detail_records += event_cdr
    elif parameters['situation'] == 2:
        call_detail_records = situation2(call_detail_records, customers_obj, operators_obj)

    call_detail_records = sorted(call_detail_records, key=operator.attrgetter('timestamp'))
    write2file(call_detail_records)

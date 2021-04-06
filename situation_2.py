import json
from datetime import datetime
import numpy as np


def read_params():
    with open('./resources/situation2params.json') as file:
        params = json.load(file)
    return params


def situation2(cdr, customers, operators):
    params = read_params()
    failed_company = np.random.choice(operators)
    print(f"Failed company: {failed_company.name}")
    print(f"Marketshare: {failed_company.marketshare}")
    print('--------------------------------------')

    out_list = []
    for customer in customers:
        if customer.operator.name == failed_company.name and \
           np.random.binomial(1, params['stationSize']):
            out_list.append(customer)

    start = datetime.strptime(params['failureStart'], '%Y-%m-%d %H:%M')
    end = datetime.strptime(params['failureEnd'], '%Y-%m-%d %H:%M')
    for index, row in enumerate(cdr):
        call_time = datetime.strptime(row.timestamp, '%Y-%m-%d %H:%M')
        if (row.caller in out_list or row.called in out_list) and \
           call_time > start and call_time < end:
            cdr[index].duration = 0

    return cdr

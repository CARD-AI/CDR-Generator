class LocalCustomer:
    def __init__(self, customerid):
        self.customerid = customerid
        self.operator = ""
        self.friends = []
        self.acquaintances = []
        self.call_contacts = []
        self.call_records = []


class InternationalCustomer:
    def __init__(self, internationalid, internationalop):
        self.customerid = internationalid
        self.operator = internationalop

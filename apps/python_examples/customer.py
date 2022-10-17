from uuid import uuid4

class Customer(object):
    """
        nw.customers Customer
    """

    # Use __slots__ to explicitly declare all data members.
    __slots__ = ["id", "createdOnMillis", "updatedOnMillis", "customerId", "companyName", "contactName", "contactTitle", "address", "city", "region", "postalCode", "country", "phone", "fax"]

    def __init__(self, createdOnMillis=None, updatedOnMillis=None, customerId=None,
                companyName=None, contactName=None, contactTitle=None,
                address=None, city=None, region=None, 
                postalCode=None, country=None, phone=None, fax=None):
        self.createdOnMillis=createdOnMillis
        self.updatedOnMillis=updatedOnMillis
        self.customerId=customerId
        self.companyName=companyName
        self.contactName=contactName
        self.contactTitle=contactTitle
        self.address=address
        self.city=city
        self.region=region
        self.postalCode=postalCode
        self.country=country
        self.phone=phone
        self.fax=fax

        # Unique id used to track produce request success/failures.
        # Do *not* include in the serialized object.
        self.id = uuid4()

    @staticmethod
    def dict_to_customer(obj, ctx):
        return Customer(obj['createdOnMillis', 'updatedOnMillis', 'customerId', 'companyName', 'contactName', 'contactTitle', 'address', 'city', 'region', 'postalCode', 'country', 'phone', 'fax'])
    
    @staticmethod
    def customer_to_dict(customer, ctx):
        return Customer.to_dict(customer)

    def to_dict(self):
        """
            The Avro Python library does not support code generation.
            For this reason we must provide a dict representation of our class for serialization.
        """
        return dict(createdOnMillis=self.createdOnMillis, updatedOnMillis=self.updatedOnMillis,
            customerId=self.customerId, companyName=self.companyName, contactName=self.contactName,
            contactTitle=self.contactTitle, address=self.address,
            city=self.city, region=self.region, postalCode=self.postalCode,
            country=self.country, phone=self.phone, fax=self.fax)

from uuid import uuid4

class Order(object):
    """
        nw.orders Order
    """

    # Use __slots__ to explicitly declare all data members.
    __slots__ = ["id", "createdOnMillis", "updatedOnMillis", "orderId", "customerId", "employeeId", "orderDateMillis", "requiredDateMillis", "shippedDateMillis", "shipVia", "freight", "shipName", "shipAddress", "shipCity", "shipRegion", "shipPostalCode", "shipCountry"]

    def __init__(self, createdOnMillis=None, updatedOnMillis=None, orderId=None,
                customerId=None, employeeId=None, orderDateMillis=None, requiredDateMillis=None,
                shippedDateMillis=None, shipVia=None, freight=1, shipName=None,
                shipAddress=None, shipCity=None, shipRegion=None, shipPostalCode=None,
                shipCountry=None):
        self.createdOnMillis=createdOnMillis
        self.updatedOnMillis=updatedOnMillis
        self.orderId=orderId
        self.customerId=customerId
        self.employeeId=employeeId
        self.orderDateMillis=orderDateMillis
        self.requiredDateMillis=requiredDateMillis
        self.shippedDateMillis=shippedDateMillis
        self.shipVia=shipVia
        self.freight=freight
        self.shipName=shipName
        self.shipAddress=shipAddress
        self.shipCity=shipCity
        self.shipRegion=shipRegion
        self.shipPostalCode=shipPostalCode
        self.shipCountry=shipCountry

        # Unique id used to track produce request success/failures.
        # Do *not* include in the serialized object.
        self.id = uuid4()

    @staticmethod
    def dict_to_order(obj, ctx):
        return Order(obj['createdOnMillis', 'updatedOnMillis', 'orderId', 'customerId', 'employeeId', 'orderDateMillis', 'requiredDateMillis', 'shippedDateMillis', 'shipVia', 'freight', 'shipName', 'shipAddress', 'shipCity', 'shipRegion', 'shipPostalCode', 'shipCountry'])
    
    @staticmethod
    def order_to_dict(order, ctx):
        return Order.to_dict(order)

    def to_dict(self):
        """
            The Avro Python library does not support code generation.
            For this reason we must provide a dict representation of our class for serialization.
        """
        return dict(createdOnMillis=self.createdOnMillis, updatedOnMillis=self.updatedOnMillis,
            orderId=self.orderId, customerId=self.customerId, employeeId=self.employeeId,
            orderDateMillis=self.orderDateMillis, requiredDateMillis=self.requiredDateMillis,
            shippedDateMillis=self.shippedDateMillis, shipVia=self.shipVia, freight=self.freight,
            shipName=self.shipName, shipAddress=self.shipAddress, shipCity=self.shipCity,
            shipRegion=self.shipRegion, shipPostalCode=self.shipPostalCode, shipCountry=self.shipCountry)

from django.db import models

class ProductLine(models.Model):
    productLine = models.CharField(primary_key=True, max_length=50)
    textDescription = models.TextField(blank=True, null=True)
    htmlDescription = models.TextField(blank=True, null=True)
    image = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'productlines'

    def __str__(self):
        return self.productLine


class Products(models.Model):
    productCode = models.CharField(primary_key=True, max_length=15)
    productName = models.CharField(max_length=70)
    productLine = models.ForeignKey(ProductLine, on_delete=models.DO_NOTHING, db_column='productLine', related_name='products')
    productScale = models.CharField(max_length=10)
    productVendor = models.CharField(max_length=50)
    productDescription = models.TextField()
    quantityInStock = models.SmallIntegerField()
    buyPrice = models.DecimalField(max_digits=10, decimal_places=2)
    MSRP = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'products'

    def __str__(self):
        return self.productName


class Offices(models.Model):
    officeCode = models.CharField(primary_key=True, max_length=10)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    addressLine1 = models.CharField(max_length=50)
    addressLine2 = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50)
    postalCode = models.CharField(max_length=15)
    territory = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'offices'

    def __str__(self):
        return self.city


class Employees(models.Model):
    employeeNumber = models.IntegerField(primary_key=True)
    lastName = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50)
    extension = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    officeCode = models.ForeignKey(Offices, on_delete=models.DO_NOTHING, db_column='officeCode', related_name='employees')
    reportsTo = models.ForeignKey('self', on_delete=models.DO_NOTHING, db_column='reportsTo', blank=True, null=True, related_name='subordinates')
    jobTitle = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'employees'

    def __str__(self):
        return f"{self.firstName} {self.lastName}"


class Customers(models.Model):
    customerNumber = models.IntegerField(primary_key=True)
    customerName = models.CharField(max_length=50)
    contactLastName = models.CharField(max_length=50)
    contactFirstName = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    addressLine1 = models.CharField(max_length=50)
    addressLine2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50, blank=True, null=True)
    postalCode = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=50)
    salesRepEmployeeNumber = models.ForeignKey(Employees, on_delete=models.DO_NOTHING, db_column='salesRepEmployeeNumber', blank=True, null=True, related_name='customers')
    creditLimit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'

    def __str__(self):
        return self.customerName


class Payments(models.Model):
    customerNumber = models.ForeignKey(Customers, on_delete=models.DO_NOTHING, db_column='customerNumber', related_name='payments')
    checkNumber = models.CharField(max_length=50)
    paymentDate = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'payments'
        unique_together = (('customerNumber', 'checkNumber'),)

    def __str__(self):
        return f"{self.customerNumber.customerName} - {self.checkNumber}"


class Orders(models.Model):
    orderNumber = models.IntegerField(primary_key=True)
    orderDate = models.DateField()
    requiredDate = models.DateField()
    shippedDate = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=15)
    comments = models.TextField(blank=True, null=True)
    customerNumber = models.ForeignKey(Customers, on_delete=models.DO_NOTHING, db_column='customerNumber', related_name='orders')

    class Meta:
        managed = False
        db_table = 'orders'

    def __str__(self):
        return f"Order #{self.orderNumber}"


class OrderDetails(models.Model):
    orderNumber = models.ForeignKey(Orders, on_delete=models.DO_NOTHING, db_column='orderNumber', related_name='orderdetails')
    productCode = models.ForeignKey(Products, on_delete=models.DO_NOTHING, db_column='productCode', related_name='orderdetails')
    quantityOrdered = models.IntegerField()
    priceEach = models.DecimalField(max_digits=10, decimal_places=2)
    orderLineNumber = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'orderdetails'
        unique_together = (('orderNumber', 'productCode'),)

    def __str__(self):
        return f"{self.orderNumber} - {self.productCode}"

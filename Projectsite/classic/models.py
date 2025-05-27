from django.db import models

class ProductLine(models.Model):
    productLine = models.CharField(primary_key=True, max_length=50)
    textDescription = models.TextField(blank=True, null=True)
    htmlDescription = models.TextField(blank=True, null=True)
    image = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'productlines'


class Products(models.Model):
    productCode = models.CharField(primary_key=True, max_length=15)
    productName = models.CharField(max_length=70)
    productLine = models.ForeignKey(ProductLine, on_delete=models.DO_NOTHING, db_column='productLine')
    productScale = models.CharField(max_length=10)
    productVendor = models.CharField(max_length=50)
    productDescription = models.TextField()
    quantityInStock = models.SmallIntegerField()
    buyPrice = models.DecimalField(max_digits=10, decimal_places=2)
    MSRP = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'products'


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


class Employees(models.Model):
    employeeNumber = models.IntegerField(primary_key=True)
    lastName = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50)
    extension = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    officeCode = models.ForeignKey(Offices, on_delete=models.DO_NOTHING, db_column='officeCode')
    reportsTo = models.ForeignKey('self', on_delete=models.DO_NOTHING, db_column='reportsTo', blank=True, null=True)
    jobTitle = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'employees'


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
    salesRepEmployeeNumber = models.ForeignKey(Employees, on_delete=models.DO_NOTHING, db_column='salesRepEmployeeNumber', blank=True, null=True)
    creditLimit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'


class Payments(models.Model):
    customerNumber = models.ForeignKey(Customers, on_delete=models.DO_NOTHING, db_column='customerNumber')
    checkNumber = models.CharField(max_length=50)
    paymentDate = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'payments'
        unique_together = (('customerNumber', 'checkNumber'),)


class Orders(models.Model):
    orderNumber = models.IntegerField(primary_key=True)
    orderDate = models.DateField()
    requiredDate = models.DateField()
    shippedDate = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=15)
    comments = models.TextField(blank=True, null=True)
    customerNumber = models.ForeignKey(Customers, on_delete=models.DO_NOTHING, db_column='customerNumber')

    class Meta:
        managed = False
        db_table = 'orders'


class OrderDetails(models.Model):
    orderNumber = models.ForeignKey(Orders, on_delete=models.DO_NOTHING, db_column='orderNumber')
    productCode = models.ForeignKey(Products, on_delete=models.DO_NOTHING, db_column='productCode')
    quantityOrdered = models.IntegerField()
    priceEach = models.DecimalField(max_digits=10, decimal_places=2)
    orderLineNumber = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'orderdetails'
        unique_together = (('orderNumber', 'productCode'),)

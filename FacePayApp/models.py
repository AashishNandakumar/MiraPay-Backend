from django.db import models


# Create your models here.
# User Information part
class UserInformation(models.Model):
    userId = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.DateField(auto_now_add=True)
    phone_number = models.CharField(max_length=15, unique=True)  # tighter constraints will be placed in future
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')))  # (value stored in db, value presented)


class FinancialInformation(models.Model):
    userId = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=12)
    upi_id = models.CharField(max_length=100)
    address = models.TextField()


# Invoice part
class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50)
    due_date = models.DateField()
    from_name = models.CharField(max_length=100)
    from_email_address = models.EmailField()
    from_phone_number = models.CharField(max_length=15)
    to_name = models.CharField(max_length=100)
    to_email_address = models.EmailField()
    to_phone_number = models.CharField(max_length=15)
    discount_percentage = models.FloatField()
    tax_percentage = models.FloatField()
    total_cost = models.FloatField()
    notes = models.TextField()


class Item(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    description = models.TextField()
    category = models.CharField(max_length=50)  # yet to add 'check' constraint

    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)




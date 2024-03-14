from django.db import models


# Create your models here.
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


class InvoiceInformation(models.Model):
    invoice_number = models.CharField(max_length=50)
    due_date = models.DateField()
    from_name = models.CharField(max_length=100)
    from_email_address = models.EmailField()
    from_phone_number = models.CharField(max_length=15)
    to_name = models.CharField(max_length=100)
    to_email_address = models.EmailField()
    to_phone_number = models.CharField(max_length=15)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=3)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=3)
    total_cost = models.DecimalField(max_digits=5, decimal_places=3)
    notes = models.TextField()


class ItemInformation(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=3)
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=50)  # yet to add 'check' constraint
    invoice = models.ForeignKey(InvoiceInformation, on_delete=models.CASCADE)



from django.db import models

# Create your models here.
class CreditCard(models.Model):
    name = models.CharField(max_length=50, null=False)

    # limits
    limit_amount = models.PositiveIntegerField(null=False)

    # dates
    last_close_date = models.DateField(null=True)
    last_exp_date = models.DateField(null=True)
    current_close_date = models.DateField(null=True)
    current_exp_date = models.DateField(null=True)
    next_close_date = models.DateField(null=True)
    next_exp_date = models.DateField(null=True)

    def __str__(self) -> str:
        return self.name


class Purchase(models.Model):
    name = models.CharField(max_length=50, null=False)
    cc_name = models.CharField(max_length=50, null=False)

    total_amount = models.FloatField(null=False)
    refund_amount = models.PositiveIntegerField(null=False)
    remaining_amount = models.FloatField(null=False)

    purchase_date = models.DateField(null=True)
    first_payment_date = models.DateField(null=True)

    # relations
    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, null=False)

    def __str__(self) -> str:
        return f"{self.name} ({self.purchase_date})"


class Period(models.Model):
    month = models.PositiveIntegerField(null=False)
    year = models.PositiveIntegerField(null=False)

    def __str__(self) -> str:
        return f"{self.month}/{self.year}"


class Installment(models.Model):
    amount = models.FloatField(null=False)
    status = models.CharField(max_length=20, null=False)
    number = models.PositiveIntegerField(null=False)

    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=False)
    period = models.ForeignKey(Period, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.purchase.name} - ${self.amount} - {self.period} - {self.status}"

from typing import List

from django.db import models

from .config import constants

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

    # relations
    @property
    def purchases(self):
        return self.purchase_set.all()

    @property
    def remaning_amount(self):
        used_amount = 0.0
        purchases: List[Purchase] = self.purchase_set.all()
        for purchase in purchases:
            used_amount += purchase.remaining_amount
        return self.limit_amount - used_amount

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
    financing_installments = models.PositiveIntegerField(null=False, default=0)

    # relations
    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, null=False)

    def __str__(self) -> str:
        return f"{self.name} - {self.total_amount} ({self.purchase_date})"

    def __create_installments(self):
        remaining_amount = self.total_amount
        remaining_installments = self.financing_installments
        current_installment = 1
        current_payment_month = self.first_payment_date.month
        current_payment_year = self.first_payment_date.year
        new_installments = []
        while remaining_installments > 0:
            # aux values
            installment_amount = round(remaining_amount / remaining_installments, 2)
            if current_installment == 1:
                installment_amount -= self.refund_amount

            # new installment
            new_installment = Installment()
            new_installment.amount = installment_amount
            new_installment.status = constants.INSTALLMENT_STATUS['not-confirmed']
            new_installment.number = current_installment
            new_installment.purchase = self
            new_installment.period = Period.get_period(month=current_payment_month, year=current_payment_year)
            new_installments.append(new_installment)

            # update values
            remaining_amount -= installment_amount
            remaining_installments -= 1
            current_installment += 1
            current_payment_year += 1 if current_payment_month == 12 else 0
            current_payment_month += 1

        [installment.save() for installment in new_installments]
        return self.installment_set.all()

    @property
    def installments(self) -> list:
        return self.installment_set.all()
        # installment_list: List[Installment] = self.installment_set.all()
        


    def update_amounts(self):
        if self.financing_installments == 0:
            # TODO: es una suscripción, manejar
            pass

        if len(self.installments) == 0:
            # At this point, we have no installments yet. Need create them
            self.__create_installments()


class Period(models.Model):
    month = models.PositiveIntegerField(null=False)
    year = models.PositiveIntegerField(null=False)

    def __str__(self) -> str:
        return f"{self.month}/{self.year}"

    @classmethod
    def get_period(self, year:int, month: int):
        period = Period.objects.filter(year=year, month=month)
        period = period[0] if len(period) > 0 else None

        if period is None:
            period = Period(year=year, month=month)
            period.save()
        
        return period


class Installment(models.Model):
    amount = models.FloatField(null=False)
    status = models.CharField(max_length=20, null=False)
    number = models.PositiveIntegerField(null=False)

    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=False)
    period = models.ForeignKey(Period, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.purchase.name} - ${self.amount} - {self.period} - {self.status}"

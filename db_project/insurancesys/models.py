from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator, MaxValueValidator
import datetime

numeric_regex = RegexValidator(
    r'^[0-9]+$', 'Only numeric characters are allowed.')

uppercase_regex = RegexValidator(
    r'^[A-Z]+$', 'Only uppercase characters are allowed.'
)


def year_choices():
    return [(r, r) for r in range(1950, datetime.date.today().year+1)]


def current_year():
    return datetime.date.today().year


class Customer(models.Model):
    FEMALE = 'F'
    MALE = 'M'
    GENDER = (
        (FEMALE, 'female'),
        (MALE, 'male'),
    )

    SINGLE = 'S'
    MARRIED = 'M'
    WIDOW_WIDOWER = 'W'
    MARITAL_STATUS = (
        (SINGLE, 'single'),
        (MARRIED, 'married'),
        (WIDOW_WIDOWER, 'widow or widower'),
    )

    AUTO_POLICY = 'A'
    HOME_POLICY = 'H'
    AUTO_HOME = 'AH'
    CUSTOMER_TYPE = (
        (AUTO_POLICY, 'auto policy customer'),
        (HOME_POLICY, 'home policy customer'),
        (AUTO_HOME, 'auto & home policy customer')
    )

    c_id = models.CharField(max_length=10, primary_key=True, validators=[
                            numeric_regex, MinLengthValidator(10)])
    c_firstname = models.CharField(max_length=30)
    c_lastname = models.CharField(max_length=30)
    c_street = models.CharField(max_length=30)
    c_city = models.CharField(max_length=30)
    c_state = models.CharField(max_length=2, validators=[
                               uppercase_regex, MinLengthValidator(2)])
    c_zipcode = models.CharField(max_length=5, validators=[
                                 numeric_regex, MinLengthValidator(5)])
    c_gender = models.CharField(max_length=1, choices=GENDER)
    c_maritalstatus = models.CharField(
        max_length=1, choices=MARITAL_STATUS)
    c_customertype = models.CharField(
        max_length=2, choices=CUSTOMER_TYPE)

    def __str__(self):
        return self.c_firstname + self.c_lastname


class Policy(models.Model):
    CURRENT = 'C'
    EXPIRED = 'P'
    POLICY_STATUS = (
        (CURRENT, 'policy is current'),
        (EXPIRED, 'policy is expired'),
    )

    AUTO_POLICY = 'A'
    HOME_POLICY = 'H'
    POLICY_TYPE = (
        (AUTO_POLICY, 'auto policy'),
        (HOME_POLICY, 'home policy'),
    )

    policy_id = models.CharField(max_length=12, primary_key=True, validators=[
                                    numeric_regex, MinLengthValidator(12)])
    startdate = models.DateField(auto_now=False, auto_now_add=False)
    enddate = models.DateField(auto_now=False, auto_now_add=False)
    premium_amount = models.DecimalField(max_digits=22, decimal_places=2)
    policy_status = models.CharField(max_length=1, choices=POLICY_STATUS)
    policy_type = models.CharField(max_length=1, choices=POLICY_TYPE)
    c_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.policy_id


class Invoice(models.Model):
    YES = 'Y'
    NO = 'N'
    INSTALLMENT = (
        (YES, 'Pay by Installment'),
        (NO, 'Full Payment')
    )

    invoice_id = models.CharField(max_length=15, primary_key=True, validators=[
        numeric_regex, MinLengthValidator(15)])
    invoice_amount = models.DecimalField(max_digits=22, decimal_places=2)
    payment_due = models.DateField(auto_now=False, auto_now_add=False)
    installment = models.CharField(max_length=1, choices=INSTALLMENT)
    policy_id = models.ForeignKey(Policy, on_delete=models.CASCADE)

    def __str__(self):
        return self.invoice_id


class Payment(models.Model):
    CHECK = 'CHECK'
    PAYPAL = 'PAYPAL'
    CREDIT = 'CREDIT'
    DEBIT = 'DEBIT'
    METHOD = (
        (CHECK, 'pay with check'),
        (PAYPAL, 'pay with paypal'),
        (CREDIT, 'pay with credit card'),
        (DEBIT, 'pay with debit card'),
    )

    pay_id = models.CharField(max_length=15, primary_key=True, validators=[
                                  numeric_regex, MinLengthValidator(15)])
    payment_date = models.DateField(auto_now=False, auto_now_add=False)
    payment_method = models.CharField(max_length=6, choices=METHOD)
    pay_amount = models.DecimalField(max_digits=22, decimal_places=2, default=0.00)
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    def __str__(self):
        return self.pay_id


class Vehicle(models.Model):
    LEASED = 'L'
    FINANCED = 'F'
    OWNED = 'O'
    VEHICLE_STATUS = (
        (LEASED, 'vehicle is leased'),
        (FINANCED, 'vehicle is financed'),
        (OWNED, 'vehicle is owned'),
    )

    vin = models.CharField(max_length=12, primary_key=True, validators=[
                           numeric_regex, MinLengthValidator(12)])
    model_year = models.IntegerField(
        ('make_model_year'), choices=year_choices(), default=current_year)
    vehiclestatus = models.CharField(max_length=1, choices=VEHICLE_STATUS)
    policys = models.ManyToManyField(Policy)

    def __str__(self):
        return self.vin

class Driver(models.Model):
    driver_licence = models.CharField(max_length=15, primary_key=True, validators=[
                                      numeric_regex, MinLengthValidator(15)])
    d_firstname = models.CharField(max_length=30)
    d_lastname = models.CharField(max_length=30)
    d_birthdate = models.DateField(auto_now=False, auto_now_add=False)
    vin = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    def __str__(self):
        return self.driver_licence


class Home(models.Model):
    SINGLE = 'S'
    MULTI = 'M'
    CONDO = 'C'
    TOWN = 'T'
    HOME_TYPE = (
        (SINGLE, 'single family'),
        (MULTI, 'multi family'),
        (CONDO, 'condominium'),
        (TOWN, 'town house'),
    )

    YES = '1'
    NO = '0'
    YES_NO = (
        (YES, 'yes'),
        (NO, 'no'),
    )

    UNDERGROUND = 'U'
    OVERGROUND = 'O'
    INDOOR = 'I'
    MULTIPLE = 'M'
    NULL = 'N'
    SWIMMING_POOL = (
        (UNDERGROUND, 'underground swimming pool'),
        (OVERGROUND, 'overground swimming pool'),
        (INDOOR, 'indoor swimming pool'),
        (MULTIPLE, 'multiple swimming pool'),
        (NULL, 'no swmming pool'),

    )
    home_id = models.CharField(max_length=14, primary_key=True, validators=[
                               numeric_regex, MinLengthValidator(14)])
    purchase_date = models.DateField(auto_now=False, auto_now_add=False)
    purchase_value = models.DecimalField(max_digits=22, decimal_places=2)
    homearea = models.DecimalField(max_digits=22, decimal_places=2)
    hometype = models.CharField(max_length=1, choices=HOME_TYPE)
    auto_fire_notification = models.CharField(max_length=1, choices=YES_NO)
    home_security_system = models.CharField(max_length=1, choices=YES_NO)
    swimming_pool = models.CharField(max_length=1, choices=SWIMMING_POOL)
    basement = models.CharField(max_length=1, choices=YES_NO)
    policys = models.ManyToManyField('Policy')

    def __str__(self):
        return self.home_id

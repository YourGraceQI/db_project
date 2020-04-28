from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator

numeric_regex = RegexValidator(
    r'^[0-9]*$', 'Only numeric characters are allowed.')



# Create your models here.


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
    MARITALSTATUS = (
        (SINGLE, 'single'),
        (MARRIED, 'married'),
        (WIDOW_WIDOWER, 'widow or widower'),
    )

    AUTO_INSURANCE = 'A'
    HOME_INSURANCE = 'H'
    CUSTOMERTYPE = (
        (AUTO_INSURANCE, 'customer with auto insurance'),
        (HOME_INSURANCE, 'customer with home insurance'),
    )

    c_id = models.CharField(max_length=10, primary_key=True, validators=[
                            numeric_regex, MinLengthValidator(10)])
    c_firstname = models.CharField(max_length=30, null=False)
    c_lastname = models.CharField(max_length=30, null=False)
    c_street = models.CharField(max_length=30, null=False)
    c_city = models.CharField(max_length=30, null=False)
    c_state = models.CharField(max_length=2, null=False, validators=[
                               MinLengthValidator(2)])
    c_zipcode = models.CharField(max_length=5, null=False, validators=[
                                 numeric_regex, MinLengthValidator(5)])
    c_gender = models.CharField(max_length=1, null=False, choices=GENDER)
    c_maritalstatus = models.CharField(max_length=1, null=False, choices=MARITALSTATUS)
    c_customertype = models.CharField(max_length=1, null=False, choices=CUSTOMERTYPE)


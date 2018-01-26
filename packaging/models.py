from django.db import models
from django.utils import timezone
from decimal import *


# Global Variables

SEP = ' | '

# Methods

def to_bbl(f, q):
        """
        Takes two arguments: format(f), quantity(q)
        Returns value(v) as a Decimal object, rounded to two places. 

        """
        BBL_CONVERSION_MAPPING = {
            '12oz/CS': 0.07258064516129033,
            '16oz/CS': 0.0967741935483871,
            '375ml/CS': 0.038387096774193545,
            '500ml/CS': 0.05112903225806451,
            '750ml/CS': 0.07677419354838709,
            '1/6bbl': 0.16666666666666666,
            '1/4bbl': 0.25,
            '1/2bbl': 0.5,
            '50l': 0.426,
            'Firkin (10.8g)': 0.34838709677419355,
            'Pin (5.4g)': 0.17419354838709677
        }

        if f in BBL_CONVERSION_MAPPING:
            v  = Decimal(q) * Decimal(BBL_CONVERSION_MAPPING[f])
            return v.quantize(Decimal('1.00'))


# Classes 

class Beer(models.Model):
    name = models.CharField('Trade Name', max_length=50)

    def __str__(self):
        return self.name


    
class Gyle(models.Model):
    batch_number = models.CharField('#', max_length=7)

    def __str__(self):
        return self.batch_number


    
class BrewingEvent(models.Model):
    brewed_beer = models.ForeignKey(
        'Beer',
        on_delete=models.CASCADE,
    )
    gyle = models.ForeignKey(
        'Gyle',
        on_delete=models.CASCADE,
    )
    gyle2 = models.ForeignKey(
        'Gyle',
        on_delete=models.CASCADE,
        related_name='+'
    )
    brew_date = models.DateField(default=timezone.now)

    def __str__(self):
        if self.gyle2:
            return str(self.brew_date) + SEP + self.brewed_beer.name + SEP + str(self.gyle) + ', ' + str(self.gyle2)
        else:
            return str(self.brew_date) + SEP + self.brewed_beer.name + SEP + str(self.gyle)


    class Meta:
        verbose_name = "Brewing Event"



class PackagingEvent(models.Model):
    user = models.ForeignKey('auth.User')
    packaged_beer = models.ForeignKey(
        'Beer',
        on_delete=models.CASCADE,
    )
    packaging_date = models.DateField(default=timezone.now)
    PACKAGING_FORMATS = (
        ('12oz/CS', '12oz/CS'),
        ('16oz/CS', '16oz/CS'),
        ('375ml/CS', '375ml/CS'),
        ('500ml/CS', '500ml/CS'),
        ('750ml/CS', '750ml/CS'),
        ('1/6bbl', '1/6bbl'),
        ('1/4bbl', '1/4bbl'),
        ('1/2bbl', '1/2bbl'),
        ('50l', '50l'),
        ('Firkin (10.8g)', 'Firkin (10.8g)'),
        ('Pin (5.4g)', 'Pin (5.4g)'),
    )
    packaged_beer_format = models.CharField('Format', max_length=20, choices=PACKAGING_FORMATS, blank=True, default='12oz/CS')
    packaged_quantity = models.DecimalField(max_digits=5, decimal_places=2, default='0')
    

    def package(self):
        self.save()

    def __str__(self):
        # packaged_quantity_bbl = to_bbl(self.packaged_beer_format, self.packaged_quantity)
        return str(self.packaging_date) + SEP + self.packaged_beer.name + SEP + self.packaged_beer_format + SEP + str(to_bbl(self.packaged_beer_format, self.packaged_quantity)) + ' bbl'
        # return str(type(self.packaged_beer_format)) + str(type(self.packaged_quantity))
        # return str(to_bbl(self.packaged_beer_format, self.packaged_quantity))


    class Meta:
        verbose_name = "Packaging Event"



class PackagingFormat(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "Packaging Format"




class Hop(models.Model):
    name = models.CharField(max_length=50)
    min = models.PositiveIntegerField
    max = models.PositiveIntegerField
    on_hand = models.PositiveIntegerField
    
    def __str__(self):
        return self.name

    

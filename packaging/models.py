from django.db import models
from django.utils import timezone
from decimal import *
from brewing.models import BrewingEvent

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

def get_many_objects(queryset):
    """
    gets all objects from a queryset (manytomanyfields)
    returns comma-separated strings
    """
    return ", ".join([str(p) for p in queryset])

# Classes


class Format(models.Model):
    """
    Generic Format Model
    """
    TYPE = (
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
    # NOTE: type is a reserved python word.
    format_type = models.CharField("format type", max_length=20, choices=TYPE)

    def __str__(self):
        return self.format_type


class PackagedFormat(Format):
    """
    An instance of Format used for packaging events
    """
    quantity = models.DecimalField("quantity", max_digits=10, decimal_places=2,
        help_text="Total packaged quantity for this format.")

    def __str__(self):
        return self.format_type + ': ' + str(to_bbl(self.format_type, self.quantity))
        #return str(to_bbl(self.format_type, self.quantity))

class PackagingEvent(models.Model):
    NAME = (
        ("tyler", "Tyler"),
        ("ron", "Ron"),
        ("chris", "Chris"),
        ("shea", "Shea"),
        ("ian", "Ian"),
        ("brandon", "Brandon")
    )

    packager = models.CharField("packager", max_length=100, choices=NAME, blank=True, null=True)
    brewing_event = models.ForeignKey('brewing.BrewingEvent', help_text="BrewingEvent associated with this packaging event.",
        blank=True, null=True, verbose_name="Packaging Source")

    packaging_date = models.DateField(default=timezone.now, blank=True, verbose_name="Date Packaged")
    formats = models.ManyToManyField('PackagedFormat', blank=True, null=True, help_text="Zero or more formats")

    def package(self):
        self.save()

    def get_formats(self):        
        #return "\n".join([str(p) for p in self.formats.all()])
        return ", ".join([str(p) for p in self.formats.all()])
    get_formats.short_description = 'Format: Volume(bbl)'

    def __str__(self):
        # packaged_quantity_bbl = to_bbl(self.packaged_beer_format, self.packaged_quantity)
        return str(self.brewing_event) + SEP + self.packager + SEP + get_many_objects(self.formats.all())
        # + SEP + str(to_bbl(self.packaged_beer_format, self.packaged_quantity)) + ' bbl'
        # return str(type(self.packaged_beer_format)) + str(type(self.packaged_quantity))
        # return str(to_bbl(self.packaged_beer_format, self.packaged_quantity))


    class Meta:
        verbose_name = "Packaging Event"

    

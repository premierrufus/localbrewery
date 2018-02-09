# -*- coding: utf-8 -*-
#
#===============================================================================
# Not exactly PEP8 compliant, but so be it... 
# 
# _beerxml_attrs:
#  All field names try to follow the naming convention from beerxml
#  unless field name is a reserved python word. If field is a reserved
#  word, model should include a dict  _beerxml_attrs = {"beerxml_name" : "model_name",}
#  for each field not following the beerxml standard.
#
# BeerXML reference
#  - http://www.beerxml.com/beerxml.htm
#
# Data formats:
# All DecimalFields are this big to support scientific input numbers
#  - Record         : Model (database table)
#  - Text           : CharField or TextField dependent on situation
#  - Integer        : IntegerField (may include negative values, 
#                     except version which is PositiveSmallIntegerField)
#  - Percentage     : DecimalField (max digits: 14, decimal places: 9 = max val 99999.999999999)
#  - Weight         : DecimalField (max_digits: 14, decimal_places: 9 = max val 99999.999999999)
#  - Temperature    : DecimalField (max_digits: 14, decimal_places: 9 = max val 99999.999999999)
#  - List           : CharField with choices (key=numeric index, value=display value)
#  - Time           : DecimalField (max_digits: 14, decimal_places: 9 = max val 99999.999999999)
#  - Floating Point : DecimalField (max_digits: 14, decimal_places: 9 = max val 99999.999999999)
#  - Boolean        : BooleanField
#
#
# Units:
#  The following units are allowed and may be used interchangeably. However, only units of 
#  the appropriate type may be used for a given value. For example "volume" units may not be 
#  used for "Weight" fields.
#
#  Weight Units
#    kg - Kilograms g - Grams
#    oz - Ounces
#    lb – Pounds
#
#  Volume Units
#    tsp – Teaspoons tblsp – Tablespoons oz – Ounces (US) cup – Cups (US)
#    pt – Pints (US)
#    qt – Quarts (US)
#    ml - Milliliters
#    l – Liters
#
#  Temperature Units
#    F – Degrees Fahrenheit C – Degrees Celsius
#    Time Units
#    min - Minutes hour - Hours day – Days week – Weeks
#
#  Color Units
#    srm – SRM Color ebc – EBC Color
#    L – Degrees lovibond.
#
#  Specific Gravity Units
#    sg – The relative gravity by weight when compared to water. For example “1.035 sg” 
#    plato – Gravity measured in degrees plato
#===============================================================================

from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.dispatch.dispatcher import receiver
from django.template.defaultfilters import slugify

from django.utils import timezone


# Global Variables
SEP = ' | '


# Functions

def get_batches(queryset):
    return ", ".join([str(p) for p in queryset])

# Classes

class Batch(models.Model):
    '''
    Batches have a number (or gyle)
    '''
    number = models.CharField(_("Batch Number(s)"), max_length=5, unique=True)

    def __str__(self):
        return self.number


    class Meta:
        verbose_name_plural = "Batches"


class Beer(models.Model):
    name = models.CharField('Trade Name', max_length=50)

    def __str__(self):
        return self.name



    
class BrewingEvent(models.Model):
    """
    Model Fields
    """

    NAME = (
        ("sean", "Sean"),
        ("shea", "Shea"),
        ("ian", "Ian"),
        ("ron", "Ron"),
        ("brandon", "Brandon")
    )

    batch_number = models.ManyToManyField('Batch', help_text="Batch Number(s) associated with this brewing event. ", blank=True, null=True)
    brewer = models.CharField(_("name of brewer"), max_length=100, choices=NAME, blank=True, null=True)
    asst_brewer = models.CharField(_("assistant brewer"), max_length=100, blank=True, 
                                   null=True)
    recipe = models.ForeignKey('Recipe', blank=True, null=True)
    brew_date = models.DateField(default=timezone.now, blank=True, null=True)
    vessel = models.ForeignKey('Equipment', blank=True, null=True)
    notes = models.TextField(_("notes"), blank=True, null=True)

    """
    Methods
    """
    def get_batches(self):        
        return ", ".join([str(p) for p in self.batch_number.all()])
    get_batches.short_description = 'Batch Numbers'


    def __str__(self):
        return str(self.recipe) + SEP + get_batches(self.batch_number.all())

    """
    Meta
    """
    class Meta:
        verbose_name = "Brewing Event"


#
# Models
#

class BeerXMLBase(models.Model):
    """
    Base model which all other models inherit
    from. This model has fields and methods which
    are common for all models
    """

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        app_label = "brewing"
        
    name = models.CharField(_("name"), max_length=100)
    version = models.PositiveSmallIntegerField(_("version"), default=1,
                                        editable=False, help_text="XML version")
    slug = models.SlugField(max_length=100, blank=True)
    registered_by = models.ForeignKey(User, blank=True, null=True,
            related_name="%(app_label)s_%(class)s_registered_by_set", help_text="Registered by")
    modified_by = models.ForeignKey(User, blank=True, null=True,
            related_name="%(app_label)s_%(class)s_modified_by_set", help_text="Modified by")
    cdt = models.DateTimeField(_("created"), editable=False, auto_now_add=True)
    mdt = models.DateTimeField(_("modified"), editable=False, auto_now=True)
    
            
class Equipment(BeerXMLBase):
    """
    Database model for equipment
    """

    capacity = models.DecimalField(_("Equipment Capactiy"), max_digits=5, 
            decimal_places=2, help_text="""Maximum capacity of this container (in bbl).""")
    notes = models.TextField(_("notes"), blank=True, null=True)

    
    def __unicode__(self):
        return u"%s" % self.name
    

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)

    
    class Meta:
        verbose_name_plural = 'Equipment'
      
            
class Fermentable(BeerXMLBase):
    """
    The term "fermentable" encompasses all fermentable items that contribute 
    substantially to the beer including extracts, grains, sugars, honey, fruits.
    """
    
    TYPE = (
        (u"grain", u"Grain"),
        (u"sugar", u"Sugar"),
        (u"extract", u"Extract"),
        (u"dry extract", u"Dry extract"),
        (u"adjunct", u"Adjunct")
    )
    
    # NOTE: type is a reserved python word.
    ferm_type = models.CharField(_("fermentable type"), max_length=12, choices=TYPE)
    amount = models.DecimalField(_("amount"), max_digits=14, decimal_places=9,
            help_text="Weight of the fermentable, extract or sugar in pounds.")
    # NOTE: yield is a reserved python word.
    ferm_yield = models.DecimalField(_("yield percentage"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""Percent dry yield (fine grain) 
            for the grain, or the raw yield by weight if this is an 
            extract adjunct or sugar.""")
    color = models.DecimalField(_("color"), max_digits=14, decimal_places=9,
            blank=True, null=True, help_text="""The color of the item in Lovibond Units 
            (SRM for liquid extracts).""")
    origin = models.CharField(_("origin country"), max_length=100, blank=True, null=True)
    supplier = models.TextField(_("supplier"), blank=True, null=True)
    notes = models.TextField(_("notes"), blank=True, null=True)
    coarse_fine_diff = models.DecimalField(_("coarse/fine percentage"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""Percent difference 
            between the coarse grain yield and fine grain yield.  Only appropriate for 
            a "Grain" or "Adjunct" type, otherwise this value is ignored.""")
    moisture = models.DecimalField(_("moisture percentage"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""Percent 
            moisture in the grain. Only appropriate for a "Grain" or "Adjunct" type, 
            otherwise this value is ignored.""")
    diastatic_power = models.DecimalField(_("diastatic power"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""The diastatic power 
            of the grain as measured in "Lintner" units. Only appropriate for a 
            "Grain" or "Adjunct" type, otherwise this value is ignored.""")
    protein = models.DecimalField(_("protein percentage"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""The percent 
            protein in the grain. Only appropriate for a "Grain" or "Adjunct" type, 
            otherwise this value is ignored.""")
    max_in_batch = models.DecimalField(_("max percentage per batch"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""The recommended 
            maximum percentage (by weight) this ingredient should represent in a 
            batch of beer.""")
    recommend_mash = models.NullBooleanField(_("recommended mash"), default=False, 
            blank=True, null=True, help_text="""True if it is recommended the grain 
            be mashed, False if it can be steeped. A value of True is only appropriate 
            for a "Grain" or "Adjunct" types. The default value is False. Note that 
            this does NOT indicate whether the grain is mashed or not – it is only 
            a recommendation used in recipe formulation.""")
    ibu_gal_per_lb = models.DecimalField(_("bitterness (IBU*gal/lb)"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""For hopped extracts 
            only - an estimate of the number of IBUs per pound of extract in a gallon 
            of water. To convert to IBUs we multiply this number by the "Amount" 
            field (in pounds) and divide by the number of gallons in the batch. 
            Based on a sixty minute boil. Only suitable for use with an "Extract" type, 
            otherwise this value is ignored.""")
    
    # Optional extension for BeerXML display
    display_amount = models.CharField(_("display amount"), max_length=50, blank=True, 
            null=True, help_text="""The amount of fermentables in this record along 
            with the units formatted for easy display in the current user defined units. 
            For example “1.5 lbs” or “2.1 kg”.""")
    potential = models.DecimalField(_("potential"), max_digits=14, decimal_places=9, 
            blank=True, null=True, help_text="""The yield of the fermentable converted 
            to specific gravity units for display. For example “1.036” or “1.040” 
            might be valid potentials.""")
    inventory = models.CharField(_("inventory"), max_length=50, blank=True, null=True,
            help_text="""Amount in inventory for this item along with the units 
            – for example “10.0 lb”""")
    display_color = models.CharField(_("display color"), max_length=50, blank=True, 
            null=True, help_text="""Color in user defined color units along with the 
            unit identified – for example “200L” or “40 ebc""")
    
    _beerxml_attrs = {
        "type": "ferm_type",
        "yield": "ferm_yield"
    }
    
    def __unicode__(self):
        return u"%s" % self.name

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.ferm_type:
            self.ferm_type = u"%s" % self.ferm_type.lower()
    
    
class Hop(BeerXMLBase):
    """
    The “Hop” identifier is used to define all varieties of hops.
    """
    USE = (
        ("@ 60 Minutes", "@ 60 Minutes"),
        ("@ 10 Minutes", "@ 10 Minutes"),
        ("@ 5 Minutes", "@ 5 Minutes"),
        ("@ Whirlpool", "@ Whirlpool"),
        ("@ First Dry-Hop", "@ First Dry-Hop"),
        ("@ Second Dry-Hop", "@ Second Dry-Hop")
    )

    amount = models.DecimalField(_("amount"), max_digits=14, decimal_places=9,
            help_text="Weight in pounds of the hops used in the recipe.")
    use = models.CharField(_("usage"), max_length=50, choices=USE,
            help_text="""The phase at which this hop is added.""")
    notes = models.TextField(_("notes"), blank=True, null=True)
    origin = models.CharField(_("origin"), max_length=100, blank=True, null=True)

    inventory = models.CharField(_("inventory"), max_length=50, blank=True, null=True,
            help_text="""Amount in inventory for this item along with the units 
            – for example “10.0 oz.”""")
    
    def __unicode__(self):
        return u"%s" % self.name

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.use:
            self.use = u"%s" % self.use.lower()


class Salt(BeerXMLBase):
    """
    The “Salt” identifier is used to define all varieties of salts.
    """

    amount = models.DecimalField(_("amount"), max_digits=14, decimal_places=9,
            help_text="Weight in ounces of the salt used in the recipe.")
    notes = models.TextField(_("notes"), blank=True, null=True)
    inventory = models.CharField(_("inventory"), max_length=50, blank=True, null=True,
            help_text="""Amount in inventory for this item along with the units 
            – for example “10.0 oz.”""")
    
    def __unicode__(self):
        return u"%s" % self.name

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)


class Misc(BeerXMLBase):
    """
    Database model for various items
    """
    
    TYPE = (
        (u"spice", u"Spice"),
        (u"fining", u"Fining"),
        (u"water agent", u"Water agent"),
        (u"herb", u"Herb"),
        (u"flavor", u"Flavor"),
        (u"other", u"Other")
    )
    
    USE = (
       (u"boil", u"Boil"),
       (u"mash", u"Mash"),
       (u"primary", u"Primary"),
       (u"secondary", u"Secondary"),
       (u"bottling", u"Bottling")
    )
    
    # NOTE: type is a reserved python word.
    misc_type = models.CharField(_("hop type"), max_length=12, choices=TYPE, default=4)
    use = models.CharField(_("hop type"), max_length=12, choices=USE, default=2)
    time = models.DecimalField(_("time"), max_digits=14, decimal_places=9,
            help_text="Amount of time the misc was boiled, steeped, mashed, etc in minutes.")
    amount = models.DecimalField(_("yield percentage"), max_digits=14, decimal_places=9,
            help_text="""Amount of item used. The default measurements are by weight, 
            but this may be the measurement in volume units if AMOUNT_IS_WEIGHT is set 
            to TRUE for this record. For liquid items this is liters, for solid the  
            weight is measured in kilograms.""")
    amount_is_weight = models.BooleanField(_("amount is weight"), default=False,
            help_text="""TRUE if the amount measurement is a weight measurement and FALSE if 
            the amount is a volume measurement.""")
    use_for = models.TextField(_("use for"), blank=True, null=True,
            help_text="Short description of what the ingredient is used for in text")
    notes = models.TextField(_("notes"), blank=True, null=True,
            help_text="Detailed notes on the item including usage.")
    
    # Optional extension for BeerXML display
    display_amount = models.CharField(_("display amount"), max_length=50, blank=True, 
            null=True, help_text="""The amount of the item in this record along with 
            the units formatted for easy display in the current user defined units. 
            For example “1.5 lbs” or “2.1 kg”.""")
    inventory = models.CharField(_("inventory"), max_length=50, blank=True, null=True,
            help_text="""Amount in inventory for this item along with the units 
            – for example “10.0 lb.”""")
    display_time = models.CharField(_("display time"), max_length=50, blank=True, 
            null=True, help_text="""Time in appropriate units along with the units 
            as in “10 min” or “3 days”.""")
    
    _beerxml_attrs = {
        "type": "misc_type"
    }
    
    def __unicode__(self):
        return u"%s" % self.name
    
    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.misc_type:
            self.misc_type = u"%s" % self.misc_type.lower()
        if self.use:
            self.use = u"%s" % self.use.lower()
    
    
class Yeast(BeerXMLBase):
    """
    Database model for yeast
    """
    
    TYPE = (
        (u"ale", u"Ale"),
        (u"lager", u"Lager"),
        (u"wheat", u"Wheat"),
        (u"wine", u"Wine"),
        (u"champagne", u"Champagne")
    )
    
    FORM = (
        (u"liquid", u"Liquid"),
        (u"dry", u"Dry"),
        (u"slant", u"Slant"),
        (u"culture", u"Culture")
    )
    
    FLOCCULATION = (
        (u"low", u"Low"),
        (u"medium", u"Medium"),
        (u"high", u"High"),
        (u"very high", u"Very high")
    )
    
    # NOTE: type is a reserved python word.
    yiest_type = models.CharField(_("yeast type"), max_length=12, choices=TYPE, 
                                  default=1)
    form = models.CharField(_("yeast form"), max_length=12, choices=FORM, default=1)
    amount = models.DecimalField(_("amount"), max_digits=14, decimal_places=9,
            help_text="""The amount of yeast, measured in liters. For a starter this is the 
            size of the starter. If the flag AMOUNT_IS_WEIGHT is set to TRUE then this 
            measurement is in kilograms and not liters.""")
    amount_is_weight = models.BooleanField(_("amount is weight or litres"), default=False,
            help_text="""TRUE if the amount measurement is a weight measurement and FALSE 
            if the amount is a volume measurement.  Default value (if not present) is 
            assumed to be FALSE – therefore the yeast measurement is a liquid amount 
            by default.""")
    laboratory = models.CharField(_("laboratory name"), max_length=100, blank=True, null=True)
    product_id = models.CharField(_("product id"), max_length=100, blank=True, null=True,
            help_text="""The manufacturer’s product ID label or number that identifies this 
            particular strain of yeast.""")
    min_temperature = models.DecimalField(_("min temperature"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""The minimum 
            recommended temperature for fermenting this yeast strain in degrees 
            Celsius.""")
    max_temperature = models.DecimalField(_("max temperature"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""The maximum 
            recommended temperature for fermenting this yeast strain in Celsius.""")
    flocculation = models.CharField(_("yeast form"), max_length=12, choices=FLOCCULATION, 
                                    default=1, blank=True, null=True)
    attenuation = models.DecimalField(_("attenuation percentage"), max_digits=14, 
            decimal_places=9, blank=True, null=True, help_text="""Average 
            attenuation for this yeast strain.""")
    notes = models.TextField(_("notes"), blank=True, null=True)
    best_for = models.TextField(_("best for"), blank=True, null=True,
            help_text="Styles or types of beer this yeast strain is best suited for.")
    times_cultured = models.PositiveSmallIntegerField(_("times recultured"), 
            blank=True, null=True, help_text="""Number of times this yeast has 
            been reused as a harvested culture. This number should be zero if this 
            is a product directly from the manufacturer.""")
    max_reuse = models.PositiveSmallIntegerField(_("max recultures"), blank=True, 
            null=True, help_text="""Recommended of times this yeast can be reused 
            (recultured from a previous batch)""")
    add_to_secondary = models.BooleanField(_("amount is weight"), default=False,
            help_text="""Flag denoting that this yeast was added for a secondary (or later) 
            fermentation as opposed to the primary fermentation. Useful if one uses two              
            or more yeast strains for a single brew (eg: Lambic). Default value is FALSE.""")
    
    
    def __unicode__(self):
        return u"%s" % self.name

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.yiest_type:
            self.yiest_type = u"%s" % self.yiest_type.lower()
        if self.form:
            self.form = u"%s" % self.form.lower()
        if self.flocculation:
            self.flocculation = u"%s" % self.flocculation.lower()
    
    
    
class Style(BeerXMLBase):
    """
    Database model for brewing styles
    """
    
    TYPE = (
        (u"lager", u"Lager"),
        (u"ale", u"Ale"),
        (u"mead", u"Mead"),
        (u"wheat", u"Wheat"),
        (u"mixed", u"Mixed"),
        (u"cider", u"Cider")
    )
    
    # NOTE: type is a reserved python word.
    style_type = models.CharField(_("type"), max_length=12, choices=TYPE, default=1,
            help_text="""May be “Lager”, “Ale”, “Mead”, “Wheat”, “Mixed” or “Cider”. 
            Defines the type of beverage associated with this category.""")
    
    def __unicode__(self):
        return u"%s" % self.name

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.style_type:
            self.style_type = u"%s" % self.style_type.lower()

    
    
class Recipe(BeerXMLBase):
    """
    Database model for reciepes
    """

    style = models.ForeignKey(Style, null=True, help_text="""The style of the 
            beer this recipe is associated with.""")
    pre_boil_batch_size = models.DecimalField(_("pre boil batch size"), max_digits=14, decimal_places=9,
            help_text="Target pre boil batch size in hectoliters(Hl).")
    pre_boil_gravity = models.DecimalField(_("pre boil gravity"), max_digits=14, decimal_places=9,
            help_text="Target pre boil gravity(Brix).")
    fermentation_temp = models.DecimalField(_("fermentation temperature"), max_digits=5, decimal_places=2,
            help_text="Target fermentation temperature (F)")
    mash_temp = models.DecimalField(_("mash temperature"), max_digits=5, decimal_places=2,
            help_text="Target mash temperature (F)")
    strike_temperature = models.DecimalField(_("strike temperature"), max_digits=5, decimal_places=2,
            help_text="Target strike temperature (F)")
    strike = models.DecimalField(_("strike"), max_digits=5, decimal_places=2,
            help_text="Target strike value (Gal)")
    sparge = models.DecimalField(_("sparge"), max_digits=5, decimal_places=2,
            help_text="Target sparge (Gal)")
    ibu = models.DecimalField(_("IBU"), max_digits=4, decimal_places=2,
            help_text="Target IBU")
    abv = models.DecimalField(_("ABV"), max_digits=4, decimal_places=2,
            help_text="Target ABV (%)")
    srm = models.DecimalField(_("SRM"), max_digits=4, decimal_places=2,
            help_text="Target SRM")
    hops = models.ManyToManyField(Hop, blank=True, null=True, 
                                  help_text="Zero or more hops")
    fermentables = models.ManyToManyField(Fermentable, blank=True, null=True, 
                                          help_text="Zero or more fermentable ingredients")
    salts = models.ManyToManyField(Salt, blank=True, null=True, 
                                  help_text="Zero or more salts")
    miscs = models.ManyToManyField(Misc, blank=True, null=True, 
                                   help_text="Zero or more misc records")
    yeasts = models.ManyToManyField(Yeast, blank=True, null=True, 
                                    help_text="Zero or more yeast records")
    notes = models.TextField(_("notes"), blank=True, null=True)
    
    
    def __unicode__(self):
        return u"%s" % self.name

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)
    
    

class RecipeOption(models.Model):
    """
    Each recipe can have a different set of options.
    """
    
    class Meta:
        app_label = "brewing"
        
    # Units
    WEIGHT = (
        (0, u"Use SI units"),
        (1, u"Use US traditional units"),
        (2, u"Use British imperial units")
    )
    
    VOLUME = (
        (0, u"Use SI units"),
        (1, u"Use US traditional units"),
        (2, u"Use British imperial units")
    )

    TEMPERATURE = (
        (0, u"Celsius"),
        (1, u"Fahrenheit")
    )

    GRAVITY = (
        (0, u"20C/20C Specific gravity"),
        (1, u"Plato/Brix/Bailing")
    )
    
    COLOR = (
        (0, u"Use SRM"),
        (1, u"Use EBC")
    )
    
    # Formulas
    COLOR_FORMULAS = (
        (0, u"Mosher's approximation"),
        (1, u"Daniel's approximation"),
        (2, u"Morey's approximation")
    )
    
    IBU_FORMULA = (
        (0, u"Tinseth's approximation"),
        (1, u"Rager's approximation"),
        (2, u"Garetz' approximation")
    )
    
    recipe = models.OneToOneField(Recipe)
    weight = models.PositiveSmallIntegerField(_("weight units"), choices=WEIGHT,
            default=1, help_text="Weight units for this recipe")
    volume = models.PositiveSmallIntegerField(_("volume units"), choices=VOLUME, 
            default=1, help_text="Volume units for this recipe")
    temperature = models.PositiveSmallIntegerField(_("temperature units"), 
            choices=TEMPERATURE, default=1, help_text="""Temperature units for 
            this recipe""")
    gravity = models.PositiveSmallIntegerField(_("gravity units"), 
            choices=GRAVITY, default=0, help_text="Gravity units for this recipe")
    color = models.PositiveSmallIntegerField(_("color system"), choices=COLOR, 
            default=0, help_text="Color system for this recipe")
    color_formula = models.PositiveSmallIntegerField(_("color formula"), 
            choices=COLOR_FORMULAS, default=2, help_text="""Color formula to use 
            for calculating the color for this recipe""")
    ibu_formula = models.PositiveSmallIntegerField(_("ibu formula"), choices=IBU_FORMULA, 
            default=0, help_text="IBU formula to use for calculating IBU for this recipe")
    slug = models.SlugField(max_length=100, blank=True)
    registered_by = models.ForeignKey(User, blank=True, null=True,
            related_name="%(app_label)s_%(class)s_registered_by_set", help_text="Registered by")
    modified_by = models.ForeignKey(User, blank=True, null=True,
            related_name="%(app_label)s_%(class)s_modified_by_set", help_text="Modified by")
    cdt = models.DateTimeField(_("created"), editable=False, auto_now_add=True)
    mdt = models.DateTimeField(_("modified"), editable=False, auto_now=True)
    
    def __unicode__(self):
        return u"%s Recipe options" % self.recipe.name
    
    def clean(self):
        if not self.slug:
            self.slug = slugify("%s-recipe-options" % self.recipe)
# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-09 15:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=5, unique=True, verbose_name='Batch Number(s)')),
            ],
            options={
                'verbose_name_plural': 'Batches',
            },
        ),
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Trade Name')),
            ],
        ),
        migrations.CreateModel(
            name='BrewingEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brewer', models.CharField(blank=True, choices=[('sean', 'Sean'), ('shea', 'Shea'), ('ian', 'Ian'), ('ron', 'Ron'), ('brandon', 'Brandon')], max_length=100, null=True, verbose_name='name of brewer')),
                ('asst_brewer', models.CharField(blank=True, max_length=100, null=True, verbose_name='assistant brewer')),
                ('brew_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('notes', models.TextField(blank=True, null=True, verbose_name='notes')),
                ('batch_number', models.ManyToManyField(blank=True, help_text='Batch Number(s) associated with this brewing event. ', null=True, to='brewing.Batch')),
            ],
            options={
                'verbose_name': 'Brewing Event',
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('version', models.PositiveSmallIntegerField(default=1, editable=False, help_text='XML version', verbose_name='version')),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('cdt', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('mdt', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('capacity', models.DecimalField(decimal_places=2, help_text='Maximum capacity of this container (in bbl).', max_digits=5, verbose_name='Equipment Capactiy')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='notes')),
                ('modified_by', models.ForeignKey(blank=True, help_text='Modified by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brewing_equipment_modified_by_set', to=settings.AUTH_USER_MODEL)),
                ('registered_by', models.ForeignKey(blank=True, help_text='Registered by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brewing_equipment_registered_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Equipment',
            },
        ),
        migrations.CreateModel(
            name='Fermentable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('version', models.PositiveSmallIntegerField(default=1, editable=False, help_text='XML version', verbose_name='version')),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('cdt', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('mdt', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('ferm_type', models.CharField(choices=[('grain', 'Grain'), ('sugar', 'Sugar'), ('extract', 'Extract'), ('dry extract', 'Dry extract'), ('adjunct', 'Adjunct')], max_length=12, verbose_name='fermentable type')),
                ('amount', models.DecimalField(decimal_places=9, help_text='Weight of the fermentable, extract or sugar in pounds.', max_digits=14, verbose_name='amount')),
                ('ferm_yield', models.DecimalField(blank=True, decimal_places=9, help_text='Percent dry yield (fine grain) \n            for the grain, or the raw yield by weight if this is an \n            extract adjunct or sugar.', max_digits=14, null=True, verbose_name='yield percentage')),
                ('color', models.DecimalField(blank=True, decimal_places=9, help_text='The color of the item in Lovibond Units \n            (SRM for liquid extracts).', max_digits=14, null=True, verbose_name='color')),
                ('origin', models.CharField(blank=True, max_length=100, null=True, verbose_name='origin country')),
                ('supplier', models.TextField(blank=True, null=True, verbose_name='supplier')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='notes')),
                ('coarse_fine_diff', models.DecimalField(blank=True, decimal_places=9, help_text='Percent difference \n            between the coarse grain yield and fine grain yield.  Only appropriate for \n            a "Grain" or "Adjunct" type, otherwise this value is ignored.', max_digits=14, null=True, verbose_name='coarse/fine percentage')),
                ('moisture', models.DecimalField(blank=True, decimal_places=9, help_text='Percent \n            moisture in the grain. Only appropriate for a "Grain" or "Adjunct" type, \n            otherwise this value is ignored.', max_digits=14, null=True, verbose_name='moisture percentage')),
                ('diastatic_power', models.DecimalField(blank=True, decimal_places=9, help_text='The diastatic power \n            of the grain as measured in "Lintner" units. Only appropriate for a \n            "Grain" or "Adjunct" type, otherwise this value is ignored.', max_digits=14, null=True, verbose_name='diastatic power')),
                ('protein', models.DecimalField(blank=True, decimal_places=9, help_text='The percent \n            protein in the grain. Only appropriate for a "Grain" or "Adjunct" type, \n            otherwise this value is ignored.', max_digits=14, null=True, verbose_name='protein percentage')),
                ('max_in_batch', models.DecimalField(blank=True, decimal_places=9, help_text='The recommended \n            maximum percentage (by weight) this ingredient should represent in a \n            batch of beer.', max_digits=14, null=True, verbose_name='max percentage per batch')),
                ('recommend_mash', models.NullBooleanField(default=False, help_text='True if it is recommended the grain \n            be mashed, False if it can be steeped. A value of True is only appropriate \n            for a "Grain" or "Adjunct" types. The default value is False. Note that \n            this does NOT indicate whether the grain is mashed or not – it is only \n            a recommendation used in recipe formulation.', verbose_name='recommended mash')),
                ('ibu_gal_per_lb', models.DecimalField(blank=True, decimal_places=9, help_text='For hopped extracts \n            only - an estimate of the number of IBUs per pound of extract in a gallon \n            of water. To convert to IBUs we multiply this number by the "Amount" \n            field (in pounds) and divide by the number of gallons in the batch. \n            Based on a sixty minute boil. Only suitable for use with an "Extract" type, \n            otherwise this value is ignored.', max_digits=14, null=True, verbose_name='bitterness (IBU*gal/lb)')),
                ('display_amount', models.CharField(blank=True, help_text='The amount of fermentables in this record along \n            with the units formatted for easy display in the current user defined units. \n            For example “1.5 lbs” or “2.1 kg”.', max_length=50, null=True, verbose_name='display amount')),
                ('potential', models.DecimalField(blank=True, decimal_places=9, help_text='The yield of the fermentable converted \n            to specific gravity units for display. For example “1.036” or “1.040” \n            might be valid potentials.', max_digits=14, null=True, verbose_name='potential')),
                ('inventory', models.CharField(blank=True, help_text='Amount in inventory for this item along with the units \n            – for example “10.0 lb”', max_length=50, null=True, verbose_name='inventory')),
                ('display_color', models.CharField(blank=True, help_text='Color in user defined color units along with the \n            unit identified – for example “200L” or “40 ebc', max_length=50, null=True, verbose_name='display color')),
                ('modified_by', models.ForeignKey(blank=True, help_text='Modified by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brewing_fermentable_modified_by_set', to=settings.AUTH_USER_MODEL)),
                ('registered_by', models.ForeignKey(blank=True, help_text='Registered by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brewing_fermentable_registered_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Hop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('version', models.PositiveSmallIntegerField(default=1, editable=False, help_text='XML version', verbose_name='version')),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('cdt', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('mdt', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('amount', models.DecimalField(decimal_places=9, help_text='Weight in pounds of the hops used in the recipe.', max_digits=14, verbose_name='amount')),
                ('use', models.CharField(choices=[('@ 60 Minutes', '@ 60 Minutes'), ('@ 10 Minutes', '@ 10 Minutes'), ('@ 5 Minutes', '@ 5 Minutes'), ('@ Whirlpool', '@ Whirlpool'), ('@ First Dry-Hop', '@ First Dry-Hop'), ('@ Second Dry-Hop', '@ Second Dry-Hop')], help_text='The phase at which this hop is added.', max_length=50, verbose_name='usage')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='notes')),
                ('origin', models.CharField(blank=True, max_length=100, null=True, verbose_name='origin')),
                ('inventory', models.CharField(blank=True, help_text='Amount in inventory for this item along with the units \n            – for example “10.0 oz.”', max_length=50, null=True, verbose_name='inventory')),
                ('modified_by', models.ForeignKey(blank=True, help_text='Modified by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brewing_hop_modified_by_set', to=settings.AUTH_USER_MODEL)),
                ('registered_by', models.ForeignKey(blank=True, help_text='Registered by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brewing_hop_registered_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Misc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('version', models.PositiveSmallIntegerField(default=1, editable=False, help_text='XML version', verbose_name='version')),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('cdt', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('mdt', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('misc_type', models.CharField(choices=[('spice', 'Spice'), ('fining', 'Fining'), ('water agent', 'Water agent'), ('herb', 'Herb'), ('flavor', 'Flavor'), ('other', 'Other')], default=4, max_length=12, verbose_name='hop type')),
                ('use', models.CharField(choices=[('boil', 'Boil'), ('mash', 'Mash'), ('primary', 'Primary'), ('secondary', 'Secondary'), ('bottling', 'Bottling')], default=2, max_length=12, verbose_name='hop type')),
                ('time', models.DecimalField(decimal_places=9, help_text='Amount of time the misc was boiled, steeped, mashed, etc in minutes.', max_digits=14, verbose_name='time')),
                ('amount', models.DecimalField(decimal_places=9, help_text='Amount of item used. The default measurements are by weight, \n            but this may be the measurement in volume units if AMOUNT_IS_WEIGHT is set \n            to TRUE for this record. For liquid items this is liters, for solid the  \n            weight is measured in kilograms.', max_digits=14, verbose_name='yield percentage')),
                ('amount_is_weight', models.BooleanField(default=False, help_text='TRUE if the amount measurement is a weight measurement and FALSE if \n            the amount is a volume measurement.', verbose_name='amount is weight')),
                ('use_for', models.TextField(blank=True, help_text='Short description of what the ingredient is used for in text', null=True, verbose_name='use for')),
                ('notes', models.TextField(blank=True, help_text='Detailed notes on the item including usage.', null=True, verbose_name='notes')),
                ('display_amount', models.CharField(blank=True, help_text='The amount of the item in this record along with \n            the units formatted for easy display in the current user defined units. \n            For example “1.5 lbs” or “2.1 kg”.', max_length=50, null=True, verbose_name='display amount')),
                ('inventory', models.CharField(blank=True, help_text='Amount in inventory for this item along with the units \n            – for example “10.0 lb.”', max_length=50, null=True, verbose_name='inventory')),
                ('display_time', models.CharField(blank=True, help_text='Time in appropriate units along with the units \n            as in “10 min” or “3 days”.', max_length=50, null=True, verbose_name='display time')),
                ('modified_by', models.ForeignKey(blank=True, help_text='Modified by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brewing_misc_modified_by_set', to=settings.AUTH_USER_MODEL)),
                ('registered_by', models.ForeignKey(blank=True, help_text='Registered by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brewing_misc_registered_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('version', models.PositiveSmallIntegerField(default=1, editable=False, help_text='XML version', verbose_name='version')),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('cdt', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('mdt', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('pre_boil_batch_size', models.DecimalField(decimal_places=9, help_text='Target pre boil batch size in hectoliters(Hl).', max_digits=14, verbose_name='pre boil batch size')),
                ('pre_boil_gravity', models.DecimalField(decimal_places=9, help_text='Target pre boil gravity(Brix).', max_digits=14, verbose_name='pre boil gravity')),
                ('fermentation_temp', models.DecimalField(decimal_places=2, help_text='Target fermentation temperature (F)', max_digits=5, verbose_name='fermentation temperature')),
                ('mash_temp', models.DecimalField(decimal_places=2, help_text='Target mash temperature (F)', max_digits=5, verbose_name='mash temperature')),
                ('strike_temperature', models.DecimalField(decimal_places=2, help_text='Target strike temperature (F)', max_digits=5, verbose_name='strike temperature')),
                ('strike', models.DecimalField(decimal_places=2, help_text='Target strike value (Gal)', max_digits=5, verbose_name='strike')),
                ('sparge', models.DecimalField(decimal_places=2, help_text='Target sparge (Gal)', max_digits=5, verbose_name='sparge')),
                ('ibu', models.DecimalField(decimal_places=2, help_text='Target IBU', max_digits=4, verbose_name='IBU')),
                ('abv', models.DecimalField(decimal_places=2, help_text='Target ABV (%)', max_digits=4, verbose_name='ABV')),
                ('srm', models.DecimalField(decimal_places=2, help_text='Target SRM', max_digits=4, verbose_name='SRM')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='notes')),
                ('fermentables', models.ManyToManyField(blank=True, help_text='Zero or more fermentable ingredients', null=True, to='brewing.Fermentable')),
                ('hops', models.ManyToManyField(blank=True, help_text='Zero or more hops', null=True, to='brewing.Hop')),
                ('miscs', models.ManyToManyField(blank=True, help_text='Zero or more misc records', null=True, to='brewing.Misc')),
                ('modified_by', models.ForeignKey(blank=True, help_text='Modified by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brewing_recipe_modified_by_set', to=settings.AUTH_USER_MODEL)),
                ('registered_by', models.ForeignKey(blank=True, help_text='Registered by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brewing_recipe_registered_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RecipeOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveSmallIntegerField(choices=[(0, 'Use SI units'), (1, 'Use US traditional units'), (2, 'Use British imperial units')], default=1, help_text='Weight units for this recipe', verbose_name='weight units')),
                ('volume', models.PositiveSmallIntegerField(choices=[(0, 'Use SI units'), (1, 'Use US traditional units'), (2, 'Use British imperial units')], default=1, help_text='Volume units for this recipe', verbose_name='volume units')),
                ('temperature', models.PositiveSmallIntegerField(choices=[(0, 'Celsius'), (1, 'Fahrenheit')], default=1, help_text='Temperature units for \n            this recipe', verbose_name='temperature units')),
                ('gravity', models.PositiveSmallIntegerField(choices=[(0, '20C/20C Specific gravity'), (1, 'Plato/Brix/Bailing')], default=0, help_text='Gravity units for this recipe', verbose_name='gravity units')),
                ('color', models.PositiveSmallIntegerField(choices=[(0, 'Use SRM'), (1, 'Use EBC')], default=0, help_text='Color system for this recipe', verbose_name='color system')),
                ('color_formula', models.PositiveSmallIntegerField(choices=[(0, "Mosher's approximation"), (1, "Daniel's approximation"), (2, "Morey's approximation")], default=2, help_text='Color formula to use \n            for calculating the color for this recipe', verbose_name='color formula')),
                ('ibu_formula', models.PositiveSmallIntegerField(choices=[(0, "Tinseth's approximation"), (1, "Rager's approximation"), (2, "Garetz' approximation")], default=0, help_text='IBU formula to use for calculating IBU for this recipe', verbose_name='ibu formula')),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('cdt', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('mdt', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('modified_by', models.ForeignKey(blank=True, help_text='Modified by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brewing_recipeoption_modified_by_set', to=settings.AUTH_USER_MODEL)),
                ('recipe', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='brewing.Recipe')),
                ('registered_by', models.ForeignKey(blank=True, help_text='Registered by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brewing_recipeoption_registered_by_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Salt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('version', models.PositiveSmallIntegerField(default=1, editable=False, help_text='XML version', verbose_name='version')),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('cdt', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('mdt', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('amount', models.DecimalField(decimal_places=9, help_text='Weight in ounces of the salt used in the recipe.', max_digits=14, verbose_name='amount')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='notes')),
                ('inventory', models.CharField(blank=True, help_text='Amount in inventory for this item along with the units \n            – for example “10.0 oz.”', max_length=50, null=True, verbose_name='inventory')),
                ('modified_by', models.ForeignKey(blank=True, help_text='Modified by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brewing_salt_modified_by_set', to=settings.AUTH_USER_MODEL)),
                ('registered_by', models.ForeignKey(blank=True, help_text='Registered by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brewing_salt_registered_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('version', models.PositiveSmallIntegerField(default=1, editable=False, help_text='XML version', verbose_name='version')),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('cdt', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('mdt', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('style_type', models.CharField(choices=[('lager', 'Lager'), ('ale', 'Ale'), ('mead', 'Mead'), ('wheat', 'Wheat'), ('mixed', 'Mixed'), ('cider', 'Cider')], default=1, help_text='May be “Lager”, “Ale”, “Mead”, “Wheat”, “Mixed” or “Cider”. \n            Defines the type of beverage associated with this category.', max_length=12, verbose_name='type')),
                ('modified_by', models.ForeignKey(blank=True, help_text='Modified by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brewing_style_modified_by_set', to=settings.AUTH_USER_MODEL)),
                ('registered_by', models.ForeignKey(blank=True, help_text='Registered by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brewing_style_registered_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Yeast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('version', models.PositiveSmallIntegerField(default=1, editable=False, help_text='XML version', verbose_name='version')),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('cdt', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('mdt', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('yiest_type', models.CharField(choices=[('ale', 'Ale'), ('lager', 'Lager'), ('wheat', 'Wheat'), ('wine', 'Wine'), ('champagne', 'Champagne')], default=1, max_length=12, verbose_name='yeast type')),
                ('form', models.CharField(choices=[('liquid', 'Liquid'), ('dry', 'Dry'), ('slant', 'Slant'), ('culture', 'Culture')], default=1, max_length=12, verbose_name='yeast form')),
                ('amount', models.DecimalField(decimal_places=9, help_text='The amount of yeast, measured in liters. For a starter this is the \n            size of the starter. If the flag AMOUNT_IS_WEIGHT is set to TRUE then this \n            measurement is in kilograms and not liters.', max_digits=14, verbose_name='amount')),
                ('amount_is_weight', models.BooleanField(default=False, help_text='TRUE if the amount measurement is a weight measurement and FALSE \n            if the amount is a volume measurement.  Default value (if not present) is \n            assumed to be FALSE – therefore the yeast measurement is a liquid amount \n            by default.', verbose_name='amount is weight or litres')),
                ('laboratory', models.CharField(blank=True, max_length=100, null=True, verbose_name='laboratory name')),
                ('product_id', models.CharField(blank=True, help_text='The manufacturer’s product ID label or number that identifies this \n            particular strain of yeast.', max_length=100, null=True, verbose_name='product id')),
                ('min_temperature', models.DecimalField(blank=True, decimal_places=9, help_text='The minimum \n            recommended temperature for fermenting this yeast strain in degrees \n            Celsius.', max_digits=14, null=True, verbose_name='min temperature')),
                ('max_temperature', models.DecimalField(blank=True, decimal_places=9, help_text='The maximum \n            recommended temperature for fermenting this yeast strain in Celsius.', max_digits=14, null=True, verbose_name='max temperature')),
                ('flocculation', models.CharField(blank=True, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('very high', 'Very high')], default=1, max_length=12, null=True, verbose_name='yeast form')),
                ('attenuation', models.DecimalField(blank=True, decimal_places=9, help_text='Average \n            attenuation for this yeast strain.', max_digits=14, null=True, verbose_name='attenuation percentage')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='notes')),
                ('best_for', models.TextField(blank=True, help_text='Styles or types of beer this yeast strain is best suited for.', null=True, verbose_name='best for')),
                ('times_cultured', models.PositiveSmallIntegerField(blank=True, help_text='Number of times this yeast has \n            been reused as a harvested culture. This number should be zero if this \n            is a product directly from the manufacturer.', null=True, verbose_name='times recultured')),
                ('max_reuse', models.PositiveSmallIntegerField(blank=True, help_text='Recommended of times this yeast can be reused \n            (recultured from a previous batch)', null=True, verbose_name='max recultures')),
                ('add_to_secondary', models.BooleanField(default=False, help_text='Flag denoting that this yeast was added for a secondary (or later) \n            fermentation as opposed to the primary fermentation. Useful if one uses two              \n            or more yeast strains for a single brew (eg: Lambic). Default value is FALSE.', verbose_name='amount is weight')),
                ('modified_by', models.ForeignKey(blank=True, help_text='Modified by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brewing_yeast_modified_by_set', to=settings.AUTH_USER_MODEL)),
                ('registered_by', models.ForeignKey(blank=True, help_text='Registered by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brewing_yeast_registered_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='salts',
            field=models.ManyToManyField(blank=True, help_text='Zero or more salts', null=True, to='brewing.Salt'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='style',
            field=models.ForeignKey(help_text='The style of the \n            beer this recipe is associated with.', null=True, on_delete=django.db.models.deletion.CASCADE, to='brewing.Style'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='yeasts',
            field=models.ManyToManyField(blank=True, help_text='Zero or more yeast records', null=True, to='brewing.Yeast'),
        ),
        migrations.AddField(
            model_name='brewingevent',
            name='recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='brewing.Recipe'),
        ),
        migrations.AddField(
            model_name='brewingevent',
            name='vessel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='brewing.Equipment'),
        ),
    ]

"""Defines Models for database tables of inventory for ecommerce site.

UUID version 4 is used in the Product Line model.
"""

import uuid

from django.db import models


class Product(models.Model):
    """this class is for the Product table

    Args:
        pid (CharField): Product ID number
        name (CharField): Product name
        slug (SlugField): Product slug data
        description (TextField): Product description
        is_digital (BooleanField): Product data
        created_at (DateTimeField): Product data creation date, auto created
        updated_at (DateTimeField): Product data last updated date, auto created
        is_active (BooleanField): Product data
        stock_status (CharField): options are "IS" | "OOS" | "BO"
    """

    IN_STOCK = "IS"
    OUT_OF_STOCK = "OOS"
    BACKORDERED = "BO"

    STOCK_STATUS = {
        IN_STOCK: "In Stock",
        OUT_OF_STOCK: "Out of Stock",
        BACKORDERED: "Back Ordered",
    }

    pid = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(null=True)
    is_digital = models.BooleanField(default=False)
    # auto_now sets it to whenever it is edited.
    # auto_now_add stores creation date and locks it
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=False)
    stock_status = models.CharField(
        max_length=3,
        choices=STOCK_STATUS,
        default=OUT_OF_STOCK,
    )


class ProductLine(models.Model):
    """class for Product Line table

    Args:
        price (DecimalField): Product price
        sku (UUIDField): version 4 uuid for product
        stock_qty (IntegerField): how many of the products are in stock
        is_active (BooleanField): if the product is active
        order (IntegerField): order number of product line
        weight (FloatField): weight of product
    """

    price = models.DecimalField()
    sku = models.UUIDField(default=uuid.uuid4)
    stock_qty = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    order = models.IntegerField()
    weight = models.FloatField()


class ProductImage(models.Model):
    """class for Product Image table, stores image url

    Args:
        name (CharField): title of product image
        alternative_text (CharField): alt_text for product image
        url (ImageField): url of image
        order (IntegerField): _description_
    """

    name = models.CharField(max_length=100)
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField()
    order = models.IntegerField()


#
class Category(models.Model):
    """Class for Category table. Products are organized by Category.

    Args:
        name (CharField): name of category
        slug (SlugField): category slug
        is_active (BooleanField): whether the category is active
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField()
    is_active = models.BooleanField(default=False)


# class for Seasonal Events table
class SeasonalEvents(models.Model):
    """SeasonalEvents table, manual entry

    Args:
        start_date (DateTimeField): beginning date and time of event
        end_date (DateTimeField): ending date and time of event
        name (CharField): name of the seasonal event
    """

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.CharField(max_length=100)

"""Defines Models for database tables of inventory for ecommerce site.
Primary keys are id numbers, BigAutoField.
UUID version 4 is used in the Product Line model.
"""

import uuid

from django.db import models


class Category(models.Model):
    """Class for Category table. Products are organized by Category. Categories have
    self-referencing relationships to allow parent-child hierarchy structures.

    Args:
        name (CharField): name of category
        slug (SlugField): category slug
        is_active (BooleanField): whether the category is active
        parent(ForeignKey): references self, allowing subcategories. Categories are
            protected from deletion if they have any parent subcategories.
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=False)
    parent = models.ForeignKey("self", on_delete=models.PROTECT)


class SeasonalEvents(models.Model):
    """SeasonalEvents table, manual entry

    Args:
        id (BigAutoField): auto-generated primary key
        start_date (DateTimeField): beginning date and time of event
        end_date (DateTimeField): ending date and time of event
        name (CharField): unique name of the seasonal event
    """

    id = models.BigAutoField(primary_key=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.CharField(max_length=100, unique=True)


class ProductType(models.Model):
    """ProductType is self-referencing so it can have subcategories. Has a Many to Many
        relationship with Product table.

    Args:
        name (CharField): type of product
        parent (ForeignKey): references self, deletes referenced data on deletion
    """

    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", on_delete=models.CASCADE)


class Product(models.Model):
    """this class is for the Product table.

    Args:
        pid (CharField): Product ID number
        name (CharField): Unique Product name
        slug (SlugField): Product url-friendly string helps select individual products
        description (TextField): Product description
        is_digital (BooleanField): Product is digital or not
        created_at (DateTimeField): Product data creation date, auto created
        updated_at (DateTimeField): Product data last updated date, auto created
        is_active (BooleanField): Product is active or not
        stock_status (CharField): options are "IS" | "OOS" | "BO"
        category (ForeignKey): refrences Category table, set to null on deletion
        seasonal_event (ForeignKey): references SeasonalEvents table, null on deletion
        product_type (ManyToManyField): has a M2M relationship with ProductType table
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
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
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
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    seasonal_event = models.ForeignKey(
        SeasonalEvents, on_delete=models.SET_NULL, null=True
    )
    product_type = models.ManyToManyField(ProductType, related_name="product_type")


class Attribute(models.Model):
    """Attributes are generic so they can be applied to each product. Has a Many to Many
        relationship with ProductLine table.

    Args:
        name (CharField): name of attribute
        description (TextField): describes the attribute
    """

    name = models.CharField(max_length=100)
    description = models.TextField(null=True)


class AttributeValue(models.Model):
    """AttributeValue has a M2M relationship with the ProductLine table, and a many-to-1
    relationship with the Attribute table. It stores the actual attribute value of a
    product in the ProductLine.

    Args:
        attribute_value (CharField): description of attribute data
        attribute (ForeignKey): references Attribute table, deletes referenced data on
            deletion
    """

    attribute_value = models.CharField(max_length=100)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)


class ProductLine(models.Model):
    """class for Product Line table

    Args:
        price (DecimalField): Product price
        sku (UUIDField): version 4 uuid for product
        stock_qty (IntegerField): how many of the products are in stock
        is_active (BooleanField): if the product is active
        order (IntegerField): order number of product line
        weight (FloatField): weight of product
        product (ForeignKey): references Product table, protects on deletion
        attribute_value (ManyToManyField): M2M relationship with AttributeValue table
    """

    price = models.DecimalField()
    sku = models.UUIDField(default=uuid.uuid4)
    stock_qty = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    order = models.IntegerField()
    weight = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    attribute_value = models.ManyToManyField(
        AttributeValue, related_name="attribute_value"
    )


class ProductImage(models.Model):
    """class for Product Image table, stores image url

    Args:
        name (CharField): title of product image
        alternative_text (CharField): alt_text for product image
        url (ImageField): url of image
        order (IntegerField): ProductImage data order
        product_line (ForiegnKey): references ProductLine table, cascades on deletion
    """

    name = models.CharField(max_length=100)
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField()
    order = models.IntegerField()
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE)


class ProductLine_AttributeValue(models.Model):
    """ProductLine_AttributeValue resolves the M2M relationship between ProductLine and
    AttributeValue tables. It has a many-to-one relationship with the ProductLine table
    and a many-to-one relationship with the AttributeValue table. It's a "linked" or
    "through" table.

    Args:
        attribute_value (ForeignKey): references AttributeValue table, deletes
            referenced data on deletion
        product_line (ForeignKey): references ProductLine table, deletes referenced
            data on deletion
    """

    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE)


class Product_ProductType(models.Model):
    """Product_ProductType resolves the M2M relationship between Product and ProductType
    tables. It has a many-to-one relationship with the Product table and a many-to-one
    relationship with the ProductType table. It's a "linked" or "through" table.

    Args:
        product (ForeignKey): references Product table, deletes referenced data on
            deletion
        product_type (ForeignKey): references ProductType table, deletes referenced
            data on deletion
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)


# this class might be implemented in the future if needed.
# class StockControl(models.Model):
#     """StockControl has a 1-to-1 relationship with the Product table. It tracks the
#     amount of each product in stock and who last checked the inventory.

#     Args:
#         stock_qty (IntegerField): the number of product in stock
#         name (CharField): the person who last checked the inventory for this product
#         stock_product (OneToOneField): references Product table, cascades on deletion
#     """

#     stock_qty = models.IntegerField()
#     name = models.CharField(max_length=100)
#     stock_product = models.OneToOneField(Product, on_delete=models.CASCADE)

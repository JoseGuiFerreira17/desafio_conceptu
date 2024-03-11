import os
import uuid
from django.db import models
from django.utils.text import slugify
from apps.core.models import BaseModelMixin


class Category(BaseModelMixin):
    name = models.CharField("nome", max_length=60)
    slug = models.SlugField("slug", unique=True)
    parent = models.ForeignKey(
        "self", blank=True, null=True, related_name="children", on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        full_path = [self.name]
        i = self.parent
        while i is not None:
            full_path.append(i.name)
            i = i.parent
        return " -> ".join(full_path[::-1])

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"


def product_image_directory_path(instance, filename):
    name, extension = os.path.splitext(filename)
    return "{0}/product/{1}{2}".format(instance.slug, name, extension)


class Product(BaseModelMixin):
    category = models.ForeignKey(
        "product.Category",
        verbose_name="categoria",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField("nome", max_length=100)
    slug = models.SlugField("slug", unique=True, db_index=True)
    description = models.TextField("descrição", null=True, blank=True)
    value = models.DecimalField("valor", max_digits=22, decimal_places=2)
    image = models.ImageField(
        verbose_name="imagem",
        upload_to=product_image_directory_path,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "produto"
        verbose_name_plural = "produtos"

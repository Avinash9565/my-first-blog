from django.db import models
# Create your models here.
class Customer(models.Model):
    Name = models.CharField( max_length=50)
    Mail = models.EmailField( max_length=254)
    Phnno = models.BigIntegerField()
    worker = models.BooleanField()
    work = models.CharField( max_length=50)
    user_ID = models.CharField(max_length=20,primary_key=True)
    password = models.CharField( max_length=50)
    def __str__(self):
        return self.Name
class order(models.Model):
    user = models.CharField( max_length=25)
    work = models.CharField( max_length=25)
    worker = models.CharField( max_length=25)
    date = models.DateField()
    slot = models.CharField( max_length=25)
class p_order(models.Model):
    user = models.CharField( max_length=25)
    work = models.CharField( max_length=25)
    worker = models.CharField( max_length=25)
    date = models.DateField()
    slot = models.CharField( max_length=25)
    part = models.CharField( max_length=25)


    

    """class Meta:
        verbose_name = _("")
        verbose_name_plural = _("s")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})"""



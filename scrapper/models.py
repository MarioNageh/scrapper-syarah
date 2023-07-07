from django.db import models
from scrapper.modules.car import Car as CarModel
from scrapper.modules.scrapper_memory import Memory


class Car(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    image_url = models.CharField(max_length=1024)  # max Url Size 1kb
    currency = models.CharField(max_length=255)
    hash = models.CharField(max_length=255)
    scrapped_time = models.DateTimeField()


    def __str__(self):
        return f"Name: {self.name}, price: {self.price}"

    @staticmethod
    def insert(car: CarModel):
        # if Website Change its order don't duplicate data
        car_by_hash = Car.objects.filter(hash=car.hash).first()
        if car_by_hash:
            return car_by_hash

        c = Car(
            name=car.name,
            status=car.status,
            price=car.price,
            image_url=car.image_url,
            currency=car.currency,
            hash=car.hash,
            scrapped_time=car.scrapped_time
        )
        c.save()
        return c


class ScrapperMemory(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    total_scrapped_itme = models.IntegerField(default=0)
    last_scrapped_car = models.ForeignKey(Car, null=True, on_delete=models.SET_NULL)
    last_scrolled_page = models.IntegerField(default=0)
    last_scrapped_item_number = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.pk = 1  # to ensure only one row
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Scrapper Memory"

    @staticmethod
    def update_memory(m: Memory):
        memory = ScrapperMemory.objects.get(id=1)
        memory.last_scrapped_item_number = m.last_scrapped_item_number
        memory.last_scrolled_page = m.last_scrolled_page_number
        memory.last_scrapped_car = m.last_scrapped_item
        memory.total_scrapped_itme = m.total_scrapped_item

        memory.save()

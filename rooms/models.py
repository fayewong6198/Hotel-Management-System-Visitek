from django.db import models
from datetime import datetime
from accounts.models import User
# Create your models here.


class Room(models.Model):
    room_id = models.CharField(max_length=31, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    adults = models.SmallIntegerField(default=1)
    children = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.room_id


class Payment(models.Model):
    WAITING = "WAITING"
    CHECKED_IN = "CHECKED_IN"
    CHECKED_OUT = "CHECKED_OUT"
    PAID = "PAID"
    CANCLED = "CANCLED"

    STATUS_CHOICES = (
        (WAITING, "WAITING"),
        (CHECKED_IN, "CHECKED_IN"),
        (CHECKED_OUT, "CHECKED_OUT"),
        (PAID, "PAID"),
        (CANCLED, "CANCLED"),

    )

    room = models.ForeignKey(
        Room, on_delete=models.DO_NOTHING, related_name="payments")
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="payments")
    expected_check_in_date = models.DateField()
    expected_check_out_date = models.DateField()
    check_in_date = models.DateField(blank=True, null=True)
    check_out_date = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=WAITING
    )
    service_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.room.room_id + " --- " + self.created_at.strftime("%d-%b-%Y (%H:%M:%S.%f)")


class RoomImage(models.Model):
    image = models.ImageField(upload_to='room_images/')
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return self.image.url

    def get_url(self):
        return self.image.url

    def to_dict_url(self):
        return {"image": self.image.url}

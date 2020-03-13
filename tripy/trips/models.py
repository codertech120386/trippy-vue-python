import datetime
from django.db import models
from utils.abstract_models import Base


class Trip(Base):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    destination = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    comment = models.TextField()

    def search_blob(self):
        return "::".join([self.destination, str(self.start_date), str(self.end_date), self.comment]).lower()

    def __str__(self):
        return "{} - {}".format(self.user.email, self.destination)

    def days_left(self):
        return (self.start_date - datetime.date.today()).days

    class Meta:
        db_table = "trips"

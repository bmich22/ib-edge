from django.db import models

# Create your models here.


# Tutoring subjects like "Math HL", "English SL"
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


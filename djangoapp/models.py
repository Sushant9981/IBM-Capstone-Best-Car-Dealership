# Uncomment the following imports before adding the Model code

from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.


class CarMake(models.Model):
    """Model representing a car make (e.g., BMW, Toyota)."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Other fields as needed

    def __str__(self):
        return self.name  # Return the name as the string representation


class CarModel(models.Model):
    """Model representing a specific car model."""
    car_make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE
    )  # Many-to-One relationship
    name = models.CharField(max_length=100)

    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        # Add more choices as required
    ]
    type = models.CharField(
        max_length=10,
        choices=CAR_TYPES,
        default='SUV'
    )
    year = models.IntegerField(
        default=2023,
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015),
        ],
    )
    # Other fields as needed

    def __str__(self):
        return self.name  # Return the name as the string representation


class LocalReview(models.Model):
    """Model to store dealer reviews locally."""
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    review = models.TextField()
    purchase_date = models.DateField(default=now)
    car_make = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    car_year = models.CharField(max_length=4)
    sentiment = models.CharField(max_length=20, default="neutral")

    def __str__(self):
        return (
            f"{self.name} - {self.car_make} "
            f"{self.car_model} ({self.car_year})"
        )

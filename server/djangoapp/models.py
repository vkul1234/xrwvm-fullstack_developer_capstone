# Uncomment the following imports before adding the Model code
from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class CarMake(models.Model):
    """
    CarMake model represents a car brand or manufacturer.
    Fields:
    - name: The name of the car manufacturer (e.g., 'Toyota').
    - description: A description of the car manufacturer.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name  # String representation returns the car make's name


class CarModel(models.Model):
    """
    CarModel model represents a specific car model.
    Fields:
    - car_make: ForeignKey to the CarMake model (one-to-many relationship).
    - name: The name of the car model (e.g., 'Camry').
    - type: The type of car (e.g., 'SUV', 'Sedan', etc.).
    - year: The year the car model was manufactured, limited to between 2015 and 2023.
    """
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    # Define car types as a choice field
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        # Add more choices as needed
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')

    # Validate year with a minimum of 2015 and maximum of 2023
    year = models.IntegerField(
        default=2023,
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ]
    )

    def __str__(self):
        return f"{self.name} ({self.car_make.name})"  # String representation includes car make and model

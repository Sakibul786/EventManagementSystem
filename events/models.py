from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Participant(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="participant_profile",
    )

    name = models.CharField(
        max_length=100,
    )

    email = models.EmailField(
        unique=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(
        max_length=200,
    )

    description = models.TextField()

    date = models.DateField()

    time = models.TimeField()

    location = models.CharField(
        max_length=200,
    )

    # NEW
    capacity = models.PositiveIntegerField(
        default=50,
        help_text="Maximum number of participants allowed.",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="events",
    )

    participants = models.ManyToManyField(
        Participant,
        blank=True,
        related_name="events",
    )

    class Meta:
        ordering = ["date", "time"]

    def __str__(self):
        return self.name

    @property
    def participant_count(self):
        return self.participants.count()

    @property
    def seats_remaining(self):
        return max(0, self.capacity - self.participant_count)

    @property
    def is_full(self):
        return self.participant_count >= self.capacity
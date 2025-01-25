from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    TEAM_CHOICES = [
        ("Wing", "Wing Team"),
        ("Fuselage", "Fuselage Team"),
        ("Tail", "Tail Team"),
        ("Avionics", "Avionics Team"),
        ("Assembly", "Assembly Team"),
        ("NoTeam", "No Team"),
    ]
    name = models.CharField(max_length=50, choices=TEAM_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class Personnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name="personnel")

    def __str__(self):
        return self.user.username


class Aircraft(models.Model):
    AIRCRAFT_CHOICES = [
        ("TB2", "TB2"),
        ("TB3", "TB3"),
        ("AKINCI", "AKINCI"),
        ("KIZILELMA", "KIZILELMA"),
    ]
    name = models.CharField(max_length=50, choices=AIRCRAFT_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class Part(models.Model):
    PART_CHOICES = [
        ("Wing", "Wing"),
        ("Fuselage", "Fuselage"),
        ("Tail", "Tail"),
        ("Avionics", "Avionics"),
    ]
    part_type = models.CharField(max_length=50, choices=PART_CHOICES)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name="parts")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="parts")
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("part_type", "aircraft", "team")

    def __str__(self):
        return f"{self.get_part_type_display()} for {self.aircraft}"


class Assembly(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True, related_name="assemblies")
    wings = models.ForeignKey(Part, on_delete=models.SET_NULL, null=True, related_name="assembled_wings")
    fuselages = models.ForeignKey(Part, on_delete=models.SET_NULL, null=True, related_name="assembled_fuselages")
    tails = models.ForeignKey(Part, on_delete=models.SET_NULL, null=True, related_name="assembled_tails")
    avionics = models.ForeignKey(Part, on_delete=models.SET_NULL, null=True, related_name="assembled_avionics")
    assembled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assembly of {self.aircraft} at {self.assembled_at}"

from django.contrib.auth.models import User
from rest_framework import serializers

from rental.models import Aircraft, Assembly, Part, Personnel, Team


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name"]


class PersonnelSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Personnel
        fields = ["id", "user", "team"]


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ["id", "name"]


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ["id", "part_type", "aircraft", "team", "stock"]


class AssemblySerializer(serializers.ModelSerializer):
    class Meta:
        model = Assembly
        fields = ["id", "aircraft", "wings", "fuselages", "tails", "avionics", "assembled_at"]

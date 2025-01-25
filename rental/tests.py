from django.test import TestCase

from .models import Aircraft, Assembly, Part, Team


class TeamModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Wing")

    def test_team_creation(self):
        self.assertEqual(self.team.name, "Wing")
        self.assertEqual(str(self.team), "Wing Team")


class AircraftModelTest(TestCase):
    def setUp(self):
        self.aircraft = Aircraft.objects.create(name="TB2")

    def test_aircraft_creation(self):
        self.assertEqual(self.aircraft.name, "TB2")
        self.assertEqual(str(self.aircraft), "TB2")


class PartModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Wing")
        self.aircraft = Aircraft.objects.create(name="TB2")
        self.part = Part.objects.create(part_type="Wing", aircraft=self.aircraft, team=self.team, stock=10)

    def test_part_creation(self):
        self.assertEqual(self.part.part_type, "Wing")
        self.assertEqual(self.part.stock, 10)
        self.assertEqual(str(self.part), "Wing for TB2")


class AssemblyModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Assembly")
        self.aircraft = Aircraft.objects.create(name="TB2")
        self.wing = Part.objects.create(part_type="Wing", aircraft=self.aircraft, team=self.team, stock=5)
        self.fuselage = Part.objects.create(part_type="Fuselage", aircraft=self.aircraft, team=self.team, stock=5)
        self.tail = Part.objects.create(part_type="Tail", aircraft=self.aircraft, team=self.team, stock=5)
        self.avionics = Part.objects.create(part_type="Avionics", aircraft=self.aircraft, team=self.team, stock=5)
        self.assembly = Assembly.objects.create(
            aircraft=self.aircraft, wings=self.wing, fuselages=self.fuselage, tails=self.tail, avionics=self.avionics
        )

    def test_assembly_creation(self):
        self.assertEqual(str(self.assembly), f"Assembly of {self.aircraft} at {self.assembly.assembled_at}")

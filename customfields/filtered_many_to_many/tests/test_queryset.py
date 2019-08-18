from django.test import TestCase

from filtered_many_to_many.models import Person, Pet


class QuerySetTestCase(TestCase):

    fixtures = ["test"]

    def test_person_pets_success_none_deleted(self):
        expected = list(
            Pet.objects
            .filter(name__in=["Mittens", "Fluffy"])
        )
        found = list(
            Person.objects.get(name="John")
            .pets
            .all()
        )

        self.assertCountEqual(expected, found)

    def test_person_pets_success_some_deleted(self):
        expected = list(
            Pet.objects
            .filter(name__in=["Mittens", "Fluffy"])
        )
        found = list(
            Person.objects.get(name="Sally")
            .pets
            .all()
        )

        self.assertCountEqual(expected, found)

    def test_person_pets_success_all_deleted(self):
        expected = []
        found = list(
            Person.objects.get(name="Lesley")
            .pets
            .all()
        )

        self.assertCountEqual(expected, found)

    def test_pet_people_success_none_deleted(self):
        expected = list(
            Person.objects
            .filter(name__in=["John", "Sally"])
        )
        found = list(
            Pet.objects.get(name="Mittens")
            .people
            .all()
        )

        self.assertCountEqual(expected, found)

    def test_pet_people_success_some_deleted(self):
        expected = list(
            Person.objects
            .filter(name__in=["John", "Sally"])
        )
        found = list(
            Pet.objects.get(name="Fluffy")
            .people
            .all()
        )

        self.assertCountEqual(expected, found)

    def test_pet_people_success_all_deleted(self):
        expected = []
        found = list(
            Pet.objects.get(name="Boo")
            .people
            .all()
        )

        self.assertCountEqual(expected, found)

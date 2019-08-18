from django.test import TestCase

from filtered_many_to_many.models import Person, Pet


class FilterTestCase(TestCase):

    fixtures = ["test"]

    def test_person_pets_success_none_deleted(self):
        expected = list(
            Person.objects
            .filter(name__in=["John", "Sally"])
        )
        found = list(
            Person.objects
            .filter(pets__name="Mittens")
        )

        self.assertCountEqual(expected, found)

    def test_person_pets_success_some_deleted(self):
        expected = list(
            Person.objects
            .filter(name__in=["John", "Sally"])
        )
        found = list(
            Person.objects
            .filter(pets__name="Fluffy")
        )

        self.assertCountEqual(expected, found)

    def test_person_pets_success_all_deleted(self):
        expected = []
        found = list(
            Person.objects
            .filter(pets__name="Boo")
        )

        self.assertCountEqual(expected, found)

    def test_pet_people_success_none_deleted(self):
        expected = list(
            Pet.objects
            .filter(name__in=["Mittens", "Fluffy"])
        )
        found = list(
            Pet.objects
            .filter(people__name="John")
        )

        self.assertCountEqual(expected, found)

    def test_pet_people_success_some_deleted(self):
        expected = list(
            Pet.objects
            .filter(name__in=["Mittens", "Fluffy"])
        )
        found = list(
            Pet.objects
            .filter(people__name="Sally")
        )

        self.assertCountEqual(expected, found)

    def test_pet_people_success_all_deleted(self):
        expected = []
        found = list(
            Pet.objects
            .filter(people__name="Lesley")
        )

        self.assertCountEqual(expected, found)

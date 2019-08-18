from django.test import TestCase

from filtered_many_to_many.models import Person, Pet


class ValuesTestCase(TestCase):

    fixtures = ["test"]

    def test_person_pets_success_none_deleted(self):
        expected = ["Mittens", "Fluffy"]
        found = list(
            Person.objects
            .filter(name="John")
            .values_list("pets__name", flat=True)
        )

        self.assertCountEqual(expected, found)

    def test_person_pets_success_some_deleted(self):
        expected = ["Mittens", "Fluffy"]
        found = list(
            Person.objects
            .filter(name="Sally")
            .values_list("pets__name", flat=True)
        )

        self.assertCountEqual(expected, found)

    def test_person_pets_success_all_deleted(self):
        expected = []
        found = list(
            Person.objects
            .filter(name="Lesley")
            .values_list("pets__name", flat=True)
        )

        self.assertCountEqual(expected, found)

    def test_pet_people_success_none_deleted(self):
        expected = ["John", "Sally"]
        found = list(
            Pet.objects.filter(name="Mittens").values_list(
                "people__name", flat=True)
        )

        self.assertCountEqual(expected, found)

    def test_pet_people_success_some_deleted(self):
        expected = ["John", "Sally"]
        found = list(
            Pet.objects
            .filter(name="Fluffy")
            .values_list("people__name", flat=True)
        )

        self.assertCountEqual(expected, found)

    def test_pet_people_success_all_deleted(self):
        expected = []
        found = list(
            Pet.objects
            .filter(name="Boo")
            .values_list("people__name", flat=True)
        )

        self.assertCountEqual(expected, found)

import uuid

from django.db import models


class Person(models.Model):
    id = models.UUIDField("id", primary_key=True, default=uuid.uuid4)
    name = models.CharField("name", max_length=255)

    pets = models.ManyToManyField(
        "Pet",
        verbose_name="pets",
        related_name="people",
        through="PersonPetsNonDeletedView",
    )

    def __str__(self) -> str:
        return self.name


class Pet(models.Model):
    id = models.UUIDField("id", primary_key=True, default=uuid.uuid4)
    name = models.CharField("name", max_length=255)

    def __str__(self) -> str:
        return self.name


class PersonPets(models.Model):
    id = models.UUIDField("id", primary_key=True, default=uuid.uuid4)

    person = models.ForeignKey(
        Person,
        verbose_name="person",
        related_name="pet_relations",
    )
    pet = models.ForeignKey(
        Pet,
        verbose_name="pet",
        related_name="person_relations",
    )

    is_deleted = models.BooleanField("is deleted", default=False)

    def __str__(self) -> str:
        result = f"{self.person} <-> {self.pet}"

        if self.is_deleted:
            result = f"(DELETED {result})"

        return result

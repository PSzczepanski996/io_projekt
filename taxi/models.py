"""Mainapp models file."""
from django.db import models


class Klient(models.Model):  # noqa: D101

    idKlienta = models.IntegerField(primary_key=True)
    imieKlienta = models.CharField(max_length=50)
    nrTelefonu = models.CharField(max_length=9)
    dlugoscGeoKlienta = models.FloatField()
    szerokoscGeoKlienta = models.FloatField()

    def __str__(self):  # noqa: D105
        return f'{self.imieKlienta}'


class Dyspozytor(models.Model):  # noqa: D101

    idDyspozytora = models.IntegerField(primary_key=True)
    imieDyspozytora = models.CharField(max_length=50)
    nazwiskoDyspozytora = models.CharField(max_length=50)

    def __str__(self):  # noqa: D105
        return f'{self.imieDyspozytora} {self.nazwiskoDyspozytora}'


class Kierowca(models.Model):  # noqa: D101

    idKierowcy = models.IntegerField(primary_key=True)
    imieKierowcy = models.CharField(max_length=50)
    nazwiskoKierowcy = models.CharField(max_length=50)
    dlugoscGeoKierowcy = models.FloatField()
    szerokoscGeoKierowcy = models.FloatField()

    def __str__(self):  # noqa: D105
        return f'{self.imieKierowcy} {self.nazwiskoKierowcy}'


class Usluga(models.Model):  # noqa: D101

    idUsluga = models.IntegerField(primary_key=True)
    idDyspozytora = models.IntegerField()
    idKierowcy = models.ForeignKey(Kierowca, on_delete=models.CASCADE)
    idKlienta = models.ForeignKey(Klient, on_delete=models.CASCADE)
    dlugoscGeoCelu = models.FloatField()
    szerokoscGeoCelu = models.FloatField()

    def __str__(self):  # noqa: D105
        return f'Usługa o id {self.idUsluga}'
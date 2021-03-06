"""Mainapp models file."""
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from mobile.utils import state_dict


class Klient(models.Model):  # noqa: D101

    idKlienta = models.AutoField(primary_key=True)
    imieKlienta = models.CharField(max_length=50)
    nrTelefonu = models.CharField(max_length=9)

    def __str__(self):  # noqa: D105
        return f'{self.imieKlienta} {self.nrTelefonu}'

    class Meta:
        verbose_name = 'Klient'
        verbose_name_plural = 'Klienci'


class Dyspozytor(models.Model):  # noqa: D101

    idDyspozytora = models.AutoField(primary_key=True)
    imieDyspozytora = models.CharField(max_length=50)
    nazwiskoDyspozytora = models.CharField(max_length=50)

    def __str__(self):  # noqa: D105
        return f'{self.imieDyspozytora} {self.nazwiskoDyspozytora}'

    class Meta:
        verbose_name = 'Dyspozytor'
        verbose_name_plural = 'Dyspozytory'


class Kierowca(models.Model):  # noqa: D101

    idKierowcy = models.AutoField(primary_key=True)
    imieKierowcy = models.CharField(max_length=50)
    nazwiskoKierowcy = models.CharField(max_length=50)

    def __str__(self):  # noqa: D105
        return f'{self.imieKierowcy} {self.nazwiskoKierowcy}'

    def get_status(self):
        html = '<span class="fst-italic {0}">{1}</span>'
        get_drivers = []
        for key, value in state_dict.items():
            if value > timezone.now() - timedelta(minutes=getattr(settings, 'AUTOLOGOUT_MINUTES', 5)):
                get_drivers.append(key)
        busy = list(Kierowca.objects.filter(usluga__in=Usluga.objects.filter(
            statusRealizacji__in=[Usluga.W_TRAKCIE])).values_list('idKierowcy', flat=True))
        if self.idKierowcy in busy:
            return mark_safe(html.format('text-info', 'Zajęty'))
        elif self.idKierowcy in get_drivers:
            return mark_safe(html.format('text-success', 'Dostępny'))
        return mark_safe(html.format('text-danger', 'Niedostępny'))

    class Meta:
        verbose_name = 'Kierowca'
        verbose_name_plural = 'Kierowcy'


class Usluga(models.Model):  # noqa: D101

    idUsluga = models.AutoField(primary_key=True)
    W_TRAKCIE = 1
    ZAKONCZONO = 2
    STATUSY_REALIZACJI = (
        (W_TRAKCIE, 'W trakcie'),
        (ZAKONCZONO, 'Zakonczono')
    )
    statusRealizacji = models.IntegerField(choices=STATUSY_REALIZACJI)
    idDyspozytora = models.ForeignKey(
        Dyspozytor,
        on_delete=models.CASCADE,
    )
    idKierowcy = models.ForeignKey(
        Kierowca,
        on_delete=models.CASCADE,
        null=True, blank=True,
    )
    idKlienta = models.ForeignKey(
        Klient,
        on_delete=models.CASCADE,
    )
    szerokoscGeoKlienta = models.FloatField(
        null=True, blank=True,
    )
    dlugoscGeoKlienta = models.FloatField(
        null=True, blank=True,
    )
    szerokoscGeoCelu = models.FloatField()
    dlugoscGeoCelu = models.FloatField()

    def __str__(self):  # noqa: D105
        return f'Usługa o id {self.idUsluga}'

    class Meta:
        verbose_name = 'Usluga'
        verbose_name_plural = 'Uslugi'

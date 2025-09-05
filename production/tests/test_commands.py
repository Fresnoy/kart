import sys
import io
import os

from people.tests.factories import ArtistFactory
import pytest

from django.core.management import call_command
from django.db import connection

from production.tests.factories import (
    ArtworkFactory,
)


# Neutralise le clear
def fake_system_clear(cmd):
    if cmd in ("clear", "cls"):
        return 0  # neutralise le clear
    return os.system(cmd)  # tout le reste s’exécute normalement


@pytest.mark.django_db
def test_import_catalog(monkeypatch):
    "simple TEST Command: import_catalog"

    # remove 'clear' terminal
    monkeypatch.setattr("os.system", fake_system_clear)
    result = call_command('import_catalog', "--path_to_csv", "coucou.csv")
    # not really tested
    assert result is None


@pytest.mark.django_db
@pytest.mark.unaccent
def test_set_artwork_credits(monkeypatch):
    "simple TEST Command: set_artwork_credits"

    artist = ArtistFactory(nickname="Michel Serrault")
    artist.save()

    artwork = ArtworkFactory(title="Le Coucou")
    artwork.save()

    fake_input = io.StringIO("Michel Serrault: Actor\nMichel Serrault: Actor\n\nLe Coucou\n0\nn\n")

    # Remplacer sys.stdin par notre fausse entrée
    monkeypatch.setattr(sys, "stdin", fake_input)

    monkeypatch.setattr("os.system", fake_system_clear)

    # unaccent test bug
    if connection.vendor == "postgresql":
        with connection.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS unaccent;")
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

    # Lancer la commande
    result = call_command('set_artwork_credits')
    assert result is None

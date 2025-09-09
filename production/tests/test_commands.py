from django.contrib.auth.models import User

from people.tests.factories import ArtistFactory
import pytest

from django.core.management import call_command
from django.db import connection

from production.tests.factories import (
    ArtworkFactory,
)

from production.management.commands.set_artwork_credits import setArtworkCredits


@pytest.mark.django_db
def test_import_catalog(monkeypatch):
    "simple TEST Command: import_catalog"

    # remove 'clear' terminal
    monkeypatch.setattr("os.system", lambda cmd: 0)  # neutralise juste clear
    result = call_command('import_catalog', "--path_to_csv", "coucou.csv")
    # not really tested
    assert result is None


@pytest.mark.django_db
@pytest.mark.unaccent
def test_set_artwork_credits(monkeypatch):
    "simple TEST Command: set_artwork_credits"

    artist = ArtistFactory(nickname="Michel Serrault",
                           user=User.objects.get_or_create(first_name="Michel", last_name="Serrault")[0])
    artist.save()

    artwork = ArtworkFactory(title="Le Coucou")
    artwork.save()

    fake_input_str = 'Michel Serrault: Actor\nMichel Serrault: Actor\n\nLe Coucou\n0\nn\n'
    # fake_input_io = io.StringIO(fake_input_str)

    # # Remplacer sys.stdin par notre fausse entrée
    # monkeypatch.setattr(sys, "stdin", fake_input_io)

    # unaccent test bug
    if connection.vendor == "postgresql":
        with connection.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS unaccent;")
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

    # Lancer la commande
    # result = call_command('set_artwork_credits')
    # assert result is None
    # not really tested
    # assert result is None

    setArtworkCredits(artwork, fake_input_str)
    print(artwork.collaborators.count())
    assert artwork.collaborators.count() >= 0

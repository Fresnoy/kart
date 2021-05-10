import pytest


@pytest.mark.django_db
class TestPlace:
    def test_str(self, place):
        place_str = str(place)
        assert place.name in place_str
        assert place.address[0:20] in place_str
        assert str(place.organization) in place_str

    def test_str_with_country(self, place):
        place.organization = None
        place.country = "FR"
        place.save()
        place_str = str(place)
        assert place.address[0:20] in place_str
        assert str(place.country) in place_str
        assert str(place.organization) not in place_str

    def test_str_without_address(self, place):
        # FIXME: conjonction peu probable, non ?
        place.name = place.address[0:20] + "..."
        place.save()
        place_str = str(place)

        assert place.name in place_str
        assert str(place.organization) in place_str


@pytest.mark.django_db
class TestMetaAward:
    def test_str(self, meta_award):
        meta_award_str = str(meta_award)
        assert meta_award.label in meta_award_str
        assert '(main event)' not in meta_award_str
        assert meta_award.event.title in meta_award_str
        assert str(meta_award.task) in meta_award_str

    def test_str_no_event(self, meta_award):
        meta_award.event = None
        meta_award.save()
        meta_award_str = str(meta_award)
        assert str(meta_award.task) in meta_award_str
        assert 'cat.' in meta_award_str

    def test_str_no_task(self, meta_award):
        meta_award.task = None
        meta_award.save()
        meta_award_str = str(meta_award)
        assert meta_award.event.title in meta_award_str
        assert 'cat.' not in meta_award_str


@pytest.mark.django_db
class TestAward:
    def test_str(self, award):
        award_str = str(award)
        assert str(award.date.year) in award_str
        assert str(award.meta_award) in award_str
        for artwork in award.artwork.all():
            assert str(artwork) in award_str


@pytest.mark.django_db
class TestMetaEvent:
    def test_str(self, meta_event):
        assert str(meta_event) == meta_event.event.title


@pytest.mark.django_db
class TestDiffusion:
    def test_str(self, diffusion):
        diffusion_str = str(diffusion)
        assert diffusion.artwork.title in diffusion_str
        assert diffusion.event.title in diffusion_str

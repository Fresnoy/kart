import pytest


@pytest.mark.django_db
class TestPromotion:
    def test_str(self, promotion):
        promotion_str = str(promotion)
        assert promotion.name in promotion_str
        assert str(promotion.starting_year) in promotion_str
        assert str(promotion.ending_year) in promotion_str


@pytest.mark.django_db
class TestStudent:
    def test_str(self, student):
        student_str = str(student)
        assert str(student.user) in student_str
        assert str(student.artist.nickname) in student_str


@pytest.mark.django_db
class TestPhdStudent:
    def test_str(self, phdstudent):
        phdstudent_str = str(phdstudent)
        assert str(phdstudent.student.user) in phdstudent_str


@pytest.mark.django_db
class TestScienceStudent:
    def test_str(self, sciencestudent):
        sciencestudent_str = str(sciencestudent)
        assert str(sciencestudent.student.user) in sciencestudent_str


@pytest.mark.django_db
class TestTeachingArtist:
    def test_str(self, teachingartist):
        teachingartist_str = str(teachingartist)
        assert str(teachingartist.artist) in teachingartist_str


@pytest.mark.django_db
class TestVisitingStudent:
    def test_str(self, visitingstudent):
        visitingstudent_str = str(visitingstudent)
        assert str(visitingstudent.artist.user) in visitingstudent_str


@pytest.mark.django_db
class TestStudentApplicationSetup:
    def test_str(self, student_application_setup):
        student_application_setup_str = str(student_application_setup)
        assert str(student_application_setup.name) in student_application_setup_str
        assert str(student_application_setup.promotion.name) in student_application_setup_str

    def test_default_birthdate(self, student_application_setup):
        student_application_setup.date_of_birth_max = None
        student_application_setup.save()
        assert (
            int(student_application_setup.promotion.starting_year) - student_application_setup.date_of_birth_max.year
        ) == 36


@pytest.mark.django_db
class TestStudentApplication:
    def test_str(self, student_application):
        student_application_str = str(student_application)
        assert str(student_application.artist) in student_application_str
        assert str(student_application.current_year_application_count) in student_application_str

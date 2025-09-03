"""

    Transform valid Canditature to Student in promo

"""

import sys

from django.core.management.base import BaseCommand
from diffusion.management.commands.create_diffusion import input_choices
from school.models import StudentApplication, StudentApplicationSetup, Student

from people.models import Artist
from people.utils.artist_tools import getArtistByNames


class Command(BaseCommand):
    help = 'Transform valid Candidature to Student in promo'

    def handle(self, *args, **options):

        campaign = StudentApplicationSetup.objects.filter(is_current_setup=True).last()
        candidatures = StudentApplication.objects.filter(campaign__is_current_setup=True, administration__selected=True)
        promo = campaign.promotion

        # valid promotion
        str_question = "Les étudiants serons ajoutés à la promo  : {}   ? [y/n]  -  ".format(promo.name)
        valid = input(str_question)

        if valid != "y":
            sys.exit()

        # valid campaign
        str_question = "La campagne de selection est  : {}  ( {} )  ? [y/n]  -  ".format(
            campaign.candidature_date_end.year, campaign.promotion.name
        )
        valid = input(str_question)

        if valid != "y":
            sys.exit()

        # store existing artist
        student_artists = []

        for candidat in candidatures:
            # Skip if artist is already processed
            if candidat.artist in student_artists:
                print("Candidature de {} déjà traitée, passage à la suivante".format(candidat.artist))
                continue
            # Process binomial application
            if candidat.binomial_application:
                artist1 = candidat.artist

                print("{} candidate en Binome avec {}".format(artist1, candidat.binomial_application_with))

                artist2_firstname = candidat.binomial_application_with.split(' ', 1)[0]
                artist2_lastname = candidat.binomial_application_with.split(' ', 1)[1]

                print("Recherche du binome")

                list_artist = getArtistByNames(firstname=artist2_firstname, lastname=artist2_lastname, listing=True)
                artist2_choice = input_choices(list_artist)

                if(artist2_choice):
                    artist2 = artist2_choice["artist"]
                    app = artist2.student_application.filter(campaign=campaign).first()
                    if not app:
                        print("Aucune candidature trouvée pour {}".format(artist2))
                        break
                    else:
                        print("Candidature trouvée pour {} : {}".format(artist2, app))
                else:
                    print("Aucun artiste trouvé pour {}".format(candidat.binomial_application_with))
                    break

                # create a collective artist
                print("Recherche du nom du binome")
                nickname = artist1.nickname if artist1.nickname != "" else artist2.nickname
                nickname = input_choices([artist1.nickname, artist2.nickname, artist1.user, artist2.user])
                if not nickname:
                    nickname = input("Ecrire le nom du binome : ")

                artist, created = Artist.objects.get_or_create(user=None, nickname=nickname)
                if created:
                    artist.collectives.add(artist1)
                    artist.collectives.add(artist2)
                    artist.save()
                else:
                    print("L'artiste {} existe déjà, continuer ?".format(artist))
                    continue_choice = input_choices([False, True])
                    if not continue_choice:
                        break

                student_artists.append(artist1)
                student_artists.append(artist2)
            # Process normal application
            else:
                artist = candidat.artist
            # Create student
            student, created = Student.objects.get_or_create(
                artist=artist, promotion=promo, number=candidat.current_year_application_count
            )

            student_artists.append(artist)

            print("{} {} : {}".format(student, "(binôme)" if candidat.binomial_application else "", created))
        print("FIN")


def input_choices(values):

    if not values:
        return False

    print("Plusieurs valeurs sont possibles, selectionnez-en une :")
    for id, value in enumerate(values):
        print("{} : {}".format(id, value))

    print("n (ou Entré) : pas dans la liste")
    select = input("Votre choix : ")

    try:
        select_int = int(select)
        selected = values[select_int]
        return selected
    except Exception:
        return False



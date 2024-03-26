# -*- encoding: utf-8 -*-
import datetime
from itertools import chain

from django.core.management.base import BaseCommand

from django.db.models import Q

from school.models import (StudentApplication, AdminStudentApplication, Student, ScienceStudent,
                           VisitingStudent, TeachingArtist)
from people.models import Staff
from production.models import Artwork


class Command(BaseCommand):
    help = 'Remove critics informations from old Student Application'

    def add_arguments(self, parser):
        # -- required
        parser.add_argument("--year", type=int, help='Default : last year')

    def handle(self, *args, **options):
        # get the treatment year
        year = options['year'] if options['year'] else datetime.date.today().year - 1
        # get the date when set expired time : we keep 4 years
        expired_candidatures = year - 4
        # expired user : user is too old to candidate (35 years): 35 + 1
        expired_user = year - 36
        # keep user's selected infos (when user postulate more than one time)
        sa_keep_users = AdminStudentApplication.objects.filter(
                        Q(selected=True) |
                        Q(wait_listed=True) |
                        # Organisation staff
                        Q(application__artist__user__is_staff=True) |
                        # in case of bad manipulation we keep current year's application infos
                        Q(application__created_on__year=datetime.date.today().year)
                       ).values_list("application__artist__user")
        # keep staff user (they may postulate)
        staff_keep_users = Staff.objects.all().values_list("user")
        # keep student
        student_keep_users = Student.objects.all().values_list("user")
        # keep scientist
        science_student_keep_users = ScienceStudent.objects.all().values_list("student__artist__user")
        # keep visiting student
        visiting_student_keep_users = VisitingStudent.objects.all().values_list("artist__user")
        # keep teaching artist (why not?)
        teaching_artist_keep_users = TeachingArtist.objects.all().values_list("artist__user")
        # keep user making artworks
        artwork_artist_keep_users = Artwork.objects.all().values_list("authors__user")
        # keep user
        keep_users = list(chain(sa_keep_users,
                                staff_keep_users,
                                student_keep_users,
                                science_student_keep_users,
                                visiting_student_keep_users,
                                teaching_artist_keep_users,
                                artwork_artist_keep_users))

        # take olds application : last year exclude selected
        sa_olds = StudentApplication.objects.filter(
                        # __lte : less than equal year
                        created_on__year__lte=year,
                        administration__selected=False,
                  ).exclude(
                            # exclude selected user (=Artist)
                            artist__user__in=keep_users,
                            )
        # sa expired mean
        #   user is too old to candidate or
        #   we dont keep infos greater than 5 years (grpd)
        sa_expired = StudentApplication.objects.filter(
                        # Q to make OR (|) statement
                        Q(created_on__year__lte=expired_candidatures) |
                        Q(artist__user__profile__birthdate__year__lte=expired_user),
                     ).exclude(
                               # exclude selected user (= Artist)
                               artist__user__in=keep_users,
                               )
        # All sa
        sa_all = StudentApplication.objects.exclude(
                        #
                        Q(identity_card__isnull=True) |
                        Q(experience_justification__isnull=True) |
                        Q(cursus_justifications__isnull=True) |
                        Q(created_on__year__gt=year) |
                        # in case of bad manipulation we keep current year application
                        Q(created_on__year=datetime.date.today().year)
                 )
        # set list of delete info
        list_delete = []
        # Display messages
        print("Traitement des candidatures <= ", year)
        print("**** Total de : ")
        print("**** {} candidatures".format(StudentApplication.objects.all().count()))
        print("**** {} candidature a garder (are Student, Staff, visiting Artist, Teaching, )"
              .format(StudentApplication.objects.all().count() - len(sa_expired)))
        print("**** {} user a garder (are Student, Staff, visiting Artist, Teaching, )".format(len(keep_users)))
        print("**** {} étudiants".format(Student.objects.all().count()))

        print("Liste des informations qui vont être supprimées : ")
        print("/!\\ Supression complète de {} candidatures expirées".format(sa_expired.count()))
        print("/!\\ Supression des informations critiques de {} candidatures".format(sa_all.count()))
        print("/!\\ Nettoyage, si besoin, des informations de {} anciennes candidatures".format(sa_olds.count()))

        # pause to read uplines
        input('[Press any key to continue]')
        # ALL candidatures : delete critical infos
        for sa in sa_all:
            # set short list
            a = []
            # add critical identity infos
            a.extend(self.list_critical_identity_infos(sa))
            # not empty list
            if a:
                list_delete.extend(a)
        # OLDS candidatures : delete no need infos
        for sa in sa_olds:
            # set short list
            a = []
            # add critical infos
            a.extend(self.list_infos(sa))
            # not empty list
            if a:
                list_delete.extend(a)
        # Expired candidat/ure : delete all ()
        for sa in sa_expired:
            list_delete.extend([(sa, "all", sa)])

        #
        for infos in list_delete:
            model, field, value = infos
            print(model, " : ", value)
        #
        confirm = self.ask_user("Voulez-vous supprimer toutes ces informations ? (Y/n)")
        #
        if not confirm:
            print(u"Aucun fichier n'a été supprimé")
            return
        #
        print(u"C'est parti ...")
        #
        for infos in list_delete:
            model, field, value = infos
            self.del_info(model, field, value)
        print("Fin")

    def ask_user(self, str_question):
        check = str(input(str_question)).lower().strip()
        try:
            if check[0] in ('y', 'yes', 'o', 'oui',):
                return True
            elif check[0] in ('n', 'no', 'non',):
                return False
            else:
                print("Entrez une valeur correcte")
                return self.ask_user(str_question)
        except Exception as error:
            print("Entrez une valeur correcte")
            print(error)
            return self.ask_user(str_question)

    def list_critical_identity_infos(self, sa):
        a = []
        sa_fields_files = ["identity_card", "cursus_justifications", "experience_justification", ]
        for field in sa_fields_files:
            value = getattr(sa, field)
            if (value):
                a.append((sa, field, value))
        return a

    def list_infos(self, sa):
        a = []
        sa_fields_files = ["curriculum_vitae", "free_document", "justification_letter",
                           "remote_interview_info", "presentation_video",
                           "considered_project_1", "considered_project_2",
                           "artistic_referencies_project_1", "artistic_referencies_project_2", ]
        for field in sa_fields_files:
            value = getattr(sa, field)
            if (value):
                a.append((sa, field, value))

        user_fields_infos = ["photo", "social_insurance_number", "cursus", "birthdate", "birthplace",
                             "homeland_address", "homeland_zipcode", "homeland_town", "homeland_phone", ]
        for field in user_fields_infos:
            value = getattr(sa.artist.user.profile, field)
            if value:
                a.append((sa.artist.user.profile, field, value))

        artist_fields_infos = ["bio_fr", "twitter_account", "facebook_profile", ]
        for field in artist_fields_infos:
            value = getattr(sa.artist, field)
            if value:
                a.append((sa.artist, field, value))
        # websites problem : 'common.Website.None' doesn't mean that is empty
        if sa.artist.websites.count() > 0:
            a.append((sa.artist, "websites", getattr(sa.artist, "websites")))

        return a

    def del_info(self, model, field, value):
        print(model, " - ", field, " : ", value)
        # print(field, " : ", value.__class__.__name__)
        # print(value.__class__.__name__)
        if value.__class__.__name__ == 'ManyRelatedManager':
            # print("delete arrays")
            # print(value.all())
            value.all().delete()
        elif value.__class__.__name__ in ('FieldFile', 'ImageFieldFile', 'Gallery'):
            # print("delete File")
            if value.__class__.__name__ == 'Gallery':
                # detach Gallery from main Model
                model.__setattr__(field, None)
                model.save()
                # delete all Gallery's media
                value.media.all().delete()
            # remove value (file or gallery instance)
            value.delete()

        elif value.__class__.__name__ in ('str',):
            # print("delete str")
            setattr(model, field, "")
        elif value.__class__.__name__ in ('date'):
            model.__setattr__(field, None)
            model.save()
        elif value.__class__.__name__ in ('StudentApplication'):
            application = value
            artist = application.artist
            user = artist.user
            # delete user if there is no other application
            if artist.student_application.all().count == 1:
                user.delete()
                # artist is deleted : CASCADE deletion
                # artist.delete()
            # delete current application
            application.delete()
            # no save
            return
        else:
            # other model like Date
            delattr(model, field)
            # return model.save()
        model.save()

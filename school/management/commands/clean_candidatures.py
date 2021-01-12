# -*- encoding: utf-8 -*-
import datetime
import pytz
from itertools import chain

from django.core.management.base import BaseCommand

from django.db.models import Q

from school.models import StudentApplication, Student
from people.models import Staff

from school.utils import setLocale


class Command(BaseCommand):
    help = 'Remove critics informations from old Student Application'

    def add_arguments(self, parser):
        # -- optional
        parser.add_argument('--year', type=int, help='Current year or give him a year')

    def handle(self, *args, **options):
        # to avoid warning set local time
        setLocale('fr_FR.utf8')
        # convert utc to PARIS's time
        tz = pytz.timezone("Europe/Paris")

        # get current year or custom year
        current_year = datetime.date.today().year if not options['year'] else options['year']
        # get last year
        last_year = current_year - 1
        print(current_year)
        print(last_year)
        # get the date when set expired time : we keep 4 years
        expired_candidatures = datetime.datetime(current_year - 5, 1, 1).astimezone(tz)
        print(expired_candidatures)
        # expired user : user is too old to candidate (35 years): 35 + 1
        expired_user = datetime.datetime(current_year - 36, 1, 1).astimezone(tz)
        # keep user's selected infos (when user postulate more than one time)
        sa_keep_users = StudentApplication.objects.filter(
                        Q(selected=True) |
                        Q(wait_listed=True) |
                        # Organisation staff
                        Q(artist__user__is_staff=True) |
                        # in case of bad manipulation we keep current year's application infos
                        Q(created_on__year=datetime.date.today().year)
                       ).values_list("artist__user")
        # keep staff user (they may postulate)
        staff_keep_users = Staff.objects.all().values_list("user")
        # keep student
        student_keep_users = Student.objects.all().values_list("user")
        # keep user
        keep_users = list(chain(sa_keep_users, staff_keep_users, student_keep_users))

        # take olds application : last year exclude selected
        sa_olds = StudentApplication.objects.filter(
                        # __lte : less than equal last_year
                        created_on__lte=datetime.datetime(last_year, 1, 1).astimezone(tz),
                        selected=False,
                  ).exclude(
                            # exclude selected user (=Artist)
                            artist__user__in=keep_users,
                            )
        # sa expired mean
        #   user is too old to candidate or
        #   we dont keep infos greater than 5 years (grpd)
        sa_expired = StudentApplication.objects.filter(
                        # Q to make OR (|) statement
                        Q(created_on__lte=expired_candidatures) |
                        Q(artist__user__profile__birthdate__lte=expired_user),
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
                        Q(created_on__year__gt=current_year) |
                        # in case of bad manipulation we keep current year application
                        Q(created_on__year=datetime.date.today().year)
                 )
        # set list of delete info
        list_delete = []

        print(u"**** Sur un total de : ")
        print(u"**** {} candidatures totales".format(StudentApplication.objects.all().count()))
        print(u"**** {} profiles sauvegardés".format(len(keep_users)))
        print(u"**** {} étudiants".format(Student.objects.all().count()))

        print(u"Liste des informations qui vont être supprimées : ".encode('utf-8'))
        print(u"/!\\ Supression complète de {} candidatures".format(sa_expired.count()))
        print(u"/!\\ Nettoyage des informations de {} anciennes candidatures".format(sa_olds.count()))
        print(u"/!\\ Supression des informations critiques de {} candidatures".format(sa_all.count()))

        # pause to read uplines
        input('[Press any key to continue]')
        # ALL candidatures : delete critical infos
        for sa in sa_all:
            # set short list
            a = []
            # add critical identity infos
            a.extend(self.list_critical_identity_infos(sa))
            # not empty list
            if(a):
                list_delete.extend(a)
        # OLDS candidatures : delete no need infos
        for sa in sa_olds:
            # set short list
            a = []
            # add critical infos
            a.extend(self.list_infos(sa))
            # not empty list
            if(a):
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
        # print(model, " - ", field, " : ", value)
        print(field, " : ", value.__class__.__name__)
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
            artist = value.artist
            # delete sa, artist, user
            value.delete()
            artist.user.delete()
            artist.delete()
            # not save
            return
        else:
            # other model like Date
            delattr(model, field)
            # return model.save()
        model.save()

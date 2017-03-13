# -*- encoding: utf-8 -*-
import csv
from optparse import make_option

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from people.models import FresnoyProfile
from school.models import Student, Promotion


class Command(BaseCommand):
    help = 'Import students from a CSV file'

    option_list = BaseCommand.option_list + (
        make_option(
            "-f",
            "--file",
            dest="filename",
            help="specify import file",
            metavar="FILE"
        ),
    )

    def handle(self, *args, **options):
        filepath = options['filename']

        try:
            with open(filepath, 'r') as csvfile:
                csv_file = csv.reader(csvfile, delimiter=';', quotechar='"')
                for row in csv_file:
                    promotion_name = row[0].decode('utf-8').strip().title()
                    lastname = row[1].decode('utf-8').strip().title()
                    firstname = row[2].decode('utf-8').strip().title()
                    # birthdate = row[3].decode('utf-8')
                    username = slugify(u"%s%s" % (firstname[0], "".join(lastname.split())))

                    email = row[8].decode('utf-8').strip()

                    # Make artist
                    # Make promotion
                    # Make student
                    # Make artwork
                    print u" * %s %s (username=%s)" % (firstname, lastname, username)
                    promotion = Promotion.objects.get(name__iexact=promotion_name)

                    user, created = User.objects.get_or_create(username=username, first_name=firstname,
                                                               last_name=lastname, email=email)
                    if created:
                        print "  `-- User %s created" % user
                    else:
                        print "  `-- Found %s" % user
                    profile, created = FresnoyProfile.objects.get_or_create(user=user)

                    student, created = Student.objects.get_or_create(user=user, promotion=promotion)
                    if created:
                        print "  `-- Student %s created" % student

        except Exception, e:
            raise CommandError('Error while parsing "%s" %s ' % (filepath, e))

        self.stdout.write('Successfully imported csv file "%s"' % filepath)

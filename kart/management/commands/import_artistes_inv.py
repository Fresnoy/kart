# -*- encoding: utf-8 -*-
import csv
from optparse import make_option

from django.contrib.auth.models import User

from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from people.models import Artist, FresnoyProfile


class Command(BaseCommand):
    help = 'Import panorama from a CSV file'

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
                csv_file = csv.reader(csvfile, delimiter=';')
                for row in csv_file:
                    last_name = row[0].decode('utf-8').strip().title()
                    first_name = row[1].decode('utf-8').strip().title()
                    username = slugify(u"%s%s" % (first_name[0], "".join(last_name.split())))
                    # start_year = int(row[2].decode('utf-8'))
                    # end_year = int(row[3].decode('utf-8'))

                    print " * {0} {1} (username={2})".format(first_name, last_name, username)

                    user, created = User.objects.get_or_create(username=username,
                                                               first_name=first_name, last_name=last_name)
                    if created:
                        print "  `-- User {0} created".format(user)
                    else:
                        print "  `-- Found {0}".format(user)
                    profile, created = FresnoyProfile.objects.get_or_create(user=user)

                    artist, created = Artist.objects.get_or_create(user=user)
                    if created:
                        print " `-- Artist {0} created".format(artist)

        except Exception, e:
            raise CommandError('Error while parsing "{0}" {1} '.format(filepath, e))

        self.stdout.write('Successfully imported csv file "{0}"'.format(filepath))

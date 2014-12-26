# -*- encoding: utf-8 -*-
import csv
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from people.models import Artist

class Command(BaseCommand):
    help = 'Import panorama from a CSV file'

    option_list = BaseCommand.option_list + (
        make_option(
            "-f",
            "--file",
            dest = "filename",
            help = "specify import file",
            metavar = "FILE"
        ),
    )


    def handle(self, *args, **options):
        filepath = options['filename']

        import codecs

        try:
            with open(filepath, 'r') as csvfile:
                csv_file = csv.reader(csvfile, delimiter=';')
                for row in csv_file:
                    last_name = row[0].decode('utf-8').title() #
                    first_name = row[1].decode('utf-8').title()
                    start_year = int(row[2].decode('utf-8'))
                    end_year = int(row[3].decode('utf-8'))

                    artist, created = Artist.objects.get_or_create(user__first_name=first_name, user__last_name=last_name)

                    if created:
                        print "%s created" % artist

                    print "."

        except Exception, e:
            raise CommandError('Error while parsing "%s" %s ' % (filepath, e))

        self.stdout.write('Successfully imported csv file "%s"' % filepath)

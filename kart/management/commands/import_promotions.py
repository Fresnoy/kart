# -*- encoding: utf-8 -*-
import csv
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from school.models import Promotion


class Command(BaseCommand):
    help = 'Import promotion from a CSV file'

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
                csv_file = csv.reader(csvfile, delimiter=',')
                for row in csv_file:
                    name = row[0].decode('utf-8').title()
                    start_year = row[1].decode('utf-8')
                    end_year = row[2].decode('utf-8').title()

                    promotion, created = Promotion.objects.get_or_create(name=name,
                                                                         starting_year=start_year, ending_year=end_year)
                    if created:
                        print "%s created" % promotion

                    print promotion

        except Exception, e:
            raise CommandError('Error while parsing "%s" %s ' % (filepath, e))

        self.stdout.write('Successfully imported csv file "%s"' % filepath)

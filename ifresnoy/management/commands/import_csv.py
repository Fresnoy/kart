# -*- encoding: utf-8 -*-
import csv
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from django.contrib.auth.models import User
from people.models import FresnoyProfile, Artist
from school.models import Student
from common.models import Website
from production.models import Film, Installation, Performance

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
                csv_file = csv.reader(csvfile, delimiter=';', quotechar='"')
                for row in csv_file:
                    # username = row[0].decode('utf-8').lower() #
                    password = row[1].decode('utf-8')
                    firstname = row[2].decode('utf-8').strip().title() #
                    lastname = row[3].decode('utf-8').strip().title() #
                    username = slugify(u"%s%s" % (firstname[0], "".join(lastname.split())))
                    email = row[4].decode('utf-8') #
                    websites = row[5].decode('utf-8') #
                    photo = row[6].decode('utf-8')
                    bio_fr = row[7].decode('utf-8') #
                    bio_en = row[8].decode('utf-8') #
                    genre = row[9].decode('utf-8') #
                    title = row[10].decode('utf-8').strip().capitalize() #
                    subtitle = row[11].decode('utf-8') #
                    desc_fr = row[12].decode('utf-8') #
                    desc_en = row[13].decode('utf-8') #
                    prod_date = row[14].decode('utf-8') #
                    thanks_fr = row[15].decode('utf-8') #
                    thanks_en = row[16].decode('utf-8') #
                    credit_fr = row[17].decode('utf-8') #
                    credit_en = row[18].decode('utf-8') #
                    copyright_fr = row[19].decode('utf-8') #
                    copyright_en = row[20].decode('utf-8') #
                    tech_desc = row[21].decode('utf-8')
                    pano_num = row[22].decode('utf-8')


                    # Make artist
                    # Make promotion
                    # Make student
                    # Make artwork
                    print u" * %s by %s %s (username=%s)" % (title, firstname, lastname, username)
                    user = User.objects.get(username=username, first_name=firstname, last_name=lastname)
                    print "  `-- found user %s" % user
                    profile = FresnoyProfile.objects.get(user=user)

                    try:
                        artist = Student.objects.get(user=user)
                    except Student.DoesNotExist:
                        try:
                            artist = Artist.objects.get(user=user)
                        except Artist.DoesNotExist:
                            raise


                    artist.bio_fr = bio_fr
                    artist.bio_en = bio_en
                    for url in websites.split(" "):
                        website, created = Website.objects.get_or_create(url=url, language="FR", title_fr="%s %s" % (firstname, lastname), title_en="%s %s" % (firstname, lastname))
                        artist.websites.add(website)
                    artist.save()

                    # Pb: Artiste invité ou étudiant ?
                    # Quelle promotion pour un étudiant ?
                    # Date des panoramas
                    if genre == "installation":
                        ProdClass = Installation
                    elif genre == "film":
                        ProdClass = Film
                    elif genre == "performance":
                        ProdClass = Performance
                    else:
                        raise Exception("Unknown Prod Class")

                    artwork, created = ProdClass.objects.get_or_create(title=title, subtitle=subtitle, production_date=prod_date)
                    artwork.desc_fr = desc_fr
                    artwork.desc_en = desc_en
                    artwork.thanks_fr = thanks_fr
                    artwork.thanks_en = thanks_en
                    artwork.credit_fr = credit_fr
                    artwork.credit_en = credit_en
                    artwork.copyright_fr = copyright_fr
                    artwork.copyright_en = copyright_en
                    artwork.authors.add(artist)
                    if genre == "installation":
                        artwork.technical_description = tech_desc
                    artwork.save()

                    print "."



        except Exception, e:
            raise CommandError('Error while parsing "%s" %s ' % (filepath, e))

        self.stdout.write('Successfully imported csv file "%s"' % filepath)

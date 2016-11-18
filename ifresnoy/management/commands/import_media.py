# -*- encoding: utf-8 -*-
import os
from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from django.core.files import File  # you need this somewhere
from assets.models import Medium
from production.models import Event


class Command(BaseCommand):
    help = 'Import pano media'

    option_list = BaseCommand.option_list + (
        make_option(
            "-d",
            "--dir",
            dest="dirname",
            help="specify import dir",
            metavar="DIR"
        ),
    )

    def handle(self, *args, **options):
        dirpath = options['dirname']

        def feed_artwork(pano_no, artwork):
            firstname = slugify(artwork.authors.all()[0].user.first_name).replace('-', '_')
            lastname = slugify(artwork.authors.all()[0].user.last_name).replace('-', '_')

            path = "%s/panorama%d/%s_%s/image" % (dirpath, pano_no, lastname, firstname)

            print "Feeding %s by %s" % (artwork.title, path)

            if not os.path.isdir(path):
                raise Exception("Dir not found")

            if not artwork.picture:
                main_visu_path_jpg = os.path.join(path, "visuelPrincipal.jpg")
                main_visu_path_png = os.path.join(path, "visuelPrincipal.png")
                if os.path.isfile(main_visu_path_jpg):
                    artwork.picture.save(os.path.basename(main_visu_path_jpg), File(open(main_visu_path_jpg)))
                elif os.path.isfile(main_visu_path_png):
                    artwork.picture.save(os.path.basename(main_visu_path_png), File(open(main_visu_path_png)))
                else:
                    print "/!\ MAIN VISU NOT FOUND"

            # insitu
            for dirpath2, dirname, filenames in os.walk(os.path.join(path, "insitu")):
                if not len(artwork.in_situ_galleries.all()):
                    artwork.in_situ_galleries.create(label=u"%s" % artwork.title, description=u"in situ gallery")
                gall = artwork.in_situ_galleries.all()[0]

                for name in filenames:
                    print "-> [INSIT GAL] Adding %s" % name
                    full_path = os.path.join(dirpath2, name)
                    m = Medium(gallery=gall)
                    m.picture.save(os.path.basename(full_path), File(open(full_path)))
                    m.save()

                gall.save()

            # processus
            for dirpath2, dirname, filenames in os.walk(os.path.join(path, "processus")):
                if not len(artwork.process_galleries.all()):
                    artwork.process_galleries.create(label=u"%s" % artwork.title, description=u"processus gallery")
                gall = artwork.process_galleries.all()[0]

                for name in filenames:
                    print "-> [GAL PROC] Adding %s" % name
                    full_path = os.path.join(dirpath2, name)
                    m = Medium(gallery=gall)
                    m.picture.save(os.path.basename(full_path), File(open(full_path)))
                    m.save()

                gall.save()

            artwork.save()

        for pano_no in xrange(6, 15):
            print "----------- PANORAMA %s" % pano_no
            if pano_no == 10:
                continue

            event = Event.objects.get(title="Panorama %d" % pano_no)
            # film
            for film in event.films.all():
                feed_artwork(pano_no, film)

            # install
            for install in event.installations.all():
                feed_artwork(pano_no, install)

            # perf
            for perf in event.performances.all():
                feed_artwork(pano_no, perf)

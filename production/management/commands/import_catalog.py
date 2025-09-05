import os
import re
import unicodedata
import requests

from django.core.management.base import BaseCommand
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType

from taggit.models import Tag

from common.models import Website
from people.models import User, Artist, Staff
from production.models import (
    Film,
    Installation,
    Performance,
    Event,
    Organization,
    FilmGenre,
    InstallationGenre,
    OrganizationTask,
    ProductionOrganizationTask,
    StaffTask,
    ProductionStaffTask,
)

import markdownify
import csv
import unidecode
import datetime
from langdetect import detect

from people.utils.artist_tools import getArtistByNames
from people.utils.user_tools import getUserByNames
from utils.kart_tools import usernamize


DRY_RUN = False

"""
    USAGE : ./manage.py import_catalog --path_to_csv <path_to_csv_file>
    OU
    ./manage.py import_catalog --dry-run
    -> DRY_RUN NE FONCTIONNE PAS

"""

# Clear terminal
os.system('clear')
stats = {}
REMOTE_BASE_URL = "https://catalogue-panorama.lefresnoy.net"
MEDIA_PATH = "/static/uploads/photos/"
DRY_RUN = False


class Command(BaseCommand):
    help = 'Import catalogue csv file into kart database'

    def add_arguments(self, parser):
        # -- required
        parser.add_argument("--path_to_csv", type=str, help="CSV Path")

    def handle(self, *args, **options):
        # get path to csv file
        path_to_csv = options.get('path_to_csv', None)
        DRY_RUN = options.get('dry_run', False)
        if not path_to_csv:
            print("Please provide a path to the csv file with --path_to_csv <path_to_csv_file>")
            return
        if DRY_RUN:
            print("DRY RUN MODE ON, NO DATA WILL BE SAVED")
        print("Importing catalogue from file: " + path_to_csv)
        init(path_to_csv=path_to_csv)


def populateAPI(data):

    # GET DB ARTIST
    # get name
    artist_name = (
        data['artist_nickname'] if data['artist_nickname'] else data['user_first_name'] + " " + data['user_last_name']
    )
    # search
    artist_search = getArtistByNames(data['user_first_name'], data['user_last_name'], data['artist_nickname'])
    artist_search_list = getArtistByNames(
        data['user_first_name'], data['user_last_name'], data['artist_nickname'], True
    )
    print("\n")
    print(artist_name)

    # doute ?
    if artist_search["dist"] < 0.9:
        ask = input("Est-ce la même personne ? (db) {}  <-> {} (csv)".format(artist_search["artist"], artist_name))
        if "n" in ask:
            print("Artiste non trouvé")
            print("Et dans cette liste ? ")
            select_with_result_list = input_choices(artist_search_list)
            if select_with_result_list:
                artist_search = select_with_result_list["artist"]
                created = False
            else:
                # reverse name/lastname
                artist_search_reverse_list = getArtistByNames(
                    data['user_last_name'], data['user_first_name'], data['artist_nickname'], True
                )
                select_with_result_list_reverse = input_choices(artist_search_reverse_list)
                if select_with_result_list_reverse:
                    artist_search = select_with_result_list_reverse["artist"]
                    created = False
                else:
                    print("ARTIST CREATOR ERROR !!! ")
                    print("il n'existe pas alors que normalement il doit être dans la base")
                    return

    artist = artist_search["artist"]

    print("START WITH ARTIST")
    print("  {} ".format(artist))
    print("*********")

    # BIO
    bio_fr = select_french_text(data["artist_biography"], data["artist_biography_translated"])
    bio_en = select_english_text(data["artist_biography"], data["artist_biography_translated"])

    artwork_type = data["artwork_type"]

    artwork_title = data["artwork_title"]
    artwork_subtitle = data["artwork_subtitle"]
    artwork_text_fr = select_french_text(data["artwork_description"], data["artwork_description_translated"])
    artwork_text_en = select_english_text(data["artwork_description"], data["artwork_description_translated"])

    # film
    artwork_duration = data["artwork_duration"]
    artwork_shooting_format = data["artwork_shooting_format"]
    artwork_aspect_ratio = data["artwork_aspect_ratio"]
    artwork_process = data["artwork_process"]
    shooting_places = data["artwork_shooting_places"]
    artwork_languages_vo = data["artwork_languages_vo"]
    artwork_languages_subtitles = data["artwork_languages_subtitles"]
    # install
    artwork_technical_description = data["artwork_technical_description"]
    # thanks
    artwork_thanks = data["artwork_thanks"]
    # partners
    artwork_partners = data["artwork_partners"]
    partners_description = data["artwork_partners_description"]
    # credits
    artwork_credits = data["artwork_credits"]
    artwork_credits_description = data["artwork_credits_description"]
    if artwork_credits == "" and "\n" in artwork_credits_description and ':' in artwork_credits_description:
        artwork_credits = artwork_credits_description
    # keywords
    keywords = data["artwork_keywords"]
    genres = data["artwork_genres"]
    # images
    images_process = data["artwork_images_process"]
    images_screen = data["artwork_images_screen"]
    # replace urls
    images_process = replaceUrlMedia(images_process)
    images_process = images_process.split("|")

    images_screen = replaceUrlMedia(images_screen)
    images_screen = images_screen.split("|")

    artwork_avatar = images_screen.pop(0) if images_screen else images_process.pop(0) if images_process else ""
    artwork_medias = images_screen + images_process

    artwork_partners_media = replaceUrlMedia(data["artwork_logos"]).split("|") if data["artwork_logos"] else []

    # artist
    artist_db = artist

    print("ARTWORK")
    print("  {} - {}".format(artwork_title, artwork_type))
    print("*********")

    artwork = None
    if artist_db:
        artwork = getOrCreateProduction(artist_db, artwork_title, artwork_type)

    # subtitle
    artwork.subtitle = artwork_subtitle

    # artist bio
    artist_db = updateArtistBio(artist_db, bio_fr, bio_en)

    # nickname
    if artist_name and slugify(artist_name) != slugify(artist_db.user.first_name + " " + artist_db.user.last_name):
        artist_db.nickname = artist_name

    # photo
    if data.get("artist_id_photo"):
        artist_id_photo = data["artist_id_photo"].replace(
            "identity/", f"{REMOTE_BASE_URL + MEDIA_PATH}{data['user_email']}/identity/"
        )
        id_photo_name = artist_id_photo.split('/')[-1]
        id_photo_file = createFileFromUrl(artist_id_photo)
        artist_db.artist_photo.save(id_photo_name[-35:], id_photo_file, save=True)

    # union websites & RS
    websites = data["artist_website"] + "\n" + data["artist_social_networks"]
    for website in websites.split("\n"):
        if website.strip() != "":
            website = website.strip()
            if not DRY_RUN:
                set_website_or_social_network(artist_db, website)

    # ARTIST SAVE
    if not DRY_RUN:
        artist_db.save()

    # duration
    if artwork_duration:
        hours = minutes = seconds = 0
        # 20:00 or 00:20:00
        duration = artwork_duration.split(":")
        hours = int(duration[0])
        minutes = int(duration[1])
        # 00:20:00
        if len(duration) > 2:
            seconds = int(duration[2])
        #
        if hours > 2:
            seconds = minutes
            minutes = hours
            hours = 0
        artwork.duration = datetime.timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds,
        )
        print("Duration : ", artwork_duration, artwork.duration)

    # text
    # artwork.description_fr = markdownify.markdownify(artwork_text_fr)
    artwork.description_fr = artwork_text_fr
    # artwork.description_en = markdownify.markdownify(artwork_text_en)
    artwork.description_en = artwork_text_en

    # keywords
    set_keywords(artwork, "keywords", keywords)

    # genres
    genres_list = genres.split(",")
    for genre in genres_list:
        set_genre(artwork, genre)

    # print(artwork)

    # shooting_places
    if artwork_type.lower() == 'film' and shooting_places:
        places_list = shooting_places.split('\n')
        for str_place in places_list:
            place = getPlace(str_place)
            if place:
                artwork.shooting_place.add(place)

    # shooting format -> keep first()
    if artwork_type.lower() == 'film' and artwork_shooting_format:
        artwork.shooting_format = artwork_shooting_format.split(',')[0]

    # aspect_ratio -> keep first()
    if artwork_type.lower() == 'film' and artwork_shooting_format:
        artwork.aspect_ratio = artwork_aspect_ratio.split(',')[0]

    # languages_vo
    if artwork_type.lower() == 'film' and artwork_languages_vo:
        set_languages(artwork, "languages_vo", artwork_languages_vo)

    # artwork_languages_subtitles
    if artwork_type.lower() == 'film' and artwork_languages_subtitles:
        set_languages(artwork, "languages_subtitles", artwork_languages_subtitles)

    # process
    if artwork_type.lower() == 'film' and artwork_process:
        artwork.process = artwork_process.split(',')[0]

    if artwork_type.lower() == 'installation':
        artwork.technical_description = artwork_technical_description

    # avatar
    if artwork_avatar == "" and artwork_medias:
        artwork_avatar = artwork_medias.pop(0)

    if artwork_avatar and not artwork.picture:
        avatar_name = artwork_avatar.split('/')[-1]
        avatar_file = createFileFromUrl(artwork_avatar)
        artwork.picture.save(avatar_name[-35:], avatar_file, save=True)
    # gallery
    if images_process:
        # create gallery from images_process
        gallery_process, gall_created = createGalleryFromArtwork(artwork, artist_db, "Images du processus")
        artwork.process_galleries.add(gallery_process.id)
        if gall_created:
            for url in images_process:
                createMediaFromUrl(url, gallery_process.id)

    if images_screen:
        # create gallery from images_screen
        gallery_screen, gall_created = createGalleryFromArtwork(artwork, artist_db, "Images de l'écran")
        artwork.in_situ_galleries.add(gallery_screen.id)
        if gall_created:
            for url in images_screen:
                createMediaFromUrl(url, gallery_screen.id)

    # partners
    # set base production
    orga_fresnoy = Organization.objects.filter(name__icontains='le fresnoy').first()
    task_prod = OrganizationTask.objects.get(label__icontains='producteur')

    po, created = ProductionOrganizationTask.objects.get_or_create(
        task=task_prod, organization=orga_fresnoy, production=artwork
    )

    setStats(po, created)

    set_partners(artwork, artwork_partners, artwork_partners_media)

    # collaborators -> credits
    set_credits(artwork, artwork_credits)

    artwork.thanks_fr = markdownify.markdownify(artwork_thanks)
    artwork.credits_fr = markdownify.markdownify(artwork_credits_description)

    if partners_description:
        artwork.credits_fr += "\n\nDescription du partenariat:\n"
        artwork.credits_fr += markdownify.markdownify(partners_description)

    # ARTWORK SAVE
    artwork.save()

    print("END ARTWORK")
    print("  {} - {}".format(artwork, artwork.id))
    print("*********")

    return artwork


def replaceUrlMedia(str):
    return str.replace("app/static/uploads/photos/", REMOTE_BASE_URL + MEDIA_PATH)


def setStats(value_from_model, created):
    class_name = value_from_model.__class__.__name__.lower()
    attibute = class_name + "_created" if created else class_name + "_reused"
    if attibute not in stats:
        stats[attibute] = []
    stats[attibute].append(value_from_model)


def get_or_create(model, attr):

    created = False
    try:
        instance = model.objects.get(**attr)
    except Exception:
        instance = model(**attr)
        created = True
        if not DRY_RUN:
            instance.save()
    return [instance, created]


def select_french_text(str1, str2):
    str1_language = detect(str1)
    if str1_language == 'fr':
        # print("LAngue FR : ", str1[:25])
        return str1
    # print("LAngue FR : ", str2[:25])
    return str2


def select_english_text(str1, str2):
    str1_language = detect(str1)
    if str1_language == 'en':
        # print("LAngue EN : ", str1[:25])
        return str1
    # print("LAngue EN : ", str2[:25])
    return str2


def input_choices(values):

    if not values:
        return False

    print("Plusieurs valeurs sont possibles, selectionnez-en une :")
    for id, value in enumerate(values):
        print("{} : {} {}".format(id, value, highlightChoices(value)))

    print("n : pas dans la liste")
    select = input("Votre choix : ")

    # select = input("Plusieurs valeurs sont possibles, selectionnez-en une :"
    #                + str([str(id) + " : " + str(s) for id, s in enumerate(values)]))
    try:
        select_int = int(select)
        selected = values[select_int]
        return selected
    except Exception:
        return False


def highlightChoices(dict):
    hl_text = ""
    try:
        if 'user' in dict:
            user = dict['user']
            hl_text += "\n   > User : " + str(user.id) + " - " + str(user)
            if user.staff_set.all().count() > 0:
                hl_text += highlightStaff(user.staff_set.first())
            if user.artist_set.all().count() > 0:
                hl_text += highlightArtist(user.artist_set.first())
        if 'artist' in dict:
            artist = dict['artist']
            hl_text += highlightArtist(artist)
            if artist.user.staff_set.all().count() > 0:
                hl_text += highlightStaff(artist.user.staff_set.first())
    except Exception:
        # print("Error in highlightChoices: ", e)
        hl_text += "\n   > " + str(dict)
    return hl_text


def highlightArtist(artist):
    hl_text = "\n   > "
    hl_text += "Artist : " + str(artist.id) + " - " + str(artist)
    if artist.artworks.all().count() > 0:
        hl_text += "\n   > "
        hl_text += "Artworks : " + ", ".join(artist.artworks.all().values_list("title", flat=True))
    return hl_text


def highlightStaff(staff):
    hl_text = ""
    if staff.productionstafftask_set.all().count() > 0:
        hl_text += "\n   > "
        hl_text += "Tasks : " + ", ".join(staff.productionstafftask_set.all().values_list("task__label", flat=True))
    return hl_text


def set_partners(artwork, partners_str, partners_media):
    if partners_str.strip() == "":
        return
    # FORME - type : structure \n
    partners_arr = partners_str.split("\n")
    for partner in partners_arr:
        # la forme Coproduction : Julien Taïb, Crossed Lab
        partner = partner.strip()
        if partner == "":
            continue
        if ":" not in partner:
            # set default partenaire type
            partner = "Partenaire : " + partner

        # TYPE
        partner_type_str = partner.split(":")[0].strip()
        partner_types = getOrCreateMultiInstancesByStr(OrganizationTask, 'label', partner_type_str)

        # ORGANIZATION
        organization_str = partner.split(":")[1].strip()
        organizations = getOrCreateMultiInstancesByStr(Organization, "name", organization_str)

        # ADD logo to ORGA
        for organization in organizations:
            name = organization.name
            if not organization.picture and partners_media:
                print("Organisation : " + name + " est sans logo, est-ce qu'il est dans ce choix ? ")
                media_choice = input_choices(partners_media)
                if media_choice:
                    name = media_choice.split('/')[-1]
                    file = createFileFromUrl(media_choice)
                    organization.picture.save(name[-35:], file, save=True)

        # HAVE TO
        # ONE type ONE organization
        # One type Multi organizations
        # Multi types -> problems One task
        # Multi type multi organizations -> problem
        if len(partner_types) == 0 or len(organizations) == 0 or (len(partner_types) > 1 and len(organizations) > 1):
            print("*****PROBLEME DE PARTNERS  ******")
            print(partner)
            continue
        # partner : organization
        elif len(partner_types) == 1 and len(organizations) == 1:
            partner_type = partner_types[0]
            organization = organizations[0]
            pot, created = ProductionOrganizationTask.objects.get_or_create(
                task=partner_type, organization=organization, production=artwork
            )
            setStats(pot, created)
            print(pot)
        # partner : organization 1, organization 2
        elif len(partner_types) == 1 and len(organizations) > 1:
            partner_type = partner_types[0]
            for organization in organizations:
                pot, created = ProductionOrganizationTask.objects.get_or_create(
                    task=partner_type, organization=organization, production=artwork
                )
                setStats(pot, created)
                print(pot)
        # partner, coproduction  : organization
        elif len(partner_types) > 1 and len(organizations) == 1:
            organization = organizations[0]
            for partner_type in partner_types:
                pot, created = ProductionOrganizationTask.objects.get_or_create(
                    task=partner_type, organization=organization, production=artwork
                )
                setStats(pot, created)
                print(pot)


def getOrCreateMultiInstancesByStr(model, attr, txt_str):
    instances = []
    txt_str = txt_str.strip()
    char_split = [
        ",",
        "/",
        ";",
        " & ",
    ]
    if " et " in txt_str:
        print(f"'ET' est présent dans '{ txt_str }', s'agit il de PLUSIEURS { model.__name__ } ?")
        if input_choices([False, True]):
            char_split.append(' et ')

    if any(sep in txt_str for sep in char_split):
        # split by comma or "et" or " / "
        for sep in char_split:
            txt_str = txt_str.replace(sep, ",")
        str_split = txt_str.split(",")
        for s in str_split:
            instance = getOrCreateModelInstanceByStr(model, attr, s)
            instances.append(instance)
    else:
        instance = getOrCreateModelInstanceByStr(model, attr, txt_str)
        instances.append(instance)

    return instances


def getOrCreateModelInstanceByStr(model, attr, txt_str):

    instance = False

    txt_str = txt_str.strip()

    query = model.objects.filter(**{attr + "__iexact": txt_str})

    if query.count() == 0:
        query = model.objects.filter(**{attr + "__icontains": txt_str})

    if query.count() == 0:
        query = model.objects.filter(**{attr + "__unaccent__icontains": txt_str})

    if query.count() > 1:
        print(str(model) + " (csv) : " + txt_str)
        instance = input_choices(query)

    elif query.count() == 1:
        instance = query.first()

    if not instance:
        instance, created = model.objects.get_or_create(**{attr: txt_str.title()})
        setStats(instance, created)
        print("Création d'une instance" + str(model.__name__) + " : " + str(instance))

    return instance


def set_languages(instance, field, str):
    if not hasattr(instance, field):
        print("Erreur Language", instance, field, str)
        return

    list = []
    str_list = str.split(',')
    for s in str_list:
        s = s.lower().strip()
        # sometimes some detail add with lang (es_419, fr,ar_001,aeb) in str we don't need this specifications
        s = re.split(r'[^a-z]+', s)[0]
        list.append(s)
    list_str = ", ".join(list)
    setattr(instance, field, list_str)
    print("Set Languages", field, str)


def set_keywords(instance, field, str):
    if not hasattr(instance, field):
        print("Erreur KEYWORDS", instance, field, str)
        return

    list = []
    str_list = str.split(',')
    #
    contentype_id = ContentType.objects.get_for_model(instance).id
    for s in str_list:
        # sanitize
        s = s.lower().strip()
        if not s:
            continue
        # search for an existig Tag
        q = Tag.objects.filter(name__unaccent__icontains=s, taggit_taggeditem_items__content_type=contentype_id)
        if not q:
            q = Tag.objects.filter(name__unaccent__icontains=s)
        # get the most used tag
        tag_db = q.annotate(tag_count=Count('taggit_taggeditem_items')).order_by('-tag_count')
        tag_db_first = tag_db.first()
        if tag_db_first:
            # WHY sometimes hassattr ou directly an str ??
            tag_str = tag_db_first.name if hasattr(tag_db_first, 'name') else tag_db_first
            if len(tag_str) == len(s):
                s = tag_str
            else:
                tag_stats_values = (
                    q.annotate(tag_count=Count('taggit_taggeditem_items'))
                    .order_by('-tag_count')
                    .values_list(
                        "name",
                        "tag_count",
                    )
                )
                print(f"keywords '{s}' ambigus")
                print(tag_stats_values)
                s = input_choices([s, tag_str])

        list.append(s)

    print("Keywords :", str, list)
    instance.keywords.set(list)


def set_genre(aw, genre_str):
    genre_str = genre_str.strip()

    if genre_str == "":
        return

    modelGenre = None
    match aw.polymorphic_ctype.model:
        case 'film':
            modelGenre = FilmGenre
        case 'installation':
            modelGenre = InstallationGenre
        case 'performance':
            # no genre in performance
            return
        case _:
            # default
            return
    # query genre
    genre_query = modelGenre.objects.filter(label__iexact=genre_str)
    if genre_query.count() == 0:
        genre_query = modelGenre.objects.filter(label__unaccent__icontains=genre_str)

    genre = False
    if genre_query and genre_query.count() == 1:
        genre = genre_query.first()

    elif genre_query and genre_query.count() > 1:
        print("Genre csv : " + genre_str)
        genre = input_choices(genre_query)

    if not genre:
        print("********** GENRE PROBLEME *********** ")
        print(genre)
    else:
        aw.genres.add(genre)


def set_credits(aw, credits):

    # many ways detected in csv
    # staf : task \n
    # staf : name or fistname, lastname

    if "\n" not in credits:
        return False

    credits_arr = credits.split("\n")

    for credit in credits_arr:

        if ":" not in credit:
            print("/!\\ credit n'a pas de ':'" + credit)
            continue

        print("********** CREDIT *********** ")
        isReverseStaffTask = is_staff_task_reverse(credit)
        print(credit, "isReverseStaffTask: ", isReverseStaffTask)
        # if is reverse, we have to switch staf and task
        staffIndex = 0 if not isReverseStaffTask else 1
        taskIndex = 1 if not isReverseStaffTask else 0

        # SEARCH FOR USER
        user_str = credit.split(":")[staffIndex].strip()
        print("SEARCH FOR USER : " + user_str)
        users = []
        user = False
        # "," in name mean that this is an human in DB (comme with catalog plateform dev)
        # but mean sometimes two person for the same task Nina Guseva, Anna Collard : céramiste
        # OR Nina Guseva et Anna Collard (or Nina Guseva / Anna Collard)
        # on demande si "&"" : "Good Loc & Co"
        char_split = [",", "/", ";", " et "]
        #
        if " & " in user_str:
            print(f"'&' est présent dans { user_str }, s'agit il de plusieurs personnes ?")
            if input_choices([False, True]):
                char_split.append('&')

        if any(sep in user_str for sep in char_split):
            for sep in char_split:
                user_str = user_str.replace(sep, ",")
            str_split = user_str.split(",")
            first_user = str_split[0].strip()
            # is multi ? il y a un espace (nom prénom) et c'est assez long OU plus de une virgule
            if (" " in first_user and len(first_user) > 3) or len(str_split) > 2:
                # multi user
                for u in str_split:
                    user, created = get_or_create_user(u)
                    users.append(user)
        # "," est gérée dans get_or_create_user
        if not user:
            user, created = get_or_create_user(user_str)
            users.append(user)

        # Is staff
        staffs = []
        for user in users:
            if user.staff_set.count() > 0:
                staff = user.staff_set.first()
            else:
                staff, created = Staff.objects.get_or_create(user=user)
                setStats(staff, created)
            staffs.append(staff)

        # search for task
        task_str = credit.split(":")[taskIndex].strip()
        # sometimes Benjamin Griere : Graphisme 3D, Développeur 3D
        tasks = getOrCreateMultiInstancesByStr(StaffTask, 'label', task_str)

        # HAVE TO
        # ONE user ONE task
        # One user Multi tasks
        # Multi users One task
        # Multi user multi task -> problem
        if len(staffs) == 0 or len(tasks) == 0 or (len(staffs) > 1 and len(tasks) > 1):
            print("*****PROBLEME DE CREDIT ******")
            print(credit)
            continue
        elif len(staffs) == 1 and len(tasks) == 1:
            staff = staffs[0]
            task = tasks[0]
            pst, created = ProductionStaffTask.objects.get_or_create(staff=staff, task=task, production=aw)
            setStats(pst, created)
            print(pst)

        elif len(staffs) > 1 and len(tasks) == 1:
            task = tasks[0]
            for staff in staffs:
                pst, created = ProductionStaffTask.objects.get_or_create(staff=staff, task=task, production=aw)
                setStats(pst, created)
                print(pst)

        elif len(staffs) == 1 and len(tasks) > 1:
            staff = staffs[0]
            for task in tasks:
                pst, created = ProductionStaffTask.objects.get_or_create(staff=staff, task=task, production=aw)
                setStats(pst, created)
                print(pst)

    # END OF FOR CREDITS


def is_staff_task_reverse(credit):
    """
    Check if the credit is in reverse order (task : staff) normaly (staff : task)
    :param credit: str
    :return: bool
    """

    isReverseStaffTask = False
    # normalement staff : task
    credit_staff = credit.split(":", 1)[0].strip()
    credit_task = credit.split(":", 1)[1].strip() if ":" in credit else ""
    # à priori les il y a des majuscules aux noms mais pas aux taches
    if credit_task and credit_staff:
        # compte le nombre de majuscules
        staff_upper = sum(1 for c in credit_staff if c.isupper())
        task_upper = sum(1 for c in credit_task if c.isupper())
        # si l'un ou l'autre a des lettres en majuscules successif c'est surement un task
        if (
            re.search(r'[A-Z]{2,}', credit_staff)
            or re.search(r'[A-Z]{2,}', credit_task)
            # si c'est un chiffre ex +216
            or re.search(r'[1-9]{2,}', credit_staff)
            # egalite : même nombre de majuscule
            or task_upper == staff_upper
            # rare : Estelle, Benazet : Chargée De Production
            or (task_upper > staff_upper and "," in credit_staff)
        ):
            print("Le credit n'est pas clair : " + credit)
            print("Est ce que {} est une tache ?".format(credit_staff))
            isReverseStaffTask = input_choices([False, True])
            return isReverseStaffTask
        if task_upper > staff_upper:
            isReverseStaffTask = True
        else:
            isReverseStaffTask = False

    return isReverseStaffTask


# SET WEBSITE / SOCIAL NETWORK
def set_website_or_social_network(artist, url):
    """
    Set website and social network for a user
    :param user: Artist instance
    :param urls: str separate by \n
    :return: None
    """
    if not artist:
        print("No artist provided to set website and social network.")
        return

    if not url:
        print("No URLs provided to set website and social network.")
        return

    rs_list = ["facebook", "instagram", "twitter", "linkedin", "vimeo", "youtube", "tiktok", "mastodon"]

    website_type = "Site Web"
    website_url = url.strip()
    # set website
    # ex: Instagram : @camillesauerartk / Site web : aleksandrezharaya.net /
    if ": " in url or " :" in url:
        # split by :
        website_type, website_url = url.split(":", 1)
        website_type = website_type.strip().lower()
        website_url = website_url.strip()

        if website_type in rs_list:
            # not an URL
            if "/" not in website_url:
                website_url = "https://www.{}.com/{}".format(website_type, website_url.replace("@", ""))

    if "@" in website_url and "http" not in website_url:
        website_type = "instagram"
        website_url = "https://www.instagram.com/{}".format(website_url.replace("@", ""))

    if "http" not in website_url:
        website_url = "https://{}".format(website_url)

    if any(rs in url for rs in rs_list):
        # get the good one
        for rs in rs_list:
            if rs in url:
                website_type = rs
                break

    # find in DB
    artist_website_db = artist.websites.filter(url__icontains=website_url)
    if artist_website_db.exists():
        print(f"Le siteweb existe {website_type}", artist_website_db)
        return

    # test url is valid return code 2XX
    test_url_error = False
    print(f"URL test {website_type} : {website_url} ({url})")
    try:
        response = requests.get(website_url, timeout=50)
        if response.status_code >= 400:
            print(f"Invalid URL: {website_url} (status code: {response.status_code})")
            test_url_error = True

    except requests.RequestException as e:
        print(f"Error accessing URL: {website_url} - {e}")
        test_url_error = True

    if test_url_error:
        print("Le site web n'a pas l'air de répondre, sauvegarde quand-même ?")
        if not input_choices([False, True]):
            return

    # instagram -> Instagram
    website_type = website_type.title()
    # create new website
    print("Site web inexistant dans la base, création")
    website, created = Website.objects.get_or_create(
        title_fr=f" {website_type} de {artist} ",
        title_en=f" {artist}' {website_type}",
        language="FR",
        url=website_url,
    )
    artist.websites.add(website)

    artist.save()


# END WEBSITE / SOCIAL NETWORK


def get_or_create_user(user_str):
    # search user from usersearchutils
    # return user

    first_name, last_name = get_first_last_name_from_str(user_str)
    print("firsname:" + first_name)
    print("lastname:" + last_name)

    user = False
    user_search = False
    created = False
    search_list_artist = False
    # are we lucky ?
    # , mean that this is an human in DB
    if "," in user_str:
        user_search = getUserByNames(user_str.split(",")[0], user_str.split(",")[1])
        search_list = getUserByNames(first_name, last_name, True)

    # search by artist : ça arrive (SMITH?!)
    if not user_search:
        user_search = getArtistByNames("", "", user_str)
        search_list_artist = getArtistByNames("", "", user_str, True)
        if user_search and user_search["dist"] >= 0.9:
            artist = user_search["artist"]
            # ça peut etre un DUO ?
            if not artist.user and artist.collectives.all().count() > 1:
                print("c'est un duo d'artistes, on crée un userStaff pour le collectif")
                user = False
                created = False
                user_search = False
            else:
                user = artist.user
                created = False
        else:
            user_search = False
            user = False

    # try user_search if we are not in previous cases
    if not user and not user_search:
        user_search = getUserByNames(first_name, last_name)
        search_list = getUserByNames(first_name, last_name, True)

    # search in DB
    if not user and user_search:
        if user_search["dist"] <= 1:
            print("Recherche d'un User : " + user_str)
            # concat arrays if exist
            list = search_list + search_list_artist if search_list_artist else search_list
            select_with_result_list = input_choices(list)
            if select_with_result_list:
                if "user" in select_with_result_list:
                    user = select_with_result_list["user"]

                if "artist" in select_with_result_list:
                    artist = select_with_result_list['artist']
                    user = artist.user
                created = False
        else:
            user = user_search["user"]
            created = False
            print("KNOW User : " + str(user) + "(kart)  pour " + user_str + " (csv)")
            # print(user_search)

    if not user:
        username = usernamize(first_name, last_name, False)
        try:
            user, created = User.objects.get_or_create(
                first_name=first_name.title(), last_name=last_name.title(), username=username
            )
        except Exception:
            username = usernamize(first_name, last_name, True)
            user, created = User.objects.get_or_create(
                first_name=first_name.title(), last_name=last_name.title(), username=username
            )
        setStats(user, created)
        print("CREATE User : " + str(user))

    return [user, created]


def get_or_create_stafftask(task_str):
    print("SEARCH FOR TASK : " + task_str)
    # delete spaces
    task_str = task_str.strip()
    # search by query exact and second time filter
    task_query = StaffTask.objects.filter(label__iexact=task_str)
    if task_query.count() == 0:
        task_query = StaffTask.objects.filter(label__unaccent__icontains=task_str)
    # init task
    task = False
    # find more than one ? choose !
    if task_query.count() > 1:
        print("Plusieurs tâches ont été trouvées pour : " + task_str)
        task = input_choices(task_query)

    elif task_query.count() == 1:
        task = task_query.first()
    if not task:
        task, created = StaffTask.objects.get_or_create(label=task_str.title())
        setStats(task, created)
        print("Création TASK : " + str(task))

    print(task)

    return task


#
def get_first_last_name_from_str(str):
    str = str.strip()
    sep_list = [",", " "]
    for sep in sep_list:
        if sep in str:
            str_split = str.split(sep, 1)
            first_name = str_split[0]
            last_name = str_split[1]

            return [first_name, last_name]

    return ["", str]


#
def getPlace(str_place):
    from geopy.geocoders import Nominatim
    from geopy import distance

    from diffusion.models import Place

    # recharche dans les places existant
    print("Place cherche : ", str_place, ".")
    # clear str
    if str_place.strip() == "":
        return None
    # error
    char_split = [",", "/", ";", " & ", " et ", " - ", "(", ")"]
    if any(sep in str_place for sep in char_split):
        # split by comma or "et" or " / "
        for sep in char_split:
            str_place = str_place.replace(sep, ",")

    if "," not in str_place:
        city = country = str(str_place)
    else:
        city, country = str_place.split(',', 1)
    # search place in bdd
    place_search_db = (
        Place.objects.filter(city__unaccent__icontains=city)
        .union(Place.objects.filter(name__unaccent__icontains=city))
        .union(Place.objects.filter(name__unaccent__icontains=str_place))
        .union(Place.objects.filter(name__unaccent__icontains=country))
    )
    place = input_choices(place_search_db)
    if place:
        # print( "Trouve dans la base : ", place)
        return place
    else:
        # recherche dans les internets
        geolocator = Nominatim(user_agent="panorama_creation_place")
        location = geolocator.geocode(str_place, language="fr", addressdetails=True, timeout=None)

        if not location:
            # print( "!!!!!!!! Nouvel essaie : ", str_place)
            from functools import partial

            geo = partial(geolocator.geocode, language="fr", addressdetails=True, timeout=None)
            location = geo(str_place)

        if not location:
            # print( "!!!!!_____ Nouvel essaie : ", str_place)
            from functools import partial

            geo = partial(geolocator.geocode, language="fr", addressdetails=True, timeout=None)
            location = geo(country)

        if not location:
            # print( "!!!!!_____ Nouvel essaie : ", str_place)
            from functools import partial

            geo = partial(geolocator.geocode, language="fr", addressdetails=True, timeout=None)
            location = geo(city)

        if not location:
            # print( "!!!!!_____ Nouvel essaie : ", str_place)
            from functools import partial

            geo = partial(geolocator.geocode, language="fr", addressdetails=True, timeout=None)
            location = geo(str_place + ", " + country)

        if location:
            # print( "Trouve dans les internets : ", location)
            # -> si trouve, recherche si pas loin d'une place existante
            places = Place.objects.all()
            for p in places:
                point1 = (p.latitude, p.longitude)
                point2 = (location.latitude, location.longitude)
                if distance.distance(point1, point2).km < 0.1:
                    print("_______ UNE place dans la base a été trouvée : ", p)
                    return p
            print("Pas de place dans la base à proximité, création")

            country_code = location.raw['address']['country_code'] if location.raw else ""
            # city
            location_city = city
            for key in ["town", "city", "village", "province"]:
                if key in location.raw['address']:
                    location_city = location.raw['address'][key]
                    break

            place = Place(
                name=city,
                description=city,
                address=location.address[:255],
                latitude=location.latitude,
                longitude=location.longitude,
                city=location_city[:50],
                country=country_code,
            )
            if not DRY_RUN:
                place.save()
            return place
    print("/!\\/!\\/!\\/!\\ Rien trouvé ! :", str_place, "\n")
    return None


def createFileFromUrl(url):
    from django.core.files import File
    from django.core.files.temp import NamedTemporaryFile
    import urllib

    if url == "":
        return None

    # url = url.replace("app/static/", "https://catalogue-panorama.lefresnoy.net/static/")

    # get size of the file in MB
    import urllib.request

    try:
        response = urllib.request.urlopen(url)
        file_size = response.length or 0
        file_size = str(round(file_size / (1024 * 1024), 2)) + "MB"
    except Exception as e:
        print("Error getting file size: ", e)
        file_size = 0

    print(f"téléchargement du media ({file_size}) : {url}")

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(open(urllib.request.urlretrieve(url)[0], 'rb').read())
    img_temp.flush()

    return File(img_temp)


def createMediaFromUrl(url, gallery_id):
    from assets.models import Medium

    if url == "":
        return None

    file = createFileFromUrl(url)
    name = url.split('/')[-1]

    medium = Medium()
    medium.gallery_id = gallery_id
    medium.picture.save(name[-35:], file, save=True)

    medium.save()

    return medium


def createGalleryFromArtwork(artwork, authors, gallery_type):
    from assets.models import Gallery

    label = "{0} - {1}".format(gallery_type, artwork.title)
    gallery, created = get_or_create(Gallery, {'label': label})

    gallery.description = "{0} \n {1}".format(authors, artwork.title)
    gallery.description += "{0} {1}".format(artwork.polymorphic_ctype.name, artwork.production_date.year)
    gallery.description += "\nProduction Le Fresnoy – Studio national des arts contemporains"
    gallery.description += "\n© {}".format(authors)

    gallery.save()
    return [gallery, created]


def updateArtistBio(artist, bio_fr, bio_en):

    bio_fr = markdownify.markdownify(bio_fr)
    bio_en = markdownify.markdownify(bio_en)

    # print(bio_fr)
    # verify empty bio
    if artist.bio_fr == "":
        # print(artist.__str__() + " : update bio")
        artist.bio_fr = bio_fr
    else:
        # keep infos
        # print(artist.__str__() + " : has an old bio")
        if "<!--" not in artist.bio_fr and bio_fr not in artist.bio_fr:
            # print(artist.__str__() + " : update his old bio")
            artist.bio_fr = "<!--" + artist.bio_fr + "-->\n" + bio_fr

    if artist.bio_en == "":
        artist.bio_en = bio_en
    else:
        if "<!--" not in artist.bio_en and bio_fr not in artist.bio_en:
            artist.bio_en = "<!--" + artist.bio_en + "-->\n" + bio_en

    return artist


def getStudent(name, firstname, email):
    return getArtist(name, firstname, email, True)


def createArtist(name, firstname, email):
    username = unidecode.unidecode(firstname[0] + name)
    user, user_created = User.objects.get_or_create(
        username=username, email=email, first_name=firstname, last_name=name
    )
    artist, artist_created = Artist.objects.get_or_create(user=user)

    return artist


def getArtist(idartist):
    searchresult = None
    try:
        return Artist.objects.get(id=idartist)
    except (Artist.MultipleObjectsReturned, Artist.DoesNotExist):
        searchresult = None
    return searchresult


def getOrCreateProduction(artist, title, type):

    production = None
    created = False
    production_year = datetime.datetime.now().year

    if type.lower() == "film":
        production, created = get_or_create(
            Film, {'title': title, 'production_date': datetime.date(production_year, 1, 1)}
        )

    if type.lower() == "installation":
        production, created = get_or_create(
            Installation, {'title': title, 'production_date': datetime.date(production_year, 1, 1)}
        )
    if type.lower() == "performance":
        production, created = get_or_create(
            Performance, {'title': title, 'production_date': datetime.date(production_year, 1, 1)}
        )

    if created:
        production.authors.add(artist)

    setStats(production, created)

    return production


def cleanHTML(text):
    markdownify.markdownify(text)


def slugify(text):
    """
    Crée un "slug" à partir d'une chaîne de caractères donnée.

    Un slug est une version conviviale pour les URL, généralement en minuscules,
    avec des espaces remplacés par des tirets et les caractères spéciaux supprimés.

    Args:
        text (str): La chaîne de caractères à "slugifier".

    Returns:
        str: Le slug généré.
    """
    text = str(text)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    text = re.sub(r'[-\s]+', '-', text)
    return text


# Mapping entre les colonnes CSV et les champs du modèle
FIELD_MAPPING = {
    'email': 'user_email',
    'first_name': 'user_first_name',
    'last_name': 'user_last_name',
    'artist_type': 'artist_type',
    'artist_name': 'artist_nickname',
    'id_photo': 'artist_id_photo',
    'artist_email': 'artist_email',
    'website': 'artist_website',
    'social_networks': 'artist_social_networks',
    'biography': 'artist_biography',
    'biography_translated': 'artist_biography_translated',
    'type': 'artwork_type',
    'title': 'artwork_title',
    'subtitle': 'artwork_subtitle',
    'description': 'artwork_description',
    'description_translated': 'artwork_description_translated',
    'duration': 'artwork_duration',
    'shooting_format': 'artwork_shooting_format',
    'aspect_ratio': 'artwork_aspect_ratio',
    'process': 'artwork_process',
    'genres': 'artwork_genres',
    'languages_vo': 'artwork_languages_vo',
    'languages_subtitles': 'artwork_languages_subtitles',
    'technical_description': 'artwork_technical_description',
    'thanks': 'artwork_thanks',
    'partners': 'artwork_partners',
    'partners_description': 'artwork_partners_description',
    'credits': 'artwork_credits',
    'credits_description': 'artwork_credits_description',
    'keywords': 'artwork_keywords',
    'shooting_places': 'artwork_shooting_places',
    'images_process': 'artwork_images_process',
    'images_screen': 'artwork_images_screen',
    'logos': 'artwork_logos',
}


def map_csv_to_model(row):
    """Map les données d'une ligne CSV aux champs du modèle."""

    mapped_data = {}
    for csv_column, model_field in FIELD_MAPPING.items():
        mapped_data[model_field] = row.get(csv_column).strip()
    return mapped_data


def init(path_to_csv, *args):
    # settup args
    if 'DRY_RUN' in args:
        DRY_RUN = True
        print("DRY_RUN Script")
        c = input("LE DRYRUN NE FONCTIONNE PAS ! Voulez-vous continuer ? Y/n")
        if c == "n":
            return
    # get the file
    fichier_csv = path_to_csv
    if not os.path.exists(fichier_csv):
        print("Le fichier CSV n'existe pas : " + fichier_csv)
        return

    os.system('clear')
    input("Vérifiez que vous avez la dernière version du catalalogue à mettre dans : " + fichier_csv)

    # create Panorama event
    current_year = datetime.datetime.now().year
    event, created = Event.objects.get_or_create(
        title="Panorama " + str(current_year + 2 - 2000),
        # starting_date=datetime.datetime(current_year, 1, 1, tzinfo=pytz.timezone("Europe/Paris")),
    )

    with open(fichier_csv, 'r') as csvfile:
        lecteur_csv = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        # TEST : avance dans le tableau
        # for i in range(4):
        #     row = next(lecteur_csv)

        for row in lecteur_csv:
            data = map_csv_to_model(row)
            artwork = populateAPI(data)
            # set event to panorama
            match artwork.polymorphic_ctype.model:
                case 'film':
                    event_artworks = event.films
                case 'installation':
                    event_artworks = event.installations
                case 'performance':
                    event_artworks = event.performances
            event_artworks.add(artwork)

    for elt in stats:
        print(elt + " : " + str(len(stats[elt])))

    event.save()

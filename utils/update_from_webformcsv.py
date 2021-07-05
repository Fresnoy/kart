#! /usr/bin/env python
# -*- coding=utf8 -*-

"""
update_from_webformcsv

Update Kart with data extracted from a webform produced csv file.

Data source : https://www.lefresnoy.net/fr/node/6059/webform


Admitted rules
--------------
If a user can not be found in Kart from csv data, no further research for potential match with artist or student data in csv is made

"""


import os
import sys
import re
import time

from difflib import SequenceMatcher
import pathlib
import logging
import pandas as pd
import pytz
from datetime import datetime
import json

from django.db.utils import IntegrityError
from django_countries import countries
from django.db.models.functions import Concat, Lower
from django.db.models import CharField, Value
from django.contrib.postgres.search import TrigramSimilarity
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


import unidecode

# Shell Plus Django Imports (uncomment to use script in standalone mode, recomment before flake8)
import django
from django.conf import settings
# settings.configure(DEBUG=True)
# Add root to python path for standalone running
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kart.settings")
django.setup()
################## end shell plus

from production.models import Artwork, Event, Film, Installation
from people.models import Artist
from diffusion.models import Award, MetaAward, Place
from school.models import Student, Promotion
from django.contrib.auth.models import User
# Full width print of dataframe
pd.set_option('display.expand_frame_repr', False)


# TODO: Harmonise created and read files (merge.csv, ...)
DRY_RUN = False  # No save() if True
DEBUG = True

# Set file location as current working directory
OLD_CWD = os.getcwd()
os.chdir(pathlib.Path(__file__).parent.absolute())


# Allow to lower data in query with '__lower'
CharField.register_lookup(Lower)

# Logging
logger = logging.getLogger('import_pano_data')
logger.setLevel(logging.DEBUG)
# clear the logs
open('import_csv.log', 'w').close()
# create file handler which logs even debug messages
fh = logging.FileHandler('import_csv.log')


fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter1 = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter1)
formatter2 = logging.Formatter('%(message)s')
ch.setFormatter(formatter2)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
#####

# Timezone
tz = pytz.timezone('Europe/Paris')

# Clear terminal
os.system('clear')

##################################################
# Mappings btw webforms fields and Kart's fields #
##################################################
wf2kart_mapping = {
    'user' : {
        'e_mail':'email',
        'nom_prenom':'XXXXX',
        'lastname':'last_name',
        'firstname':'first_name',
        'views_add':''
    },

    'artist' : {
        'nom_dartiste':'nickname',
        'biographie':'bio_fr',
        'biogaphie_en':'bio_en'
    },

    'student' : {
        'promotion':'promotion',
    },

    'artwork' : {
        'type':'type',
        'titre':'title',
        'sous_titre':'subtitle',
        'duree':'duration',
        'dream_theme':'',
        'description___texte_catalogue':'description_fr',
        'description___texte_catalogue_en':'description_en',
        'remerciements':'thanks_fr',
        'Nom':'',
        'Taille du fichier (KB)':'',
        'description_des_partenaires':'partners_txt',  # Partenaires à la mano ?
        'Nom':'',
        'Taille du fichier (KB)':''
    }

}
# def testAwardsProcess():
#     """Stats stuff about the awards
#
#     Dummy code to get familiar with Kart"""
#     # ========= Stacked data: awards by events type ... ==============
#     import matplotlib.colors as mcolors
#     mcol = mcolors.CSS4_COLORS
#     mcol = list(mcol.values())
#     # mixing the colors with suficent gap to avoid too close colors
#     colss = [mcol[x+12] for x in range(len(mcol)-12) if x % 5 == 0]
#     # by type of event
#     awards.groupby(['event_year', 'event_type']).size(
#     ).unstack().plot(kind='bar', stacked=True, color=colss)
#     plt.show()
#
#
# def testArtworks():
#     """Get authors with artwork id
#
#     Dummy code to get familiar with Kart"""
#     # Get the data from csv
#     awards = pd.read_csv('awards.csv')
#     # Strip all data
#     awards = awards.applymap(lambda x: x.strip() if isinstance(x, str) else x)
#
#     # replace NA/Nan by 0
#     awards.artwork_id.fillna(0, inplace=True)
#
#     # Convert ids to int
#     awards.artwork_id = awards['artwork_id'].astype(int)
#
#     for id in awards.artwork_id:
#         # id must exist (!=0)@
#         if not id:
#             continue
#         prod = Production.objects.get(pk=id)
#         logger.info(prod.artwork.authors)

def run_import() :
    """ Main function to call to trigger the import process """

    # Clean the csv from udesired data (TODO : csv path as argument)
    clean_csv("./catalogue_panorama_23.csv")


# Clean the csv
logger.info("Cleaning the csv")

def clean_csv(csv_path, dest='./') :
    """ Clean the csv from undesired data from webform and store a cleaned csv with validated data from Kart when artist already exists in Kart.

    Parameters :
    - csv_path          :    (str) path to the csv file extracted from webform
    - dest  (optional)  :    (str) path to the csv file extracted from webform


    """

    csv_df = pd.read_csv(csv_path, skiprows=2, encoding='utf8')
    clean_df = pd.DataFrame()

    if "nom_prenom" not in csv_df.keys() :
        logger.error("The csv file does not seem to be well formated. Make sure 'Form Key' header format is checked when exporting from webform.")
        return

    # Activate or not some processes (debuging)
    check_name = True

    # The list holding validated (with match in Kart) user objects
    existing_users = list()
    # The list holding user objects that need to be created
    missing_users = list()

    # The list holding validated (with match in Kart) artist objects
    existing_artists = list()
    # The list holding artist objects that need to be created
    missing_artists = list()

    # The list holding validated (with match in Kart) student objects
    existing_students = list()
    # The list holding student objects that need to be created
    missing_students = list()

    # The list holding validated (with match in Kart) artwork objects
    valid_artworks = list()
    # The list holding artwork objects that need to be created
    create_artworks = list()

    # Main json file
    json_export = dict()
    # external json file for dream themes [{'id':23, theme:'A'}, {'id':543, theme:'C'}, ...]
    dream_l = list()
    partners_l = list()

    # Data filtering and extraction from the csv
    for index, row in csv_df.iterrows() :

        # Clean the nan's 
        for k,v in row.items():
            if 'nan' == str(v) and v in [row[kart2webf('artwork', 'subtitle')]] : 
                # logger.info(f'found nan ! : {k} {row[k]} - {v}')
                row[k] = None
        
        # Init user
        user = None

        # First, try to retrieve the user from Kart from first and last names
        firstname, lastname = get_names_from_name(row["nom_prenom"])

        # Fill new firstname and lastname columns in csv
        clean_df.loc[index,'firstname'] = firstname
        clean_df.loc[index,'lastname'] = lastname

        # User obj to created / updated
        user_dict = dict (
                    username    =   "",
                    first_name  =   firstname,
                    last_name   =   lastname,
                    email       =   row[kart2webf('user','email')],
                    password    =   ""
                )

        # Prepare the creation of an artist object
        artist_dict = dict (
                    nickname    =   row[kart2webf('artist', 'nickname')],
                    bio_fr      =   row[kart2webf('artist', 'bio_fr')],
                    bio_en      =   row[kart2webf('artist', 'bio_en')],
                    )

        # Prepare the creation of a student object
        promo_name = row[kart2webf('student', 'promotion')]
        promotion  = getPromoByName(promo_name)
        student_dict = dict (
                    promotion  = promotion
                    )

        # Prepare the creation of an artwork object
        artwork_dict =  dict (
                title            =   row[kart2webf('artwork', 'title')],
                subtitle         =   row[kart2webf('artwork', 'subtitle')],
                description_fr   =   row[kart2webf('artwork', 'description_fr')],
                description_en   =   row[kart2webf('artwork', 'description_en')],
                thanks_fr        =   row[kart2webf('artwork', 'thanks_fr')],
        )

        ##########
        #  USER  #
        ##########

        logger.info(f"User recherché : prénom > {firstname}, nom > {lastname}")

        # Try to retrieve the artist from Kart from first and last names
        userSearch = getUserByNames(lastname=lastname, firstname=firstname, dist_min=1.8)

        # If csv user match in Kart (dist = similarity btw csv last and firstnames and Kart's)
        if userSearch :

            # Get the user object from search
            user = userSearch['user']

            logger.info(f"User found {userSearch}")

            # Add user to existing users list
            existing_users += [user]

            # Set user_found col in csv
            clean_df.loc[index,'user_found'] = True
            clean_df.loc[index,'user_id'] = user.id
        else :
            # if no user match in Kart, create it
            clean_df.loc[index,'user_found'] = False
            clean_df.loc[index,'artist_found'] = False
            clean_df.loc[index,'student_found'] = False
            logger.info("Not found in Kart, add to create list.")
            # Add the index of the row to the list of users to create
            missing_users += [user]

            # Username from first and last names
            username = usernamize(firstname, lastname, check_duplicate=True)

            # Assign username
            user_dict['username'] = username

            user = User(**user_dict)

            # Save user
            if not DRY_RUN :
                user.save()


        ###########
        # ARTISTS #
        ###########

        # Init
        artist = None

        ########################################
        # TODO : script de recherche de doublons 
        # Search by similarity with nickname
        # nickname = row[kart2webf('artist', 'nickname')]
        # 
        # # Get the artist by closest nickname
        # guessArtistNN = Artist.objects.annotate(
        #     similarity=TrigramSimilarity('nickname__unaccent', nickname),
        # ).filter(nickname=nickname, similarity__gt=0.8).order_by('-similarity')
        # 
        # # List potential duplicated artist (same nickname, diff user)
        # potential_duplicates = list()
        # 
        # # If artists with close nickname is found
        # if guessArtistNN : 
        #     logger.info(f"guess nickname {row[kart2webf('artist', 'nickname')]} <--> {guessArtistNN[0].user.id} --------------- {user.id}")
        #     # For each artist found with similar nicknames, check the associated user.id
        #     for match in guessArtistNN :
        #         potential_duplicates += [{'id_artist':match.id, 'id_user':user.id}]                    
        #     # If more than 1 artist have the same nickname ...
        #     if len(potential_duplicates)>1 :
        #         # ... that means that 2 or more artists share the same nickname
        #         logger.info(f"Houston we've got a problem {potential_duplicates}")
        #         for dupli in potential_duplicates :
        #             for dupli2 in potential_duplicates :
        #                 if dupli['id_user'] == dupli2['id_user'] :
        #                     logger.info(f" !! 1 user ({dupli['id_user']}) is 2 artists ({dupli2['id_artist']}) with same nickname ({nickname}) at the same time !!")
        ##########################################

        # Check if artist object is associated with user
        try :
            # Get the artist with matching user id
            artist = Artist.objects.get(user__pk=user.id)

            logger.info(f"Associated artist found {artist}")

            # Add artist to existing artists list
            existing_artists += [artist]

            # Check artist_found in csv
            clean_df.loc[index,'artist_found'] = True

            # Fill artist_id in df
            clean_df.loc[index,'artist_id'] = artist.id

        except :  # If no associated artist found,
            # Provide user.id to artist dict
            artist_dict['user_id'] = user.id

            # Create an artist from dict
            artist = Artist(**artist_dict)

            # Check artist_found in csv
            clean_df.loc[index,'artist_found'] = False

            #  Add artist to missing artists
            missing_artists += [artist]

        # Save artist
        if not DRY_RUN :
            artist.save()

        ############
        # STUDENTS #
        ############

        # Init
        student = None
        print("promotion", promotion)
        print("user__pk=user.id", user.id, artist.id)
        if promotion :  # Create a student only when promotion is defined (otherwise invited )
            # Check if student object is associated with user
            try :
                # Get the student with matching user and artist ids
                student = Student.objects.get(user__pk=user.id, artist__pk=artist.id)

                logger.info(f"Associated student found {artist}")

                # Add student to existing students list
                existing_students += [student]

                # Check student_found in csv
                clean_df.loc[index,'student_found'] = True
                clean_df.loc[index,'student_id'] = student.id

            except :  # If no associated student found
                
                # Fill student_dict
                student_dict['user']    =   user
                student_dict['artist']  =   artist

                # Create an student from dict
                student = Student(**student_dict)

                # Check student_found in csv
                clean_df.loc[index,'student_found'] = False

                #  Add student to missing students
                missing_students += [student]

                # Save student
                if not DRY_RUN :
                    student.save()
            print("student.id", student.id)

        ############
        # ARTWORKS #
        ############

        # init artwork
        artwork = None


        # Check if aw not already in Kart (should not !)
        # Try to retrieve artworks from Kart with user in authors

        # Get the artworks associated to the current user
        aw_kart = Artwork.objects.filter(authors=artist)

        if aw_kart :
            # If an aw is found, we compare with the csv title
            for aw in aw_kart :
                aw_csv = row[kart2webf('artwork','title')]

                logger.info(f" simi {aw.title}, aw_csv : {aw_csv}" )

                if dist2(aw.title, aw_csv ) >.8 :
                    logger.info(f"\tAssociated artworks in Kart : {aw.title}")
                    logger.info(f"\t                     in csv : {row[kart2webf('artwork','title')]}")
                    logger.info(f"----> {dist2(aw.title, row[kart2webf('artwork','title')])}")
                    artwork = aw
                    # Check artwork_found in csv
                    clean_df.loc[index,'artwork_found'] = True
                    clean_df.loc[index,'artwork_id'] = artwork.id
                    break

        if not artwork :
            logger.info("No related artwork in Kart")

            # Timetag the aw as today
            now = datetime.now()
            artwork_dict['production_date'] = now

            # Romano : " je mets le 01/01/2021"

            # Get the type from csv
            aw_type = row['type']

            if "installation" == aw_type.lower() or "performance" == aw_type.lower() :
                    print("installation")
                    artwork = Installation (**artwork_dict)

            if "film" == aw_type.lower() :
                    
                    duration = str(row[kart2webf('artwork', 'duration')])
                    
                    if 'nan' == duration : duration = None
                    artwork_dict['duration'] = duration
                    artwork = Film (**artwork_dict)


            

            # Save artwork
            if not DRY_RUN :
                artwork.save()

            # Add author to the artwork
            artwork.authors.add(artist)

            # Save artwork
            if not DRY_RUN :
                artwork.save()

        print("duration", row[kart2webf('artwork', 'duration')])

        # Dream theme -> external json file
        dream_l += [{artwork.id :row['dream_theme']}]

        # Remove potential html tags
        partners_txt = clean_tags(row[kart2webf('artwork', 'partners_txt')])
        partners_l += [{artwork.id : partners_txt}]


    # Convert external data to json
    json_export["dream_theme"] = dream_l
    json_export["partners"] = partners_l
    # Store the dream themes in an external json file
    with open('./data.json', 'w') as fout:
        json.dump(json_export, fout)



    exit()



    # # Check if artist object exists from existing users
    # print("Checking existing artists in existing users...")
    # for user in existing_users :
    #     artist = Artist.objects.get(user__pk=user.id)
    #
    # # Check if artist object exists from users to create (should not !)
    # print("Checking existing artists in missing users...")
    # for user in missing_users :
    #     try :
    #         artist = Artist.objects.get(user__pk=user.id)
    #     except :
    #         print("Not an artist : ",user)
    #         pass

        # Explore the first artist (révisions :) !)
        # artist = existing_users[0]

        ############
        # STUDENTS #
        ############
        # promotion   =   getPromoByName(row[kart2webf('student','promotion')]),
            # try :
            #     student = Student.objects.get(pk=artist.student.id)
            #     print('student', student)
            # except :
            #     print("Not a student : ",user)
            #     pass
    # print(csv_df)
    # cols containing "_id"
    cols = [col for col in csv_df.columns if '_id' in col]
    clean_df[cols] = csv_df[cols].fillna(0)
    clean_df[cols] = csv_df[cols].astype(int)
    clean_df.to_csv('clean.csv',index=False)
    exit()




    # Artwork process
    # Check if artwork already exists
    # for title in csv["titre"] :
    #     print('title', title)
    #     aw = getArtworkByTitle(title)
    #     if title is None : print(aw,"\n")



    # print(artist.user)
    # print(artist.student.__dict__)

    # PROMO
    # {'_state': <django.db.models.base.ModelState object at 0x1233b6050>, 'id': 25, 'name': 'Jonas Mekas', 'starting_year': 2019, 'ending_year': 2021}


    # STUDENT
    # {'_state': <django.db.models.base.ModelState object at 0x11b953e90>, 'id': 535, 'number': '2019-209', 'promotion_id': 25, 'graduate': False, 'user_id': 1513, 'artist_id': 1493}


    # ARTIST
    # {'_state': , 'id': 1493, 'user_id': 1513, 'nickname': '', 'bio_short_fr': '', 'bio_short_en': '', 'bio_fr': '', 'bio_en': '', 'updated_on': , 'twitter_account': '', 'facebook_profile': '', 'search_name': 'Inès Sieulle', 'similarity': 0.625, '_prefetched_objects_cache': {}}

    # USER
    # {'_state':, 'id': 1513, 'password': '', 'last_login': datetime.datetime(2019, 4, 23, 13, 22, 48, tzinfo=<UTC>), 'is_superuser': , 'username': 'inessieulle', 'first_name': 'Inès', 'last_name': 'Sieulle', 'email': 'ines.sieulle@gmail.com', 'is_staff': False, 'is_active': True, 'date_joined': }

    # Identify the promotion
    promo = Promotion.objects.get(pk=artist.student.promotion_id)
    print(promo.__dict__)
    student_mapping = {
        'promotion':'',
    }


        # logger.info("\n\n")

# Identify artists / artworks
# Fill with data




















################################################################

def usernamize(fn="", ln="", check_duplicate=False) :
    """ Return a username from first and lastname """

    # Check if multipart firstname
    fn_l = re.split('\W+',fn)

    # Extract first letter of each fn part
    fn_l = [part[0].lower() for part in fn_l if part.isalpha()]

    # Lower lastname and remove non alpha chars
    ln_l = [letter.lower() for letter in ln if letter.isalnum()]

    # Concat strings
    username = "".join(fn_l) + "".join(ln_l)

    # Remove any special characters
    username = unidecode.unidecode(username)

    # Trim at 10 characters
    username = username[:10]

    if check_duplicate :
        # Check if username is already taken, add 2, 3, 4 ... until its unique
        # Init suffix
        i = 2
        while objExist(User,default_index=None,username=username) :
            username = usernamize(firstname, lastname) + f"{i}"
            i+=1

    return username

def getPromoByName(promo_name="") :
    """ Return a promotion object from a promo name"""
    # First filter by lastname similarity
    guessPromo = Promotion.objects.annotate(
                                        similarity=TrigramSimilarity('name', promo_name)
                                   ).filter(
                                        similarity__gt=0.8
                                    ).order_by('-similarity')
    if guessPromo :
        return guessPromo[0]
    print("Promo non trouvée", promo_name)
    return None

def webf2kart(model="",field=""):
    """ Return the corresponding field name in Kart from Webform field name"""
    return wf2kart_mapping[model][field]


def kart2webf(model="",field=""):
    """ Return the corresponding field name in Webform from Kart field name"""
    if model in wf2kart_mapping.keys() :
        for k, v in wf2kart_mapping[model].items():
            if v == field : return k
    return False

def dist2(item1, item2):
    """Return the distance between the 2 strings"""
    # print(f"dist2 {item1} versus {item2}")
    if not type(item1) == type(item2) == str:
        raise TypeError("Parameters should be str.")
    return round(SequenceMatcher(None, item1.lower(), item2.lower()).ratio(), 2)



def artworkCleaning():
    """Preparation and cleannig step of the awards csv file

    WARNING: this function requires a human validation and overrides `artworks_artists.csv` & `merge.csv`

    1) from the csv data, extract potential artworks already present in Kart
    2) when doubts about the name of the artwork, with close syntax, store the artwork kart_title in a csv for
    validation by head of diffusion.
    3) if no match at all, mark the artwork for creation
    """

    aws = pd.read_csv('./tmp/merge.csv')

    # Check if the id provided in the csv match with the artwork description
    # replace the nan with empty strings
    aws.fillna('', inplace=True)

    # List of object to create
    obj2create = []

    # For each award of the csv file
    for ind, aw in aws.iterrows():

        # Variables init
        no_artwork = no_artist = False

        # Parsing
        aw_id = int(aw.artwork_id) if aw.artwork_id else None
        aw_title = str(aw.artwork_title)
        lastname = str(aw.artist_lastname)
        firstname = str(aw.artist_firstname)
        _artist_l = getArtistByNames(firstname=firstname, lastname=lastname, listing=True)

        # If an id is declared, get the aw from kart and check its
        # similarity with the content of the row to validate
        if aw_id:
            # Artwork validation if the title from aw generated with id and title in csv
            aw_kart = Artwork.objects.prefetch_related('authors__user').get(pk=aw_id)
            if dist2(aw_kart.title, aw_title) < .8:
                logger.warning(f"""ARTWORK INTEGRITY PROBLEM:
                    Kart       :\"{aw_kart.title}\"
                    should match
                    Candidate  : \"{aw_title}\"""")
                aws.loc[ind, 'aw_art_valid'] = False

            # Artist/author validation
            # The closest artists in Kart from the data given in CSV (listing => all matches)
            _artist_l = getArtistByNames(firstname=firstname, lastname=lastname, listing=True)

            # If no match, should create artist ?
            if not _artist_l:
                # Add the object to the list of object to create
                o2c = {'type': 'Artist', 'data': {'firstname': firstname, 'lastname': lastname, }}
                if o2c not in obj2create:
                    logger.warning(
                        f"No artist can be found with {firstname} {lastname}: CREATE ARTIST ?\n\n")
                    obj2create.append(o2c)
                # Create the object in Kart # TODO
                # input(f'Should I create the an artist with these data: {o2c} ')
                continue

            # Compare the artists found in CSV to the authors of the artwork in Kart
            # List of the artist that are BOTH in the authots in Kart and in the CSV
            artist_in_authors = [x['artist']
                                 for x in _artist_l if x['artist'] in aw_kart.authors.all()]

            # If no match between potential artists and authors: integrity issue of the csv
            if not len(artist_in_authors):
                logger.warning(
                    f"""Artist and artwork do not match ---------- SKIPPING\nArtist: {_artist_l}\n
                    Artwork: {aw_kart}\n{aw_kart.authors.all()[0].id}\n\n""")
                aws.loc[ind, 'aw_art_valid'] = False
                continue
            else:
                # Otherwise, the authors are validated and their id are stored in csv
                aws.loc[ind, "artist_id"] = ",".join([str(x.id) for x in artist_in_authors])
                # logger.info(f"authors {aws.loc[ind, 'artist_id']}")
                # Continue to next row
                continue

        # If no id and no title provided, skip
        if not aw_id and aw_title == '':
            logger.info(
                "No data about artwork in the csv file, only artist will be specified in the award.")
            no_artwork = True

        # If partial to no artist data in the csv
        if not all([firstname, lastname]):
            if not any([firstname, lastname]):
                logger.info("No info about the artist")
                no_artist = True
            else:
                logger.info("Partial data about artist ...")

        if all([no_artwork, no_artist]):
            logger.warning(
                f"{aw_title} No info about the artwork nor the artists: SKIPPING\n{aw}\n\n")
            continue

        # IF NO ID ARTWORK
        # Retrieve artwork with title similarity
        getArtworkByTitle()

    aws.to_csv('./tmp/artworks_artists.csv', index=False)


def getArtworkByTitle(aw_title):
    guessAW = Artwork.objects.annotate(
        similarity=TrigramSimilarity('title', aw_title),
    ).filter(similarity__gt=0.7).order_by('-similarity')

    if guessAW:
        logger.warning(f"Potential artworks in Kart found for \"{aw_title}\"...")
        # Explore the potential artworks
        for gaw in guessAW:
            logger.warning(f"\t->Best guess: \"{gaw.title}\"")
            # If approaching results is exactly the same
            title_match_dist = dist2(aw_title.lower(), gaw.title.lower())
            logger.warning(f"title_match_dist {title_match_dist}")

            # if all([title_match_dist, author_match_dist, title_match_dist == 1, author_match_dist == 1]):
            #     logger.warning("Perfect match: artwork and related authors exist in Kart")
            # if all([title_match_dist, author_match_dist, title_match_dist == 1]):
            #     logger.warning(
            #         f"Sure about the artwork title, confidence in author: {author_match_dist}")
            # if all([title_match_dist, author_match_dist, author_match_dist == 1]):
            #     logger.warning(
            #         f"Sure about the authors, confidence in artwirk: {author_match_dist}")

            # TODO: include author_match_dist for higher specificity
            # if all([title_match_dist, author_match_dist, title_match_dist == 1, author_match_dist == 1]):
            #     logger.warning("Perfect match: artwork and related authors exist in Kart")
            # if all([title_match_dist, author_match_dist, title_match_dist == 1]):
            #     logger.warning(
            #         f"Sure about the artwork title, confidence in author: {author_match_dist}")
            # if all([title_match_dist, author_match_dist, author_match_dist == 1]):
            #     logger.warning(
            #         f"Sure about the authors, confidence in artwirk: {author_match_dist}")

    else:  # no artwork found in Kart
        logger.warning(f"No approaching artwork in KART for {aw_title}")
        # Retrieving data to create the artwork


search_cache = {}

def getArtistByNames(firstname="", lastname="", pseudo="", listing=False): # TODO pseudo
    """Retrieve the closest artist from the first and last names given

    Parameters:
    - firstname: (str) Firstname to look for
    - lastname : (str) Lastname to look for
    - pseudo   : (str) Pseudo to look for
    - listing  : (bool) If True, return a list of matching artists (Default, return the closest)

    Return:
    - artistObj    : (Django obj / bool) The closest artist object found in Kart. False if no match.
    - dist         : (float) Distance with the given names
    """
    user = getUserByNames(firstname, lastname, listing=listing)
    if user :
        return Artist.objects.get(user__pk=user.id)
    return False


def getUserByNames(firstname="", lastname="", pseudo="", listing=False, dist_min=False): # TODO remove pseudo from params
    """Retrieve the closest user from the first and last names given

    Parameters:
    - firstname: (str) Firstname to look for
    - lastname : (str) Lastname to look for
    - listing  : (bool) If True, return a list of matching artists (Default, return the closest)
    - dist_min : (float) Maximum dist, return False if strinctly under

    Return:
    - artistObj    : (Django obj / bool) The closest user object found in Kart. False if no match.
    - dist         : (float) Distance with the given names
    """

    # If no lastname no pseudo
    if not any([lastname, pseudo]):
        logger.info(
            f"\n** getArtistByNames **\nAt least a lastname or a pseudo is required.\nAborting research. {firstname}")
        return False

    # If data not string
    # print([x for x in [firstname,lastname,pseudo]])
    if not all([type(x) == str for x in [firstname, lastname, pseudo]]):
        logger.info(
            "\n** getArtistByNames **\nfirstname,lastname,pseudo must be strings")
        return False

    # List of users that could match
    users_l = []

    # Clean names from accents to
    if lastname:
        # lastname_accent = lastname
        lastname = unidecode.unidecode(lastname).lower()
    if firstname:
        # firstname_accent = firstname
        firstname = unidecode.unidecode(firstname).lower()
    # if pseudo:
    #     # pseudo_accent = pseudo
    #     pseudo = unidecode.unidecode(pseudo).lower()
    fullname = f"{firstname} {lastname}"

    # Cache
    fullkey = f'{firstname} {lastname} {pseudo}'
    try:
        # logger.warning("cache", search_cache[fullkey])
        return search_cache[fullkey] if listing else search_cache[fullkey][0]
    except KeyError:
        pass

    # SEARCH WITH LASTNAME then FIRSTNAME
    # # First filter by lastname similarity
    # guessArtLN = Artist.objects.prefetch_related('user').annotate(
    #     # Concat the full name "first last" to detect misclassifications like: "Hee Won -- Lee" where Hee Won is first
    #     # name but can be stored as "Hee  -- Won Lee"
    #     search_name=Concat('user__first_name__unaccent__lower',
    #                        Value(' '), 'user__last_name__unaccent__lower')
    # ).annotate(
    #     similarity=TrigramSimilarity('search_name', fullname),
    # ).filter(
    #     similarity__gt=0.3
    # ).order_by('-similarity')

    # First filter by lastname similarity
    guessArtLN = User.objects.annotate(
        # Concat the full name "first last" to detect misclassifications like: "Hee Won -- Lee" where Hee Won is first
        # name but can be stored as "Hee  -- Won Lee"
        search_name=Concat('first_name__unaccent__lower',
                           Value(' '), 'last_name__unaccent__lower')
    ).annotate(
        similarity=TrigramSimilarity('search_name', fullname),
    ).filter(
        similarity__gt=0.3
    ).order_by('-similarity')

    # Refine results
    if guessArtLN:
        # TODO: Optimize by checking a same artist does not get tested several times
        for user_kart in guessArtLN:

            # print(f"\tARTIST : {user_kart}")
            # Clear accents (store a version with accents for further accents issue detection)
            kart_lastname_accent = user_kart.last_name
            kart_lastname = unidecode.unidecode(kart_lastname_accent).lower()
            kart_firstname_accent = user_kart.first_name
            kart_firstname = unidecode.unidecode(kart_firstname_accent).lower()
            kart_fullname_accent = user_kart.search_name
            # print(f"\t\tuser_kart.search_name {user_kart.search_name}")
            kart_fullname = f"{kart_firstname} {kart_lastname}".lower()

            dist_full = dist2(kart_fullname, fullname)

            # logger.warning('match ',kart_fullname , dist2(kart_fullname,fullname), fullname,kart_fullname == fullname)
            # In case of perfect match ...
            if dist_full > .9:
                if kart_fullname == fullname:
                    # store the artist in potential matches with extreme probability (2)
                    # and continue with next candidate
                    users_l.append({"user": user_kart, 'dist': 2})
                    continue
                # Check if Kart and candidate names are exactly the same
                elif kart_lastname != lastname or kart_firstname != firstname :

                    logger.warning(f"""Fullnames globally match {fullname} but not in first and last name correspondences:
                    Kart       first: {kart_firstname} last: {kart_lastname}
                    candidate  first: {firstname} last: {lastname}
                                            """)
                    users_l.append({"user": user_kart, 'dist': dist_full*2})
                    # ### Control for accents TODO still necessary ?
                    #
                    # accent_diff = kart_lastname_accent != lastname_accent or \
                    #               kart_firstname_accent != firstname_accent
                    # if accent_diff: logger.warning(f"""\
                    #                 Accent or space problem ?
                    #                 Kart: {kart_firstname_accent} {kart_lastname_accent}
                    #                 Candidate: {firstname_accent} {lastname_accent} """)
                    continue

            # Control for blank spaces

            if kart_lastname.find(" ") >= 0 or lastname.find(" ") >= 0:
                # Check distance btw lastnames without spaces
                if dist2(kart_lastname.replace(" ", ""), lastname.replace(" ", "")) > .9:
                    bef = f"\"{kart_lastname}\" <> \"{lastname}\""
                    logger.warning(f"whitespace problem ? {bef}")

            if kart_firstname.find(" ") >= 0 or firstname.find(" ") >= 0:
                # Check distance btw firstnames without spaces
                if dist2(kart_firstname.replace(" ", ""), firstname.replace(" ", "")) > .9:
                    bef = f"\"{kart_firstname}\" <> \"{firstname}\""
                    logger.warning(f"whitespace problem ? {bef}")
            ###

            # Artists whose lastname is the candidate's with similar firstname

            # Distance btw the lastnames
            dist_lastname = dist2(kart_lastname, lastname)

            # # try to find by similarity with firstname
            # guessArtFN = Artist.objects.prefetch_related('user').annotate(
            #     similarity=TrigramSimilarity('user__first_name__unaccent', firstname),
            # ).filter(user__last_name=lastname, similarity__gt=0.8).order_by('-similarity')

            guessUserFN = User.objects.annotate(
                similarity=TrigramSimilarity('first_name__unaccent', firstname),
            ).filter(last_name=lastname, similarity__gt=0.8).order_by('-similarity')


            # if user whose lastname is the candidate's with similar firstname names are found
            if guessUserFN:

                # Check users with same lastname than candidate and approaching firstname
                for userfn_kart in guessUserFN:
                    kart_firstname = unidecode.unidecode(userfn_kart.first_name)
                    # Dist btw candidate firstname and a similar found in Kart
                    dist_firstname = dist2(f"{kart_firstname}", f"{firstname}")
                    # Add the candidate in potential matches add sum the distances last and firstname
                    users_l.append({"user": userfn_kart, 'dist': dist_firstname+dist_lastname})

                    # Distance evaluation with both first and last name at the same time
                    dist_name = dist2(f"{kart_firstname} {kart_lastname}",
                                      f"{firstname} {lastname}")
                    # Add the candidate in potential matches add double the name_dist (to score on 2)
                    users_l.append({"user": userfn_kart, 'dist': dist_name*2})

            else:
                # If no close firstname found, store with the sole dist_lastname (unlikely candidate)
                users_l.append({"user": user_kart, 'dist': dist_lastname})

            ### end for user_kart in guessArtLN

        # Take the highest distance score
        users_l.sort(key=lambda i: i['dist'], reverse=True)

        # Return all results if listing is true, return the max otherwise
        if listing:
            search_cache[fullkey] = users_l
            return users_l
        else:
            search_cache[fullkey] = [users_l[0]]
            # Return the result if dist_min is respected (if required)
            if (dist_min is not False and users_l[0]['dist']>dist_min) or (not dist_min) :
                return users_l[0]
            else :
                return False
    else:
        # research failed
        search_cache[fullkey] = False
        return False
    #####


def infoCSVeventTitles():
    """Display info about potentialy existing events in Kart

    Check if event names exist with a different case in Kart and display warning
    """
    eventsToCreate = pd.read_csv('./tmp/events_title.csv')

    for evt_title in eventsToCreate.NomFichier:
        # If a title already exist with different case
        exact = Event.objects.filter(title__iexact=evt_title)
        if exact:
            logger.warning(
                f"Event already exist with same name (but not same case) for {evt_title}:\n{exact}\n")

        # If a title already contains with different case
        contains = Event.objects.filter(title__icontains=evt_title)
        if contains:
            logger.warning(
                f"Event already exist with very approaching name (but not same case) for {evt_title}:\n{contains}\n")


def createEvents():
    """ Create (in Kart) the events listed in awards csv file

    1) Retrieve the data about the events listed in awards csv file
    2) Parse those data and prepare if for Event creation
    3) (optional) Check if meta event exits for the created event, creates it if needed
    """

    # Get the events from awards csv extended with title cleaning (merge.csv)
    events = pd.read_csv('./tmp/merge.csv')

    # Create/get the events in Kart
    for ind, event in events.iterrows():
        title = event.NomDefinitif
        # Starting dates are used only for the year info (default 01.01.XXX)
        starting_date = event.event_year
        # Convert the year to date
        starting_date = datetime.strptime(str(starting_date), '%Y')
        starting_date = pytz.timezone('Europe/Paris').localize(starting_date)

        # All events are associated with type festival
        # TODO: Add other choices to event ? Delete choices constraint ?
        type = "FEST"

        # If no title is defined, skip the event
        if str(title) in ["nan", ""]:
            continue

        # Check if meta event exists, if not, creates it
        evt = Event.objects.filter(
            title=title,
            type=type,
            main_event=True
        )
        # If event already exist
        if len(evt):
            # Arbitrarily use the first event of the queryset (may contain more than 1)
            # TODO: what if more than one ?
            evt = evt[0]
            created = False
        else:
            # Create the main event
            evt = Event(
                title=title,
                # default date to 1st jan 70, should be replaced by the oldest edition
                starting_date=datetime.strptime("01-01-70", "%d-%m-%y").date(),
                type=type,
                main_event=True
            )
            if not DRY_RUN:
                evt.save()
            created = True

        if created:
            logger.info(f"META {title} was created")
        else:
            logger.info(f"META {title} was already in Kart")

        # Check if event exists, if not, creates it
        evt = Event.objects.filter(
            title=title,
            type=type,
            # just use the starting date for now
            # TODO: events with more details
            starting_date=starting_date
        )

        if len(evt):
            # Arbitrarily use the first event of the queryset
            evt = evt[0]
            created = False
        else:
            logger.info("obj is getting created")
            evt = Event(
                title=title,
                type=type,
                starting_date=starting_date
            )
            if not DRY_RUN:
                evt.save()
            created = True

        if created:
            logger.info(f"{title} was created")
        else:
            logger.info(f"{title} was already in Kart")
        # Store the ids of newly created/already existing events in a csv
        events.loc[ind, 'event_id'] = evt.id
    events.to_csv('./tmp/events.csv', index=False)


def getISOname(countryName=None, simili=False):
    """Return the ISO3166 international value of `countryName`

    Parameters:
    - countryName  : (str) The name of a country
    - simili         : (bool) If True (default:False), use similarity to compare the names
    """
    # Process the US case (happens often!)
    if re.search('[EeéÉ]tats[ ]?-?[ ]?[Uu]nis', countryName):
        return "US"
    # Kosovo is not liste in django countries (2020)
    if re.search('kosovo', countryName, re.IGNORECASE):
        return 'XK'

    # General case
    if not simili:
        for code, name in list(countries):
            if name == countryName:
                return code
        return False
    else:
        # The dic holding the matches
        matchCodes = []
        for code, name in list(countries):
            dist = SequenceMatcher(None, str(countryName).lower(), name.lower()).ratio()
            # logger.info(f"DIST between {countryName} (unknown) and {name}: {dist}")
            if dist >= .95:
                matchCodes.append({'dist': dist, 'code': code})  # 1 ponctuation diff leads to .88
            if dist >= .85:
                cn1 = unidecode.unidecode(str(countryName))
                cn2 = unidecode.unidecode(name)
                dist2 = SequenceMatcher(None, cn1.lower(), cn2.lower()).ratio()
                if dist2 > dist:
                    logger.info(
                        f"""------------------- ACCENTUATION DIFF {countryName} vs {name}\n
                        Accents removed: {cn1} vs {cn2}: {dist2}""")
                    # 1 ponctuation diff leads to .88
                    matchCodes.append({'dist': dist2, 'code': code})
                else:
                    if DEBUG:
                        return code
                    cont = input(f"""
                                 NOT FOUND but {countryName} has a close match with {name}
                                 Should I keep it ? (Y/n):   """)
                    if re.search("NO?", cont, re.IGNORECASE):
                        continue
                    else:
                        return code

    # Sort the matches by similarity
    sorted(matchCodes, key=lambda i: i['dist'])
    try:
        # Return the code with the highest score
        return matchCodes[0]['code']
    except IndexError:
        return False


def createPlaces():
    """Create the places listed in the awards csv files

    """

    # Get the data from awards csv extended with title cleaning and events (merge.csv)
    merge = pd.read_csv('./tmp/events.csv')
    # Drop duplicates
    places = merge.drop_duplicates(['place_city', 'place_country'])
    # Remove rows with full empty location
    places = places.dropna(subset=['place_city', 'place_country'], how="all")
    # Replace NA/NaN (similarity fails otherwise)
    places.fillna('', inplace=True)

    for ind, place in places.iterrows():
        city = place.place_city
        country = place.place_country
        if city == country == '':
            continue
        logger.info(f"\n\nPLACE: {city} - {country}")

        # Processing CITY
        # Look for really approaching (simi=.9) name of city in Kart
        guessCity = Place.objects.annotate(
            similarity=TrigramSimilarity('name', city),
        ).filter(similarity__gt=0.9).order_by('-similarity')

        # If a city in Kart is close from the city in csv file
        if guessCity:
            logger.info(f"CITY FOUND IN KART: {guessCity[0].city}")
        else:
            logger.info("No close city name in Kart, the place should be created or is empty")

        # Processing COUNTRY
        # Look for ISO country code related to the country name in csv
        codeCountryCSV = getISOname(country)

        # If code is easly found, keep it
        if codeCountryCSV:
            logger.info(f"CODE FOUND: {country} -> {codeCountryCSV}")

        # If no code found, check if the country associated with the city found in Kart
        # is close from the country in csv file to use its code instead
        elif guessCity:
            codeCountryKart = guessCity[0].country
            countryNameKart = dict(countries)[codeCountryKart]

            # Compute the distance between the 2 country names
            dist = round(SequenceMatcher(None, str(country).lower(),
                                         countryNameKart.lower()).ratio(), 2)

            # If really close, keep the Kart version
            if dist > .9:
                logger.info(f"Really close name, replacing {country} by {countryNameKart}")
                codeCountryCSV = codeCountryKart
            else:
                # Process the us case (happens often!)
                if re.search('[EeéÉ]tats[ ]?-?[ ]?[Uu]nis', country):
                    codeCountryCSV = "US"
                else:  # If not close to the Kart version, try with similarity with other countries
                    codeCountryCSV = getISOname(country, simili=True)

        else:  # No city found, so no clue to find the country => full search
            # parameter simili=True triggers a search by similarity btw `country` and django countries entries
            codeCountryCSV = getISOname(country, simili=True)
            if codeCountryCSV:
                logger.info(
                    f"Looked for the country code of {country} and obtained {codeCountryCSV}")
            else:
                # Check for Kosovo:
                # Although Kosovo has no ISO 3166-1 code either, it is generally accepted to be XK temporarily;
                # see http://ec.europa.eu/budget/contracts_grants/info_contracts/inforeuro/inforeuro_en.cfm or the CLDR
                if re.search("kosovo", country, re.IGNORECASE):
                    codeCountryCSV = "XK"
                logger.info("No city found, no country found:-(")

        # Check if place exists, if not, creates it
        place_obj = Place.objects.filter(
            name=city if city else country,
            city=city,
            country=codeCountryCSV if codeCountryCSV else ''
        )
        # If place already exist
        if len(place_obj):
            # Arbitrarily use the first place of the queryset (may contain more than 1)
            # TODO: what if more than one ?
            place_obj = place_obj[0]
            created = False
        else:
            # Create the Place
            place_obj = Place(
                name=city if city else country,
                city=city,
                country=codeCountryCSV if codeCountryCSV else ''
            )
            if not DRY_RUN:
                place_obj.save()
            created = True
        if place.place_city == '':
            logger.info(f'Empty City ============== {place_obj}')

        if created:
            logger.info(f"Place {place_obj} was created")
        else:
            logger.info(f"Place {place_obj} was already in Kart")
        # Store the id of the place
        places.loc[ind, 'place_id'] = place_obj.id

    # Store the places
    places.to_csv('./tmp/places.csv', index=False)

    # test to deal with city only rows, use "NULL" to allow the merging with missing data
    places.loc[places['place_city'] == '', 'place_city'] = "**NULL**"
    merge.loc[merge['place_city'].isna(), 'place_city'] = "**NULL**"

    merge_df = pd.merge(
        merge,
        places[["place_city", "place_country", "place_id"]],
        how='left', on=["place_city", "place_country"]
    )
    # Restore the missing data after the merge
    merge_df.loc[merge_df['place_city'] == "**NULL**", 'place_city'] = ''
    merge_df.to_csv('./tmp/merge_events_places.csv', index=False)

# TODO: Fill artwork in the event


def associateEventsPlaces():
    """Fill the place field of created events with the created places

    """

    # Get the events and places csv
    evt_places = pd.read_csv("./tmp/merge_events_places.csv")

    # Update the events with the place
    for ind, award in evt_places.iterrows():
        event_id = int(award.event_id)
        if str(award.place_id) != "nan":
            try:  # some events have no places specified
                place_id = int(award.place_id)
                evt = Event.objects.get(pk=event_id)
                evt.place_id = place_id
                if not DRY_RUN:
                    evt.save()
                logger.info(evt)
            except ValueError as ve:
                logger.info("ve", ve, "award.place_id", award.place_id)


def safeGet(obj_class=None, default_index=None, force=False, **args):
    """Try to `get`the object in Kart. If models.MultipleObjectsReturned error, return the first oject returned
        or the one in index `default_index`

    Parameters:
    - objClass     : (Django obj) The class on which to apply the get function
    - default      : (int) The index of the queryset to return in case of MultipleObjectsReturned error.
                      '0' is used in case of IndexError
    - args         : the arguments of the get query
    - force        : (bool) Force the return of the whole queryset rather than just one object - Default: False

    Return:
    - obj          : (Django obj or bool) a unique object of `obj_class`matching the **args,
                       False if `ObjectDoesNotExist` is raised
    - filtered     : a boolean indicating if the returned obj was unique or from a >1 queryset
    """

    try:
        obj = obj_class.objects.get(**args)
        return obj, False

    # If the object does not exist, return False
    except ObjectDoesNotExist:
        return False, False

    # If multiple entries for the query, fallback on filter
    except MultipleObjectsReturned:
        objs = obj_class.objects.filter(**args)
        logger.info(f"The request of {args}  returned multiple entries for the class {obj_class}")

        if default_index:
            try:
                return objs[default_index], True
            except ValueError:
                return objs[0], True
        else:
            # Return the first object of the queryset
            return objs[0], True


def objExistPlus(obj_class=None, default_index=None, **args):
    """Return a True if one or more objects with `**args` parameters exist

    Parameters:
    - objClass     : (DjangoObject) The class on which to apply the get function
    - default      : (int) The index of the queryset to return in case of MultipleObjectsReturned error.
                      '0' is used in case of IndexError
    - args         : the arguments of the get query

    Return:
    - exists       : (bool)
    - multiple     : (int) the amount of existing object
    """

    objs, filtered = safeGet(obj_class, force=True, **args)
    if objs:
        return True, len(objs)
    else:
        return False,


def objExist(obj_class=None, default_index=None, **args):
    """Return a True if one or more objects with `**args` parameters exist

    Parameters:
    - objClass     : (DjangoObject) The class on which to apply the get function
    - default      : (int) The index of the queryset to return in case of MultipleObjectsReturned error.
                      '0' is used in case of IndexError
    - args         : the arguments of the get query

    Return:
    - exists       : (bool)
    """

    objs, filtered = safeGet(obj_class, force=True, **args)
    if objs:
        return True
    else:
        return False


def createAwards():
    """Create the awards listed in csv in Kart

    """
    print("Create AWARDS")
    # Load the events associated to places and artworks (generated by createPlaces())
    awards = pd.read_csv("./tmp/merge_events_places.csv")

    # Load the artists and associated artworks (generated by artworkCleaning())
    authors = pd.read_csv("./tmp/artworks_artists.csv")

    # Merge all the data in a dataframe
    total_df = pd.merge(awards, authors, how='left')
    total_df["notes"] = ""
    total_df.fillna('', inplace=True)
    cpt = 0

    # Check if artist are ok (not fully controled before ...)
    # if no artist_id, search by name in db
    for id, row in total_df[total_df['artist_id'] == ''].iterrows():
        art = getArtistByNames(firstname=row['artist_firstname'], lastname=row['artist_lastname'], listing=False)
        # if there is a match
        # dist == 2 is the maximum score for artist matching
        if art and art['dist'] == 2:
            # the id is stored in df
            total_df.loc[id, "artist_id"] = art['artist'].id

    for ind, award in total_df.iterrows():
        # init
        artwork_id = artist = False

        label = award.meta_award_label
        event_id = int(award.event_id)

        # An artwork id is required to create the award
        if (award.artwork_id):
            artwork_id = int(award.artwork_id)
        else:
            logger.warning(f"No idartwork for {award.artwork_title}")
            continue

        if (award.artist_id):
            artist = Artist.objects.get(pk=int(award.artist_id))
        else:
            cpt += 1
            print("NO ID ARTIST ", label, event_id)

        # try:
        #     print("award.artist_id",int(award.artist_id))
        # except ValueError:
        #     print("------------------>", award.artist_id)
        note = award.meta_award_label_details

        description = award.meta_award_label_details
        if pd.isna(award.meta_award_label_details):
            description = ''

        # GET THE META-eventsToCreate
        # Retrieve the Kart title of the event
        event, filt = safeGet(Event, pk=event_id)
        mevent, filt = safeGet(Event, title=event.title, main_event=True)

        # GET OR CREATE THE META-AWARD
        # Check if award exists in Kart, otherwise creates it
        maward, filt = safeGet(MetaAward, label=f"{label}", event=mevent.id)

        if maward:
            logger.info(f"MetaAward {label} exist in Kart")
        else:
            maward = MetaAward(
                label=f"{label}",
                event=mevent,
                description=description,
                type="INDIVIDUAL"  # indivudal by default, no related info in csv
            )
            print(f"label {maward.label}, event {mevent}, description {description}")
            if not DRY_RUN:
                maward.save()
            logger.info(f"\"{maward}\" created ")

        # GET OR CREATE THE AWARDS
        new_aw, filt = safeGet(Award,
                               meta_award=maward.id,
                               artwork=artwork_id,
                               event=event.id,
                               # artists = artist_id
                               )
        logger.setLevel(logging.WARNING)
        if new_aw:
            logger.info(f"{new_aw} exist in Kart")
            try:
                new_aw.artist.add(artist.id)
            except IntegrityError:
                # logger.warning(f"Artist_id: {artist} caused an IntegrityError")
                pass
            except AttributeError:
                # logger.warning(f"Artist_id: {artist} caused an AttributeError")
                pass
            if not DRY_RUN:
                new_aw.save()
        else:
            new_aw = Award(
                meta_award=maward,
                event=event,
                date=event.starting_date,
                note=note
            )
            try:
                if not DRY_RUN:
                    new_aw.save()
                    new_aw.artwork.add(artwork_id)
                    new_aw.save()
                    print(f"{new_aw}  created")
            except ValueError:
                # logger.warning(f"Artist_id: {artist} caused an IntegrityError")
                pass
        # print("CPT", cpt)

# Fonctions à lancer dans l'ordre chronologique
# WARNING: eventCleaning and artworkCleaning should not be used !! (Natalia, head of diffusion, already
# validated diffusion/utils/import_awards/events_title.csv and diffusion/utils/import_awards/artworks_artists.csv)

# WARNING: this function requires a human validation and overrides `events_title.csv` & `merge.csv`
# eventCleaning()
# WARNING: this function requires a human validation and overrides `artworks_title.csv` & `merge.csv`
# artworkCleaning()

# logger.setLevel(logging.CRITICAL)
# DRY_RUN = True
# #
# # # createEvents()
# # # createPlaces()
# # # associateEventsPlaces()
# createAwards()
# #
#
# art = getArtistByNames(firstname="Daphné", lastname="Hérétakis", pseudo=None, listing=False)
# print('\n')
# print(art['artist'].id)



#   _____ _      ______          _   _
#  / ____| |    |  ____|   /\   | \ | |
# | |    | |    | |__     /  \  |  \| |
# | |    | |    |  __|   / /\ \ | . ` |
# | |____| |____| |____ / ____ \| |\  |
#  \_____|______|______/_/    \_\_| \_|
#
# TODO Database cleanings :
# - strip : remove leading / trailing spaces in string fields

def get_names_from_name(name) :
    """ Extract and return first and lastname from webform string """

    # Extract the uppercase string to get the lastname (TODO : should separate columns in webform)
    # List from string with space separator
    nn = [unkown for unkown in name.split(' ')]

    # Init lists
    firstname = list()
    lastname = list()

    # Set lastname when string is fully uppercased, firstname otherwise
    # strip strings as leading space may occur
    for unknown in nn :
        is_all_uppercase = [letter.isupper() for letter in unknown if letter.isalpha()]
        if all(is_all_uppercase) :
            lastname += [unknown]
        else :
            firstname += [unknown]

    # Convert lists to strings
    firstname = (" ".join(firstname)).strip()
    lastname = (" ".join(lastname)).strip()
    return firstname, lastname


import re, html
def clean_tags(html_code="") :
    """ Remove html tags from html_code and return the subsequent text"""

    if 'nan' == str(html_code) : return None

    tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')

    # Remove well-formed tags, fixing mistakes by legitimate users
    no_tags = tag_re.sub('', html_code)

    # Clean up anything else by escaping
    ready_for_web = html.escape(no_tags)

    return ready_for_web

def create_or_update(obj_type=None, properties=None, save=False) :
    """ Return an object of type obj_type populated with properties.
        If the object already exists, update it with, if not create it.

        Parameters :
        - obj_type          :    (str) type of kart obj to create
        - properties        :    (str) associated properties
        - save  (optional)  :    (str) If true, save the object in db - default : False
    """

    # -*- coding: utf-8 -*-
    try :
        obj = eval(f'{obj_type}({properties})')
        print("obj ", obj)
    except Exception as e :
        print("e" ,e)

if __name__ == "__main__" :
    run_import()

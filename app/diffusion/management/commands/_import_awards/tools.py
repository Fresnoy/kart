#! /usr/bin/env python
# -*- coding=utf8 -*-


import sys
import os
from difflib import SequenceMatcher

# import matplotlib.pyplot as plt
import pathlib
import logging
import pandas as pd
import pytz
from datetime import datetime
from django.db.utils import IntegrityError
from django_countries import countries
from django.db.models.functions import Concat, Lower
from django.db.models import CharField, Value
from django.contrib.postgres.search import TrigramSimilarity
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

import re
import unidecode

from django.apps import apps
import warnings

# Uncomment paragraph for standalone mode
import django

from production.models import Artwork, Event
from people.models import Artist
from diffusion.models import Award, MetaAward, Place

ppp = pathlib.Path(__file__).parent.parent.parent.parent.parent.absolute()
sys.path.append(str(ppp))
# Shell Plus Django Imports (uncomment to use script in standalone mode, recomment before flake8)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kart.settings")
django.setup()

# Full width print of dataframe
pd.set_option("display.expand_frame_repr", False)


# TODO: Harmonise created and read files (merge.csv, ...)
# TODO : clean examples and debug code
# TODO : logging system (debug, info ...)

DRY_RUN = False  # No save() if True
DEBUG = True

# Set file location as current working directory
OLD_CWD = os.getcwd()
os.chdir(pathlib.Path(__file__).parent.absolute())

# Create .tmp dir if needed
pathlib.Path("./.tmp").mkdir(exist_ok=True)

# Allow to lower data in query with '__lower'
CharField.register_lookup(Lower)

# Logging
logger = logging.getLogger("import_awards")
logger.setLevel(logging.DEBUG)
# clear the logs
open("awards.log", "w").close()
# create file handler which logs even debug messages
fh = logging.FileHandler("awards.log")
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter1 = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter1)
formatter2 = logging.Formatter("%(message)s")
ch.setFormatter(formatter2)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
#####

# Timezone
tz = pytz.timezone("Europe/Paris")

# Clear terminal
os.system("clear")


def dist2(item1, item2):
    """Return the distance between the 2 strings"""
    if not isinstance(item1, str) or not isinstance(item2, str):
        raise TypeError("Parameters should be str.")
    return round(SequenceMatcher(None, item1.lower(), item2.lower()).ratio(), 2)


def eventCleaning():
    """Preparation and cleannig step of the awards csv file

    WARNING: this function requires a human validation and overrides `events_title.csv` & `merge.csv`

    1) from the csv data, extract potential events already present in Kart
    2) when doubts about the name of the event, with close syntax, store the event kart_title in a csv for validation by
    head of diffusion.
    3) if no match at all, mark the event for creation
    """
    # lists to store the titles during process
    # Titles from events listed in the csv file
    csv_titles = list()
    # Titles from events in Kart
    kart_titles = list()
    # Validated titles when doubts/diff
    def_titles = list()
    # Id of existing events
    # def_ids = list()

    # Get the data from csv
    awards = pd.read_csv("awards.csv")
    # Strip all data
    awards = awards.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # We only use event titles for this phase. Drop rows with dup. titles
    aw_events = awards.drop_duplicates(["event_title"])

    # With the name/title of each event in the csv file ...
    for ind, csv_event in aw_events.iterrows():
        # ... retrieve event from Kart by title similarity and human selection of best action
        # to take (keep one or the other or create)
        csv_title = str(csv_event.event_title)
        csv_titles.append(csv_title)

        guess = (
            Event.objects.annotate(
                similarity=TrigramSimilarity("title", csv_title),
            )
            .filter(similarity__gt=0.5)
            .order_by("-similarity")
        )

        nbGuess = len(guess)

        # If no similar event found in Kart
        if nbGuess == 0:
            def_titles.append(csv_title)
            kart_titles.append("")
            continue

        else:
            go = 1
            # TODO: drop_duplicates in guess
            while go:
                identical = False
                # check for identical title in the results
                for i in range(nbGuess):
                    kart_title = guess[i].title
                    if guess[i].title == csv_title:
                        logger.info(
                            f"\n\nTitle found in Kart\nBoth titles are the same {csv_title} = {kart_title}\n"
                        )
                        def_titles.append(csv_title)
                        kart_titles.append(kart_title)
                        identical = True
                        break

                # Next event if identical was found ...
                if identical:
                    cont = "c"
                    break

                # ... otherwise, ask user what to do
                logger.info("\n\n======================================================")
                logger.info(f"CSV\t\t\t|{csv_title}|")
                for i in range(nbGuess):
                    # Distance btw the title from csv and the one found in Kart
                    dist = round(
                        SequenceMatcher(
                            None, str(guess[i].title).lower(), csv_title.lower()
                        ).ratio(),
                        2,
                    )
                    logger.info(f"({i+1}) Kart\t\t|{guess[i].title}|\t\t\t(dist:{dist})")

                cont = input(
                    """
                What should I do with the name of this event ?
                - Keep from csv (press 'c' or 'enter')
                - Use match from Kart (press '1','2',..)
                - Ignore the event: won't be processed in either way (press 'x')
                > c, 1-9, x:   """
                )

                if cont == "":
                    cont = "c"  # Default value, we keep csv

                # We keep the csv data and update Kart (TODO)
                if cont.lower() == "c":
                    def_titles.append(csv_title)
                    kart_titles.append("")
                    break

                # Ignore the event
                if cont.lower() == "x":
                    # Remove the title from the list - won't be processed
                    csv_titles.pop()
                    break

                # We keep the kart data
                try:
                    if int(cont) in range(1, nbGuess + 1):
                        cont = int(cont)
                        kart_title = guess[cont - 1].title
                        kc = input(f"Use kart title: {kart_title} ? (Y/n): ")
                        if kc != "n":
                            def_titles.append(kart_title)
                            kart_titles.append(kart_title)
                            break
                        else:
                            cont = False
                except TypeError:
                    pass

    # DF with the events names to validate
    event_df = pd.DataFrame(
        {"NomFichier": csv_titles, "NomKart": kart_titles, "NomDefinitif": def_titles}
    )

    # merge the cleaned data with awards csv
    merge_df = pd.merge(awards, event_df, how="left", left_on="event_title", right_on="NomFichier")
    # Drop duplicates
    event_df.drop_duplicates(inplace=True)

    # Export to csv
    event_df.to_csv("./.tmp/events_title.csv", index=False)
    merge_df.to_csv("./.tmp/merge.csv", index=False)


def artworkCleaning():
    """Preparation and cleannig step of the awards csv file

    WARNING: this function requires a human validation and overrides `artworks_artists.csv` & `merge.csv`

    1) from the csv data, extract potential artworks already present in Kart
    2) when doubts about the name of the artwork, with close syntax, store the artwork kart_title in a csv for
    validation by head of diffusion.
    3) if no match at all, mark the artwork for creation
    """

    aws = pd.read_csv("./.tmp/merge.csv")

    # Check if the id provided in the csv match with the artwork description
    # replace the nan with empty strings
    aws.fillna("", inplace=True)

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
            aw_kart = Artwork.objects.prefetch_related("authors__user").get(pk=aw_id)
            if dist2(aw_kart.title, aw_title) < 0.8:
                logger.warning(
                    f"""ARTWORK INTEGRITY PROBLEM:
                    Kart       :\"{aw_kart.title}\"
                    should match
                    Candidate  : \"{aw_title}\""""
                )
                aws.loc[ind, "aw_art_valid"] = False

            # Artist/author validation
            # The closest artists in Kart from the data given in CSV (listing => all matches)
            _artist_l = getArtistByNames(firstname=firstname, lastname=lastname, listing=True)

            # If no match, should create artist ?
            if not _artist_l:
                # Add the object to the list of object to create
                o2c = {
                    "type": "Artist",
                    "data": {
                        "firstname": firstname,
                        "lastname": lastname,
                    },
                }
                if o2c not in obj2create:
                    logger.warning(
                        f"No artist can be found with {firstname} {lastname}: CREATE ARTIST ?\n\n"
                    )
                    obj2create.append(o2c)
                # Create the object in Kart # TODO
                # input(f'Should I create the an artist with these data: {o2c} ')
                continue

            # Compare the artists found in CSV to the authors of the artwork in Kart
            # List of the artist that are BOTH in the authots in Kart and in the CSV
            artist_in_authors = [
                x["artist"] for x in _artist_l if x["artist"] in aw_kart.authors.all()
            ]

            # If no match between potential artists and authors: integrity issue of the csv
            if not len(artist_in_authors):
                logger.warning(
                    f"""Artist and artwork do not match ---------- SKIPPING\nArtist: {_artist_l}\n
                    Artwork: {aw_kart}\n{aw_kart.authors.all()[0].id}\n\n"""
                )
                aws.loc[ind, "aw_art_valid"] = False
                continue
            else:
                # Otherwise, the authors are validated and their id are stored in csv
                aws.loc[ind, "artist_id"] = ",".join([str(x.id) for x in artist_in_authors])
                # logger.info(f"authors {aws.loc[ind, 'artist_id']}")
                # Continue to next row
                continue

        # If no id and no title provided, skip
        if not aw_id and aw_title == "":
            logger.info(
                "No data about artwork in the csv file, only artist will be specified in the award."
            )
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
                f"{aw_title} No info about the artwork nor the artists: SKIPPING\n{aw}\n\n"
            )
            continue

        # IF NO ID ARTWORK
        # Retrieve artwork with title similarity
        getArtworkByTitle()

    aws.to_csv("./.tmp/artworks_artists.csv", index=False)


def getArtworkByTitle(aw_title):
    guessAW = (
        Artwork.objects.annotate(
            similarity=TrigramSimilarity("title", aw_title),
        )
        .filter(similarity__gt=0.7)
        .order_by("-similarity")
    )

    if guessAW:
        logger.warning(f'Potential artworks in Kart found for "{aw_title}"...')
        # Explore the potential artworks
        for gaw in guessAW:
            logger.warning(f'\t->Best guess: "{gaw.title}"')
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


def getArtistByNames(firstname="", lastname="", pseudo="", listing=False):  # TODO pseudo
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

    # If no lastname no pseudo
    if not any([lastname, pseudo]):
        logger.info(
            f"\n** getArtistByNames **\nAt least a lastname or a pseudo is required.\nAborting research. {firstname}"
        )
        return False

    # If data not string
    # print([x for x in [firstname,lastname,pseudo]])
    if not all([isinstance(x, str) for x in [firstname, lastname, pseudo]]):
        logger.info("\n** getArtistByNames **\nfirstname,lastname,pseudo must be strings")
        return False

    # List of artists that could match
    art_l = []

    # Clean names from accents to
    if lastname:
        # lastname_accent = lastname
        lastname = unidecode.unidecode(lastname).lower()
    if firstname:
        # firstname_accent = firstname
        firstname = unidecode.unidecode(firstname).lower()
    if pseudo:
        # pseudo_accent = pseudo
        pseudo = unidecode.unidecode(pseudo).lower()
    fullname = f"{firstname} {lastname}"

    # Cache
    fullkey = f"{firstname} {lastname} {pseudo}"
    try:
        # logger.warning("cache", search_cache[fullkey])
        return search_cache[fullkey] if listing else search_cache[fullkey][0]
    except KeyError:
        pass

    # SEARCH WITH LASTNAME then FIRSTNAME
    # First filter by lastname similarity
    guessArtLN = (
        Artist.objects.prefetch_related("user")
        .annotate(
            # Concat the full name "first last" to detect misclassifications like: "Hee Won -- Lee"
            # where Hee Won is first
            # name but can be stored as "Hee  -- Won Lee"
            search_name=Concat(
                "user__first_name__unaccent__lower",
                Value(" "),
                "user__last_name__unaccent__lower",
            )
        )
        .annotate(
            similarity=TrigramSimilarity("search_name", fullname),
        )
        .filter(similarity__gt=0.3)
        .order_by("-similarity")
    )

    # Refine results
    if guessArtLN:
        # TODO: Optimize by checking a same artist does not get tested several times
        for artist_kart in guessArtLN:

            # Clear accents (store a version with accents for further accents issue detection)
            kart_lastname_accent = artist_kart.user.last_name
            kart_lastname = unidecode.unidecode(kart_lastname_accent).lower()
            kart_firstname_accent = artist_kart.user.first_name
            kart_firstname = unidecode.unidecode(kart_firstname_accent).lower()
            # kart_fullname_accent = artist_kart.search_name
            kart_fullname = f"{kart_firstname} {kart_lastname}".lower()

            dist_full = dist2(kart_fullname, fullname)

            # logger.warning('match ',kart_fullname , dist2(kart_fullname,fullname), fullname,kart_fullname == fullname)
            # In case of perfect match ...
            if dist_full > 0.9:
                if kart_fullname == fullname:
                    # store the artist in potential matches with extreme probability (2)
                    # and continue with next candidate
                    art_l.append({"artist": artist_kart, "dist": 2})
                    continue
                # Check if Kart and candidate names are exactly the same
                elif kart_lastname != lastname or kart_firstname != firstname:

                    logger.warning(
                        f"""Fullnames globally match {fullname} but not in first and last name correspondences:
                    Kart       first: {kart_firstname} last: {kart_lastname}
                    candidate  first: {firstname} last: {lastname}
                                            """
                    )
                    art_l.append({"artist": artist_kart, "dist": dist_full * 2})
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
                if dist2(kart_lastname.replace(" ", ""), lastname.replace(" ", "")) < 0.9:
                    bef = f'"{kart_lastname}" <> "{lastname}"'
                    logger.warning(f"whitespace problem ? {bef}")

            if kart_firstname.find(" ") >= 0 or firstname.find(" ") >= 0:
                # Check distance btw firstnames without spaces
                if dist2(kart_firstname.replace(" ", ""), firstname.replace(" ", "")) < 0.9:
                    bef = f'"{kart_firstname}" <> "{firstname}"'
                    logger.warning(f"whitespace problem ? {bef}")
            ###

            # Artists whose lastname is the candidate's with similar firstname

            # Distance btw the lastnames
            dist_lastname = dist2(kart_lastname, lastname)

            # try to find by similarity with firstname
            guessArtFN = (
                Artist.objects.prefetch_related("user")
                .annotate(
                    similarity=TrigramSimilarity("user__first_name__unaccent", firstname),
                )
                .filter(user__last_name=lastname, similarity__gt=0.8)
                .order_by("-similarity")
            )

            # if artist whose lastname is the candidate's with similar firstname names are found
            if guessArtFN:

                # Check artists with same lastname than candidate and approaching firstname
                for artistfn_kart in guessArtFN:
                    kart_firstname = unidecode.unidecode(artistfn_kart.user.first_name)
                    # Dist btw candidate firstname and a similar found in Kart
                    dist_firstname = dist2(f"{kart_firstname}", f"{firstname}")
                    # Add the candidate in potential matches add sum the distances last and firstname
                    art_l.append(
                        {
                            "artist": artistfn_kart,
                            "dist": dist_firstname + dist_lastname,
                        }
                    )

                    # Distance evaluation with both first and last name at the same time
                    dist_name = dist2(
                        f"{kart_firstname} {kart_lastname}", f"{firstname} {lastname}"
                    )
                    # Add the candidate in potential matches add double the name_dist (to score on 2)
                    art_l.append({"artist": artistfn_kart, "dist": dist_name * 2})

            else:
                # If no close firstname found, store with the sole dist_lastname (unlikely candidate)
                art_l.append({"artist": artist_kart, "dist": dist_lastname})

        # Take the highest distance score
        art_l.sort(key=lambda i: i["dist"], reverse=True)

        # Return all results if listing is true, return the max otherwise
        if listing:
            search_cache[fullkey] = art_l
            return art_l
        else:
            search_cache[fullkey] = [art_l[0]]
            return art_l[0]
    else:
        # research failed
        search_cache[fullkey] = False

        return False
    #####


def infoCSVeventTitles():
    """Display info about potentialy existing events in Kart

    Check if event names exist with a different case in Kart and display warning
    """
    eventsToCreate = pd.read_csv("./.tmp/events_title.csv")

    for evt_title in eventsToCreate.NomFichier:
        # If a title already exist with different case
        exact = Event.objects.filter(title__iexact=evt_title)
        if exact:
            logger.warning(
                f"Event already exist with same name (but not same case) for {evt_title}:\n{exact}\n"
            )

        # If a title already contains with different case
        contains = Event.objects.filter(title__icontains=evt_title)
        if contains:
            logger.warning(
                f"Event already exist with very approaching name (but not same case) for {evt_title}:\n{contains}\n"
            )


def createEvents(events_df=None, title_key="event_title"):
    """Create (in Kart) the events listed in awards csv file

    1) Retrieve the data about the events listed in awards csv file
    2) Parse those data and prepare if for Event creation
    3) (optional) Check if meta event exits for the created event, creates it if needed
    """

    # Get the events from awards csv extended with title cleaning (merge.csv)
    if events_df is None:
        events_df = pd.read_csv("./.tmp/merge.csv")

    # Create/get the events in Kart
    for ind, event in events_df.iterrows():
        if title_key is None:
            title = event.NomDefinitif
        else:
            title = event[title_key]

        # Starting dates are used only for the year info (default 01.01.XXX)
        starting_date = event.event_year
        # Convert the year to date
        starting_date = datetime.strptime(str(starting_date), "%Y")
        starting_date = pytz.timezone("Europe/Paris").localize(starting_date)

        # All events are associated with type festival
        # TODO: Add other choices to event ? Delete choices constraint ?
        type = "FEST"

        # If no title is defined, skip the event
        if str(title) in ["nan", ""]:
            continue

        # Check if meta event exists, if not, creates it
        evt = Event.objects.filter(title=title, type=type, main_event=True)
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
                main_event=True,
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
            starting_date=starting_date,
        )

        if len(evt):
            # Arbitrarily use the first event of the queryset
            evt = evt[0]
            created = False
        else:
            logger.info("obj is getting created")
            evt = Event(title=title, type=type, starting_date=starting_date)
            if not DRY_RUN:
                evt.save()
            created = True

        if created:
            logger.info(f"{title} was created")
        else:
            logger.info(f"{title} was already in Kart")
        # Store the ids of newly created/already existing events in a csv
        events_df.loc[ind, "event_id"] = evt.id
    events_df.to_csv("./.tmp/events.csv", index=False)


def getISOname(countryName=None, simili=False):
    """Return the ISO3166 international value of `countryName`

    Parameters:
    - countryName  : (str) The name of a country
    - simili         : (bool) If True (default:False), use similarity to compare the names
    """
    # Process the US case (happens often!)
    if re.search("[EeéÉ]tats[ ]?-?[ ]?[Uu]nis", countryName):
        return "US"
    # Kosovo is not liste in django countries (2020)
    if re.search("kosovo", countryName, re.IGNORECASE):
        return "XK"

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
            if dist >= 0.95:
                matchCodes.append({"dist": dist, "code": code})  # 1 ponctuation diff leads to .88
            if dist >= 0.85:
                cn1 = unidecode.unidecode(str(countryName))
                cn2 = unidecode.unidecode(name)
                dist2 = SequenceMatcher(None, cn1.lower(), cn2.lower()).ratio()
                if dist2 > dist:
                    logger.info(
                        f"""------------------- ACCENTUATION DIFF {countryName} vs {name}\n
                        Accents removed: {cn1} vs {cn2}: {dist2}"""
                    )
                    # 1 ponctuation diff leads to .88
                    matchCodes.append({"dist": dist2, "code": code})
                else:
                    if DEBUG:
                        return code
                    cont = input(
                        f"""
                                 NOT FOUND but {countryName} has a close match with {name}
                                 Should I keep it ? (Y/n):   """
                    )
                    if re.search("NO?", cont, re.IGNORECASE):
                        continue
                    else:
                        return code

    # Sort the matches by similarity
    sorted(matchCodes, key=lambda i: i["dist"])
    try:
        # Return the code with the highest score
        return matchCodes[0]["code"]
    except IndexError:
        return False


def createPlaces(source_df=None):
    """Create the places listed in the awards csv files"""

    if source_df is None:
        # Get the data from awards csv extended with title cleaning and events (merge.csv)
        source_df = pd.read_csv("./.tmp/events.csv")

    # Drop duplicates
    places = source_df.drop_duplicates(["place_city", "place_country"])
    # Remove rows with full empty location
    places = places.dropna(subset=["place_city", "place_country"], how="all")
    # Replace NA/NaN (similarity fails otherwise)
    places.fillna("", inplace=True)

    for ind, place in places.iterrows():
        city = place.place_city
        country = place.place_country
        if city == country == "":
            continue
        logger.info(f"\n\nPLACE: {city} - {country}")

        # Processing CITY
        # Look for really approaching (simi=.9) name of city in Kart
        guessCity = (
            Place.objects.annotate(
                similarity=TrigramSimilarity("name", city),
            )
            .filter(similarity__gt=0.9)
            .order_by("-similarity")
        )

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
            dist = round(
                SequenceMatcher(None, str(country).lower(), countryNameKart.lower()).ratio(),
                2,
            )

            # If really close, keep the Kart version
            if dist > 0.9:
                logger.info(f"Really close name, replacing {country} by {countryNameKart}")
                codeCountryCSV = codeCountryKart
            else:
                # Process the us case (happens often!)
                if re.search("[EeéÉ]tats[ ]?-?[ ]?[Uu]nis", country):
                    codeCountryCSV = "US"
                else:  # If not close to the Kart version, try with similarity with other countries
                    codeCountryCSV = getISOname(country, simili=True)

        else:  # No city found, so no clue to find the country => full search
            # parameter simili=True triggers a search by similarity btw `country` and django countries entries
            codeCountryCSV = getISOname(country, simili=True)
            if codeCountryCSV:
                logger.info(
                    f"Looked for the country code of {country} and obtained {codeCountryCSV}"
                )
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
            country=codeCountryCSV if codeCountryCSV else "",
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
                country=codeCountryCSV if codeCountryCSV else "",
            )
            if not DRY_RUN:
                place_obj.save()
            created = True
        if place.place_city == "":
            logger.info(f"Empty City ============== {place_obj}")

        if created:
            logger.info(f"Place {place_obj} was created")
        else:
            logger.info(f"Place {place_obj} was already in Kart")
        # Store the id of the place
        places.loc[ind, "place_id"] = place_obj.id

    # Store the places
    places.to_csv("./.tmp/places.csv", index=False)

    # test to deal with city only rows, use "NULL" to allow the merging with missing data
    places.loc[places["place_city"] == "", "place_city"] = "**NULL**"
    source_df.loc[source_df["place_city"].isna(), "place_city"] = "**NULL**"

    merge_df = pd.merge(
        source_df,
        places[["place_city", "place_country", "place_id"]],
        how="left",
        on=["place_city", "place_country"],
    )
    # Restore the missing data after the merge
    merge_df.loc[merge_df["place_city"] == "**NULL**", "place_city"] = ""
    merge_df.to_csv("./.tmp/merge_events_places.csv", index=False)


# TODO: Fill artwork in the event


def associateEventsPlaces():
    """Fill the place field of created events with the created places"""

    # Get the events and places csv
    evt_places = pd.read_csv("./.tmp/merge_events_places.csv")

    # Update the events with the place
    for ind, award in evt_places.iterrows():
        if str(award.event_id) != "nan":
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
        else:
            logger.warning(f"no event associated with {award.meta_award_label}")


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
        return (False,)


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


def createAwards(awards_df=None):
    """Create the awards listed in csv in Kart"""
    print("Create AWARDS")

    if awards_df is None:
        # Load the events associated to places and artworks (generated by createPlaces())
        awards_df = pd.read_csv("./.tmp/merge_events_places.csv")

    awards_df.fillna("", inplace=True)

    # Filter for bugs
    bugs_df = awards_df.loc[awards_df["bug"] != "", :]
    bugs_df.to_csv("./.tmp/bugs.csv")

    awards_df = awards_df.loc[awards_df["bug"] == "", :]

    # Filter for artwork missing
    no_artw_df = awards_df.loc[awards_df["artwork"] == "", :]
    no_artw_df.to_csv("./.tmp/no-artwork.csv")

    awards_df = awards_df.loc[awards_df["artwork"] != "", :]

    # Check for required cols
    # print("awards_df.columns", awards_df.columns)

    # Pattern to unparse artw code
    code_pat = re.compile(r"code:(\d*)$")

    for ind, row in awards_df.iterrows():
        # init
        code = False

        # Retrieve artwork string e.g. Under construction film de Zhenchen Liu |code:212
        artw_str = row["artwork"]
        # Extract code
        search_code = re.search(code_pat, artw_str)
        if search_code:
            code = int(search_code.group(1))

        if code:
            artw, filt = safeGet(Artwork, pk=code)
            awards_df.loc[ind, "artwork_id"] = code

            authors = artw.authors.all()

            # Generate a string of ids separated by commas
            author_ids = ",".join([str(author.id) for author in authors])
            awards_df.loc[ind, "authors"] = author_ids

    for ind, award in awards_df.iterrows():
        # init
        artwork_id = artist = False

        if award.event_id == "":
            logger.warning(f"award.event_id empty {award.artwork}")
            continue

        label = award.meta_award_label
        event_id = int(award.event_id)

        # An artwork id is required to create the award
        if award.artwork_id:
            artwork_id = int(award.artwork_id)
        else:
            logger.warning(f"No idartwork for {award.artwork_title}")
            continue

        # List of authors obj
        authors_l = []

        # La liste des ids des auteurs awardés
        authors_id_l = award.authors.split(",")

        # authors is a list of ids 123,342
        for author_id in authors_id_l:
            artist = Artist.objects.get(pk=int(author_id))
            authors_l += [artist]

        if len(authors_l) > 1:
            print("ARTISTS ", authors_l)

        # try:
        #     print("award.artist_id",int(award.artist_id))
        # except ValueError:
        #     print("------------------>", award.artist_id)
        note = award.meta_award_label_details

        description = award.meta_award_label_details
        if pd.isna(award.meta_award_label_details):
            description = ""

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
                type="INDIVIDUAL",  # indivudal by default, no related info in csv
            )
            # print(f"MetaAward : label {maward.label}, event {mevent}, description {description}")

            if not DRY_RUN:
                maward.save()
            logger.info(f'"{maward}" created ')

        # GET OR CREATE THE AWARDS
        new_aw, filt = safeGet(
            Award,
            meta_award=maward.id,
            artwork=artwork_id,
            event=event.id,
            # artists = artist_id
        )

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
            new_aw = Award(meta_award=maward, event=event, date=event.starting_date, note=note)
            try:
                if not DRY_RUN:
                    new_aw.save()
                    new_aw.artwork.add(artwork_id)
                    new_aw.save()
                    print(f"not DRY_RUN ::: {new_aw}  created")
            except ValueError:
                logger.warning(f"Artist_id: {artist} caused an IntegrityError")

            logger.info(f'"{new_aw}" created ')


def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return f"...{args[1][-50:]} line {args[2]} - warning : {str(msg)} \n"


warnings.formatwarning = custom_formatwarning


def summary(restrict=None):
    """Return general description and statistics about the current database

    Params
    restrict(list): List of models that will be considered in the summary. If empty (default), all models are included.
    """

    # Get the all the current models
    mods = apps.get_models()

    # Dict to hold summary data
    summary_d = {}

    # Iterate through models ...
    for m in mods:
        # .. to populate the summary dict if models is in restrict list
        # or no restriction required
        if (restrict and (m.__name__ in restrict)) or not restrict:
            summary_d[f"{m._meta.app_label}.{m.__name__}"] = m._default_manager.count()

    # Return the summary dict
    return summary_d


def compareSummaries(sum1=None, sum2=None, restrict=None, force_display=False):
    """Compare 2 summaries and expose counting differences

    params :
    - sum1(dict) : a summary generated by the summary function
    - sum2(dict) : a summary generated by the summary function
    - restrict(list) : list of models that will be compared
    - force_display(bool) : force the display of result even if no differences spotted

    Examples :
    # Ask for full summary
    sum1 = summary()
    # Restrict summary to some models
    # sum1 = summary(['Student','Diffusion'])
    sum2 = summary()
    compareSummaries(sum1)
    """

    if not sum1 or not sum2 or type(sum1) is not dict or type(sum2) is not dict:
        raise TypeError("compareSummaries requires 2 dict as arguments")

    sum1 = {key: value for key, value in sorted(sum1.items())}
    sum2 = {key: value for key, value in sorted(sum2.items())}

    # The dict holding counting differences
    diff_d = {}

    # fake a difference for debug purposes
    fakediff = force_display

    # Try to globally compare dictionnaries
    # if sum1 == sum2:
    #     warnings.warn("Summaries are identical.")

    # Iterate models and countings
    for k, v in sum1.items():

        # If the model is not in both summaries, no comp is possible
        if k not in sum2.keys():
            warnings.warn(f"Model {k} not in both summaries")
            continue

        # Diff btw before and after countings
        diff = sum2[k] - v

        # If diff and model is in the restricted list, show it
        if fakediff or (
            diff and ((restrict and (k in restrict and k in sum2.keys())) or not restrict)
        ):

            sign = "-" if diff < 0 else "+"
            print(f"{k} model count was {v}, is now {sum2[k]} ({sign} {diff})")
            diff_d[k] = f"{sign} {diff}"

    if diff_d == {}:
        diff_d = "No difference"

    return diff_d


def geoloc_all_cities(save=False, debug=False):
    """
    Geolocate the cities of Kart's places

    From
    """
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter

    geolocator = Nominatim(user_agent="Kart_location")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)

    # List cities and store their geolocalisation coordinates
    for place in Place.objects.all():

        # Get the city
        city = place.city

        # Get the country
        country = place.country

        if city:
            if debug:
                print(city)
            # if the place has no lat or long
            if not (place.latitude and place.longitude):

                if country:
                    search_request = f"{city}, {country}"
                else:
                    search_request = city
                # Call to geocode api
                try:
                    print("searching for ", search_request)
                    location = geocode(search_request)
                except Exception as e:
                    print(" --- ERROR --- UNKNOWN CITY : ", city, str(e))
                    continue
                # If a location is found, fill the missing data
                if location:
                    if not place.latitude:
                        place.latitude = location.latitude
                    if not place.longitude:
                        place.longitude = location.longitude

                    # Save the Place in Kart
                    if save:
                        print(
                            "Saving place : ",
                            place.city,
                            place.latitude,
                            place.longitude,
                        )
                        place.save()
                else:
                    print("---------------- Location unknown : ", city)


if __name__ == "__main__":
    pass

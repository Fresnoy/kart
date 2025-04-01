from django.contrib.postgres.search import TrigramSimilarity
import os
import unidecode

# Load user model
from django.db.models.functions import Lower
from django.db.models import CharField

# Import our models
from people.models import Artist
import logging
import pytz

from people.utils.user_tools import getUserByNames
from utils.kart_tools import dist2


# Logging
logger = logging.getLogger('artist_utils')
logger.setLevel(logging.DEBUG)
#####

# Timezone
tz = pytz.timezone('Europe/Paris')

# Clear terminal
os.system('clear')

search_cache = {}


# Allow to lower data in query with '__lower'
CharField.register_lookup(Lower)


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
    if not all([type(x) is str for x in [firstname, lastname, pseudo]]):
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
        pseudo = unidecode.unidecode(pseudo).lower().strip()
    # fullname = f"{firstname} {lastname}"

    # Cache
    fullkey = f'{firstname} {lastname} {pseudo}'
    try:
        # logger.warning("cache", search_cache[fullkey])
        return search_cache[fullkey] if listing else search_cache[fullkey][0]
    except Exception:
        pass

    # SEARCH WITH LASTNAME then FIRSTNAME
    users = getUserByNames(firstname, lastname, listing)
    if users and users['user'] and users['user'].artist_set.count() > 0:
        # only one
        users['artist'] = users['user'].artist_set.first()
        art_l.append(users)
    if users and listing and len(users) > 0:
        # add ArtistObj in array
        for k, u in enumerate(users):
            if u['user'] and u['user'].artist_set:
                u['artist'] = u['user'].artist_set.first()

                art_l.append(u)

    # PSEUDO
    if pseudo:
        guessArtNN = (
            Artist.objects.annotate(
                similarity_pseudo=TrigramSimilarity('nickname__unaccent__lower', pseudo),
            )
            .filter(similarity_pseudo__gt=0.3)
            .order_by('-similarity_pseudo')
        )

        if guessArtNN:
            for artist_kart in guessArtNN:
                kart_nickname_accent = artist_kart.nickname
                kart_nickname = unidecode.unidecode(kart_nickname_accent).lower().strip()

                dist_full = dist2(kart_nickname, pseudo)

                # In case of perfect match ...
                if dist_full > 0.9:
                    if kart_nickname == pseudo:
                        # store the artist in potential matches with extreme probability (2)
                        # and continue with next candidate
                        art_l.append({"artist": artist_kart, 'dist': 2})
                        continue
                    else:
                        art_l.append({"artist": artist_kart, 'dist': dist_full})
                else:
                    logger.warning(
                        f"""Pseudo globally match {pseudo} but not in pseudo correspondences:
                    Kart pseudo: {kart_nickname} : {pseudo}"""
                    )
                    # art_l.append({"artist": artist_kart, 'dist': dist_full})

    if art_l:
        # Take the highest distance score
        art_l.sort(key=lambda i: i['dist'], reverse=True)

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

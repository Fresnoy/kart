import unidecode
from django.contrib.auth.models import User

from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.postgres.lookups import Unaccent

from django.db.models.functions import Concat, Lower
from django.db.models import CharField, Value

from utils.kart_tools import dist2

import logging

# Logging
logger = logging.getLogger('artist_utils')
logger.setLevel(logging.DEBUG)
#####

# Allow to lower data in query with '__lower'
CharField.register_lookup(Lower)
CharField.register_lookup(Unaccent)


def getUserByNames(firstname="", lastname="", listing=False, dist_min=False):
    """Retrieve the closest user from the first and last names given

    Parameters:
    - firstname: (str) Firstname to look for
    - lastname : (str) Lastname to look for
    - listing  : (bool) If True, return a list of matching artists (Default, return the closest)
    - dist_min : (float) Maximum dist, return False if strinctly under

    Return:
    - userObj    : (Django obj / bool) The closest user object found in Kart. False if no match.
    - dist         : (float) Distance with the given names
    """

    # If no lastname
    if not any(
        [
            lastname,
        ]
    ):
        logger.info(f"\n** getUserByNames **\nAt least a lastname is required.\nAborting research. {firstname}")
        return False

    # If data not string
    if not all([type(x) is str for x in [firstname, lastname]]):
        logger.info("\n** getUserByNames **\nfirstname,lastname must be strings")
        return False

    # List of users that could match
    users_l = []

    # Clean names from accents to
    if lastname:
        # lastname_accent = lastname
        lastname = unidecode.unidecode(lastname).lower().strip()
    if firstname:
        # firstname_accent = firstname
        firstname = unidecode.unidecode(firstname).lower().strip()

    fullname = f"{firstname} {lastname}"

    # Cache
    # fullkey = f'{firstname} {lastname}'

    # First filter by lastname similarity
    guessArtLN = (
        User.objects.annotate(
            # Concat the full name "first last" to detect misclassifications like: "Hee Won -- Lee"
            # where Hee Won is first
            # name but can be stored as "Hee  -- Won Lee"
            search_name=Concat('first_name__unaccent__lower', Value(' '), 'last_name__unaccent__lower')
        )
        .annotate(
            similarity=TrigramSimilarity('search_name', fullname),
        )
        .filter(similarity__gt=0.3)
        .order_by('-similarity')
    )

    # Refine results
    if guessArtLN:
        # TODO: Optimize by checking a same artist does not get tested several times
        for user_kart in guessArtLN:

            # Clear accents (store a version with accents for further accents issue detection)
            kart_lastname_accent = user_kart.last_name
            kart_lastname = unidecode.unidecode(kart_lastname_accent).lower().strip()
            # print("kart_lastname_accent", kart_lastname_accent,"kart_lastname", kart_lastname)
            kart_firstname_accent = user_kart.first_name
            kart_firstname = unidecode.unidecode(kart_firstname_accent).lower().strip()

            # kart_fullname_accent = user_kart.search_name

            # Stripping issues
            # kart_data = {
            #     'cleaned': {'lastname': kart_lastname, 'firstname': kart_firstname},
            #     'raw': {'lastname': kart_lastname_accent, 'firstname': kart_firstname_accent},
            # }

            kart_fullname = f"{kart_firstname} {kart_lastname}".lower()

            dist_full = dist2(kart_fullname, fullname)

            # logger.warning('match ',kart_fullname , dist2(kart_fullname,fullname), fullname,kart_fullname == fullname)
            # In case of perfect match ...
            if dist_full > 0.9:
                if kart_fullname == fullname:
                    # store the artist in potential matches with extreme probability (2)
                    # and continue with next candidate
                    users_l.append({"user": user_kart, 'dist': 2})
                    continue
                # Check if Kart and candidate names are exactly the same
                elif kart_lastname != lastname or kart_firstname != firstname:

                    logger.warning(
                        f"""Fullnames globally match {fullname} but not in first and last name correspondences:
                    Kart       first: >{kart_firstname}< last: >{kart_lastname}<
                    candidate  first: >{firstname}< last: >{lastname}<
                                            """
                    )
                    users_l.append({"user": user_kart, 'dist': dist_full})

                    # ### Control for accents TODO still necessary ?
                    #
                    # accent_diff = kart_lastname_accent != lastname_accent or \
                    #               kart_firstname_accent != firstname_accent
                    # if accent_diff: logger.warning(f"""\
                    #                 Accent or space problem ?
                    #                 Kart: {kart_firstname_accent} {kart_lastname_accent}
                    #                 Candidate: {firstname_accent} {lastname_accent} """)

            # Control for blank spaces

            if kart_lastname.startswith(" ") or kart_lastname.endswith(" "):
                print(f"before : kart_lastname.strip() >{kart_lastname}<")
                print(f"kart_lastname.strip() >{kart_lastname.strip()}<")
                print(f"after : kart_lastname.strip() >{kart_lastname}<")

            if lastname.startswith(" ") or lastname.endswith(" "):
                print(f"before : lastname.strip() >{lastname}<")
                print(f"lastname.strip() >{lastname.strip()}<")
                print(f"after : lastname.strip() >{lastname}<")
                # Check for leading/trailing whitespace in lastname
                if kart_lastname.strip() == lastname.strip():
                    if kart_lastname.find(" ") >= 0:
                        # cor = Correction(kart_lastname,kart_lastname.strip())
                        pass
                    bef = f"\"{kart_lastname}\" <> \"{lastname}\""
                    logger.warning(f"Leading/trailing whitespace {bef}")

                # Check distance btw lastnames without spaces
                elif dist2(kart_lastname.replace(" ", ""), lastname.replace(" ", "")) > 0.9:
                    bef = f"\"{kart_lastname}\" <> \"{lastname}\""
                    logger.warning(f"whitespace problem ? {bef}")

            if kart_firstname.find(" ") >= 0 or firstname.find(" ") >= 0:

                if kart_firstname.strip() == firstname.strip():
                    bef = f"\"{kart_firstname}\" <> \"{firstname}\""
                    logger.warning(f"Leading/trailing whitespace {bef}")

                # Check distance btw firstnames without spaces
                elif dist2(kart_firstname.replace(" ", ""), firstname.replace(" ", "")) > 0.9:
                    bef = f"\"{kart_firstname}\" <> \"{firstname}\""
                    logger.warning(f"whitespace problem ? {bef}")
                    users_l.append({"user": user_kart, 'dist': dist_full})
            ###

            # Artists whose lastname is the candidate's with similar firstname

            # Distance btw the lastnames
            dist_lastname = dist2(kart_lastname, lastname)

            # # try to find by similarity with firstname
            # guessArtFN = Artist.objects.prefetch_related('user').annotate(
            #     similarity=TrigramSimilarity('user__first_name__unaccent', firstname),
            # ).filter(user__last_name=lastname, similarity__gt=0.8).order_by('-similarity')

            guessUserFN = (
                User.objects.annotate(
                    similarity=TrigramSimilarity('first_name__unaccent', firstname),
                )
                .filter(last_name=lastname, similarity__gt=0.8)
                .order_by('-similarity')
            )

            # if user whose lastname is the candidate's with similar firstname names are found
            if guessUserFN:

                # Check users with same lastname than candidate and approaching firstname
                for userfn_kart in guessUserFN:
                    kart_firstname = unidecode.unidecode(userfn_kart.first_name)
                    # Dist btw candidate firstname and a similar found in Kart
                    dist_firstname = dist2(f"{kart_firstname}", f"{firstname}")
                    # Add the candidate in potential matches add sum the distances last and firstname
                    users_l.append({"user": userfn_kart, 'dist': dist_firstname + dist_lastname})

                    # Distance evaluation with both first and last name at the same time
                    dist_name = dist2(f"{kart_firstname} {kart_lastname}", f"{firstname} {lastname}")
                    # Add the candidate in potential matches add double the name_dist (to score on 2)
                    users_l.append({"user": userfn_kart, 'dist': dist_name * 2})

            else:
                # If no close firstname found, store with the sole dist_lastname (unlikely candidate)
                users_l.append({"user": user_kart, 'dist': dist_lastname})

            # ## end for user_kart in guessArtLN

        # Take the highest distance score
        users_l.sort(key=lambda i: i['dist'], reverse=True)

        # Return all results if listing is true, return the max otherwise
        if listing:
            return users_l
        else:
            # Return the result if dist_min is respected (if required)
            if (dist_min is not False and users_l[0]['dist'] > dist_min) or (not dist_min):
                return users_l[0]
            else:
                return False
    else:
        # research failed
        return False
    #####

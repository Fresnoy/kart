#! /usr/bin/env python
"""
Kart Tools
----------

Functions dedicated to Kart creation, modification of content

"""
import re
import unidecode

from difflib import SequenceMatcher

import logging

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from django.contrib.auth.models import User


# Logging
logger = logging.getLogger('artist_utils')
logger.setLevel(logging.DEBUG)
#####


def usernamize(fn="", ln="", check_duplicate=False):
    """Return a username from first and lastname.

    params:
    fn              : (str) Firstname
    ln              : (str) Lastname
    check_duplicate : (boo) If true, verify if username do not already exist in db,
                     increment suffix if needed (default=False).

    e.g. :
    fn = "Andy"
    ln = "Wharol"
    computed username : "awarhol"
    if awarhol already taken, compute "awarhol2", if "awarhol2" exists, compute "awarhol3" and so on ...
    """

    # Check if multipart firstname
    fn_l = re.split(r'\W+', fn)

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

    if check_duplicate:
        # Check if username is already taken, add 2, 3, 4 ... until its unique
        # Init suffix
        i = 2
        while objExist(User, default_index=None, username=username):
            username = usernamize(fn, ln) + f"{i}"
            i += 1

    return username


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


def dist2(item1, item2):
    """Return the distance between the 2 strings"""
    if not type(item1) == type(item2) == str:
        raise TypeError("Parameters should be str.")
    return round(SequenceMatcher(None, item1.lower(), item2.lower()).ratio(), 2)

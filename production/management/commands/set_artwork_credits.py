# -*- encoding: utf-8 -*-
import os
import re
import sys

from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

from production.models import Artwork, ProductionStaffTask, StaffTask, Staff

from people.utils.user_tools import getUserByNames
from people.utils.artist_tools import getArtistByNames

from utils.kart_tools import usernamize
from production.management.commands.import_catalog import getOrCreateMultiInstancesByStr


stats = {}


class Command(BaseCommand):
    help = 'Set credits for artwork step by step, no argument'

    def handle(self, *args, **options):

        # Clear terminal
        if '--test-mode' not in sys.argv:
            os.system('clear')

        init()


def init():
    print(
        """Coller le texte des crédits de la forme (multiligne) :
             user : task
             user et user et ... : task
             user : task , task, ...
             user , user, ... : task et task et ...
             ...
             ***et OU "," SONT ACCEPTÉS***
          """
    )
    # Get credits
    credits_text = multiline_input()
    # Get artwork
    artwork = searchArtwork()

    # collaborators -> credits
    setArtworkCredits(artwork, credits_text)

    print("\n".join([str(pst.staff) + " : " + str(pst.task) for pst in artwork.staff_tasks.all()]))

    print("FIN")
    print("---")

    exit = input("Créer une autre  ? y/n")
    if "n" in exit:
        os._exit(0)
    init()


def searchArtwork():

    artwork_str = input("L'œuvre : ")
    artwork_search = Artwork.objects.filter(title__icontains=artwork_str)
    artwork = input_choices(artwork_search)

    if not artwork:
        print("Aucune œuvre trouvée, veuiller retenter votre recherche ")
        return searchArtwork()

    print(artwork)
    return artwork


def setArtworkCredits(aw, credits):

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


def input_choices(values):
    """
    Prompts the user to select a value from a list of choices.

    Args:
        values: A list of values to choose from.

    Returns:
        The selected value, or False if no valid choice was made.
    """

    if not values:
        return False

    print("Plusieurs valeurs sont possibles, selectionnez-en une :")
    for id, value in enumerate(values):
        print("{} : {}".format(id, value))

    select = int(input("Votre choix : "))

    try:
        select_int = int(select)
        selected = values[select_int]
        return selected
    except Exception as e:
        print("Choix invalide", e)
        return False


#
def get_first_last_name_from_str(str):
    str = str.strip()
    if " " in str:
        str_split = str.split(" ", 1)
        first_name = str_split[0]
        last_name = str_split[1]

        return [first_name, last_name]
    return ["", str]


#


def get_or_create_user(user_str):
    # search user from usersearchutils
    # return user

    first_name, last_name = get_first_last_name_from_str(user_str)
    print("firsname:" + first_name)
    print("lastname:" + last_name)

    user = False
    user_search = False
    created = False
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
        task_query = StaffTask.objects.filter(label__icontains=task_str)
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


def multiline_input():
    print("Enter/Paste your content. End input with an empty line.")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)


def setStats(value_from_model, created):
    class_name = value_from_model.__class__.__name__.lower()
    attibute = class_name + "_created" if created else class_name + "_reused"
    if attibute not in stats:
        stats[attibute] = []
    stats[attibute].append(value_from_model)

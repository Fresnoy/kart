# -*- encoding: utf-8 -*-
import os

from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

from production.models import Artwork, ProductionStaffTask, StaffTask, Staff

from people.utils.user_tools import getUserByNames
from people.utils.artist_tools import getArtistByNames

from utils.kart_tools import usernamize


# Clear terminal
os.system('clear')

stats = {}


class Command(BaseCommand):
    help = 'Set credits for artwork step by step, no argument'

    def handle(self, *args, **options):

        init()


def init():

    # Clear terminal
    os.system('clear')

    print("""Coller le texte des crédits de la forme (multiligne) :
             user : task
             user et user et ... : task
             user : task , task, ...
             user , user, ... : task et task et ...
             ...
             ***et OU "," SONT ACCEPTÉS***
          """)
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

        # SEARCH FOR USER
        user_str = credit.split(":")[0].strip()
        print("SEARCH FOR USER : " + user_str)
        users = []
        user = False
        # "," in name mean that this is an human in DB (comme with catalog plateform dev)
        # but mean sometimes two person for the same task Nina Guseva, Anna Collard : céramiste
        # OR Nina Guseva et Anna Collard
        if "," in user_str or " et " in user_str:
            str_split = user_str.split(",") if "," in user_str else user_str.split(" et ")
            first_user = str_split[0].strip()
            # is multi ? il y a un espace (nom prénom) et c'est assez long
            if (" " in first_user and len(first_user) > 3):
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
        task_str = credit.split(":")[1].strip()
        # sometimes Benjamin Griere : Graphisme 3D, Développeur 3D
        tasks = getOrCreateMultiInstancesByStr(StaffTask, 'label', task_str)

        # HAVE TO
        # ONE user ONE task
        # One user Multi tasks
        # Multi users One task
        # Multi user multi task -> problem
        if (len(staffs) == 0 or
            len(tasks) == 0 or
                (len(staffs) > 1 and len(tasks) > 1)):
            print("Multi user multi task : " + credit)
            for staff in staffs:
                for task in tasks:
                    pst, created = ProductionStaffTask.objects.get_or_create(staff=staff, task=task, production=aw)
                    setStats(pst, created)
                    print(pst)
                    print(task, staff)

            continue
        elif len(staffs) == 1 and len(tasks) == 1:
            print("One user One task : " + credit)
            staff = staffs[0]
            task = tasks[0]
            pst, created = ProductionStaffTask.objects.get_or_create(staff=staff, task=task, production=aw)
            setStats(pst, created)
            print(pst)

        elif len(staffs) > 1 and len(tasks) == 1:
            print("Multi user One task : " + credit)
            task = tasks[0]
            for staff in staffs:
                pst, created = ProductionStaffTask.objects.get_or_create(staff=staff, task=task, production=aw)
                setStats(pst, created)
                print(pst)

        elif len(staffs) == 1 and len(tasks) > 1:
            print("One user Multi task : " + credit)
            staff = staffs[0]
            for task in tasks:
                pst, created = ProductionStaffTask.objects.get_or_create(staff=staff, task=task, production=aw)
                setStats(pst, created)
                print(pst)

    # END OF FOR CREDITS


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

    select = input("Votre choix : ")

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
    print("firsname:"+first_name)
    print("lastname:"+last_name)

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
        if user_search and user_search["dist"] >= .9:
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
            user, created = User.objects.get_or_create(first_name=first_name.title(), last_name=last_name.title(),
                                                       username=username)
        except Exception as e:
            username = usernamize(first_name, last_name, True)
            user, created = User.objects.get_or_create(first_name=first_name.title(), last_name=last_name.title(),
                                                       username=username)
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


def getOrCreateMultiInstancesByStr(model, attr, txt_str):
    instances = []
    txt_str = txt_str.strip()

    if "," in txt_str or " et " in txt_str:
        str_split = txt_str.split(",") if "," in txt_str else txt_str.split(" et ")
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

    query = model.objects.filter(**{attr+"__iexact": txt_str})
    if query.count() == 0:
        query = model.objects.filter(**{attr+"__icontains": txt_str})

    if query.count() > 1:
        print(str(model) + " (csv) : " + txt_str)
        instance = input_choices(query)

    elif query.count() == 1:
        instance = query.first()

    if not instance:
        instance, created = model.objects.get_or_create(**{attr: txt_str.title()})
        setStats(instance, created)
        print("Création d'une instance" + str(model) + " : " + str(instance))

    return instance


def multiline_input():
    print("Enter/Paste your content. Ctrl-D to save it.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    return '\n'.join(contents)


def setStats(value_from_model, created):
    class_name = value_from_model.__class__.__name__.lower()
    attibute = class_name + "_created" if created else class_name + "_reused"
    if attibute not in stats:
        stats[attibute] = []
    stats[attibute].append(value_from_model)

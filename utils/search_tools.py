
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


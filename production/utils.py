
from datetime import datetime, date
from django.contrib.postgres.search import TrigramSimilarity

from production.models import Event
from utils.search_tools import input_choices


def get_or_create_event(title, start_date, end_date, event_type):

    event = search_event(title, start_date, end_date)
    if event:
        return event
    
    return None
    # If not found, create new event

    # event, created = Event.objects.get_or_create(
    #     title=title,
    #     starting_date=start_date,
    #     ending_date=end_date,
    #     type=event_type
    # )
    # return event


def search_event(title:str, start_date:date, end_date:date):
    """Search for an event by title and dates.
    Parameters:
    - title       : (str) The title of the event
    - start_date  : (date) The starting date of the event
    - end_date    : (date) The ending date of the event
    """
    # full seach (lucky day)
    print (f"Searching for event: {title} ({start_date} - {end_date})")
    try:
        event = Event.objects.get(
            title__unaccent__icontains=title,
            starting_date__date=start_date,
            ending_date__date=end_date
        )
        return event
    except Event.DoesNotExist:
        # continue searching
        pass
    except Event.MultipleObjectsReturned:
        # if multiple events are found, ask the user
        events = Event.objects.filter(
            title__unaccent__icontains=title,
            starting_date__date=start_date,
            ending_date__date=end_date
        )
        print("Multiple events found with the same title and dates.")
        event = input_choices(list(events))
        if event:
            return event
    
    print("No exact match found, trying partial matches...")
    # search by title and starting date only
    events = Event.objects.filter(
        title__unaccent__icontains=title,
        starting_date__year=start_date.year,
    )
    if events:
        print("Multiple events found with the same title and starting year.")
        event = input_choices(list(events))
        if event:
            return event

    print("TrigramSimilarity search")
    # search by title only TrigramSimilarity
    events = Event.objects.annotate(
        similarity=TrigramSimilarity('title', title)
    ).filter(similarity__gt=0.8).order_by('-similarity')

    if events:
        print("Multiple events found with similar titles.")
        event = input_choices(list(events))
        if event:
            return event
    
    print("No matching event found.")
    return None

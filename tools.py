#! /usr/bin/env python
# -*- coding=utf8 -*-

import os

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kart.settings")
django.setup()

from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from assets.models import Gallery, Medium
from common.models import BTBeacon, Website
from diffusion.models import Award, Diffusion, MetaAward, MetaEvent, Place
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.contrib.sites.models import Site
from guardian.models import GroupObjectPermission, UserObjectPermission
from people.models import Artist, FresnoyProfile, Organization, Staff
from production.models import Artwork, Event, Exhibition, Film, FilmGenre, Installation, InstallationGenre, Itinerary, ItineraryArtwork, OrganizationTask, Performance, Production, ProductionOrganizationTask, ProductionStaffTask, StaffTask
from rest_framework.authtoken.models import Token
from school.models import Promotion, Student, StudentApplication, StudentApplicationSetup
from taggit.models import Tag, TaggedItem
from tastypie.models import ApiAccess, ApiKey
# Shell Plus Django Imports
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When, Exists, OuterRef, Subquery
from django.utils import timezone
from django.urls import reverse


import pandas as pd 
from pathlib import Path
import matplotlib.pyplot as plt 
import math

# Full width print of dataframe 
pd.set_option('display.expand_frame_repr', False)

DEBUG = True

# Get the data from csv
awards = pd.read_csv('awards.csv')
# Strip all data
awards = awards.applymap(lambda x: x.strip() if isinstance(x, str) else x)


def testAwardsProcess() :
    """Stats stuff about the awards 
    
    Dummy code to get familiar with Kart"""
    # ========= Stacked data : awards by events type ... ==============
    import matplotlib.colors as mcolors
    mcol = mcolors.CSS4_COLORS
    mcol = list(mcol.values())
    # mixing the colors with suficent gap to avoid too close colors 
    colss = [mcol[x+12] for x in range(len(mcol)-12) if x%5==0]
    # by type of event 
    awards.groupby(['event_year','event_type']).size().unstack().plot(kind='bar', stacked=True,color=colss)
    plt.show()


def testArtworks() : 
    """Get authors with artwork id

    Dummy code to get familiar with Kart"""
    ##### Artworks

    # replace NA/Nan by 0
    awards.artwork_id.fillna(0,inplace=True)

    # Convert ids to int 
    awards.artwork_id = awards['artwork_id'].astype(int) 

    for id in awards.artwork_id :
        # id must exist (!=0)
        if not id : continue 
        prod = Production.objects.get(pk=id)
        print(prod.artwork.authors)



#### Events 

from django.contrib.postgres.search import TrigramSimilarity
from difflib import SequenceMatcher

def eventCleaning():
    """Preparation and cleannig step of the awards csv file

    WARNING : this function requires a human validation and overrides `events_title.csv` & `merge.csv`

    1) from the csv data, extract potential events already present in Kart
    2) when doubts about the name of the event, with close syntax, store the event kart_title in a csv for validation by head of diffusion. 
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

    # We only use event titles for this phase. Drop rows with dup. titles
    awards.drop_duplicates(['event_title'], inplace=True)

    # With the name/title of each event in the csv file ...
    for ind, csv_event in awards.iterrows() :
        # ... retrieve event from Kart by title similarity and human selection of best action 
        # to take (keep one or the other or create)
        csv_title = csv_event.event_title

        guess = Event.objects.annotate(
            similarity=TrigramSimilarity('title', csv_title),
            ).filter(similarity__gt=0.5).order_by('-similarity')
        
        print("guess",guess)
        # If events with similar title found in Kart  
        for i in range(len(guess)):
            kart_event = guess[i]
            kart_title = kart_event.title
            
            # Distance btw the title from csv and the one found in Kart 
            dist = round(SequenceMatcher(None, str(kart_title).lower(), csv_title.lower()).ratio(),2)
            
            print(f"\n\n============================\ncsv : {csv_title}  <- {dist} -> kart : {kart_title}")

            # Store the titles for further process 
            csv_titles.append(str(csv_title))
            kart_titles.append(str(kart_title))
            
            # If titles are really close ...
            if dist > .9 :
                print("high similarity!")
                # ... the title from csv is kept 
                def_titles.append(csv_title)
                # The kart id is associated with the event
                # def_ids.append(kart_event.id)
                break
            # if dist is too low, ask what to do 
            elif dist > .7 :
                cont = input("""
                What should I do ? 
                - keep from csv  (c)
                - keep from Kart (k)
                - csv is not in kart, creaTe it (t)
                - pass (p)  
                > c, k, t, p :   """)
                
                # We keep the csv data 
                if cont.lower() == 'c':
                    def_titles.append(str(csv_title))
                    # def_ids.append('0')
                    break

                # We keep the kart data (update the csv)
                if cont.lower() == 'k':
                    def_titles.append(str(kart_title)) 
                    # def_ids.append(kart_event.id)
                    break

                # Create the event from csv data 
                if cont.lower() == 't':
                    def_titles.append(csv_title)
                    # def_ids.append('<create>')
                    break

                # otherwise pass and live final name blank
                if cont.lower() not in ['t','c','k']:
                    def_titles.append("")
                    # def_ids.append('0')

                # If no event with close title found in Kart, tag for creation    
                else :
                    def_titles.append("<create>")
                    # def_ids.append('0')

    # print("def_ids",def_ids)
    # DF with the events names to validate 
    event_df = pd.DataFrame({'NomFichier':csv_titles,
                               'NomKart':kart_titles,
                               'NomDefinitif':def_titles,
                               # 'event_id':def_ids
                                })

    # merge the cleaned data with awards csv
    merge_df = pd.merge(awards,event_df,left_on="event_title",right_on="NomFichier")
    # Drop duplicates 
    event_df.drop_duplicates(inplace=True)

    # Export to csv 
    event_df.to_csv('events_title.csv',index=False)
    merge_df.to_csv('merge.csv',index=False)
    
# eventCleaning()

# 
# def getEventsToCreate() :
#     """Return a df with the events that need to be created 
# 
#     The event is identified in the award csv file with its name 'NomFichier'
#     """
#     evt = pd.read_csv('events_title.csv')
# 
#     # check the event that tagged as <create> from previous process (manualSelection)
#     return evt.loc[evt['NomDefinitif']=="<create>",["NomFichier"]]


def infoCSVeventTitles():
    """Display info about potentialy existing events in Kart 

    Check if event names exist with a different case in Kart and display warning 
    """
    eventsToCreate = pd.read_csv('events_title.csv')
    
    for evt_title in eventsToCreate.NomFichier :
        # If a title already exist with different case 
        exact = Event.objects.filter(title__iexact=evt_title)
        if exact : 
            print(f"Event already exist with same name (but not same case) for {evt_title} :\n{exact}\n")
        
        # If a title already contains with different case 
        contains = Event.objects.filter(title__icontains=evt_title)
        if contains : 
            print(f"Event already exist with very approaching name (but not same case) for {evt_title} :\n{contains}\n")
        

# infoCSVeventTitles()

from datetime import datetime 

def createEvents() :
    """ Create (in Kart) the events listed in awards csv file 
    
    1) Retrieve the data about the events listed in awards csv file
    2) Parse those data and prepare if for Event creation
    3) (optional) Check if meta event exits for the created event, creates it if needed
    """
    
    # Get the events from awards csv extended with title cleaning (merge.csv)
    events = pd.read_csv('merge.csv')
    
    # Create/get the events in Kart
    for ind, event in events.iterrows() :
        title = event.NomDefinitif
        # Starting dates are used only for the year info (default 01.01.XXX)
        starting_date = event.event_year
        # Convert the year to date
        starting_date = datetime.strptime(str(starting_date),'%Y').date()
        # All events are associated with type festival 
        # TODO: Add other choices to event ? Delete choices constraint ? 
        type = "FEST"
        
        # Create the meta event 
        obj, created = Event.objects.get_or_create(
            title=title,
            # default date to 1st jan 70, should be replaced by the oldest edition 
            starting_date=datetime.strptime("01-01-70","%d-%m-%y").date(),
            type=type,
            main_event=True
        )
        if created :
            print(f"META {title} was created")
        else : 
            print(f"META {title} was already in Kart")
        
        obj, created = Event.objects.get_or_create(
            title=title,
            starting_date=starting_date,
            type=type,
        )
        if created :
            print(f"{title} was created")
        else : 
            print(f"{title} was already in Kart")
        events.loc[ind,'id_event'] = obj.id
    events.to_csv('events.csv',index=False)

createEvents()

from django_countries import countries
import unidecode
from collections_extended import collection

def getISOname(countryName=None, simili=False) :
    """Return the ISO3166 international value of `countryName`

    Parameters :
    - countryName   : (str) The name of a country
    - simili          : (bool) If True (default:False), use similarity to compare the names
    """
    # Process the US case (happens often!)
    if re.search('[EeéÉ]tats[ ]?-?[ ]?[Uu]nis',countryName) : 
        return "US"
    # Kosovo is not liste in django countries (2020)
    if re.search('kosovo',countryName,re.IGNORECASE) :
        return 'XK'

    # General case 
    if not simili :
        for code, name in list(countries):
            if name == countryName : return code
        return False
    else :
        # The dic holding the matches
        matchCodes = []
        for code, name in list(countries):
            dist = SequenceMatcher(None, str(countryName).lower(),name.lower()).ratio()
            # print(f"DIST between {countryName} (unknown) and {name} : {dist}")
            if dist >= .95 :
                matchCodes.append({'dist':dist, 'code':code}) # 1 ponctuation diff leads to .88
            if dist >= .85 :
                cn1 = unidecode.unidecode(str(countryName))
                cn2 = unidecode.unidecode(name)
                dist2 = SequenceMatcher(None, cn1.lower(),cn2.lower()).ratio()
                if dist2 > dist :
                    print(f"------------------- ACCENTUATION DIFF {countryName} vs {name}\nAccents removed : {cn1} vs {cn2} : {dist2}")
                    matchCodes.append({'dist':dist2, 'code':code}) # 1 ponctuation diff leads to .88
                else :
                    if DEBUG :
                        return code
                    cont = input(f"""
                                 NOT FOUND but {countryName} has a close match with {name}
                                 Should I keep it ? (Y/n) :   """)
                    if re.search("NO?", cont, re.IGNORECASE) :
                        continue
                    else :
                        return code
                    
    # Sort the matches by similarity
    sorted(matchCodes, key = lambda i: i['dist'])
    try :
        # Return the code with the highest score
        return matchCodes[0]['code']
    except IndexError :
        return False

    
import re
def createPlaces() :
    """Create the places listed in the awards csv files
    
    """

    # List the places in the file
    places = awards[['place_city','place_country']]
    # Drop duplicates
    places = places.drop_duplicates()
    # Remove empty rows
    places = places.dropna(how="all")
    # Replace NA/NaN (similarity fails otherwise)
    places.fillna('',inplace=True)

    # List of places to create (not in Kart)
    placesToCreate = []
    print("places",places)
    for i,place in places.iterrows() :
        city = place.place_city
        country = place.place_country
        if city == country == '' : continue
        print(f"\n\nPLACE : {city} - {country}")
    
        ###### Processing CITY 
        # Look for really approaching (simi=.9) name of city in Kart 
        guessCity = Place.objects.annotate(
                similarity=TrigramSimilarity('name', city),
                ).filter(similarity__gt=0.9).order_by('-similarity')
        
        # If a city in Kart is close from the city in csv file 
        if guessCity :
            print(f"CITY FOUND IN KART : {guessCity[0].city}")
            cityInKart = True
        else :
            print(f"No close city name in Kart, the place should be created")

        ###### Processing COUNTRY 
        # Look for ISO country code related to the country name in csv
        codeCountryCSV = getISOname(country)

        # If code is easly found, keep it 
        if codeCountryCSV :
            print(f"CODE FOUND : {country} -> {codeCountryCSV}\n")
            pass

        # If no code found, check if the country associated with the city found in Kart 
        # is close from the country in csv file to use its code instead
        elif guessCity :
            codeCountryKart = guessCity[0].country
            countryNameKart = dict(countries)[codeCountryKart]
            
            # Compute the distance between the 2 country names 
            dist = round(SequenceMatcher(None, str(country).lower(),
                         countryNameKart.lower()).ratio(),2)
            
            # If really close, keep the Kart version
            if dist>.9 :
                print(f"Really close name, replacing {country} by {countryNameKart}")
                codeCountryCSV = codeCountryKart
            else :
                # Process the us case (happens often!)
                if re.search('[EeéÉ]tats[ ]?-?[ ]?[Uu]nis',country) : 
                    codeCountryCSV = "US"
                else : # If not close to the Kart version, try with similarity with other countries
                    codeCountryCSV = getISOname(country, simili=True)
                    
        else : # No city found, so no clue to find the country => full search
            # parameter simili=True triggers a search by similarity btw `country` and django countries entries
            codeCountryCSV = getISOname(country, simili=True)
            if codeCountryCSV :
                print(f"Looked for the country code of {country} and obtained {codeCountryCSV}")
            else : 
                # Check for Kosovo :
                # Although Kosovo has no ISO 3166-1 code either, it is generally accepted to be XK temporarily; see http://ec.europa.eu/budget/contracts_grants/info_contracts/inforeuro/inforeuro_en.cfm or the CLDR
                if re.search("kosovo",country,re.IGNORECASE) :
                    codeCountryCSV = "XK"
                print("No city found, no country found :-(")

        print("codeCountryCSV",codeCountryCSV)
        
        obj, created = Place.objects.get_or_create (
            name = city if city else country,
            city = city,
            country = codeCountryCSV if codeCountryCSV else ''
        )

        print(f"obj : {obj}, created : {created}")
    
# createPlaces()

# TODO: Fill artwork in the event 

# ASSOCIATE PLACES AND EVENTS 

def associateEventsPlaces() :
    """Fill the place field of created events with the created places

    """
    

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

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

# Full width print of dataframe 
pd.set_option('display.expand_frame_repr', False)


# TODO: Harmonise created and read files (merge.csv, ...)

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

def dist2(item1,item2) :
    """Return the distance between the 2 strings"""
    if not type(item1)==type(item2)==str :
        raise TypeError("Parameters should be str.")
    return round(SequenceMatcher(None, item1.lower(),item2.lower()).ratio(),2)


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
    aw_events = awards.drop_duplicates(['event_title'])
    
    # With the name/title of each event in the csv file ...
    for ind, csv_event in aw_events.iterrows() :
        # ... retrieve event from Kart by title similarity and human selection of best action 
        # to take (keep one or the other or create)
        csv_title = str(csv_event.event_title)
        csv_titles.append(csv_title)

        guess = Event.objects.annotate(
            similarity=TrigramSimilarity('title', csv_title),
            ).filter(similarity__gt=0.5).order_by('-similarity')

        nbGuess = len(guess)

        # If no similar event found in Kart
        if nbGuess==0 :
            def_titles.append(csv_title)
            kart_titles.append("")
            continue

        else :
            go = 1
            # TODO : drop_duplicates in guess
            while go : 
                identical = False
                # check for identical title in the results
                for i in range(nbGuess):
                    kart_title = guess[i].title
                    if guess[i].title == csv_title :
                        print(f"\n\nTitle found in Kart\nBoth titles are the same {csv_title} = {kart_title}\n")
                        def_titles.append(csv_title)
                        kart_titles.append(kart_title)
                        identical = True
                        break

                # Next event if identical was found ...
                if identical :
                    cont = 'c'
                    break
                
                # ... otherwise, ask user what to do
                print(f"\n\n======================================================")
                print(f"CSV\t\t\t|{csv_title}|")
                for i in range(nbGuess):
                    # Distance btw the title from csv and the one found in Kart 
                    dist = round(SequenceMatcher(None, str(guess[i].title).lower(), csv_title.lower()).ratio(),2)
                    print(f"({i+1}) Kart\t\t|{guess[i].title}|\t\t\t(dist :{dist})")

                cont = input(f"""
                What should I do with the name of this event ? 
                - Keep from csv (press 'c' or 'enter')
                - Use match from Kart (press '1','2',..)
                - Ignore the event : won't be processed in either way (press 'x')
                > c, 1-9, x :   """)
                
                if cont == '':
                    cont = 'c' # Default value, we keep csv
                    
                # We keep the csv data and update Kart (TODO)
                if cont.lower() == 'c' :
                    def_titles.append(csv_title)
                    kart_titles.append("")
                    break

                # Ignore the event
                if cont.lower() == 'x':
                    # Remove the title from the list - won't be processed
                    csv_titles.pop() 
                    break

                # We keep the kart data
                try :
                    if int(cont) in range(1,nbGuess+1):
                        cont = int(cont)
                        kart_title = guess[cont-1].title
                        kc = input(f"Use kart title : {kart_title} ? (Y/n) : ")
                        if kc != "n" :
                            def_titles.append(kart_title) 
                            kart_titles.append(kart_title)
                            break
                        else :
                            cont = False
                except :
                    pass
                
        
    # DF with the events names to validate 
    event_df = pd.DataFrame({'NomFichier':csv_titles,
                             'NomKart':kart_titles,
                             'NomDefinitif':def_titles
                            })

    # merge the cleaned data with awards csv
    merge_df = pd.merge(awards,event_df,how='left',left_on="event_title",right_on="NomFichier")
    # Drop duplicates 
    event_df.drop_duplicates(inplace=True)

    # Export to csv 
    event_df.to_csv('events_title.csv',index=False)
    merge_df.to_csv('merge.csv',index=False)
    
# eventCleaning()


def artworkCleaning():
    """Preparation and cleannig step of the awards csv file

    WARNING : this function requires a human validation and overrides `artworks_title.csv` & `merge.csv`

    1) from the csv data, extract potential artworks already present in Kart
    2) when doubts about the name of the artwork, with close syntax, store the artwork kart_title in a csv for validation by head of diffusion. 
    3) if no match at all, mark the artwork for creation 
    """

    aws = pd.read_csv('merge.csv')

    
    
    # Check if the id provided in the csv match with the artwork description
    # replace the nan with empty strings
    aws.fillna('',inplace=True)
    # # Get the artwork with no id
    # aw_noID = aws[aws['artwork_id']=='']
     
    for ind, aw in aws.iterrows():
        # print("\n--------------------------")
        # Variables init
        no_artwork = no_artist = author_match_dist = title_match_dist = False 
        # Parsing
        aw_id       =   int(aw.artwork_id) if aw.artwork_id else None
        aw_title    =   str(aw.artwork_title)
        lastname    =   str(aw.artist_lastname)
        firstname   =   str(aw.artist_firstname)

        # If an id is declared, get the aw from kart and check its 
        # similarity with the content of the row to validate 
        if aw_id :
            ### Artwork validation if the title from aw generated with id and title in csv
            aw_kart = Artwork.objects.prefetch_related('authors__user').get(pk=aw_id)
            if dist2(aw_kart.title,aw_title)<.8 : 
                print (f"ARTWORK INTEGRITY PROBLEM : \"{aw_kart.title}\" should match \"{aw_title}\"")
                aws.loc[ind,'aw_art_valid'] = False

            ### Artist/author validation
            # The closest artists in Kart from the data given in CSV (listing => all matches)
            _artist, dist = getArtistByNames(firstname=firstname,lastname=lastname, listing=True)
            if not _artist :
                print(f"No artist can be found with {firstname} {lastname} : CREATE ARTIST ?\n\n")
                continue
            # Compare it to the authors of the artwork
            # Dealing with duplicated artists ... 
            # Check if any artists that match first and last names match the author of the artwork    
            # If no match between potential artists and authors : integrity issue
            artist_in_authors = [x['artist'] in aw_kart.authors.all() for x in _artist]
            if not any(artist_in_authors) : 
                print(f"Artist and artwork do not match ---------- SKIPPING\nArtist : {_artist}\nArtwork : {aw_kart}\n{aw_kart.authors.all()[0].id}\n\n")
                aws.loc[ind,'aw_art_valid'] = False
                continue
            else :
                # The matching author among the potential duplicates 
                the_one = _artist[artist_in_authors.index(True)]['artist']
                # Indicate the artist_id in the csv
                aws.loc[ind, "artist_id"] = the_one.id
                # print("the_one",the_one, the_one.id)
                # Continue to next row
                continue
            

        # If no id and no title provided, skip
        if not aw_id and aw_title == '':
            print("No data about artwork in the csv file, only artist will be specified in the award.")
            no_artwork = True

        # If partial to no artist data in the csv
        if not all([firstname,lastname]):
            if not any([firstname,lastname]):
                print("No info about the artist")
                no_artist = True
            else : print("Partial data about artist ...")
        
        if all([no_artwork,no_artist]) :
            print(f"{aw_title} No info about the artwork nor the artists : SKIPPING\n{aw}\n\n")
            continue

        # IF NO ID ARTWORK
        # Retrieve artwork with title similarity
        guessAW = Artwork.objects.annotate(
                    similarity=TrigramSimilarity('title', aw_title),
                    ).filter(similarity__gt=0.7).order_by('-similarity')
        
        if guessAW :
            print(f"Potential artworks in Kart found for \"{aw_title}\"...")
            # Explore the potential artworks
            for gaw in guessAW :
                print(f"\t->Best guess : \"{gaw.title}\"")
                # If approaching results is exactly the same
                title_match_dist = dist2(aw_title.lower(),gaw.title.lower())
                print("title_match_dist",title_match_dist)
                artist, author_match_dist = getArtistByNames(firstname=firstname,lastname=lastname)
                
             
                if all([title_match_dist, author_match_dist, title_match_dist==1, author_match_dist == 1]) :
                    print("Perfect match : artwrok and related authors exist in Kart")
                if all([title_match_dist, author_match_dist, title_match_dist==1]) :
                    print(f"Sure about the artwork title, confidence in author : {author_match_dist}")
                if all([title_match_dist, author_match_dist, author_match_dist==1]) :
                    print(f"Sure about the authors, confidence in artwirk : {artwork_match_dist}")


        else : # no artwork found in Kart
            print(f"No approaching artwork in KART for {aw_title}")
            # Retrieving data to create the artwork
        
        ######### ARTIST 
        artist, dist = getArtistByNames(firstname=firstname,lastname=lastname)
        

    aws.to_csv('artworks_artists.csv', index=False)



def getArtistByNames(firstname=None, lastname=None, pseudo=None, listing=False):
    """Retrieve the closest artist from the first and last names given
    
    Parameters :
    - listing   : (bool) If True, return a list of matching artists (Default, return the closest)

    Return :
    - artistObj     : (Django obj / bool) The closest artist object found in Kart. False if no match.
    - dist          : (float) Distance with the given names
    """
    
    # If no lastname no pseudo
    if not any([lastname, pseudo]) :
        print("At least a lastname or a pseudo is required")
        return False, False

    # List of artists that could match
    art_l = []
    
    # First filter by lastname similarity
    guessArtLN = Artist.objects.prefetch_related('user').annotate(
                similarity=TrigramSimilarity('user__last_name', lastname),
                ).filter(similarity__gt=0.8).order_by('-similarity')

    # If lastname returns results, refine with firstname
    if guessArtLN : 
        # TODO: Optimize by checking a same artist does not get tested several times 
        for artist_kart in guessArtLN :
    
            kart_lastname   = artist_kart.user.last_name
            kart_firstname  = artist_kart.user.first_name

            # Control for blank spaces
            if  kart_lastname.find(" ")>=0 or lastname.find(" ")>=0 :
                bef = f"\"{kart_lastname}\" <> \"{lastname}\""
                if dist2(kart_lastname.replace(" ", ""),lastname.replace(" ", ""))<.9 :
                    print(f"whitespace problem ? {bef}")
            if  kart_firstname.find(" ")>=0 or firstname.find(" ")>=0 :
                bef = f"\"{kart_firstname}\" <> \"{firstname}\""
                if dist2(kart_firstname.replace(" ", ""),firstname.replace(" ", ""))<.9 :
                    print(f"whitespace problem ? {bef}")
            
            # Check if Kart and tested names are exactly the same 
            if kart_lastname == lastname and kart_firstname == firstname :
                art_l.append({"artist":artist_kart,'dist':2})
                continue

            
            
            dist_lastname = dist2(kart_lastname,lastname)

            # try to find by similarity with firstname
            guessArtFN = Artist.objects.prefetch_related('user').annotate(
                        similarity=TrigramSimilarity('user__first_name', firstname),
                        ).filter(user__last_name=lastname,similarity__gt=0.8).order_by('-similarity')
            
            # if artist with same lastname and similar firstname names are found
            if guessArtFN :
                # Check all possibilities
                for artistfn_kart in guessArtFN :
                    kart_firstname = artistfn_kart.user.first_name
                    dist_firstname = dist2(f"{kart_firstname}",f"{firstname}")

                    art_l.append({"artist":artistfn_kart,'dist':dist_lastname+dist_lastname})
                
                # # Use the most similar
                # kart_artist = guessArtFN[0]
            else :
                # If no close firstname found
                art_l.append({"artist":artist_kart,'dist':dist_lastname})
            
            
        # Take the highest distance score
        # print(f"{firstname} {lastname} ----------------> art_l.",art_l)
        sorted(art_l, key = lambda i: i['dist'])
        if listing :
            return art_l, False
        else :
            return art_l[0]['artist'], art_l[0]['dist']
    else :
        return False, 0
    
    
    
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
        
        # Check if meta event exists, if not, creates it
        obj = Event.objects.filter(
            title=title,
            type=type,
            main_event=True
        )
        # If event already exist 
        if len(obj) :
            # Arbitrarily use the first event of the queryset (may contain more than 1)
            # TODO: what if more than one ? 
            obj = obj[0]
            created = False 
        else :
            # Create the main event
            obj = Event(
                title=title,
                # default date to 1st jan 70, should be replaced by the oldest edition 
                starting_date=datetime.strptime("01-01-70","%d-%m-%y").date(),
                type=type,
                main_event=True
            )
            obj.save()
            created = True
        
        if created :
            print(f"META {title} was created")
        else : 
            print(f"META {title} was already in Kart")
        
        # Check if event exists, if not, creates it
        obj = Event.objects.filter(
            title=title,
            type=type,
            # just use the starting date for now
            # TODO: events with more details
            starting_date=starting_date
        )
        
        if len(obj) :
            # Arbitrarily use the first event of the queryset 
            obj = obj[0]
            created = False 
        else :
            print("obj is getting created")
            obj = Event(
                title=title,
                type=type,
                starting_date=starting_date
            )
            obj.save()
            created = True
        
        if created :
            print(f"{title} was created")
        else : 
            print(f"{title} was already in Kart")
        # Store the ids of newly created/already existing events in a csv
        events.loc[ind,'event_id'] = obj.id
    events.to_csv('events.csv',index=False)


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

    # Get the data from awards csv extended with title cleaning and events (merge.csv)
    merge = pd.read_csv('events.csv')
    # Drop duplicates
    places = merge.drop_duplicates(['place_city','place_country'])
    # Remove rows with full empty location
    places = places.dropna(subset=['place_city','place_country'],how="all")
    # Replace NA/NaN (similarity fails otherwise)
    places.fillna('',inplace=True)

    # List of places to create (not in Kart)
    placesToCreate = []

    for ind, place in places.iterrows() :
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
            print(f"No close city name in Kart, the place should be created or is empty")

        ###### Processing COUNTRY 
        # Look for ISO country code related to the country name in csv
        codeCountryCSV = getISOname(country)

        # If code is easly found, keep it 
        if codeCountryCSV :
            print(f"CODE FOUND : {country} -> {codeCountryCSV}")
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

        

        # Check if place exists, if not, creates it
        obj = Place.objects.filter(
            name = city if city else country,
            city = city,
            country = codeCountryCSV if codeCountryCSV else ''
        )
        # If place already exist 
        if len(obj) :
            # Arbitrarily use the first place of the queryset (may contain more than 1)
            # TODO: what if more than one ? 
            obj = obj[0]
            created = False 
        else :
            # Create the Place
            obj = Place(
                name = city if city else country,
                city = city,
                country = codeCountryCSV if codeCountryCSV else ''
            )
            obj.save()
            created = True
        if place.place_city == '' :
            print('==========================================================================',obj)
        if created :
            print(f"Place {obj} was created")
        else : 
            print(f"Place {obj} was already in Kart")
        # Store the id of the place
        places.loc[ind,'place_id'] = obj.id 
    
    # Store the places 
    places.to_csv('places.csv',index=False)

    # test to deal with city only rows, use "NULL" to allow the merging with missing data
    places.loc[places['place_city'] == '','place_city'] = "**NULL**"
    merge.loc[merge['place_city'].isna(),'place_city'] = "**NULL**"

    merge_df = pd.merge(
                        merge,
                        places[["place_city","place_country","place_id"]],
                        how='left',on=["place_city","place_country"]
                        )
    # Restore the missing data after the merge
    merge_df.loc[merge_df['place_city']=="**NULL**",'place_city'] = ''
    merge_df.to_csv('merge_events_places.csv',index=False)

# TODO: Fill artwork in the event 

def associateEventsPlaces() :
    """Fill the place field of created events with the created places

    """

    # Get the events and places csv
    evt_places = pd.read_csv("merge_events_places.csv")

    # Update the events with the place 
    for ind, award in evt_places.iterrows():
        event_id = int(award.event_id)
        try: # some events have no places specified
            place_id = int(award.place_id)
            evt = Event.objects.get(pk=event_id)
            evt.place_id = place_id
            evt.save()
            print(evt)
        except ValueError as ve:
            print("ve",ve)



def safeGet(obj_class=None, default_index=None, force=False, **args) :
    """Try to `get`the object in Kart. If models.MultipleObjectsReturned error, return the first oject returned or the one in index `default_index`

    Parameters :
    - objClass      : (Django obj) The class on which to apply the get function
    - default       : (int) The index of the queryset to return in case of MultipleObjectsReturned error. 
                      '0' is used in case of IndexError
    - args          : the arguments of the get query
    - force         : (bool) Force the return of the whole queryset rather than just one object - Default : False

    Return : 
    - obj           : (Django obj or bool) a unique object of `obj_class`matching the **args, 
                       False if `ObjectDoesNotExist` is raised 
    - filtered      : a boolean indicating if the returned obj was unique or from a >1 queryset
    """

    try : 
        obj = obj_class.objects.get(**args)
        return obj , False

    # If the object does not exist, return False 
    except ObjectDoesNotExist :
        return False, False

    # If multiple entries for the query, fallback on filter
    except MultipleObjectsReturned:
        objs = obj_class.objects.filter(**args)
        print(f"The request of {args}  returned multiple entries for the class {obj_class}")

        if default_index : 
            try :
                return objs[default_index], True
            except :
                return objs[0], True
        else :
            # Return the first object of the queryset
            return objs[0], True
    
def objExistPlus(obj_class=None, default_index=None ,**args) :
    """Return a True if one or more objects with `**args` parameters exist 

    Parameters :
    - objClass      : (DjangoObject) The class on which to apply the get function
    - default       : (int) The index of the queryset to return in case of MultipleObjectsReturned error. 
                      '0' is used in case of IndexError
    - args          : the arguments of the get query

    Return : 
    - exists        : (bool)
    - multiple      : (int) the amount of existing object
    """

    objs, filtered = safeGet(obj_class, force= True, **args)
    if objs :
        return True, len(objs)
    else :
        return False, 

def objExist(obj_class=None, default_index=None ,**args) :
    """Return a True if one or more objects with `**args` parameters exist 

    Parameters :
    - objClass      : (DjangoObject) The class on which to apply the get function
    - default       : (int) The index of the queryset to return in case of MultipleObjectsReturned error. 
                      '0' is used in case of IndexError
    - args          : the arguments of the get query

    Return : 
    - exists        : (bool)
    """

    objs, filtered = safeGet(obj_class, force= True, **args)
    if objs :
        return True
    else :
        return False

def createAwards() :
    """Create the awards listed in csv in Kart
    
    """

    awards = pd.read_csv("merge_events_places.csv")
    
    for ind, award in awards.iterrows():
        label = award.meta_award_label
        event_id = int(award.event_id)
        artxork_id = int(award.artwork_id)

        description = award.meta_award_label_details
        if pd.isna(award.meta_award_label_details):
            description = ''

        ### GET THE META-eventsToCreate 
        # The only way to retrieve the meta event of an event is by title (TODO : foregin key)
        # Retrieve the Kart title of the event
        event, filt = safeGet(Event, pk=event_id)
        mevent, filt = safeGet(Event, title=event.title, main_event = True)
        
        ### GET OR CREATE THE META-AWARD
        # Check if award exists in Kart, otherwise creates it 
        maward, filt = safeGet(MetaAward, label = f"{label}", event = mevent.id)
        
        if maward : 
            print(f"MetaAward {label} exist in Kart")
        else :
            maward = MetaAward(
                label = f"{label}",
                event = mevent,
                description = description,
                type = "INDIVIDUAL" # indivudal by default, no related info in csv
            )
            maward.save()
            print(f"\"{maward}\" created ")

        ###  GET OR CREATE THE AWARDS
        maward, filt = safeGet(Award, label = f"{label}", event = mevent.id)

artworkCleaning()
# eventCleaning()
# createEvents()
# createPlaces()
# associateEventsPlaces()
# WIP : createAwards()

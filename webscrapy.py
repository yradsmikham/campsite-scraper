from bs4 import BeautifulSoup
from textmagic.rest import TextmagicRestClient
import requests, json, urllib2

client = TextmagicRestClient("yradsmikham", "VlY7PjdtNSZkiiyZn6U1GX0KV7jLTl")

# inputs
# enter phone number, specify dates and campground id
phone_number = "" # must include country code
campground_id = "232472" # example correponds to Yosemite Upper Pines Campground
start_date = "2019-01-28"
end_date = "2019-01-30"

#232472 Indian Cove JTree

# specify url
url = "https://www.recreation.gov/api/camps/availability/campground/"+campground_id+"?start_date="+start_date+"T00%3A00%3A00.000Z&end_date="+end_date+"T00%3A00%3A00.000Z"

def webscrape(url):
    # query website and return html
    data = urllib2.urlopen(url)

    # parse the html using beautiful soup and store in variable 
    soup = str(BeautifulSoup(data, 'html.parser'))
    campsite_json = json.loads(soup)

    # iterate through each campsite to check for availabilities
    available_campsites = []
    for campsite in campsite_json['campsites']:
        days = campsite_json['campsites'][campsite]["availabilities"]
        availabilities = []
        for key,value in days.items():
            if value != None:
                availabilities.append(value)
        if not availabilities:
            #print("List is empty.")
            pass
        else:
            #print(availabilities)
            #print(all(dawgie == 'Open' or 'Available' for dawgie in availabilities))
            if all(dawgie == 'Open' or 'Available' for dawgie in availabilities):
                #print("THERE IS AN AVAILABLE CAMPSITE!")
                available_campsites.append(campsite)
            else:
                #print("NO CAMPSITES AVAILABLE.")
                continue
        #print("------------------------------------------------------------------------")
    #print("AVAILABLE CAMPSITES:" + str(available_campsites))
    return available_campsites

result = webscrape(url)
#print(result[:5])
def send_notifcation(url, list_of_available_campsites):
# send text notification
    if len(result) != 0:
        client.messages.create(phones=phone_number, text="There are campsites available at " + campground_id + ". The following campsites are available: " +  str(result[:5]))
    else:
        webscrape(url)
        send_notifcation(url, list_of_available_campsites)

# notes:
# multiprocessing/threaded?
# possibly kick off another script that will log in and adds to cart?

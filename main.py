from bs4 import BeautifulSoup
import requests
import pandas as pd


# List to store similar apps links from given app
links_list1 = []


# Function to extract Application's Name

def get_AppName(soup):
    try:
        # Extracting Application's Name
        AppName = soup.find("h1", attrs={"class": 'Fd93Bb F5UCq p5VxAd'}).find("span").string.strip()
    except AttributeError:
        AppName = "N/A"

    return AppName


# Function to extract App's Maker's Name

def get_MakerName(soup):
    try:
        # Extracting App's Maker's Name
        MakerName = soup.find("div", attrs={'class': 'Vbfug auoIOc'}).find("span").string.strip()
    except AttributeError:
        MakerName = "N/A"

    return MakerName


# Function to extract App's Download Count

def get_DownloadCount(soup):
    try:
        # Check if app is new to play store or not (if yes then it won't have section for reviews hence, we don't find next ClM70 class)
        if(get_AppRating(soup) == "New To google play store"):
            Download_count = soup.find("div", attrs={"class": "w7Iutd"}).find_next("div", attrs={"class": "ClM7O"}).get_text()
        else:
            # Extracting App's Download Count
            Download_count = soup.find("div", attrs={"class": "w7Iutd"}).find_next("div", attrs={"class": "ClM7O"}).find_next("div", attrs={"class": "ClM7O"}).get_text()

    except AttributeError:
        Download_count = "New to google play store"

    return Download_count


# Function to extract Application's Rating

def get_AppRating(soup):
    try:
        # Extracting Application's Ratings
        rating = soup.find("div", attrs={'class': 'w7Iutd'}).find("div", attrs={"class": "TT9eCd"}).get('aria-label')
    except AttributeError:
        rating = "New To google play store"

    # If the app is new to google play it won't have review section and hence we would get AttributeError, which we'll simply return without any slicing
    if(rating == "New To google play store"):
        return rating
    
    return rating[6:9]


# Function to extract Application's Review Count

def get_ReviewCount(soup):
    try:
        # Check if app is new to play store or not (if yes then it won't have section for reviews hence, we return "New To google play store")
        if(get_AppRating(soup) == "New To google play store"):
            rating_count = "New To google play store"
        else:
            # Extracting Application's Review Count
            rating_count = soup.find("div", attrs={'class': 'g1rdde'}).string.strip()
    except AttributeError:
        rating_count = "New To google play store"

    return rating_count


# Function to extract App's Developer Email

def get_Email(soup):
    try:
        # Extracting App's Developer Email
        dev_email = soup.find("div", attrs={'class': "pSEeg"}).find_next("div", attrs={'class': "pSEeg"}).string.strip()
    except AttributeError:
        dev_email = "N/A"

    return dev_email


# Function to extract Similar Applications related to given app

def get_SimilarApps1(soup):
    links = soup.find_all("a", attrs={'class': 'Si6A0c nT2RTe'})

    # Loop for extracting links from Tag Objects
    for link in links:
        links_list1.append("https://play.google.com"+link.get('href'))
    
    # As we don't want a list of links, we create a string out of it
    similar_apps = ''.join([str(item)+"\n" for item in links_list1])
    return similar_apps


# Function to extract Similar Applications related to Similar Applications of given app

def get_SimilarApps2(soup):
    links = soup.find_all("a", attrs={'class': 'Si6A0c nT2RTe'})
    # Store the links
    links_list2 = []

    # Loop for extracting links from Tag Objects
    for link in links:
        links_list2.append("https://play.google.com"+link.get('href'))
    
    # As we don't want a list of links, we create a string out of it
    similar_apps = ''.join([str(item)+"\n" for item in links_list2])
    return similar_apps


if __name__ == '__main__':

    # Add your user agent
    HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})

    # The webpage URL
    URL = "https://play.google.com/store/apps/details?id=com.galvanizetestprep.vocabbuilder&pli=1"

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Dictionary for storing all details and then creating a CSV file
    d1 = {"App Name": [], "Maker's Name": [], "Download Count": [], "Rating (OUT OF 5)": [], "Review Count": [], "Email from Description": [], "Similar App Links": []} 

    # Loop for extracting product details from each link
    print("Extracting details of the given app....")

    # Extracting details for the given app
    d1["App Name"].append(get_AppName(soup))
    d1["Maker's Name"].append(get_MakerName(soup))
    d1["Download Count"].append(get_DownloadCount(soup))
    d1["Rating (OUT OF 5)"].append(get_AppRating(soup))
    d1["Review Count"].append(get_ReviewCount(soup))
    d1["Email from Description"].append(get_Email(soup))
    d1["Similar App Links"].append(get_SimilarApps1(soup)) 

    print("Extraction completed for given app :)")

    # Loop for extracting product details from each link
    print("\nExtracting details of Similar Apps....")
    i = 0

    for item in links_list1:
        print("Running for App "+str(i+1))
        i +=1
        new_webpage = requests.get(item, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        d1["App Name"].append(get_AppName(new_soup))
        d1["Maker's Name"].append(get_MakerName(new_soup))
        d1["Download Count"].append(get_DownloadCount(new_soup))
        d1["Rating (OUT OF 5)"].append(get_AppRating(new_soup))
        d1["Review Count"].append(get_ReviewCount(new_soup))
        d1["Email from Description"].append(get_Email(new_soup))
        d1["Similar App Links"].append(get_SimilarApps2(new_soup))
    
    print("Extraction completed for similar apps :)")

    # Converting dictionary d1 to CSV file using pandas
    playStore_df = pd.DataFrame(d1)
    playStore_df.to_csv("PlayStore.csv", index=False)

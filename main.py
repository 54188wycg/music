# Initialize required libraries and browser instance
# DrissionPage.Chromium: For browser automation
# BeautifulSoup: For parsing HTML content
# time: For adding delays/wait times
# json: For handling JSON file operations
from DrissionPage import Chromium
from bs4 import BeautifulSoup
import time, json

# Initialize Chromium browser instance
browser = Chromium()

# Access Kugou Music homepage and navigate to Hot Songs Chart
# Get the latest active tab in the browser
tab1 = browser.latest_tab
# Navigate to Kugou Music official website
tab1.get('https://www.kugou.com/')

# Login verification and operation
# Parse the HTML content of tab1 using BeautifulSoup with html.parser
search1 = BeautifulSoup(tab1.html, 'html.parser')
# Check if the login button is visible (style attribute is None means visible)
if search1.find(class_="cmhead1_d5 _login").get('style') == None:
    # Click the login button to trigger login interface
    tab1.ele('css:.cmhead1_d5._login').click()
    # Loop to wait for login completion (check until login button is hidden)
    while True:
        # Re-parse HTML to check login status
        search1 = BeautifulSoup(tab1.html, 'html.parser')
        try:
            # If style attribute is not None, login is completed (button hidden)
            if search1.find(class_="cmhead1_d5 _login").get('style') != None:
                break
        except:
            # Ignore exceptions during status checking
            pass
        # Short delay to reduce CPU usage
        time.sleep(0.1)

# Click to enter Hot Songs Chart page
# Locate and click the second item (Hot Songs Chart) in the navigation menu
tab1.ele('css:#secoundContent .homep_d1_d2 .homep_d1_d2_d1 .homep_d1_d2_d1_a1:nth-of-type(2) .homep_cm_item_st1_d1').click()

# Custom wait function for different page loading scenarios
# Parameters:
#   x (str): Type of wait scenario - "song" for song playback page, "home" for homepage/search page
def wait(x):
    # Declare global variables to access/update across function scope
    global search1, search2, old, url
    
    # Wait scenario 1: Song playback page (wait for audio source URL to load)
    if x == "song":
        while True:
            # Parse playback page HTML
            search2 = BeautifulSoup(tab2.html, 'html.parser')
            # Locate audio element to get the song source URL
            audio_tag = search2.find(id="myAudio")
            url = audio_tag.get('src')
            # Short delay for URL loading
            time.sleep(0.1)
            
            # Handle pop-up dialog (play song dialog) if it appears
            if search2.find(class_="ui-dialog playsong") != None:
                # Close the pop-up dialog
                tab2.ele('css:.ui-dialog-close').click()
                # Click list button to reset playback state
                tab2.ele('css:#list.icon.list').click()
                # Reset URL to empty (invalid song source)
                url = ""
                break
            
            # Exit loop when new URL is loaded (different from old URL)
            if url != old:
                old = url
                break
    
    # Wait scenario 2: Homepage/search page (wait for page content to load)
    elif x == "home":
        while True:
            # 1-second delay to check page state
            time.sleep(1)
            # Re-parse homepage HTML
            search1 = BeautifulSoup(tab1.html, 'html.parser')
            # Check loading state via "before_page" element's style
            state = search1.find(id="before_page").get('style')
            # Additional short delay for state stability
            time.sleep(0.5)
            
            # Exit loop when page loading is complete (before_page is hidden)
            if state == "display: none;":
                break
    
    # Handle invalid parameter input
    else:
        raise ValueError('x is not "song" or "home", please re-enter.')

# Initialize empty list to store hot songs data
data = []
# 3-second delay to ensure hot songs page fully loads
time.sleep(3)

# Initialize song playback tab (get latest tab opened by Hot Songs Chart)
tab2 = browser.latest_tab
# Wait for playback page to start loading
tab2.wait.load_start()
# Click list button to show song list
tab2.ele('css:#list.icon.list').click()
# Initialize old URL variable to track song source changes
old = ''

# Scrape Hot Songs Chart (first 30 songs)
for i in range(30):
    # Click the (i+1)th song in the music list to play
    tab2.ele(f'css:#musicbox .musiclist li:nth-of-type({i+1})').click()
    # Wait for song playback URL to load
    wait("song")
    
    # Skip if URL is empty (invalid song source)
    if url == "":
        continue
    
    # Extract song name from the list
    names = search2.find_all('span', class_='musiclist-songname-txt')
    name = names[i].get('title')
    # Add song name and source URL to data list
    data.append({"name": name, "addr": url})

# Save hot songs data to hot.json file
# Use UTF-8 encoding to support Chinese characters
# ensure_ascii=False: Preserve non-ASCII characters (Chinese)
# indent=2: Pretty-print JSON with 2-space indentation
with open('hot.json', 'w+', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Update personalized playlist (student.json)
# Read existing student playlist data from JSON file
with open('student.json', 'r', encoding='utf-8') as f:
    x = json.load(f)

# Reset data list for new personalized playlist data
data = []
# Process first 100 songs in personalized playlist
for i in range(100):
    # Clear search input field
    tab1.ele("css:input").clear()
    # Input song name from student.json into search box
    tab1.ele("css:input").input(x[i]['name'])
    # Press ENTER key to trigger search
    tab1.actions.key_down('ENTER')
    
    # Wait for search results page to load
    wait("home")
    
    # Select the first search result (checkbox)
    tab1.ele('css:#search_song .list_content.clearfix li:nth-of-type(1) .search_icon.checkbox').click()
    # Click play button to load song playback page
    tab1.ele('css:#search_song .play_all .search_icon').click()
    
    # Wait for song playback URL to load
    wait("song")
    
    # Extract song source URL from audio element
    audio_tag = search2.find(id="myAudio")
    url = audio_tag.get('src')
    # Add updated song data to list
    data.append({"name": x[i]['name'], "addr": url})

# Save updated personalized playlist data back to student.json
with open('student.json', 'w+', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Update singer data (singers.json)
# Read existing singer data from JSON file
with open('singers.json', 'r', encoding='utf-8') as f:
    x = json.load(f)

# Reset data list for new singer data
data = []
# Process each singer in the singers.json list
for i in x:
    # Clear existing song list in playback page
    tab2.ele('css:.icon.list-menu-icon-del.clear').click()
    
    # Clear search input field
    tab1.ele("css:input").clear()
    # Input singer name into search box
    tab1.ele("css:input").input(i["name"])
    # Press ENTER key to trigger search
    tab1.actions.key_down('ENTER')
    
    # Wait for singer search results page to load
    wait('home')
    
    # Select all search results for the singer (check all checkbox)
    tab1.ele('css:#search_song .search_icon.checkall').click()
    # Click play all button to load all songs into playback list
    tab1.ele('css:#search_song .play_all .search_icon').click()
    
    # Initialize list to store songs for current singer
    songs = []
    # 3-second delay to ensure all songs load into playback list
    time.sleep(3)
    
    # Scrape first 30 songs for the current singer
    for j in range(30):
        # Click the (j+1)th song in playback list
        tab2.ele(f'css:#musicbox .musiclist li:nth-of-type({j+1})').click()
        # Wait for song URL to load
        wait("song")
        
        # Skip if URL is empty
        if url == "":
            continue
        
        # Extract song name
        names = search2.find_all('span', class_='musiclist-songname-txt')
        name = names[j].get('title')
        # Add song to current singer's song list
        songs.append({"name": name, "addr": url})
    
    # Add singer name and their songs to data list
    data.append({"name": i["name"], "songs": songs})

# Save updated singer data back to singers.json
with open('singers.json', 'w+', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Close the browser instance to clean up resources
browser.quit()

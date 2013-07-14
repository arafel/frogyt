#!/usr/bin/python

import httplib2
import os
import sys
import json
import string

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run

def jsonprint(item):
    return json.dumps(item, indent=4, separators=(',', ': '))

# CLIENT_SECRETS_FILE, name of a file containing the OAuth 2.0 information for
# this application, including client_id and client_secret. You can acquire an
# ID/secret pair from the API Access tab on the Google APIs Console
#   http://code.google.com/apis/console#access
# For more information about using OAuth2 to access Google APIs, please visit:
#   https://developers.google.com/accounts/docs/OAuth2
# For more information about the client_secrets.json file format, please visit:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
# Please ensure that you have enabled the YouTube Data API for your project.
CLIENT_SECRETS_FILE = "client_secrets.json"

# Helpful message to display if the CLIENT_SECRETS_FILE is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the APIs Console
https://code.google.com/apis/console#access

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# An OAuth 2 access scope that allows for full read/write access.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
  message=MISSING_CLIENT_SECRETS_MESSAGE,
  scope=YOUTUBE_READ_WRITE_SCOPE)

#storage = Storage("%s-oauth2.json" % sys.argv[0])
storage = Storage("%s-oauth2.json" % "playlist.py")
credentials = storage.get()

if credentials is None or credentials.invalid:
  credentials = run(flow, storage)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  http=credentials.authorize(httplib2.Http()))

def get_playlists(youtube):
    p = youtube.playlists()
    pagetoken = None
    totalresults = 0
    totalsofar = 0
    lastPage = False
    playlists = {}
    
    while True:
        # Get the response
        playlist_response = p.list(pageToken=pagetoken, part="snippet", mine=True, maxResults=50).execute()
    
        # Get housekeeping info from the response
        if playlist_response.has_key("nextPageToken"):
            pagetoken = playlist_response["nextPageToken"]
        else:
            print "No next page token, last page"
            lastPage = True
        pi = playlist_response["pageInfo"]
        if totalresults == 0:
            totalresults = pi["totalResults"]
        
        # Then process the items we wanted
        items = playlist_response["items"]
        totalsofar = totalsofar + len(items)
        for i in items:
            #print jsonprint(i)
            snippet = i["snippet"]
            title = snippet["title"]
            playlistid = i["id"]
            playlists[title] = playlistid
            #print "Playlist %s - id %s" % (title, playlistid)

        # Tell the user how we're doing
        print "Progress: %i/%i" % (totalsofar, totalresults)
        if totalsofar >= totalresults:
            print "Total so far (%i) >= totalresults (%i), break" % (totalsofar, totalresults)
            break
        if lastPage:
            print "Shouldn't reach this point"
            break

    return playlists

def get_playlist_items(playlist_id):
    p = youtube.playlistItems()
    playlist_response = p.list(playlistId=playlist_id, part="snippet", maxResults=50).execute()
    items = playlist_response["items"]
    for i in items:
        snippet = i["snippet"]
        print jsonprint(snippet)

    return None

if __name__ == "__main__":
    try:
        print "Loading playlists from JSON"
        playlists = json.load(open("playlists.json"))
    except:
        print "That didn't work; dumping from YouTube"
        playlists = get_playlists(youtube)
        open("playlists.json", "wb").write(json.dumps(playlists))

    print "Requesting Music playlist (id %s)" % playlists["Music"]
    items = get_playlist_items(playlists["Music"])
    if items:
        for i in items:
            print i

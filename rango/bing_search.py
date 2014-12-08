import json
import urllib,urllib2
from keys import BING_API_KEY
import sys

def run_query(search_terms):
    # Specify the base
    root_url = 'https://api.datamarket.azure.com/Bing/Search/'
    source = 'Web'

    # Specify how many results we wish to be returned per page
    # Offset specifies where in the results lists to start from
    # with results_per_page = 10 and offset = 11, this would start from page 2.
    results_per_page = 10
    offset = 0

    # Wrap quotes around our query terms as required by the Bing API.
    # The query we will then use is stored within variable query.
    query = "'{0}'".format(search_terms)
    query = urllib.quote(query)

    # Construct the latter part of our request's URL
    # Sets the format of the response to JSON ans sets others properties
    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url,
        source,
        results_per_page,
        offset,
        query)

    # Setup authentication with Bing Servers
    # The username MUST be a blank string, and put in your API key
    username = ''

    # Create a 'password_manager' which handles authentication for us
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None,search_url,username,BING_API_KEY)

    # Create our results list which we will populate
    results = []

    try:
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)

        # Connect to te server and read the response generated.
        response = urllib2.urlopen(search_url).read()

        # Convert the string response to a Python dictionary object
        json_response = json.loads(response)

        # Loop through each page returned, populatin out result list
        for result in json_response['d']['results']:
            results.append({
                'title': result['Title'],
                'link': result['Url'],
                'summary': result['Description']
                })
    # Catch a URLError exception - something went wrong when connecting
    except urllib2.URLError, e:
        print "Error when querying the Bing API: ", e

    # return the results
    return results


def main():
    arg = str(sys.argv[1])
    print BING_API_KEY
    print "arg :%s" % arg
    results = run_query(arg)
    for result in results:
        print "title : %s" % result['title']
        print "link : %s" % result['link']
        print "Description : %s" % result['summary']





if __name__ == "__main__":
    main()







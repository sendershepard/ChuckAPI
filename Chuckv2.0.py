import requests
import random

class LolWut(object):
    pass

class ChuckNorrisJokesAPI(object):
    def __init__(self):
        self = [] # You set up the new object instance here
    
    def get_categories(self):
        """
        Queries the API for a list of categories, and returns a copy
        of the list.
        """
        categories_response = requests.get('https://api.chucknorris.io/jokes/categories')
        c_js = categories_response.json()

        return (c_js)

    def get_random_joke(self, category=None):
        """
        Gets a random joke from the API.

        If category is present, then we'll only get a random joke from
        the provided category.
        """
        if category:
            payload = {'category': category}
            response = requests.get('https://api.chucknorris.io/jokes/random', params=payload)
            if response.status_code != 200:
                return False
        else:
            response = requests.get('https://api.chucknorris.io/jokes/random')

        r_js = response.json()['value']

        return (r_js)
 
    def search_jokes(self, query):
        """
        For now, just do the search and return the raw results!
        We'll make this more powerful in the future! :)
        """
        payload = {'query': query}
        query = requests.get('https://api.chucknorris.io/jokes/search', params=payload)
        if query.status_code != 200:
            print('Sorry, but no matches were found for keyword', query, '. Please try again.')
        else:
            return False 

        s_js = query.json()
        jokes = s_js['result']

        print('\nYour query brought back ', len(jokes), ' results.')

        return (s_js)

def demo_commands():
    chuck = ChuckNorrisJokesAPI()
    # Calling this twice should only hit the API once (hint: you'll
    # need to store the results on the object instance of self)
    categories = chuck.get_categories()
    categories = chuck.get_categories()
    # These should both work
    joke = chuck.get_random_joke()
    joke = chuck.get_random_joke(categories[0])
    # You should handle this error case
    joke = chuck.get_random_joke("does-not-exist")
    # And this should obviously work
    jokes = chuck.search_jokes("dork")

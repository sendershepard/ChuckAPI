import requests
import random

class ChuckNorrisJokesAPI(object):
    def __init__(self):
        self.categories_cache = None 
 
    def _get_categories(self):
        """
        Private function that hits the remote API
        """
        #print("Hitting the remote API")
        categories_response = requests.get('https://api.chucknorris.io/jokes/categories')
        c_js = categories_response.json()

        return (c_js)

    def categories(self):
        """
        Public method that queries the API for a list of categories, and returns a copy
        of the list.
        """
        if not self.categories_cache: 
            self.categories_cache = self._get_categories() 
        return self.categories_cache.copy()

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
            return False 

        s_js = query.json()

        return (s_js)

class ChuckNorrisJokesMain(object):

    def __init__(self):
        self.api = ChuckNorrisJokesAPI()

    def run(self):

        print('\nHere are the categories to chose from: \n')
        categories = self.api.categories()
        for cat in categories:
            print(cat)
            
        while True:
            user_input = input('\nPlease input category: ')
            if user_input not in categories:
                print('Error, not proper input. Please try again.')
            else:
                #print("\nJoke in category, ", user_input, " is:\n")    
                #c_joke = self.api.get_random_joke(user_input)
                #print(c_joke)
                break
        
        print("\nHere is a random joke:\n")
        joke = self.api.get_random_joke()
        print(joke)

        

def demo_commands():
    chuck = ChuckNorrisJokesAPI()
    # Calling this twice should only hit the API once (hint: you'll
    # need to store the results on the object instance of self)
    categories = chuck.categories()
    categories = chuck.categories()
    # These should both work
    joke = chuck.get_random_joke()
    joke = chuck.get_random_joke(categories[0])
    # You should handle this error case
    joke = chuck.get_random_joke("does-not-exist")
    # And this should obviously work
    jokes = chuck.search_jokes("dork")

if __name__ == '__main__':
    main = ChuckNorrisJokesMain()
    main.run() #all of interactions and ...... 

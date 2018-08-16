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

        r_js = response.json()

        return (r_js)
 
    def search_jokes(self, query):
        """
        For now, just search and return the raw results!
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
        """
        Calling the categories so that the user can chose from.
        """
        print('\nHere are the categories to chose from: \n')
        categories = self.api.categories()
        for cat in categories:
            print(cat)

        """
        Calling the get_random_joke with user input.
        """
        while True:
            user_input = input('\nPlease input category: ')
            if user_input not in categories:
                print('Error, not proper input. Please try again.')
            else:
                print("\nA random joke in category, '", user_input, "' is:\n")    
                c_joke = self.api.get_random_joke(user_input)
                print(c_joke['value'])
                break

        print("\nHere is a random joke:\n")
        joke = self.api.get_random_joke()
        print(joke['value'])

        """
        User is prompted to enter a query to search the API's jokes that match the query.
        If the query returns multiple results the user will be provided a random joke and
        this joke will be popped off from the stack and will show more if user enters 'y'
        """
        while True:
            user_query = input('\nPlease enter a query: ')
            query = self.api.search_jokes(user_query)
            if query == False:
                print('Sorry, but no matches were found for keyword', user_query, '. Please try again.') 
            else:
                break

        s_jokes = query['result']
        print('\nYour query brought back ', len(s_jokes), ' results.')
        
        user_input = 'y'
        while (len(s_jokes)) and (user_input == 'y'):
            print('We will chose a random joke from the results for you: ')
            rand = random.randint(0, (len(s_jokes) - 1))
            print('\n', s_jokes[rand]['value'])
            del s_jokes[rand]

            print('\nThere are ', len(s_jokes), ' left.')
            user_input = input('\n Do you want to another? "y" or "n"')


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
    main.run()

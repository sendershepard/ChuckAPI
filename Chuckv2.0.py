import requests
import random


class ChuckAPIError(Exception):
    """ Base class for exceptions in this API. """
    pass


class InvalidCategoryError(ChuckAPIError): 
    """ Exceptions raised for errors in input. """
    pass 


class ChuckNorrisJokesAPI(object):
    BASE_URI = 'https://api.chucknorris.io/jokes'
    
    def __init__(self):
        self.categories_cache = None

    def _fetch(self, path, payload=None): 
        """
        Refacturing code to create a path definition that will bring the json
        if link responds as found, else raise an exception.
        """
        headers = {"accept": "application/json"}
        
        self.response = requests.get(self.BASE_URI + path, headers=headers, params=payload)
        if self.response.status_code != 200:
            raise ChuckAPIError("Failed to obtain a valid kind for %r Status Code: %r" % (path, self.response.status_code))

        return self.response.json()
 
    def _get_categories(self):
        """ Private function that hits the remote API. """
        return self._fetch(path='/categories', payload=None)

    def categories(self):
        """ Fetches the API for a list of categories, and returns a copy. """
        if not self.categories_cache: 
            self.categories_cache = self._get_categories()
            
        return self.categories_cache.copy()

    def get_random_joke(self, category=None):
        """
        Gets a random joke from the API.

        If category is present, then we'll only get a random joke from
        the provided category.
        """
        payload = None
        
        if category:
            if category not in self.categories():
                raise InvalidCategoryError("%r is not a valid category" % category)
            payload = {'category': category}
        
        return self._fetch('/random',payload)

 
    def search_jokes(self, query):
        """ Just searches and returns the raw results! """
        return  self._fetch('/search', payload={'query': query}) 



class ChuckNorrisJokesMain(object):
    def __init__(self):
        self.api = ChuckNorrisJokesAPI()

    def run(self):
        print("\n***Welcome to the Chuck Norris (satirical) facts page!***")

        user_input = 'y'
        while(user_input == 'y'):
            self.chuck_menu()
            user_input = input('\n Do you want to go back to the main menu? "y" or "n"')

        print("\n***Thank you for visiting the Chuck Norris (satirical) facts page!***")


    def random_joke(self):
        print("\nHere is a random joke:\n")
        print(self.api.get_random_joke()['value'])

    def categories(self):
        """ Calling the categories so that the user can chose from. """
        print('\nHere are the categories to chose from: \n')
        categories = self.api.categories()
        for cat in categories:
            print(cat)

        """ Calling the get_random_joke based on category. """
        while True:
            user_input = input('\nPlease input category: ')
            if user_input not in categories:
                print('Error, not proper input. Please try again.')
            else:
                print("\nA random joke in category, '", user_input, "' is:\n")    
                c_joke = self.api.get_random_joke(category = user_input)
                print(c_joke['value'])
                break
            
    def search_joke(self):
        """
        User is prompted to enter a query to search the API's jokes that match the query.
        If the query returns multiple results the user will be provided a random joke and
        this joke will be popped off from the stack and will show more if user enters 'y'
        """
        while True:
            try:
                user_query = input('\nPlease enter a query: ')
                query = self.api.search_jokes(user_query)
                if type(query) != dict:
                    raise ChuckAPIError
                break
            except ChuckAPIError:
                print("\n'Sorry, but no matches were found for keyword", user_query, ". Please try again.")
            
            
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

    def chuck_menu(self):
        print("\nPlease pick from the Menu below: ")
        print("\nFor a random fact enter: 1")
        print("For a random fact based on category enter: 2")
        print("To search a fact using a key-word enter: 3\n")

        entries=["1", "2" ,"3"]
        while True:
            ans = self.prompt_user(prompt="Please pick a number",
                                   reminder="Input must match the options!",
                                   entries=entries)
            if ans in entries:
                break
            
        if ans == "1":
            self.random_joke()
        elif ans == "2":
            self.categories()
        elif ans == "3":
            self.search_joke()

    def prompt_user(self, prompt, reminder=None, entries=None):
        while True:
            user_answer = input(prompt)
            if user_answer in entries:
                return user_answer
            else:
                print(reminder)
                return False
        

""" Main """
if __name__ == '__main__':
    main = ChuckNorrisJokesMain()
    main.run()

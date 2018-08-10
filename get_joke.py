import requests
import random

def chuck_random_joke():
       random_response = requests.get('https://api.chucknorris.io/jokes/random')
       r_js = random_response.json()

       print('\n', r_js['value'], '\n')

def chuck_categories():
       categories_response = requests.get('https://api.chucknorris.io/jokes/categories')
       c_js = categories_response.json()
       print('\nHere are the categories to chose from: \n')
       
       for w in c_js:
              print(w)

       while True:
           user_input = input('\nPlease input category: ')
           if user_input not in c_js:
               print('Error, not proper input. Please try again.')
           else:
               break

       payload = {'category': user_input}
       j_category = requests.get('https://api.chucknorris.io/jokes/random', params=payload)

       cat = j_category.json()

       print('\n', cat['value'])

#def chuck_query():
while True:
       user_query = input('\nPlease enter a query: ')
       payload = {'query': user_query}
       query = requests.get('https://api.chucknorris.io/jokes/search', params=payload)
       if query.status_code != 200:
              print('Sorry, but no matches were found for keyword', user_query, '. Please try again.')
       else:
              break

q_js = query.json()
jokes = q_js['result']
print('\nYour query brought back ', len(jokes), ' results.')


user_input = 'y'
while (len(jokes)) and (user_input == 'y'):
       print('We will chose a random joke from the results for you: ')
       rand = random.randint(0, (len(jokes) - 1))
       print('\n', jokes[rand]['value'])
       del jokes[rand]

       print('\nThere are ', len(jokes), ' left.')
       user_input = input('\n Do you want to another? "y" or "n"')
       
    



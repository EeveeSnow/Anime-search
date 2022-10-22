# Here we define our query as a multi-line string
from pprint import pprint
import requests


query = '''
query ($name: String) { # Define which variables will be used in the query (id)
  Media (search: $name, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
    idMal
    description
    tags {
      name
    }
    title {
      romaji
      english
      native
    }
  }
}
'''

# Define our query variables and values that will be used in the query request
variables = {
    'name': "22/7"
}

url = 'https://graphql.anilist.co'

# Make the HTTP Api request
response = requests.post(url, json={'query': query, 'variables': variables})
js = response.json()['data']['Media']
pprint(response.json())
tags = js["tags"][0:5]
jp_name = js["title"]["native"]
id = js['idMal']
description = js['description']
pprint(tags)
pprint(jp_name)
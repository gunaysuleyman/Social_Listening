import os
from dotenv import load_dotenv
import requests

load_dotenv()  
API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"

def search_movie_or_tv(name, content_type):
    """
    Search for a movie or TV show by name and return the first match.
    """
    if content_type == "movie":
        search_url = f"{BASE_URL}/search/movie"
    elif content_type == "tv":
        search_url = f"{BASE_URL}/search/tv"
    else:
        print("Invalid content type. Please choose 'movie' or 'tv'.")
        return None

    params = {
        "api_key": API_KEY,
        "query": name,
        "language": "tr-TR" 
    }
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0] 
        else:
            print("No results found.")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

def get_cast(content_type, content_id):
    """
    Get the cast of a movie or TV show by its ID.
    """
    if content_type == "movie":
        credits_url = f"{BASE_URL}/movie/{content_id}/credits"
    elif content_type == "tv":
        credits_url = f"{BASE_URL}/tv/{content_id}/credits"
    else:
        print("Invalid content type. Please choose 'movie' or 'tv'.")
        return []

    params = {
        "api_key": API_KEY
    }
    response = requests.get(credits_url, params=params)
    if response.status_code == 200:
        data = response.json()
        cast = data.get('cast', [])
        return [actor['name'] for actor in cast] 
    else:
        print(f"Error: {response.status_code}")
        return []

def main():
    name = input("Enter the name of the movie or TV show: ")
    content_type = input("Is it a movie or a TV show? (Enter 'movie' or 'tv'): ").strip().lower()

    if content_type not in ["movie", "tv"]:
        print("Invalid input. Please enter 'movie' or 'tv'.")
        return

    result = search_movie_or_tv(name, content_type)
    if result:
        title = result.get('title') if content_type == "movie" else result.get('name')
        release_date = result.get('release_date') if content_type == "movie" else result.get('first_air_date')
        content_id = result['id']

        print(f"Found: {title} ({release_date})")
        cast = get_cast(content_type, content_id)
        if cast:
            print(f"Cast of '{title}':")
            for actor in cast:
                print(actor)
        else:
            print("No cast information found.")
    else:
        print("No results found.")

if __name__ == "__main__":
    main()
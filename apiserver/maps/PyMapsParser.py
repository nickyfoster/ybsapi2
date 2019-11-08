import random

import googlemaps
from resources import keywords
import auth


# TODO keywords repeating bug
# TODO form pictures

# About 10, 4 random, 4 interest, 4 overall interests

class PyMapsParser:
    """Custom Google Maps API class for searching new place."""
    """Nick: remember to set_coordinates first!"""

    def __init__(self, language='ru', radius=5000):
        self.gmaps = googlemaps.Client(key=auth.google_maps_API)  # Google Maps API initialization
        self.coordinates = (59.93555, 30.321777)  # The lat/lon center point values. Default: Saint-Petersburg center
        self.language = language  # The language in which to return results.
        self.radius = radius  # Distance in meters within which to bias results.

    def set_coordinates(self, custom_coordinates):
        self.coordinates = custom_coordinates

    def get_places_by_query(self, search_text):
        return self.gmaps.places_autocomplete_query(input_text=search_text, location=self.coordinates,
                                                    radius=self.radius, language=self.language)

    def get_place_info_by_id(self, place_id):
        place_info = self.gmaps.place(place_id=place_id, language='ru')
        return place_info

    def get_parsed_places(self, search_text):
        parsed_places = []
        # search_text += ' '
        print(f"\t**** SEARCHING FOR: {search_text} ****")
        unparsed_places = self.gmaps.places_autocomplete_query(input_text=search_text, location=self.coordinates,
                                                               radius=self.radius, language=self.language)
        for place in unparsed_places:
            try:
                parsed_places.append({'place_description': place['description'], 'place_id': place['place_id']})
                break  # ust one place for one keyword
            except Exception:
                pass
        return parsed_places

    def get_random_place(self):
        N_RANDOM_WORDS = 6
        random_places = []
        words = set(['музыка', 'ресторан', 'кинотеатр', 'столовая', 'музей', 'кафе', 'спортзал', 'театр', 'продукты',
                     'пекарня', 'цирк', 'бар', 'живая музыка', 'торговый центр', 'одежда', 'спа'])
        random_words = random.sample(words, N_RANDOM_WORDS)
        for random_word in random_words:
            random_places.extend(self.format_recommended_places([self.get_parsed_places(random_word)], True))
        return random_places

    def get_recommended_places(self, true_user_keywords):
        recommended_places = []
        for keyword in true_user_keywords:
            recommended_places.append(self.get_parsed_places(keyword))
        return recommended_places

    def format_place(self, place_id, place_description, isRandom):
        formatted_data = {}
        place_data = self.get_place_info_by_id(place_id)
        try:
            formatted_data['name'] = place_data['result']['name']
            formatted_data['description'] = place_description
            formatted_data['address'] = place_data['result']['formatted_address']
            formatted_data['phone'] = place_data['result']['international_phone_number']
            formatted_data['website'] = place_data['result']['website']
            formatted_data['icon'] = place_data['result']['icon']
            formatted_data['url'] = place_data['result']['url']
            formatted_data['rating'] = place_data['result']['rating']
            formatted_data['user_ratings_total'] = place_data['result']['user_ratings_total']
            formatted_data[
                'photo_url'] = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={place_data['result']['photos'][0]['photo_reference']}&key={auth.google_maps_API}"

        except Exception as e:
            pass

        if isRandom:
            formatted_data['isRandom'] = 1
        else:
            formatted_data['isRandom'] = 0

        return formatted_data

    def format_recommended_places(self, recommended_places, isRandom):
        formatted_recommended_places = []
        for places in recommended_places:
            for place in places:
                formatted_recommended_places.append(
                    self.format_place(place['place_id'], place['place_description'], isRandom))

        return formatted_recommended_places

    # Magic begins here

    def get_random_place(self):
        N_RANDOM_WORDS = 5
        random_places = []
        random_words = random.sample(set(keywords.words), N_RANDOM_WORDS)
        for random_word in random_words:
            random_places.extend(self.find_one_place(random_word))
        return random_places


    def find_one_place(self, search_text):
        unparsed_places = self.gmaps.places_nearby(keyword=search_text, location=self.coordinates,
                                                   radius=self.radius, language=self.language, rank_by='prominence')
        data = []
        count = 0
        for place in unparsed_places['results']:
            if count == 3:
                break
            temp = {}
            try:
                temp['name'] = place['name']
                temp['types'] = place['types']
                temp['address'] = place['vicinity']
                temp['rating'] = place['rating']
                temp['user_ratings_total'] = place['user_ratings_total']
                temp[
                    'photo_url'] = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={place['photos'][0]['photo_reference']}&key={auth.google_maps_API}"
                temp['key_word'] = search_text
                data.append(temp)
                count += 1
            except Exception as e:
                pass

        return data

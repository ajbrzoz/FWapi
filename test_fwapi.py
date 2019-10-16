import datetime
import unittest

from fwapi.film import Film
from fwapi.person import Person
from fwapi.utils import make_request


class TestFilm(unittest.TestCase):
    
    def setUp(self):
        self.films = list(Film.search("john malkovich"))
        self.example = self.films[0]
        
        #several directors, screenwriters, genres, countries
        self.soup = make_request("http://www.filmweb.pl/Matrix")
        
        #no descrition; duration less than hour
        self.soup2 = make_request("http://www.filmweb.pl/film/Sipur+Ahava-1990-352246")
        
    def test_search_single_page(self):
        """
        One page of results - no pagination
        """
        self.assertEqual(len(self.films), 4)
        self.assertIsInstance(self.example, Film)
        self.assertEqual(self.example.title, "Być jak John Malkovich")
        self.assertEqual(self.example.url, "http://www.filmweb.pl/film/By%C4%87+jak+John+Malkovich-1999-868")
        self.assertEqual(self.example.year, 1999)
        self.assertEqual(self.example.id_, 868)

    def test_search_multiple_pages(self):
        """
        Walking through a series of pages
        """
        results = list(Film.search("terminator", max_page=3))
        single_film = results[0]
        self.assertEqual(len(results), 28)
        self.assertIsInstance(single_film, Film)
        self.assertEqual(single_film.title, "Terminator: Mroczne przeznaczenie")
        self.assertEqual(single_film.url, "http://www.filmweb.pl/film/Terminator%3A+Mroczne+przeznaczenie-2019-723372")
        
    def test_search_no_results(self):
        results = list(Film.search("sdfghjfghj"))
        self.assertListEqual(results, [])
        
    def test_get_by_id(self):
        film = Film.get_by_id(868)
        self.assertIsInstance(film, Film)
        self.assertEqual(film.title, "Być jak John Malkovich")
        self.assertEqual(film.url, "http://www.filmweb.pl/film/By%C4%87+jak+John+Malkovich-1999-868")
        self.assertEqual(film.year, 1999)
        self.assertEqual(film.id_, 868)
        
    def test_get_by_id_not_found(self):
        film = Film.get_by_id(67825)
        self.assertIsNone(film)
        
    def test_parse_actors(self):
        actors = Film.parse_actors(self.soup)
        expected = {'Julian Arahanga': 'Apoc', 'Carrie-Anne Moss': 'Trinity',
                    'Gloria Foster': 'Wyrocznia', 'Marcus Chong': 'Tank',
                    'Hugo Weaving': 'Agent Smith', 'Keanu Reeves': 'Neo',
                    'Laurence Fishburne': 'Morfeusz', 'Joe Pantoliano': 'Cypher'}
        self.assertDictEqual(actors, expected)
        
    def test_parse_country(self):
        countries = Film.parse_country(self.soup)
        self.assertListEqual(countries, ["Australia", "USA"])
        
    def test_parse_description(self):
        descr = Film.parse_description(self.soup)
        expected = "Haker komputerowy Neo dowiaduje się od tajemniczych " \
                   "rebeliantów, że świat, w którym żyje, jest tylko " \
                   "obrazem przesyłanym do jego mózgu przez roboty."
        self.assertEqual(descr, expected)
        
    def test_parse_no_description(self):
        """
        Film has no description
        """
        descr = Film.parse_description(self.soup2)
        self.assertEqual(descr, "")

    def test_parse_director(self):
        directors = Film.parse_director(self.soup)
        self.assertListEqual(directors, ["Lilly Wachowski", "Lana Wachowski"])

    def test_parse_duration(self):
        dur = Film.parse_duration(self.soup)
        self.assertEqual(dur, datetime.time(2, 16))

    def test_parse_duration_lt_hour(self):
        """
        Film is shorter than 1 hour
        """
        dur = Film.parse_duration(self.soup2)
        self.assertEqual(dur, datetime.time(0, 30))

    def test_parse_genre(self):
        genres = Film.parse_genre(self.soup)
        self.assertListEqual(genres, ["Akcja", "Sci-Fi"])

    def test_parse_original_title(self):
        o_title = Film.parse_original_title(self.soup)
        self.assertEqual(o_title, "The Matrix")

    def test_parse_screenwriter(self):
        screenwriters = Film.parse_screenwriter(self.soup)
        self.assertListEqual(screenwriters, ["Lilly Wachowski", "Lana Wachowski"])

    def test_populate_film(self):
        self.example.populate()
        expected_actors = {'Catherine Keener': 'Maxine Lund', 'Gregory Sporleder': 'Meżczyzna w barze',
                    'John Cusack': 'Craig Schwartz', 'Willie Garson': 'Facet w restauracji',
                    'W. Earl Brown': 'Pierwszy klient J.M. Inc.', 'Orson Bean': 'Dr Lester',
                    'Cameron Diaz': 'Lotte Schwartz', 'Mary Kay Place': 'Floris'}
        expected_description = "Pracownik odnajduje w swoim biurze drzwi prowadzące do " \
                               "świadomości znanego aktora - Johna Malkovicha."
        
        self.assertDictEqual(self.example.actors, expected_actors)
        self.assertListEqual(self.example.country, ["USA"])
        self.assertEqual(self.example.description, expected_description)
        self.assertListEqual(self.example.director, ["Spike Jonze"])
        self.assertEqual(self.example.duration, datetime.time(1, 52))
        self.assertListEqual(self.example.genre, ["Surrealistyczny", "Komedia"])
        self.assertEqual(self.example.original_title, "Being John Malkovich")
        self.assertListEqual(self.example.screenwriter, ["Charlie Kaufman"])


class TestPerson(unittest.TestCase):
    
    def setUp(self):
        self.people = list(Person.search("john malkovich"))
        self.example = self.people[0]
        
        self.soup = make_request("http://www.filmweb.pl/person/John.Malkovich")
        
    def test_search_person(self):
        self.assertEqual(len(self.people), 1)
        self.assertIsInstance(self.example, Person)
        self.assertEqual(self.example.name, "John Malkovich")
        self.assertEqual(self.example.url, "http://www.filmweb.pl/person/John.Malkovich")
        
    def test_parse_full_name(self):
        full_name = Person.parse_full_name(self.soup)
        self.assertEqual(full_name, "John Gavin Malkovich")

    def test_parse_birth_date(self):
        bd = Person.parse_birth_date(self.soup)
        self.assertEqual(bd, datetime.date(1953, 12, 9))

    def test_parse_filmography(self):
        filmography = Person.parse_filmography(self.soup)
        self.assertEqual(len(filmography.keys()), 113)
        self.assertIn("Być jak John Malkovich", filmography)
        
    def test_populate_person(self):
        self.example.populate()
        self.assertEqual(self.example.full_name, "John Gavin Malkovich")
        self.assertEqual(self.example.birth_date, datetime.date(1953, 12, 9))
        self.assertEqual(len(self.example.filmography.keys()), 113)
        self.assertIn("Być jak John Malkovich", self.example.filmography)

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestFilm))
suite.addTest(unittest.makeSuite(TestPerson))
unittest.TextTestRunner().run(suite)

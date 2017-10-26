# FWapi
Simple Python API for Filmweb.pl website

## Installation

Use pip to install:

    $ pip install fwapi

## Usage

### Searching for films

You can find a film using its id:

    >>> from fwapi.film import Film
    >>> film = Film.get_by_id(995)
    >>> film.title
    'Terminator'
    >>> film.year
    1984
    >>> film.url
    'http://www.filmweb.pl/Terminator'

In order to get more details, you need to populate the object first:

    >>> film.populate()
    >>> film.original_title
    'The Terminator'
    >>> film.duration
    datetime.time(1, 47)    # 1h 47min
    >>> film.director
    ['James Cameron']
    >>> film.screenwriter
    ['James Cameron', 'Gale Anne Hurd']
    >>> film.genre
    ['Akcja', 'Sci-Fi']
    >>> film.country
    ['USA', 'Wielka Brytania']
    >>> film.description
    'Elektroniczny morderca zostaje wysłany z przyszłości do roku 1984, by zabić matkę przyszłego lidera rewolucji. W ślad za nim              rusza Kyle Reese, który ma chronić kobietę.'
    >>> film.actors
    {'Paul Winfield': 'Porucznik Ed Traxler', 'Arnold Schwarzenegger': 'Terminator', 'Earl Boen': 'Dr Peter Silberman', 'Michael     Biehn': 'Kyle Reese', 'Linda Hamilton': 'Sarah Connor', 'Lance Henriksen': 'Detektyw Hal Vukovich', 'Bess Motta': 'Ginger Ventura', 'Rick Rossovich': 'Matt Buchanan'}   #actors with roles

You can also search for films by their title. In this case it returns a generator:

    >>> films = Film.search("terminator")
    >>> films
    <generator object FilmwebObject.search at 0x7fafb6fdc888>
    >>> list_of_films = list(films)
    >>> list_of_films
    [<Terminator: 1984>, <Terminator 2: Dzień sądu: 1991>, <Terminator: Ocalenie: 2009>, <Terminator: Genisys: 2015>, <Terminator 3: Bunt maszyn: 2003>, <Terminator II: 1989>, <Terminator 6: 2019>, <Terminator 3: 2018>, <Terminator i Bond w jednym: 1992>, <Ninja Terminator: 1985>]
    >>> list_of_films[0].title
    'Terminator'

If the results are displayed on several pages, by default you get only those from the first one. Although you can change set the number of pages you want to retrieve the data from:

    >>> films = Film.search("terminator", max_page=2)
    >>> list_of_films = list(films)
    >>> list_of_films
    [<Terminator: 1984>, <Terminator 2: Dzień sądu: 1991>, <Terminator: Ocalenie: 2009>, <Terminator: Genisys: 2015>, <Terminator 3: Bunt maszyn: 2003>, <Terminator II: 1989>, <Terminator 6: 2019>, <Terminator 3: 2018>, <Terminator i Bond w jednym: 1992>, <Ninja Terminator: 1985>, <Alien Terminator: 1995>, <Terminator Woman: 1993>, <Russian Terminator: 1989>, <Terminator: Termination: 2011>, <The Making of 'Terminator': 1984>, <RoboCop vs Terminator: 2006>, <Boyong Manalac Hoodlum Terminator: 2001>, <The (Ex)terminator: 2011>, <The Terminator-Retired: 2013>, <The Terminator: Anatoly Onoprienko: 2007>]

### Searching for people

    >>> from fwapi.person import Person
    >>> people = Person.search("James Cameron")
    >>> list_of_people = list(people)
    >>> list_of_people
    [<James Cameron I>, <James Cameron VII>, <James Cameron XIX>, <James Cameron XI>, <James Cameron II>, <James Cameron XV>, <Sean James Cameron>, <Michael James Cameron>, <Stuart James Cameron>, <Ian James Cameron>]
    >>> jc = list_of_people[0]
    >>> jc.name
    'James Cameron I'
    >>> jc.url
    'http://www.filmweb.pl/person/James.Cameron'

If you need to get more detailed information, first you need to populate the object:

    >>> jc.full_name
    'James Francis Cameron'
    >>> jc.birth_date
    datetime.date(1954, 8, 16)

You can also retrieve the person's filmography which is an ordered dictionary with entries in the following form: Film title: (role [for actors], year of production):

    >>> jc.filmography
    OrderedDict([('Avatar 5', ('', 2025)), ('Avatar 4', ('', 2024)), ('Avatar 3', ('', 2021)), ('Avatar 2', ('', 2020)), ('Avatar', ('', 2009)), ('Obcy z głębin', ('', 2005)), ('Głosy z głębin 3D', ('', 2003)), ('Ekspedycja: Bismarck', ('', 2002)), ('Titanic', ('Tancerz z przedziału najtańszej klasy', 1997)), ('T2 3-D: Battle Across Time', ('', 1996)), ('Prawdziwe kłamstwa', ('', 1994)), ('Terminator 2: Dzień sądu', ('', 1991)), ...

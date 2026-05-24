import datetime

AUTHOR = 'Ivan VenOsdel'
SITENAME = 'ramblin.dev'
SITEURL = ""
SITEYEAR = datetime.date.today().year
THEME = "themes/ramblin-simple"

THEME_STATIC_DIR = 'theme'
THEME_STATIC_PATHS = ['static']

PATH = "content"

# Files copied verbatim to the site root (robots.txt, llms.txt, IndexNow key).
STATIC_PATHS = ['extra']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/llms.txt': {'path': 'llms.txt'},
    'extra/b6746e9d951fd5f64f1059f04b919e7e94b15f34f85d8d903c73a6eb75c5f0d3.txt': {
        'path': 'b6746e9d951fd5f64f1059f04b919e7e94b15f34f85d8d903c73a6eb75c5f0d3.txt'
    },
}

PLUGINS = ['pelican.plugins.sitemap']

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.8,
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'weekly',
        'pages': 'monthly',
    },
}

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

LINKS = ()
SOCIAL = ()
MENUITEMS = ()

DEFAULT_PAGINATION = False
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

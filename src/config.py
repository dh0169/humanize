import os
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DATABASE_URI = os.environ.get("DATABASE_URI")
FLASK_SECRET_KEY = os.environ.get("SECRET_KEY")


HUMANIZE_ADMIN = os.environ.get("HUMANIZE_ADMIN")
HUMANIZE_ADMIN_PW = os.environ.get("HUMANIZE_ADMIN_PW")

HUMANIZE_TESTER1 = os.environ.get("HUMANIZE_TESTER1")
HUMANIZE_TESTER1_PW = os.environ.get("HUMANIZE_TESTER1_PW")

HUMANIZE_TESTER2 = os.environ.get("HUMANIZE_TESTER2")
HUMANIZE_TESTER2_PW = os.environ.get("HUMANIZE_TESTER2_PW")

HUMANIZE_TESTER3 = os.environ.get("HUMANIZE_TESTER3")
HUMANIZE_TESTER3_PW = os.environ.get("HUMANIZE_TESTER3_PW")


HUMANIZE_ORIGINS = os.environ.get("HUMANIZE_ORIGINS", ["http://localhost:3000", "https://humanize.live"])


auth = HTTPBasicAuth()

# if debugging
users = {
    HUMANIZE_ADMIN: generate_password_hash(HUMANIZE_ADMIN_PW),
    HUMANIZE_TESTER1: generate_password_hash(HUMANIZE_TESTER1),
    HUMANIZE_TESTER2: generate_password_hash(HUMANIZE_TESTER2),
    HUMANIZE_TESTER3: generate_password_hash(HUMANIZE_TESTER3),
}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


WS_URL = "/chat"


usernames = [
    "notabot",
    "smoot",
    "bebo",
    "pizzaboi",
    "eggboi",
    "snugglebug",
    "fluffcake",
    "bloopster",
    "jellybeaner",
    "muffinbun",
    "pudgycat",
    "noodlemon",
    "chunkydino",
    "gigglepuff",
    "tacocat",
    "chickennug",
    "honeybunz",
    "squishmallow",
    "quackduck",
    "biscuitboi",
    "cuddlecloud",
    "twinklebop",
    "wafflewhizz",
    "sporkmuffin",
    "puffysocks",
    "grumpygoose",
    "boopitybop",
    "pebbleskip",
    "bubblewrapz",
    "sillypanda",
    "poprockz",
    "smolbun",
    "lazysloth",
    "doodlefizz",
    "zippytaco",
    "grapejello",
    "ticklebunz",
    "gumbobuddy",
    "donutbop",
    "fuzzypop",
    "nibblenug",
    "bumbletoes",
    "sprinklebot",
    "slimebean",
    "wigglyworm",
    "bubblewoof",
    "caramelwhirl",
    "zippynoodle",
    "sleepykoala",
    "chompmon",
    "cheesetoast",
    "wafflebop",
    "blopfish",
    "froggysocks",
    "marshymellow",
    "cupcakerush",
    "butterbuns",
    "wigglewomp",
    "muffinpuff",
    "kookiesmash",
    "beefcakebop",
    "sugarpuff",
    "peachykeen",
    "whiskerpuff",
    "toffeetaco",
    "boogiebop",
    "chubbypuff",
    "raviolimaster",
    "splatmon",
    "wafflepuff",
    "wigglypuff",
    "tootlesnug",
    "chubbybiscuit",
    "snugglesaurus",
    "sproutbun",
    "fizzysocks",
    "doodlebun",
    "squeakysocks",
    "twinklenug",
    "sushibuddy",
    "marshmallowpuff",
    "zippyzoom",
    "fluffynoodle",
    "muffinsmile",
    "puffcake",
    "plushysocks",
    "potatopuff",
    "nibblemuffin",
    "grumpysloth",
    "fizzynug",
    "fluffypuff",
    "cupcakewhizz",
    "nuggypuff",
    "spudster",
    "wigglybop",
    "cheesypuff",
    "bananaboop",
    "chompybuns",
    "waffleboop",
    "twinklepuff",
    "chunkymon",
    "cozyboi",
    "donutwomp",
]

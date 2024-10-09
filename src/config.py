import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DATABASE_URI = os.environ.get("DATABASE_URI")
FLASK_SECRET_KEY = os.getenv("SECRET_KEY")
FLASK_USER = os.getenv("FLASK_USER")
FLASK_PW = os.getenv("FLASK_PW")
WS_URL = "/chat"


usernames = [
    'notabot', 'smoot', 'bebo', 'pizzaboi', 'eggboi', 'snugglebug', 'fluffcake', 'bloopster', 
    'jellybeaner', 'muffinbun', 'pudgycat', 'noodlemon', 'chunkydino', 'gigglepuff', 'tacocat', 
    'chickennug', 'honeybunz', 'squishmallow', 'quackduck', 'biscuitboi', 'cuddlecloud', 
    'twinklebop', 'wafflewhizz', 'sporkmuffin', 'puffysocks', 'grumpygoose', 'boopitybop', 
    'pebbleskip', 'bubblewrapz', 'sillypanda', 'poprockz', 'smolbun', 'lazysloth', 
    'doodlefizz', 'zippytaco', 'grapejello', 'ticklebunz', 'gumbobuddy', 'donutbop', 'fuzzypop', 
    'nibblenug', 'bumbletoes', 'sprinklebot', 'slimebean', 'wigglyworm', 'bubblewoof', 
    'caramelwhirl', 'zippynoodle', 'sleepykoala', 'chompmon', 'cheesetoast', 'wafflebop', 
    'blopfish', 'froggysocks', 'marshymellow', 'cupcakerush', 'butterbuns', 'wigglewomp', 
    'muffinpuff', 'kookiesmash', 'beefcakebop', 'sugarpuff', 'peachykeen', 'whiskerpuff', 
    'toffeetaco', 'boogiebop', 'chubbypuff', 'raviolimaster', 'splatmon', 'wafflepuff', 
    'wigglypuff', 'tootlesnug', 'chubbybiscuit', 'snugglesaurus', 'sproutbun', 'fizzysocks', 
    'doodlebun', 'squeakysocks', 'twinklenug', 'sushibuddy', 'marshmallowpuff', 'zippyzoom', 
    'fluffynoodle', 'muffinsmile', 'puffcake', 'plushysocks', 'potatopuff', 'nibblemuffin', 
    'grumpysloth', 'fizzynug', 'fluffypuff', 'cupcakewhizz', 'nuggypuff', 'spudster', 'wigglybop', 
    'cheesypuff', 'bananaboop', 'chompybuns', 'waffleboop', 'twinklepuff', 'chunkymon', 
    'cozyboi', 'donutwomp'
]

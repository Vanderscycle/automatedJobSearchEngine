Scraping job posting from popular job hosting services, storing them in a db where I can accurately track which jobs I have applied to. I am a junior dev and will welcome any help especially, if we can dockerize the program.

You will need to create a .env file and store all your password and fill-in the following passwords.
```
MONGO_IP=
MONGO_PORT=
MONGO_DATABASE=
USERNAME=
USERPASSWORD=
AUTHSOURCE=
MODE=local

# Tor hash key
TOR_PASS=

# coverLetterGenerator
NAME=
ADDRESS=
PHONE=
MAIL=
WEBSITE=https://github.com/Vanderscycle
GITHUB=https://github.com/Vanderscycle
```

The cover letter generator is from a forked git repo that I (modified)[https://github.com/Vanderscycle/Cover-Letter-Generator]. To obtain the files you will need to get the files using a git clone or your forked repo at the same level as this repo. 
```git
git clone -b personal/cover-letter https://github.com/Vanderscycle/Cover-Letter-Generator.git
 ```
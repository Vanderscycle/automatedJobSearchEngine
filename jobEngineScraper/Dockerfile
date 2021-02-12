FROM python:3
LABEL maintainer "Henri Vandersleyen <hvandersleyen@gmail.com>"
# 6023 is scrapy's default port
EXPOSE 6023
# set work directly so that paths can be relative
WORKDIR /usr/src/app
# copy to make usage of caching
COPY requirements.txt ./
#install dependencies
RUN python -m pip install --upgrade pip
# https://stackoverflow.com/questions/43182131/docker-download-all-from-nltk-in-dockerfile/43182517
RUN pip3 install nltk
RUN [ "python", "-c", "import nltk; nltk.download('english')" ]
RUN pip3 install --no-cache-dir -r requirements.txt
# copy code itself from local file to image
COPY . .
# to be replaced at a later date by a bash file
CMD scrapy crawl SOJobspider -L WARNING
#https://stackoverflow.com/questions/25538402/way-to-stop-unwanted-items-being-printed-to-screen-with-scrapy
FROM python:3
LABEL maintainer='Henri Vandersleyen' 
LABEL maintainerEmail='hvandersleyen@gmail.com'
# set work directly so that paths can be relative
WORKDIR /usr/src/app
# copy to make usage of caching
COPY requirements.txt ./
#install dependencies
RUN python -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
# copy code itself from local file to image
COPY . .
# to be replaced at a later date by a bash file
CMD scrapy crawl SOJobspider -L WARNING

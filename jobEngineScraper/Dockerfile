FROM python:slim
LABEL maintainer "Henri Vandersleyen <hvandersleyen@gmail.com>"
# 6023 is scrapy's default port
EXPOSE 6023
# set work directly so that paths can be relative
WORKDIR /usr/src/app
# copy to make usage of caching
COPY requirements.txt ./
#install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt
# copy code itself from local file to image
COPY . .
CMD scrapy crawl xkcdDocker
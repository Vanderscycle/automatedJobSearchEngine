# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
#requests to check the ip
import requests
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
#https://stackoverflow.com/questions/43942689/error-while-receiving-a-control-message-socketclosed-empty-socket-content-i
from stem.util.log import get_logger
logger = get_logger()
logger.propagate = False

# https://stackoverflow.com/questions/45009940/scrapy-with-privoxy-and-tor-how-to-renew-ip/45010141
from toripchanger import TorIpChanger
from stem import Signal
from stem.control import Controller
# password handling
import os
from dotenv import load_dotenv
# TOR
TOR_PASSWORD = os.getenv('TOR_PASS')
# A Tor IP will be reused only after 10 different IPs were used.
ip_changer = TorIpChanger(tor_password=TOR_PASSWORD,reuse_threshold=10)


class ProxyMiddleware(object):
    """

    learning about to learn about TOR
    https://github.com/WiliTest/Anonymous-scrapping-Scrapy-Tor-Privoxy-UserAgent
    # setting TOR for the first time on Linux
    https://jarroba.com/anonymous-scraping-by-tor-network/
    config the to for the first time
    https://2019.www.torproject.org/docs/faq#torrc
    about TorIpChanger
    https://gist.github.com/DusanMadar/8d11026b7ce0bce6a67f7dd87b999f6b
    """
    _requests_count = 0

    def process_request(self, request, spider):
        #every 10 requests will generate a new ip
        self._requests_count += 1
        if self._requests_count > 10:
            self._requests_count = 0 
            ip_changer.get_new_ip()

        request.meta['proxy'] = 'http://127.0.0.1:8118'
        spider.log(f"Proxy : {request.meta['proxy']}")
class JobenginescraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JobenginescraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

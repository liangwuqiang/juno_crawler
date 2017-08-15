# coding=utf-8

from scrapy import cmdline

name = 'juno'

# cmd = 'scrapy crawl {0} -o items.json -t json -s LOG_FILE=scrapy.log'.format(name)

cmd = 'scrapy crawl {0} -s LOG_FILE=scrapy.log'.format(name)

cmdline.execute(cmd.split())

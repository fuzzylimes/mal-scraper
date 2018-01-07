from setuptools import setup

setup(name='mal_scraper',
      version='0.1',
      description='Tool to scrape data more easily from myaimelist.net',
      url='https://github.com/fuzzylimes/mal-scraper',
      author='fuzzylimes',
      license='MIT',
      packages=['malScraper'],
      install_requires=[
          'beautifulsoup4==4.6.0',
          'lxml==4.1.1'
      ],
      zip_safe=False)
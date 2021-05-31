# scraper-thebluebook
Hi, this scraper get information from site thebluebook.com with help framework Scrapy and serviсe for solving captchas capmonster.cloud
## Running all the stuff
1. Registry on capmonster.cloud and top up your balance
2. Clone repo: `git clone https://github.com/Wadwadw/scraper-thebluebook.git`
3. Create virtualenv, for example: `python3 -m venv venv` or `virtualenv -p python3 venv`
4. Activate it `source venv/bin/activate`
5. Install all the packages `pip install -r requirements.txt`
6. In file project1/project1/spiders/scrape.py in line 14 change capmonster client key
7. Start scraper script `scrapy crawl scrape -o results.csv`

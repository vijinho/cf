#CF Engineering Challenge

#OS X Installation

- `pip install -r requirements.txt`
- RethinkDB: [brew](http://brew.sh/) - `brew install rethinkdb`
- Nginx: (How to setup an nginx SSL-forwarding proxy)[https://gist.github.com/vijinho/2a59d7660ecc0c7d8c2b]
- TBD Task Queue: [Celery](http://www.celeryproject.org/) - `sudo easy_install Celery`
- TBD Message Queueing: [RabbitMQ](https://www.rabbitmq.com/) - `brew install rabbitmq`

##RethinkDB Setup

1. `rethinkdb create`
2. `rethinkdb serve`
3. [http://localhost:8080](http://localhost:8080)
4. Create database **cf**, table **trades**
 
[RethinkDB is amazing](http://rob.conery.io/2015/04/17/rethinkdb-2-0-is-amazing/) I went with [RethinkDB](http://www.rethinkdb.com/) and highlight my reasons below:

* Has a web interface to see realtime statistics on what’s going on. 
* Can shard, replicate and index tables individually via web interface

##Testing/Data

####Message Generator

Based on the example:
<pre>
{
    "userId": "134256",
    "currencyFrom": "EUR",
    "currencyTo": "GBP",
    "amountSell": 1000,
    "amountBuy": 747.1,
    "rate": 0.7471,
    "timePlaced": "24­JAN­15 10:27:44",
    "originatingCountry": "FR"
}
</pre>

#####Usage
<pre>
> python generator/generate.py --help
Usage: generate.py [OPTIONS]

Options:
  -l, --live              Simulate a live trade?
  -t, --today             Simulate a trade made today?
  -h, --historic          Simulate historic data?
  -q, --quantity INTEGER  Exact number of trades to generate?
  -a, --amount INTEGER    Generate a random number of trades totalling APPROX
                          this amount equivalent in EUR
  -s, --datestart TEXT    Enter date range start: format "01-JAN-2015
                          00:00:00"
  -e, --dateend TEXT      Enter date range end: format "01-JAN-2015 00:00:00"
  -c, --csv               Output CSV instead of JSON?
  -f, --outfile TEXT      Filename to output results.
  -v, --verbose
  --help                  Show this message and exit.
</pre>

######Examples
- `python generator/generate.py --live --quantity=10` generate 10 trades timestamped NOW
- `python generator/generate.py --today --amount=100000` generate trades totalling around €100000 in value for today with random times
- `python generator/generate.py --historic --quantity=5` generate 5 random historic trades
- `python generator/generate.py --historic --quantity=10 -s'13-DEC-12 00:00:00' -e'25-DEC-12 05:30:00'` generate 10 historic trades between the date range 12-25 December 2012
- `python generator/generate.py --amount=5000000 -s'06-MAY-13 00:00:00' -e'06-MAY-13 00:00:00'` generate trades totally 500,000 for the date 6 May 2013
- `python generator/generate.py --quantity=5 --outfile=test.json`  write 5 random historic trades to the file test.json

#####Rethink Example Data Import  
1. Generate random data: `python generator/generate.py -h -q 100000 -f data/random.json` - 100k documents
2. Import data: `rethinkdb import --force --format json -f random.json --table cf.trades`
3. In Data Explorer: `r.db('cf').table('trades').count()`
4. Test Python script: `python bin/rethink_test.py` which runs the same query

  
#####Random Data Simulator and Validator Rules
I wanted to make as realistic a simulator to real data as possible so I tried to find out what I could about the company and public financial data to help make educated guesses for the values.

- **userId**: Randomize between 1 and 65,000 (depending on year)
- **currencyFrom/To**: Get list from (20 currencies supported, 17 from, 20 to, 30 in 2015)
- **amountSell**: Randomize between 15 and 5000000
- **amountBuy**: (amountSell * rate) 
- **rate**: (is currencyFrom into currencyTo)
- **timePlaced**: (DD-XXX-YY HH:MM:SS) Any date since May 2010
- **originatingCountry**: (from currencyFrom user)
- **amountBuyEur** temporary extra field - the amount bought valued in EUROs for calculating totals for a time period

Data: I created [ISO Country Data](https://github.com/vijinho/ISO-Country-Data) as a spin-off from this project.

My random thinking into the generator:

- CF: 600,000,000, 30,000 customers by Nov 2011
- CF: 5m euros/day average (add 1m for each year from May 2010)
- CF: 1.8 billion so far
- Estimate around median 20,000 transactions/€50million daily
- Estimate 70% of transactions during european office hours
- Int transfers: Median €5000, Average €400,000
- EU transfers: 89m x €6827, 64m x 1138, 2009, UK 34.6m x £2598
- Size of transfer like Pareto's 80/20 rule - 70/30
- Size of payments: Benford's Law - 30% of all payments the first digit of the amount is a 1, while it is a 9 for only 5% of payments
- 2008-11 The geographical distribution of trade finance (SWIFT transfers), trade credit insurance and trade  (approx) % Asia-Pacific (55), Europe (25), Middle-East (8), Africa (5), North America (5), Latin America (2)
- Use [fixer.io historical rates but limit per year](http://fixer.io/) 
- Only use currencies which we have rates for
- Python3-compatible - aided by [Python Future](http://python-future.org/quickstart.html#installation) and [2to3](https://docs.python.org/2/library/2to3.html)

**Sources**

- [Highest Trading Currencies and Countries %](http://www.mapsofworld.com/world-top-ten/world-map-richest-countries-currency.html)
- [Fees](https://www.currencyfair.com/features/currency-exchange-fees/)
- [A BILLION HERE, A BILLION THERE:
THE STATISTICS OF PAYMENTS](http://swiftinstitute.org/wp-content/uploads/2012/10/The-Statistics-of-Payments_v15.pdf) (Ch 10 - How big is that payment? The frequency distribution of payments by size)
- [ECB 2009 ](https://www.ecb.europa.eu/pub/pdf/other/paymentsystem201009en.pdf)
- [Business-to-Business Wire Transfer Payments:
Customer Preferences and
Opportunities for Financial Institutions](https://www.frbservices.org/files/communications/pdf/research/wire_transfer_research_final.pdf)
- [Trade finance: developments and issues](http://www.bis.org/publ/cgfs50.pdf)
- [USE OF CURRENCIES IN INTERNATIONAL TRADE: ANY CHANGES IN THE
PICTURE?](https://www.wto.org/english/res_e/reser_e/ersd201210_e.pdf)
 

##Message Consumer

Uses [Python Falcon Framework](http://falconframework.org/) served with [Gunicorn](http://gunicorn.org/) behind an [nginx](http://wiki.nginx.org/Main) proxy using Basic Authentication.

**Starting**: `bin/startconsumer.sh` server on Port:8000 - 
nginx on Port:80 proxies to this but when testing locally can be used directly

###Why Falcon?
- Falcon is a very fast, minimalist Python framework for building cloud APIs and app backends.
- Falcon encourages the REST architectural style
- Performance. Unlike other Python web frameworks, Falcon won't bottleneck your API's performance under highly concurrent workloads. 
- Freedom. Falcon isn't very opinionated. In other words, the framework leaves a lot of decisions and implementation details to you, the API developer
- Reliable - 100% code coverage.

###Why Gunicorn?
It's a pre-fork worker model ported from Ruby's Unicorn project. The Gunicorn server is broadly compatible with various web frameworks, simply implemented, light on server resources, and fairly speedy.
**DO NOT scale the number of workers to the number of clients you expect to have. Gunicorn should only need 4-12 worker processes to handle hundreds or thousands of requests per second.**

###Why Nginx?
[How to deploy Nginx/Python apps](https://www.digitalocean.com/community/tutorials/how-to-deploy-python-wsgi-apps-using-gunicorn-http-server-behind-nginx)
Nginx is known for its high performance, stability, rich feature set, simple configuration, and low resource consumption and is one of a handful of servers written to address the [C10K problem](http://www.kegel.com/c10k.html)

###Testing
Run **`bin/submit.sh N`** where N is the number of trades 

OR `curl -i --user 'USERNAME':'PASSWORD' -H 'Content-Type: application/json' -H 'Accept: application/json' -<NUMBER> POST -d "$(python generator/generate.py -l -q $1)" http://localhost:80/trade`

**Success Response** 
The *data* is the RethinkDB response, as in [Ten-minute guide with RethinkDB and Python](http://rethinkdb.com/docs/guide/python/)
<pre>
[{  
    "msg":"OK",
    "code":0,
    "data":{  
        "errors":0,
        "deleted":0,
        "generated_keys":[  
            "6c2c2797-b5fd-45d8-8fe3-f2eb91da50e8",
            "1d4bc741-20a1-401d-8a2b-85d0872e0432",
            "de44cccf-21aa-40e0-9503-855a467d057b"
        ],
        "unchanged":0,
        "skipped":0,
        "replaced":0,
        "inserted":3
    }
}]
</pre>

**Error Response** 
<pre>
HTTP/1.1 200 OK
* Server nginx is not blacklisted
Server: nginx
Date: Mon, 27 Apr 2015 00:32:25 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 186
Connection: keep-alive

[  
    {  
        "msg":"Error: Missing required keys for trade. Should include: (userId,currencyFrom,currencyTo,amountSell,amountBuy,rate,timePlaced,originatingCountry)",
        "code":-1,
        "data":{  

        }
    }
]
</pre>
 
###Setup
* see `conf/nginx/*.conf` files

###Security
####nginx
- 100000 'trades' in a formatted JSON file (using above script) size is 24MB.  
- Will rate limit each request to 1000 trades - approx 245K, round up to 256K `limit_req zone=limit burst=5 nodelay;` and `client_body_buffer_size 4k;`
- `limit_req_zone $binary_remote_addr zone=limit:256k rate=10r/s;` - Hard limit 256k sized request rate=10r/s 
- `limit_conn_zone $binary_remote_addr zone=perip:10m;` - `limit_conn perip 4;` - 4 connections limit per ip 
- BASIC HTTP Authentication created file with - `htpasswd -c -b -B -C 10 .htpasswd <filename> <username> <password>` for more security than default - can be run as `bin/pw.sh <filename> <username> <password>`

####gunicorn

`gunicorn --timeout 15 --graceful-timeout 10 --max-requests 16384 --max-requests-jitter 4096 --limit-request-line 256 --limit-request-fields 32 --limit-request-field_size 1024 consume:app` 

[see settings](http://docs.gunicorn.org/en/latest/settings.html)


###Ports

* **RethinkDB**
  * Listening for intracluster connections on port 29015
  * Listening for client driver connections on port 28015
  *Listening for administrative HTTP connections on port 8080
* **gunicorn**
  * Listening at: http://127.0.0.1:8000
* **nginx**
  * Listening 80

#Message Processor


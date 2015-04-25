#CF Engineering Challenge

#OS X Installation
- Task Queue: [Celery](http://www.celeryproject.org/) - `sudo easy_install Celery`
- Message Queueing: [RabbitMQ](https://www.rabbitmq.com/) - `brew install rabbitmq`
- Database: [brew](http://brew.sh/) - `brew install rethinkdb`

##RethinkDB Setup
1. `rethinkdb create`
2. `rethinkdb serve`
3. [http://localhost:8080](http://localhost:8080)

[RethinkDB is amazing](http://rob.conery.io/2015/04/17/rethinkdb-2-0-is-amazing/) I went with [RethinkDB](http://www.rethinkdb.com/) and highlight my reasons below:

* Has a web interface to see realtime statistics on what’s going on. 
* Can shard, replicate and index tables individually via web interface


##Message Consumer

###Testing
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
  -v, --verbose
  --help                  Show this message and exit.
  --help              Show this message and exit.
</pre>
######Examples
- `python generator/generate.py --live --quantity=10` - generate 10 trades timestamped NOW
- `python generator/generate.py --today --amount=100000` - generate trades totalling around €100000 in value for today with random times
- `python generator/generate.py --historic --quantity=5` - generate 5 random historic trades

- `python generator/generate.py --historic --quantity=10 -s'13-DEC-12 00:00:00' -e'25-DEC-12 05:30:00'` - generate 10 historic trades between the date range 12-25 December 2012
 
- `python generator/generate.py --amount=5000000 -s'06-MAY-13 00:00:00' -e'06-MAY-13 00:00:00'` - generate trades totally 500,000 for the date 6 May 2013
  
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
 
US Fed data on companies:
<pre>
Annual Wires Sent/Received
10-14 3%
15-24 6
25-49 5
50-99 22
100-199 17
200+ 47
</pre>

##Message Processor
HHVM


##Frontend

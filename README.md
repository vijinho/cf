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

#####Random Data Simulator and Validator Rules
I wanted to make as realistic a simulator to real data as possible so I tried to find out what I could about the company and public financial data to help.

- **userId**: Randomize between 1 and 60,000
- **currencyFrom/To**: Get list from (20 currencies supported, 17 from, 20 to, 30 in 2015)
- **amountSell**: Randomize between 15 and 50,000,000
- **amountBuy**: (amountSell * rate) 
- **rate**: (is currencyFrom into currencyTo)
- **timePlaced**: (DDmonYY HH:MM:SS) Any date since May 2010
- **originating country**: (from currencyFrom user)

**Note** simulator won't be using historical rates.

Data: I created [ISO Country Data](https://github.com/vijinho/ISO-Country-Data) as a spin-off from this project.

#####generator/generate.py
* Python3-compatible - aided by [Python Future](http://python-future.org/quickstart.html#installation) and [2to3](https://docs.python.org/2/library/2to3.html)



My random thinking into the generator:

- CF: 600,000,000, 30,000 customers by Nov 2011
- CF: 5m euros/day average (add 1m for each year from 2010)
- CF: 1.8 billion so far
- Int transfers: Median €5000, Average €400,000
- EU transfers: 89m x €6827, 64m x 1138, 2009, UK 34.6m x £2598
- Size of transfer like Pareto's 80/20 rule - 70/30
- Size of payments: Benford's Law - 30% of all payments the first digit of the amount is a 1, while it is a 9 for only 5% of payments
- 2008-11 The geographical distribution of trade finance (SWIFT transfers), trade credit insurance and trade  (approx) % Asia-Pacific (55), Europe (25), Middle-East (8), Africa (5), North America (5), Latin America (2)

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

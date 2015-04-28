curl -i --user 'cf!':'CF:$2015' -H 'Content-Type: application/json' -H 'Accept: application/json' -X POST -d "$(python cf/generate.py -l -q $1)" http://bikr.es/trade

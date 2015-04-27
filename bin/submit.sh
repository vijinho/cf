curl -i --user 'cf!':'CF:$2015' -H 'Content-Type: application/json' -H 'Accept: application/json' -X POST -d "$(python generator/generate.py -l -q $1)" http://localhost:80/trade

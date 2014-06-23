DATE=`date +%Y-%m-%d`
if [ ! -e "./data/${DATE}_restaurants.json" ]
then
    touch "./data/${DATE}_restaurants.json"
fi
if [ ! -e "./data/${DATE}_geocoded_restaurants.json" ]
then
    touch "./data/${DATE}_geocoded_restaurants.json"
fi
rm -f ./data/restaurants.json
rm -f ./data/geocoded_restaurants.json
cd scrapy
scrapy crawl list -o ../data/restaurants.json -t json
cd ..
cd geocoding
python geocoding.py
cd ..
python json_combine/json_combine.py "./data/${DATE}_restaurants.json" "./data/restaurants.json" "./data/${DATE}_restaurants.json"
python json_combine/json_combine.py "./data/${DATE}_geocoded_restaurants.json" "./data/geocoded_restaurants.json" "./data/${DATE}_geocoded_restaurants.json"

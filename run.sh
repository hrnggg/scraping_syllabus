#!/bin/bash

for year in 2021 2020 2019 2018 2017
do
python3 main.py $year
python3 format_json.py $year
done
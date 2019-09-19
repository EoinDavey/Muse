#!/bin/ash
flask run --host 0.0.0.0 &
cd Clio/ && ng serve --host 0.0.0.0 --port 4200

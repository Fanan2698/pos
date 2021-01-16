#!/bin/sh

# source virtual env first
source venv/bin/activate

while true; do
    echo Running flask migration... 
    flask db init
    flask db migrate -m "initial migration"
    flask db upgrade

    if [[ "$?" == "0" ]]; then
        break
    fi
    
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done

echo Running compile translate...
flask translate compile

# execute gunicorn
exec gunicorn -b :5000 --access-logfile - --error-logfile - setup:app

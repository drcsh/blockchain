# small shell script for running this project locally
echo "Starting Blockchain Node!"
export FLASK_APP=node.py
export FLASK_ENV=development
flask run

# Tidy up after ourselves once the server is stopped
unset FLASK_APP
unset FLASK_ENV
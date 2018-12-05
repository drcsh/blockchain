# blockchain

Basic implementation of a blockchain loosly based on the following Hackernoon article: https://hackernoon.com/learn-blockchains-by-building-one-117428612f46 

I've written the system in a more OO style than the tutorial suggests, making something more extendable.  

# Requirements
A python 3.6 (tested on 3.7) development environment with virtual environment set up. I use virtualenvwrapper + virtualenv. 

After that all you should need to do is ```pip install -r requirements.txt```

# Running a blockchain node
The run.sh file will start up the Flask development server running on localhost port 5000.

Once the server is running, you can hit the endpoints using cURL etc, or run a python3 shell and import testing.api_wrapper which formats the requests for you and prints the output nicely.

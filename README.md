# Fetch Rewards Coding Exercise

Problem statement: https://fetch-hiring.s3.us-east-1.amazonaws.com/points.pdf

## Notes:

* As stated in the problem statement, this application does not use any persistent data storage and All data is stored inside the memory. All data will be cleaned when you restart the server.
* It is assumed that the application is used by only one user. So, all the transactions are of one user only. If we want to support multiple users, drastic changes would be needed. For e.g. Authentications should be added, changes in data structure.
* I am using different data structures to store and query the data faster. In real application database queries would replace this part.

## Installation Guide


* Install latest version of Python. Download it from https://www.python.org/downloads/ based on your operating system
* Install pip. Instructions can be found on https://pip.pypa.io/en/stable/installing/
* Make sure all environment variables are set properly.
* Go to the project directory
* Use following command to install all dependencies
```
pip install -r requirements.txt
``` 
* Use following command to run the application
```
python app.py
```
* Server would start running and the server URL with port number will be shown in the command line
* You can use application like postman to test the application
* Check the below sample requests and responses for more information on endpoints request body and expected response

## Sample Use Cases
![Transaction request](/images/transaction_request.png "Transaction sample request")

![Transaction response](/images/transaction_response.png "Transaction sample response")

![Balance request](/images/balance_request_response.png "Balance sample request and response")

![Spend request](/images/spend_request.png "Spend sample request")

![Spend response](/images/spend_response.png "Spend sample response")


from flask import Flask, request, Response, jsonify
import json
import time
import datetime
from heapq import heappush, heappop
from TSNode import TransactionNode

app = Flask(__name__)

# Three app variables that holds our data in memory
# In real app, some type of database would be used
app.all_transactions = []
app.current_balance = {}
app.balance_heap = []

def get_payer_from_heap(payer, points):
    """ Gets the payer with the oldest timestamp to subtract the points.

    params:
        payer: Payer name who is paying for the points
        points: Amount of points
    
    return:
        True if points are subtracted from the payer, False otherwise
    """

    temp_list = []

    # iterate over heap
    while True:
        if not app.balance_heap:
            return False

        # Get the oldest item from heap and check if it is a particular payer    
        temp = heappop(app.balance_heap)
        if temp.payer != payer:
            temp_list.append(temp)
        else:
            # Check if payer has enough points on particular nodes
            if temp.points >= points:
                temp.points -= abs(points)

                if temp.points != 0:
                    temp_list.append(temp)
                else:
                    pass
                break
            else:
                # If payer does not have enough points on particular node, reduce points value and check on another node
                points -= temp.points

    # Add all unused nodes again back in the heap
    for item in temp_list:
        heappush(app.balance_heap, item) 

    return True
    
def get_current_balance(balance_dict):
    """ Gets the current balance.

    params:
        balance_dict: Dictionary containing values of each individual payer.

    return:
        Total balance of all payer. 
    """

    total = 0
    for _, value in balance_dict.items():
        total += value

    return total

def spend_points(points, balance_heap):
    """ Spend fix amount of points from the balance.

    params:
        points: Number of points to spend
        balance_heap: Heap containg information about payer in sorted order of time

    return:
        Transaction list containing information about transactions performed to spend the points and 
        dictionary containing information on which payer is paying how much points.
    """
    
    transactions_list = []
    payer_dict = {}

    # Iterate over heap
    while True:
        if points == 0:
            break

        node = heappop(balance_heap)

        # If the node does not have enough points to spend
        if node.points <= points:
            points -= node.points
            payer_dict[node.payer] = payer_dict.get(node.payer, 0) + node.points
            node.timestamp = time.time()
            node.points *= -1
            transactions_list.append(node)
        else:
            # If the node has enough points, subtract it from the points, and put remaining points into heap
            new_node = TransactionNode(payer=node.payer, points=node.points - points)
            transactions_list.append(new_node)
            payer_dict[node.payer] = payer_dict.get(node.payer, 0) + points
            node.points -= points
            heappush(balance_heap, node)
            break

    #print("Payer dict", payer_dict)

    return transactions_list, payer_dict

@app.route("/")
def index():
    
    return "Use /transaction, /spend or /balance route"

@app.route("/transaction", methods=["POST"])
def transactions():
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response('{"error": "Invalid request body"}', status=400, mimetype='application/json')


    # If data is missing from the request body
    if data.get("payer") is None or data.get("points") is None:
        return Response('{"error": "Invalid request body"}', status=400, mimetype='application/json')

    # To check if points value is integer
    try:
        points = int(data['points'])
    except:
        return Response(json.dumps({'error': 'Invalid point value'}), status=400, mimetype='application/json')

    payer = data['payer']

    node = TransactionNode(points=points, payer=payer)

    # If transaction points are negative, reduce it from existing points if payer has enough points, return error otherwise
    if points < 0:
        
        if app.current_balance.get(payer, 0) + points >= 0:
            resp = get_payer_from_heap(payer, points)
            
            if not resp:
                return Response(json.dumps({'error': 'Insufficient balance'}), status=400, mimetype='application/json')
            
            app.all_transactions.append(node)
            app.current_balance[payer] += points
        else:
            return Response('{"error": "Not enough points of payer for transaction"}', status=400, mimetype='application/json')
    else:
        app.current_balance[payer] = app.current_balance.get(payer, 0) + points
        app.all_transactions.append(node)
        
        heappush(app.balance_heap, node)

    response = {
        'points': points,
        'payer': payer,
        'timestamp': datetime.datetime.utcfromtimestamp(node.timestamp).strftime('%Y-%m-%dT%H:%M:%SZ')
    }

    return Response(json.dumps(response), mimetype='application/json')

@app.route("/spend", methods = ["POST"])
def spned():
    try:
        data = json.loads(request.data)
    except Exception as e:
        print(e)
        return Response('{"error": "Invalid request body"}', status=400, mimetype='application/json')

    if data.get("points") is None:
        return Response('{"error": "Invalid request body"}', status=400, mimetype='application/json')

    # To check if points value is non negative integer
    try:
        points = int(data['points'])
        if points < 0:
            raise Exception()
    except:
        return Response(json.dumps({'error': 'Invalid points value'}), status=400, mimetype='application/json')

    # First check if user has enough balance
    total_balance = get_current_balance(app.current_balance)
    if total_balance < points:
        return Response('{"error": "Insufficient balance"}', status=400, mimetype='application/json')

    # If user has enough balance, spend points
    performed_transactions, points_used = spend_points(points, app.balance_heap)
    app.all_transactions.extend(performed_transactions)

    # Prepare list of all payers and their points that are used
    response = []
    for key, value in points_used.items():
        app.current_balance[key] -= value
        temp = {}
        temp['payer'] = key
        temp['points'] = value
        response.append(temp)

    return Response(json.dumps(response), mimetype='application/json')    

@app.route("/balance", methods=["GET"])
def balance():
    return Response(json.dumps(app.current_balance), mimetype='application/json')

if __name__ == "__main__":
    app.run()
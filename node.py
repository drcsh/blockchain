from uuid import uuid4

from flask import Flask, jsonify, request

import settings
from blockchain import Blockchain, Block, Transaction

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/', methods=['GET'])
def home():
    return "Blockchain node {}".format(node_identifier)


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block.proof
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = last_block.hash()
    block = blockchain.new_block(proof, previous_hash)

    # encode response as JSON
    serialized_transactions = [transaction.__dict__ for transaction in block.transactions]

    response = {
        'message': "New Block Forged",
        'index': block.index,
        'transactions': serialized_transactions,
        'proof': block.proof,
        'previous_hash': block.previous_hash,
    }
    return jsonify(response), 200
  

@app.route('/chain', methods=['GET'])
def full_chain():
    serialized_blocks = [block.__dict__ for block in blockchain.chain]
    response = {
        'chain': serialized_blocks,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT)


@app.route('/transactions/current', methods=['GET'])
def get_current_transactions():
    response = blockchain.current_transactions
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    print(type(values))

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction

    index = blockchain.new_transaction(values.get('sender'), values.get('recipient'), int(values.get('amount')))

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


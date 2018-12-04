import time, json, hashlib


class SHA256Hashable(object):
    """ Small class for Blocks and Transactions to inheret from so that the hashing behaviour can be easily added to both. """
    
    def hash(self):
        """
            Creates an SHA3 256 hash of this object.

            :todo: If we needed different algorithms, it would be nice to allow injecting the algothim to use.
            :return: a hex string representing the hash.
            :rtype: str
        """
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        sha3 = hashlib.sha256(block_string)
        return sha3.hexdigest()
            

class Block(SHA256Hashable):

    def __init__(self, index, transactions, proof, previous_hash):

        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash


class Transaction(SHA256Hashable):

    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount


class Blockchain(object):
    def __init__(self):
        """
            Initializes the Blockchain, including setting up the genesis block
        """
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(proof=100, previous_hash=1)

    @property
    def last_block(self):
        """
            Get the last Block in the chain. 

            :return last block:
            :rtype Block:

            :raises SystemError: if there is no last block, which means the chain is empty and the genesis block is missing.
        """
        try:
            last_block = self.chain[-1]
        except IndexError as e:
            raise SystemError("Can't find previous block in the chain! This suggests that there is no genesis block!")
        return last_block


    def new_block(self, proof, previous_hash=None):
        """
            Create a new Block in the Blockchain
            
            :param int proof: The proof given by the Proof of Work algorithm
            :param str previous_hash: (Optional) Hash of previous Block
            :return: New Block
            :rtype: Block

            :raises SystemError: if no previous has is provided and there are no blocks in the chain.
        """
        index = len(self.chain) + 1

        if not previous_hash:
            previous_block = self.last_block()
            previous_hash = previous_block.hash()

        block = Block(index, self.current_transactions, proof, previous_hash)

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    
    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block

        :param str sender: Address of the Sender
        :param str recipient: Address of the Recipient
        :param int amount: Amount
        :return: The index of the Block that will hold this transaction
        :rtype int:
        """

        new_transaction = Transaction(sender, recipient, amount)

        self.current_transactions.append(new_transaction)
    
    def proof_of_work(self, last_proof):
        pass
    
    @staticmethod
    def proof_is_valid(last_proof, proof):
        pass
    
    
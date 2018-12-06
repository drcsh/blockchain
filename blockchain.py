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
    """
        A Block is the key conceptual component of a Blockchain. It is linked to the previous block in the chain by a hash, 
        and contains a record of Transactions. Because each block contains the Hash of the previous, overwriting earlier data
        is hard to achieve (but not impossible if you control a majority of Nodes).
    """

    def __init__(self, index, transactions, proof, previous_hash):

        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash

    def serialize(self):
        """
            Custom method for serlializing a block, including all attached transactions.
            :return: a serialized version of this class
            :rtype dict:
        """
        serialized_block = self.__dict__

        # __dict__ doesn't recursively convert objects, so we need to overwrite the key.
        transactions = [transaction.serialize() for transaction in self.transactions]
        serialized_block["transactions"] = transactions

        return serialized_block


class Transaction(SHA256Hashable):
    """
        Record of a transaction to be recorded in the Blockchain.
    """

    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def serialize(self):
        """
            This is technically redundant but the code is tidier with symmetry between this and Block.
            :return: a serialized version of this class
            :rtype dict:
        """
        return self.__dict__


class Blockchain(object):
    DEFAULT_PROOF_DIFFICULTY = 4

    def __init__(self):
        """
            Initializes the Blockchain, including setting up the genesis block
        """
        genesis_block = self.__create_genesis_block()

        self.chain = [genesis_block]
        self.current_transactions = []
        self.proof_difficulty = self.DEFAULT_PROOF_DIFFICULTY


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


    def __create_genesis_block(self):
        """
            Create the genesis block for this blockchain, and return it.

            :return:
            :rtype Block:
        """
        genesis_block = Block(0, [], 100, 1)
        return genesis_block


    def update_proof_difficulty(self, new_difficulty):
        """
            Cryptocurrencies adjust their proof difficulty to maintain a steady frequency of block creation. Ethereum is at
            around 1/15sec, Bitcoin at 6/hr.

            A higher proof difficulty makes mining the next block more difficult.

            :param int new_difficulty: How many leading 0s to check for in the proof hash. 
            :raises TypeError: if the value is not an int
        """
        if not isinstance(new_difficulty, int):
            raise TypeError("Proof difficulty should be an int!")
        
        self.proof_difficulty = new_difficulty
            

    def new_block(self, proof, previous_hash=None):
        """
            Create a new Block in the Blockchain
            
            :param int proof: The proof given by the Proof of Work algorithm
            :param str previous_hash: (Optional) Hash of previous Block
            :return: New Block
            :rtype: Block

            :raises SystemError: if no previous has is provided and there are no blocks in the chain.
            :raises ValueError: if the given proof is invalid
        """
        index = len(self.chain) + 1

        if not previous_hash:
            previous_hash = self.last_block.hash()

        if not self.valid_proof(self.proof_difficulty, self.last_block.proof, proof):
            raise ValueError("Invalid proof provived!")

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

        return len(self.chain)
    

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains self.proof_difficulty leadingg zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param int last_proof:
        :return: new proof of work
        :rtype int:
        """

        new_proof = 0
        while self.valid_proof(self.proof_difficulty, last_proof, new_proof) is False:
            new_proof += 1

        return new_proof


    @staticmethod
    def valid_proof(proof_difficulty, last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain proof_difficulty leading zeroes?

        :param into proof_difficulty: how many zeroes to look for
        :param int last_proof: Previous Proof
        :param int proof: Current Proof
        :return: True if correct, False if not.
        :rtype: bool
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        comparrison_str = proof_difficulty * "0"

        return guess_hash[:proof_difficulty] == comparrison_str
import hashlib
import os
import json
from time import time
from typing import Any, Dict, List

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash="1")

    def new_block(self, previous_hash: str) -> Dict[str, Any]:
        timestamp = time()

        block = {
            'index': len(self.chain) + 1,
            'timestamp': timestamp,
            'transactions': self.current_transactions,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        # Hash the block
        block['hash'] = self.hash(block)

        # Add the block to the chain
        self.chain.append(block)

        # Create a unique filename based on the current timestamp
        file_name = f'blockchain_{int(timestamp)}.json'
        file_path = os.path.join('blockchain_data', file_name)

        # Save the blockchain to the new JSON file
        self.save_to_file(file_path)

        return block

    def new_transaction(self, booking_name: str, participants: int, booking_date: str) -> int:
        self.current_transactions.append({
            'booking_name': booking_name,
            'participants': participants,
            'booking_date': booking_date,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self) -> Dict[str, Any]:
        return self.chain[-1]

    @staticmethod
    def hash(block: Dict[str, Any]) -> str:
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def new_transaction_from_user_input(self) -> None:
        """
        Add a new transaction to the list of transactions based on user input
        """
        booking_name = input("Enter booking name: ")

        # Validate input for participants
        while True:
            participants_str = input("Enter number of participants: ")
            try:
                participants = int(participants_str)
                break  # Break the loop if conversion is successful
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        booking_date = input("Enter booking date: ")

        self.new_transaction(booking_name, participants, booking_date)

    def save_to_file(self, file_path: str):
        blockchain_data = {
            'chain': self.chain,
            'current_transactions': self.current_transactions
        }

        # Save the entire blockchain to the JSON file
        with open(file_path, 'w') as file:
            json.dump(blockchain_data, file, indent=4)

    def append_to_file(self, file_path: str) -> None:
        # Save the entire blockchain to the JSON file (overwrite if it exists)
        self.save_to_file(file_path)

# Example Usage
if __name__ == "__main__":
    # Ensure the 'blockchain_data' directory exists, create it if not
    if not os.path.exists('blockchain_data'):
        os.makedirs('blockchain_data')

    my_blockchain = Blockchain()
    num_blocks = 10

    for _ in range(num_blocks):
        # Add a new transaction from user input
        my_blockchain.new_transaction_from_user_input()

        # Create a new block
        last_block = my_blockchain.last_block
        previous_hash = my_blockchain.hash(last_block)
        my_blockchain.new_block(previous_hash)

        # Append the entire blockchain to the existing file or overwrite it
        my_blockchain.append_to_file('blockchain_data/blockchain.json')

        # Inform the user that a block has been added
        print(f"Block {len(my_blockchain.chain)} has been added to the blockchain.\n")
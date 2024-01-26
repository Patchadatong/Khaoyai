import json
import os
import hashlib

BLOCKCHAIN_DIR = 'blockchain/'

def get_hash(prev_block):
    block_file_path = os.path.join(BLOCKCHAIN_DIR, prev_block)
    if os.path.exists(block_file_path):
        with open(block_file_path, 'rb') as f:
            content = f.read()
        return hashlib.md5(content).hexdigest()
    else:
        return hashlib.md5(b'').hexdigest()


def check_integrity():
    files = sorted(os.listdir(BLOCKCHAIN_DIR), key=lambda x: int(x))

    results = [] 

    for file in files[1:]:
        with open(BLOCKCHAIN_DIR + file) as f:
            block = json.load(f) 

        prev_hash = block.get('prev_block').get('hash')
        prev_filename = block.get('prev_block').get('filename')

        actual_hash = get_hash(prev_filename)

        if prev_hash == actual_hash:
            res = 'ok'
        else: 
            res = 'was Changed'

        print(f'Block {prev_filename}: {res}')
        results.append({'block': prev_filename, 'result': res})
    return results

def write_block(booking_name, participants, booking_date):
    blocks_count = len(os.listdir(BLOCKCHAIN_DIR))
    prev_block = str(blocks_count)

    data = {
        "booking_name": booking_name,
        "participants": participants,
        "booking_date": booking_date,
        "prev_block" :{
            "hash": get_hash(prev_block),
            "filename": prev_block
        }
    }

    current_block = BLOCKCHAIN_DIR + str(blocks_count + 1)

    with open(current_block, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():
  
    if not os.path.exists(BLOCKCHAIN_DIR):
        os.makedirs(BLOCKCHAIN_DIR)
    check_integrity()


if __name__ == '__main__':
    main()

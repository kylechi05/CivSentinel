def get_street_address(address: str) -> str:
    split = address.split(',')
    return ','.join(address.split(',')[:len(split) - 2]).strip()

def get_city(address: str) -> str:
    return address.split(',')[-2].strip()
    
def get_state(address: str) -> str:
    return address.split(',')[-1].strip().split(' ')[0]

def get_zip_code(address: str) -> str:
    return address.split(',')[-1].strip().split(' ')[1]

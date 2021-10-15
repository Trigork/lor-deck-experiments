
ALLBUTMSB = 0x7f
JUSTMSB = 0x80

def pop_varint(bytes : list) -> int:
    result = 0
    current_shift = 0
    bytes_popped = 0

    for b in bytes:
        bytes_popped += 1
        current = b & ALLBUTMSB
        result |= current << current_shift

        if (b & JUSTMSB) != JUSTMSB:
            del bytes[:bytes_popped]
            return result
        
        current_shift += 7

def get_varint(value : int) -> list:
    buff = [ 0x0 ] * 10
    current_idx = 0

    if (value == 0):
        return [0x0]
    
    while value != 0:
        byte_val = value & ALLBUTMSB
        value >>= 7

        if value != 0:
            byte_val |= 0x80

        buff[current_idx] = byte_val
        current_idx += 1
    
    result = []
    for idx in range(current_idx):
        result += [buff[idx]]
    return result
    
    

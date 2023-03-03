pwd = ['>krrk', 'v{xvrk']

def check_pass(str(to_check)):
    full = ""
    for letter in str(to_check):
        enc = chr(ord(letter) + 6)
        full + enc
    if full in pwd: return True
    else: return False
        
    
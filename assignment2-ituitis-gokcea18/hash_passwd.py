'''The below is a simple example of how you would use "hashing" to
compare passwords without having to save the password - you would-
save the "hash" of the password instead.
Written for the class BLG101E assignment 2.'''

'''We need to import a function for generating hashes from byte
strings.'''
from hashlib import sha256

def create_hash(password):
    pw_bytestring = password.encode()
    return sha256(pw_bytestring).hexdigest()

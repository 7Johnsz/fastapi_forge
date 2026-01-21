import hashlib

def encode_host(ip):
    return hashlib.sha256(ip.encode('utf-8')).hexdigest()

def decode_host(encoded_ip):
    return hashlib.sha256(encoded_ip.encode('utf-8')).hexdigest()
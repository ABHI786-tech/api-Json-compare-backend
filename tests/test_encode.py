from config.utils import encode_id, decode_id

print("encode_id(19):", encode_id(19))
print("decode_id(encode_id(19)):", decode_id(encode_id(19)))

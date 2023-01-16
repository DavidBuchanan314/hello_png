import zlib

# https://www.w3.org/TR/2022/WD-png-3-20221025/#5PNG-file-signature
PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'

# https://www.w3.org/TR/2022/WD-png-3-20221025/#5Chunk-layout
def write_png_chunk(stream, chunk_type, chunk_data):
	# https://www.w3.org/TR/2022/WD-png-3-20221025/#dfn-png-four-byte-unsigned-integer
	chunk_length = len(chunk_data)
	if chunk_length > 2**31 - 1:  # This is unlikely to ever happen!
		raise ValueError("This chunk has too much chonk!")
	
	# https://www.w3.org/TR/2022/WD-png-3-20221025/#5CRC-algorithm
	# Fortunately, zlib's CRC32 implementation is compatible with PNG's spec:
	crc = zlib.crc32(chunk_type + chunk_data)

	stream.write(chunk_length.to_bytes(4, "big"))
	stream.write(chunk_type)
	stream.write(chunk_data)
	stream.write(crc.to_bytes(4, "big"))


if __name__ == "__main__":
	"""
	This is not going to result in a valid PNG file, but it's a start
	"""

	ihdr = b"\0" * 13  # TODO: populate real values!
	idat = b""  # ditto

	with open("samples/out_0.png", "wb") as f: # open file for writing
		f.write(PNG_SIGNATURE)
		write_png_chunk(f, b"IHDR", ihdr)
		write_png_chunk(f, b"IDAT", idat)
		write_png_chunk(f, b"IEND", b"")

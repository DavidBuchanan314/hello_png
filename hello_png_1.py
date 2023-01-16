import zlib

# https://www.w3.org/TR/2022/WD-png-3-20221025/#5PNG-file-signature
PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'

# https://www.w3.org/TR/2022/WD-png-3-20221025/#dfn-png-four-byte-unsigned-integer
# Helper function to pack an int into a PNG 4-byte unsigned integer
def encode_png_uint31(value):
	if value > 2**31 - 1:  # This is unlikely to ever happen!
		raise ValueError("Too big!")
	return value.to_bytes(4, "big")

# https://www.w3.org/TR/2022/WD-png-3-20221025/#5Chunk-layout
def write_png_chunk(stream, chunk_type, chunk_data):
	# https://www.w3.org/TR/2022/WD-png-3-20221025/#5CRC-algorithm
	# Fortunately, zlib's CRC32 implementation is compatible with PNG's spec:
	crc = zlib.crc32(chunk_type + chunk_data)

	stream.write(encode_png_uint31(len(chunk_data)))
	stream.write(chunk_type)
	stream.write(chunk_data)
	stream.write(crc.to_bytes(4, "big"))

def encode_png_ihdr(
		width,
		height,
		bit_depth=8,           # bits per sample
		colour_type=2,         # 2 = "Truecolour" (RGB)
		compression_method=0,  # 0 = zlib/DEFLATE (only specified value)
		filter_method=0,       # 0 = "adaptive filtering" (only specified value)
		interlace_method=0):   # 0 = no interlacing (1 = Adam7 interlacing)

	ihdr = b""
	ihdr += encode_png_uint31(width)
	ihdr += encode_png_uint31(height)
	ihdr += bytes([
		bit_depth,
		colour_type,
		compression_method,
		filter_method,
		interlace_method
	])

	return ihdr

# This is all the code required to read subpixel values from an ".rgb" file
# subpixel 0=R, 1=G, 2=B
def read_rgb_subpixel(rgb_data, width, x, y, subpixel):
	return rgb_data[3 * ((width * y) + x) + subpixel]

# Note: This function assumes RGB pixel format!
# Note: This function could be written more concisely by simply concatenating
# slices of rgb_data, but I want to use approachable syntax and keep things
# abstracted neatly.
def apply_png_filters(rgb_data, width, height):
	# we'll work with an array of ints, and convert to bytes at the end
	filtered = []
	for y in range(height):
		filtered.append(0) # Filter type 0 (none!)
		for x in range(width):
			filtered += [
				read_rgb_subpixel(rgb_data, width, x, y, 0), # R
				read_rgb_subpixel(rgb_data, width, x, y, 1), # G
				read_rgb_subpixel(rgb_data, width, x, y, 2)  # B
			]
	return bytes(filtered)


if __name__ == "__main__":
	# Load the input data:
	# (these values are hardcoded because the ".rgb" "format" has no metadata)
	INPUT_WIDTH = 320
	INPUT_HEIGHT = 180
	input_rgb_data = open("./samples/hello_png.rgb", "rb").read() # read entire file as bytes

	ihdr = encode_png_ihdr(INPUT_WIDTH, INPUT_HEIGHT)

	filtered = apply_png_filters(input_rgb_data, INPUT_WIDTH, INPUT_HEIGHT)
	idat = zlib.compress(filtered, level=9) # level 9 is maximum compression!

	with open("samples/out_1.png", "wb") as f: # open file for writing
		f.write(PNG_SIGNATURE)
		write_png_chunk(f, b"IHDR", ihdr)
		write_png_chunk(f, b"IDAT", idat)
		write_png_chunk(f, b"IEND", b"")

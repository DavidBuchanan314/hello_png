# Hello PNG

PNG is my favourite file format of all time. Version 1.0 of the specification was [relased in 1996](https://www.w3.org/TR/REC-png-961001) (before I was born!) and the format remains widely used to this day. I think the main reasons it stuck around for so long are:

 - "Good enough" lossless compression.
 - Builds on existing technologies (zlib/DEFLATE compression).
 - Simple to implement (helped by the above point).
 - Support for a variety of modes and bit-depths, including "true color" (24-bit RGB) and transparency.
 - Not patented.

There are other similarly-old and similarly-ubiquitous formats (*cough* ZIP *cough*) that are [disgusting](https://bugzilla.mozilla.org/show_bug.cgi?id=1534483) to deal with due to legacy cruft, ad-hoc extensions, spec ambiguities, and mutually incompatible implementations. On the whole, PNG is not like that at all, and it's mostly due to its well-thought-out design and careful updates over the years.

I'm writing this article to fulfil my role as a PNG evangelist, spreading the joy of good-enough lossless image compression to every corner of the internet.

I'll be referencing the [Working Draft of the PNG Specification (Third Edition)](https://www.w3.org/TR/2022/WD-png-3-20221025/) released in October 2022 (!), but every feature I mention here should still be present in the 1.0 spec. I'll aim to update this article once the Third Edition releases officially.

## Writing a PNG File

I think the best way to get to grips with a file format is to write code for reading or writing it. In this instance we're going to *write* a PNG, because we can choose to focus on the simplest subset of PNG features.

A minimum-viable PNG file has the following structure:

```
PNG signature || "IHDR" chunk || "IDAT" chunk || "IEND" chunk
```

The PNG signature (aka "magic bytes") are [defined as](https://www.w3.org/TR/2022/WD-png-3-20221025/#5PNG-file-signature):

> "89 50 4E 47 0D 0A 1A 0A" (hexadecimal bytes)

Or, expressed as a Python bytes literal:

> b'\x89PNG\r\n\x1a\n'

These magic bytes must be present at the start of every PNG file, allowing programs to easily detect the presence of a PNG.

### PNG Chunks

After the signature, the rest of the PNG is just a sequence of Chunks. They each have the same overall [structure](https://www.w3.org/TR/2022/WD-png-3-20221025/#5Chunk-layout):

```
Length      - A 31-bit unsigned integer (big-endian)
Chunk Type  - 4 bytes of ASCII upper or lower-case characters
Chunk Data  - "Length" bytes of raw data (Length may be 0)
CRC         - A CRC-32 checksum of the Chunk Type + Chunk Data
```

PNG uses [Network Byte Order](https://www.w3.org/TR/2022/WD-png-3-20221025/#7Integers-and-byte-order) (aka "big-endian") to encode integers as bytes. "31-bit" is not a typo - PNG [defines](https://www.w3.org/TR/2022/WD-png-3-20221025/#dfn-png-four-byte-unsigned-integer) a "PNG four byte integer", which is limited
to the range 0 to 2\*\*31-1, to defend against the existence of C programmers.

If you're not familiar with these concepts, don't worry, Python will handle all the encoding for us.

The `Chunk Type`, in our instance, will be one of `IHDR`, `IDAT`, or `IEND` (more on these shortly).

The CRC field is a CRC-32 checksum. The spec gives a [terse mathematical definition](https://www.w3.org/TR/2022/WD-png-3-20221025/#5CRC-algorithm), but fortunately we can ignore all those details and use a library to handle it for us.

The meaning of data *within* a chunk depends on the chunk's type, and potentially context from prior chunks.

Putting all that together, here's a Python script that generates a vaguely PNG-shaped file:

```python
TODO
```

The `write_png_chunk()` function is complete and fully functional. However,
we don't have any real data to put in the chunks yet, so the script's output not a valid PNG.

Running the unix `file` tool against it gives the following output:

```
$ file samples/out_0.png 
samples/out_0.png: PNG image data, 0 x 0, 0-bit grayscale, non-interlaced
```

It correctly recognises a PNG file (due to the magic bytes), and the rest of the info it provides corresponds to the 13 zeroes I packed into the `IHDR` chunk as a placeholder. Since we haven't populated the chunks with any meaningful data yet, image viewers will refuse to load it and give an error (there is nothing to load!).

### Image Input

Before we continue, we're going to need some actual image data to put inside our PNG. Here's an example image
I came up with:

TODO: image goes here

Funnily enough, it's already a PNG, but we don't have a PNG reader yet - how can we get our script to load it? One method is to convert it into a raw bitmap, which is something Imagemagick can help us with. I used the following command:

```
$ convert ./samples/hello_png_original.png ./samples/hello_png.rgb
```

`hello_png.rgb` now contains the raw uncompressed RGB pixel data, which we can trivially read from Python as-is. For every pixel in every row, it stores a 3-byte value corresponding to the colour of that pixel. Each byte is in the range 0-255, corresponding to the brightness of each RGB sub-pixel. To be pedantic, these values represent coordinates in the [sRGB colourspace](https://en.wikipedia.org/wiki/SRGB), but that detail is not strictly necessary to understand.

This `.rgb` file isn't a "real" image file format, and we need to remember certain properties to be able to make sense of it. Firstly we need to know the width and height (in this case 320x180), the pixel format (24-bit RGB, as described above), and the colourspace (sRGB). The PNG file that we generate will contain all this metadata in its headers, but since the *input* file doesn't contain them, we will hardcode the values in our Python script.

### The IHDR (Image Header) Chunk

The IHDR Chunk contains the most important metadata in a PNG - and in our simplified case, *all* the metadata
of the PNG. It encodes the width and height of the image, the pixel format, and a couple of other details. There isn't really much to say about it, but here's the [relevant section of the spec](https://www.w3.org/TR/2022/WD-png-3-20221025/#11IHDR).

I mentioned earlier that our RGB values are in the sRGB colourspace. PNG has ways to signal this information explicitly, but in practice sRGB is assumed to be the default, so for our minimum-viable PNG implementation we can just leave it out. Colour spaces are a complex topic, and if you want to learn more I can recommend watching this talk: [Guy Davidson - Everything you know about colour is wrong](https://www.youtube.com/watch?v=_zQ_uBAHA4A)



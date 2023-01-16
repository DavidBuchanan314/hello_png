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

I think the best way to get to grips with a file format is to write code for reading or writing it. In this instance we're going to *write* a PNG, because we can choose focus on the simplest subset of PNG features.

A minimum-viable PNG file has the following structure:

```
PNG signature || "IHDR" chunk || "IDAT" chunk || "IEND" chunk
```

The PNG signature (aka "magic bytes") are [defined as](https://www.w3.org/TR/2022/WD-png-3-20221025/#5PNG-file-signature):

> "89 50 4E 47 0D 0A 1A 0A" (hexadecimal bytes)

Or, expressed as a Python bytes literal:

> b'\x89PNG\r\n\x1a\n'

These magic bytes must be present at the start of every PNG file, allowing programs to easily detect the presence of a PNG just by looking at the start.

### Chunks

The following "chunks" all have the same overall [structure](https://www.w3.org/TR/2022/WD-png-3-20221025/#5Chunk-layout):

```
Length      - A 31-bit unsigned integer (big-endian)
Chunk Type  - 4 bytes of ASCII upper or lower-case characters
Chunk Data  - "Length" bytes of raw data (Length may be 0)
CRC         - A CRC-32 checksum of the Chunk Type + Chunk Data
```

PNG uses [Network Byte Order](https://www.w3.org/TR/2022/WD-png-3-20221025/#7Integers-and-byte-order) (aka "big-endian") to encode integers as bytes. "31-bit" is not a typo, PNG [defines](https://www.w3.org/TR/2022/WD-png-3-20221025/#dfn-png-four-byte-unsigned-integer) a "PNG four byte integer", which is limited
to the range 0 to 2\*\*31-1, to defend against the existence of C programmers.

If you're not familiar with these concepts, don't worry, Python will handle all the encoding for us.

The `Chunk Type`, in our instance, will be one of `IHDR`, `IDAT`, or `IEND` (more on these shortly).

The CRC field is a CRC-32 checksum. The spec gives a [terse mathematical definition](https://www.w3.org/TR/2022/WD-png-3-20221025/#5CRC-algorithm), but fortunately we can ignore all those details and use a library to handle it for us.

Putting all that together, here's a Python script that generates
a file that's vaguely PNG shaped:

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

It correctly recognises it as a PNG file (due to the magic bytes), and the rest of the info it provides corresponds to the 13 zeroes I packed into the `IHDR` chunk as a placeholder. Since we haven't populated the chunks with any meaningful data yet, image viewers will refuse to load it and give an error (there is nothing to load!).

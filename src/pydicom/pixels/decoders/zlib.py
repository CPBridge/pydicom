# Copyright 2008-2024 pydicom authors. See LICENSE file for details.
"""Use Python to decode frame-level Deflate encoded *Pixel Data*.

This module is not intended to be used directly.
"""
from zlib import decompress

from pydicom.pixels.decoders.base import DecodeRunner
from pydicom.pixels.utils import unpack_bits
from pydicom.uid import DeflatedImageFrameCompression


DECODER_DEPENDENCIES = {DeflatedImageFrameCompression: ()}


def is_available(uid: str) -> bool:
    """Return ``True`` if a pixel data decoder for `uid` is available for use,
    ``False`` otherwise.
    """
    return uid in DECODER_DEPENDENCIES


def _decode_frame(src: bytes, runner: DecodeRunner) -> bytes:
    """Wrapper for use with the decoder interface.

    Parameters
    ----------
    src : bytes
        A single frame of Deflate encoded data.
    runner : pydicom.pixels.decoders.base.DecodeRunner


        Required parameters:

        * `rows`: int
        * `columns`: int
        * `samples_per_pixel`: int
        * `bits_allocated`: int

    Returns
    -------
    bytearray
        The decoded frame, ordered as planar configuration 1.
    """
    decoded = decompress(src, wbits=-15)

    if runner.bits_allocated == 1:
        return unpack_bits(decoded, as_array=False)
    else:
        return decoded

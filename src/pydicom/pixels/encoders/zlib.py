# Copyright 2008-2024 pydicom authors. See LICENSE file for details.
"""Interface for *Pixel Data* encoding, not intended to be used directly."""

import zlib
from pydicom.pixels.encoders.base import EncodeRunner
from pydicom.pixels.utils import pack_bits
from pydicom.uid import DeflatedImageFrameCompression


ENCODER_DEPENDENCIES = {DeflatedImageFrameCompression: ()}


def is_available(uid: str) -> bool:
    """Return ``True`` if a pixel data encoder for `uid` is available for use,
    ``False`` otherwise.
    """
    return True


def _encode_frame(src: bytes, runner: EncodeRunner) -> bytes:
    """Wrapper for use with the encoder interface.

    Parameters
    ----------
    src : bytes
        A single frame of little-endian ordered image data to be Deflate
        encoded
    runner : pydicom.pixels.encoders.base.EncodeRunner
        The runner managing the encoding process.

    Returns
    -------
    bytes
        An Deflate encoded frame.
    """
    # In the case of single bit images, the data must first be bit-packed
    # before being encoded with Deflate
    if runner.bits_allocated == 1:
        src = pack_bits(src)

    # Use wbits=-zlib.MAX_WBITS to use the maximum window length but without a
    # zlib-specific header
    compressor = zlib.compressobj(wbits=-zlib.MAX_WBITS)
    return compressor.compress(src) + compressor.flush()

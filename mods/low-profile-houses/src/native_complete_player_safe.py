"""Isolated native SLD writer generalization. No installation or file I/O on import."""
import struct,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from sld_encoder_player_safe import layer_encode,mask_encode

def write_complete_frames(original_header,frames):
    if len(original_header)<14:raise ValueError('Truncated header')
    header_size=struct.unpack_from('<H',original_header,10)[0]
    if header_size<14 or header_size>len(original_header):raise ValueError('Header extent')
    if not 0<len(frames)<=65535:raise ValueError('Frame count')
    head=bytearray(original_header[:header_size]);struct.pack_into('<H',head,6,len(frames));out=bytearray(head)
    for frame,images in frames:
        bits=set(images)
        if 0 not in bits or not bits.issubset({0,1,3,4}):raise ValueError('Layer set')
        w,h=frame['width'],frame['height']
        if w<=0 or h<=0 or w%4 or h%4:raise ValueError('Canvas')
        for b,a in images.items():
            if a.shape[:2]!=(h,w) or a.ndim!=(2 if b in (1,4) else 3):raise ValueError('Shape')
            if a.dtype.name!='uint8' or (a.ndim==3 and a.shape[2]!=4):raise ValueError('Channels/type')
        flags=sum(1<<b for b in bits)|4
        out+=struct.pack('<HHhhBBH',w,h,*frame['hotspot'],flags,frame['unknown'],frame['index'])
        for bit in sorted(bits|{2}):out+=mask_encode(images[0]) if bit==2 else layer_encode(images[bit],bit)
    return bytes(out)

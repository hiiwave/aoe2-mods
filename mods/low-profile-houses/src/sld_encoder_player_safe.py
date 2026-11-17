"""Original native SLD v4 encoder, independent unshared frames.
BC1/BC4 algorithms from format definitions; no external tool/code dependency.
"""
import struct
import numpy as np
from house_codec import bc1

def rgb565(rgb):
    r,g,b=map(int,rgb);return ((r*31+127)//255<<11)|((g*63+127)//255<<5)|((b*31+127)//255)
def bc1_encode(block):
    pix=block.reshape(16,4);solid=pix[:,3]>=128;rgb=pix[:,:3].astype(np.int32)
    if not solid.any():return struct.pack('<HHI',0,0,0xffffffff)
    colors=rgb[solid];dist=((colors[:,None,:]-colors[None,:,:])**2).sum(2);i,j=np.unravel_index(dist.argmax(),dist.shape)
    a,b=rgb565(colors[i]),rgb565(colors[j]);alpha=not solid.all()
    if alpha:a,b=min(a,b),max(a,b)
    else:
        a,b=max(a,b),min(a,b)
        if a==b:
            if a<65535:a+=1
            else:b-=1
    lut=np.array(bc1(struct.pack('<HHI',a,b,0))) # derive proper RGB from same endpoint arithmetic
    def rgb16(v):return np.array([((v>>11)&31)*255//31,((v>>5)&63)*255//63,(v&31)*255//31],np.int32)
    # Use decoder's exact bit-replication endpoints, not floor-only conversion.
    c0=np.array(bc1(struct.pack('<HHI',a,b,0))[0][:3]);c1=np.array(bc1(struct.pack('<HHI',a,b,0x55555555))[0][:3])
    pal=[c0,c1]
    if a>b:pal += [(2*c0+c1)//3,(c0+2*c1)//3]
    else:pal += [(c0+c1)//2]
    indices=np.argmin(((rgb[:,None,:]-np.array(pal)[None,:,:])**2).sum(2),axis=1)
    indices[~solid]=3
    code=sum(int(v)<<(2*k) for k,v in enumerate(indices))
    return struct.pack('<HHI',a,b,code)

def bc4_encode(block):
    p=block.reshape(16).astype(np.int32);a=int(p.max());b=int(p.min())
    if a>b:lut=[a,b]+[((7-k)*a+k*b)//7 for k in range(1,7)]
    else:lut=[a,b]+[((5-k)*a+k*b)//5 for k in range(1,5)]+[0,255]
    idx=np.argmin((p[:,None]-np.array(lut)[None,:])**2,axis=1)
    bits=sum(int(v)<<(3*k) for k,v in enumerate(idx))
    return bytes([a,b])+bits.to_bytes(6,'little')

def bc4_player_encode(block):
    p=block.reshape(16).astype(np.int32);a=int(p.max());b=int(p.min())
    if a>b:lut=np.array([a,b]+[((7-k)*a+k*b)//7 for k in range(1,7)])
    else:lut=np.array([a,b]+[((5-k)*a+k*b)//5 for k in range(1,5)]+[0,255])
    error=(p[:,None]-lut[None,:])**2
    allowed=(p[:,None]>0)==(lut[None,:]>0)
    assert np.all(allowed.any(axis=1))
    error=np.where(allowed,error,1000000000);idx=np.argmin(error,axis=1)
    assert np.array_equal(lut[idx]>0,p>0)
    bits=sum(int(v)<<(3*k) for k,v in enumerate(idx))
    return bytes([a,b])+bits.to_bytes(6,'little')

def layer_encode(a,bit):
    h,w=a.shape[:2]
    if w%4 or h%4:raise ValueError('Canvas must be block aligned')
    gray=a.ndim==2;blocks=[];occupied=[]
    for y in range(0,h,4):
        for x in range(0,w,4):
            block=a[y:y+4,x:x+4]
            live=bool(np.any(block)) if gray else bool(np.any(block[:,:,3]>=128))
            occupied.append(live)
            if live:blocks.append((bc4_player_encode(block) if bit==4 else bc4_encode(block)) if gray else bc1_encode(block))
    commands=bytearray();p=0;n=len(occupied)
    while p<n:
        skip=0
        while p<n and not occupied[p] and skip<255:skip+=1;p+=1
        draw=0
        while p<n and occupied[p] and draw<255:draw+=1;p+=1
        commands+=bytes([skip,draw])
    if len(commands)//2>65535:raise ValueError('Too many command pairs')
    flags=1 if gray else 0
    header=struct.pack('<4H2B',0,0,w,h,flags,1) if bit in (0,1) else bytes([flags,1])
    payload=header+struct.pack('<H',len(commands)//2)+commands+b''.join(blocks)
    result=struct.pack('<I',len(payload)+4)+payload
    return result+b'\0'*((-len(result))%4)

def write_sld(original_header,frames):
    head=bytearray(original_header[:16]);struct.pack_into('<H',head,6,len(frames));out=bytes(head)
    for frame,images in frames:
        if set(images)!={0,1,3,4}:raise ValueError('Expected main/shadow/damage/player')
        for b,a in images.items():
            if a.shape[:2]!=(frame['height'],frame['width']):raise ValueError('Image geometry mismatch')
            if a.ndim!=(2 if b in (1,4) else 3):raise ValueError('Image channels mismatch')
        flags=sum(1<<b for b in images)|4
        out+=struct.pack('<HHhhBBH',frame['width'],frame['height'],*frame['hotspot'],flags,0,frame['index'])
        for bit in sorted(set(images)|{2}):out+=mask_encode(images[0]) if bit==2 else layer_encode(images[bit],bit)
    return out

def mask_encode(rgba):
    h,w=rgba.shape[:2];rows=h//4;cols=w//4;streams=[];offsets=[];total=0
    for row in range(rows):
        offsets.append(total);masks=[]
        for col in range(cols):
            a=rgba[row*4:row*4+4,col*4:col*4+4,3].reshape(16)
            masks.append(sum((1<<i) for i,v in enumerate(a) if v>=128))
        stream=bytearray([0])
        for start in range(0,cols,127):
            if start:stream.append(0)
            chunk=masks[start:start+127];stream.append(128+len(chunk));stream+=struct.pack('<'+'H'*len(chunk),*chunk)
        streams.append(bytes(stream));total+=len(stream)
    if total>65535:raise ValueError('Mask row offset overflow')
    payload=struct.pack('<H',5)+struct.pack('<'+'H'*rows,*offsets)+b''.join(streams)
    out=struct.pack('<I',len(payload)+4)+payload
    return out+b'\0'*((-len(out))%4)

"""Original stateful decoder for fixed-canvas house destruction sequences."""
import struct
import numpy as np
from house_codec import bc1

def occupancy(data,frame,rect):
    x1,y1,x2,y2=rect;rows=(y2-y1)//4;cols=(x2-x1)//4
    l=next(v for v in frame['layers'] if v['bit']==2);blob=data[l['offset']+4:l['offset']+l['length']]
    tag,=struct.unpack_from('<H',blob)
    if tag!=5:raise ValueError('Unsupported occupancy encoding')
    start=2+2*rows;offsets=list(struct.unpack_from('<'+'H'*rows,blob,2))+[len(blob)-start]
    out=np.zeros((frame['height'],frame['width']),bool)
    for y in range(rows):
        p=start+offsets[y];end=start+offsets[y+1];tiles=[];last=0
        while p<end:
            tag=blob[p];p+=1
            if tag<128:tiles.extend([last]*tag)
            else:
                n=tag-128
                if p+2*n>end:raise ValueError('Mask literal bounds')
                new=list(struct.unpack_from('<'+'H'*n,blob,p));p+=2*n;tiles.extend(new)
                if new:last=new[-1]
        if len(tiles)!=cols:raise ValueError('Mask row length')
        for x,tile in enumerate(tiles):
            out[y1+y*4:y1+y*4+4,x1+x*4:x1+x*4+4]=np.array([(tile>>k)&1 for k in range(16)],bool).reshape(4,4)
    return out

def decode_layer(data,frame,bit,previous=None):
    l=next(v for v in frame['layers'] if v['bit']==bit);o=l['offset'];end=o+l['length'];gray=bit in (1,4)
    if bit in (0,1):x1,y1,x2,y2,flags,u=struct.unpack_from('<4H2B',data,o+4);p=o+14
    else:
        main=next(v for v in frame['layers'] if v['bit']==0);x1,y1,x2,y2=struct.unpack_from('<4H',data,main['offset']+4);flags,u=data[o+4:o+6];p=o+6
    if not(0<=x1<x2<=frame['width'] and 0<=y1<y2<=frame['height']):raise ValueError('Bounds')
    if (x2-x1)%4 or (y2-y1)%4:raise ValueError('Alignment')
    shape=(frame['height'],frame['width'])+(() if gray else (4,));out=np.zeros(shape,np.uint8)
    if flags&128:
        if previous is None or previous.shape!=shape:raise ValueError('Missing or mismatched prior layer')
        out[y1:y2,x1:x2]=previous[y1:y2,x1:x2]
    count,=struct.unpack_from('<H',data,p);p+=2
    if p+2*count>end:raise ValueError('Commands bound')
    cmds=data[p:p+count*2];p+=count*2;block=0;cols=(x2-x1)//4;blocks=cols*((y2-y1)//4)
    for j in range(count):
        skip,draw=cmds[j*2:j*2+2];block+=skip
        if block+draw>blocks:raise ValueError('Block bounds')
        for _ in range(draw):
            if p+8>end:raise ValueError('Truncated block')
            b=data[p:p+8];p+=8
            if gray:
                a,z=b[:2];bits=int.from_bytes(b[2:],'little');lut=[a,z]+([((7-k)*a+k*z)//7 for k in range(1,7)] if a>z else [((5-k)*a+k*z)//5 for k in range(1,5)]+[0,255]);pix=np.array([lut[(bits>>(3*k))&7] for k in range(16)],np.uint8).reshape(4,4)
            else:pix=np.array(bc1(b),np.uint8).reshape(4,4,4)
            x=x1+block%cols*4;y=y1+block//cols*4;out[y:y+4,x:x+4]=pix;block+=1
    if p!=end:raise ValueError('Layer consumption')
    if bit==0 and flags&128:
        mask=occupancy(data,frame,(x1,y1,x2,y2));out[~mask]=0
    return out

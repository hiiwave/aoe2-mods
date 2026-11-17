"""Original bounded SLD/SMX codec helpers. Static non-inherited frames only."""
import struct
import numpy as np
from PIL import Image
def bc1(blob):
    a,b,bits=struct.unpack('<HHI',blob)
    def rgb(v):
        r,g,b=(v>>11)&31,(v>>5)&63,v&31
        return ((r<<3)|(r>>2),(g<<2)|(g>>4),(b<<3)|(b>>2),255)
    c=[rgb(a),rgb(b)]
    if a>b:
        c += [tuple((2*c[0][j]+c[1][j])//3 for j in range(3))+(255,),tuple((c[0][j]+2*c[1][j])//3 for j in range(3))+(255,)]
    else:
        c += [tuple((c[0][j]+c[1][j])//2 for j in range(3))+(255,),(0,0,0,0)]
    return [c[(bits>>(2*i))&3] for i in range(16)]

def gray_layer(data,f,bit):
    l=next(l for l in f['layers'] if l['bit']==bit);o=l['offset'];end=o+l['length']
    if bit==1:x1,y1,x2,y2,fl,u=struct.unpack_from('<4H2B',data,o+4);p=o+14
    else:
        main=f['layers'][0];x1,y1,x2,y2=struct.unpack_from('<4H',data,main['offset']+4);fl,u=data[o+4:o+6];p=o+6
    if fl&128:raise ValueError('Unsupported inherited layer')
    if not(0<=x1<x2<=f['width'] and 0<=y1<y2<=f['height']):raise ValueError('Gray layer bounds')
    if (x2-x1)%4 or (y2-y1)%4:raise ValueError('Gray layer alignment')
    n,=struct.unpack_from('<H',data,p);p+=2
    if p+2*n>end:raise ValueError('Gray command bounds')
    cmd=data[p:p+2*n];p+=2*n
    out=np.zeros((f['height'],f['width']),np.uint8);cols=(x2-x1)//4;maxb=cols*((y2-y1)//4);b=0
    for j in range(n):
        skip,draw=cmd[2*j:2*j+2];b+=skip
        if b+draw>maxb:raise ValueError('Block overrun')
        for _ in range(draw):
            if p+8>end:raise ValueError('Gray block truncated')
            a,z=data[p:p+2];idx=int.from_bytes(data[p+2:p+8],'little');p+=8
            lut=[a,z]+([((7-k)*a+k*z)//7 for k in range(1,7)] if a>z else [((5-k)*a+k*z)//5 for k in range(1,5)]+[0,255])
            by,bx=y1+(b//cols)*4,x1+(b%cols)*4
            out[by:by+4,bx:bx+4]=np.array([lut[(idx>>(3*k))&7] for k in range(16)]).reshape(4,4);b+=1
    if p!=end:raise ValueError('Unconsumed gray layer')
    return out

def transform(a,anchor,scale=.58):
    # Column-dependent isometric front-ground baseline: width/ground not resized.
    out=np.zeros_like(a)
    for x in range(a.shape[1]):
        base=anchor[1]+40-abs(x-anchor[0])*.50
        for y in range(a.shape[0]):
            sy=round(base-(base-y)/scale) if y<base else y
            if 0<=sy<a.shape[0]:out[y,x]=a[sy,x]
    return out

def nearest(rgb,colors):
    vals,inv=np.unique(rgb.reshape(-1,3),axis=0,return_inverse=True);inds=[]
    for batch in np.array_split(vals,max(1,len(vals)//256)):
        inds.extend(np.argmin(((batch[:,None,:].astype(np.int32)-colors[None,:,:])**2).sum(2),axis=1))
    return np.array(inds,dtype=np.int32)[inv].reshape(rgb.shape[:2])

def layer(a,kind,anchor):
    h,w=a.shape;edges=bytearray();cmd=bytearray();pix=[]
    for row in a:
        live=np.flatnonzero(row>=0)
        if not len(live):edges+=struct.pack('<HH',65535,65535);continue
        left,right=int(live[0]),int(live[-1]);edges+=struct.pack('<HH',left,w-right-1);x=left
        while x<=right:
            v=int(row[x]);typ=0 if v<0 else (2 if kind==0 and v>=1024 else 1)
            n=1
            while n<64 and x+n<=right:
                q=int(row[x+n]);t=0 if q<0 else (2 if kind==0 and q>=1024 else 1)
                if t!=typ:break
                n+=1
            cmd.append(((n-1)<<2)|typ)
            if typ:
                if kind==0:pix.extend(int(v)%1024 for v in row[x:x+n])
                elif kind==1:cmd.extend(int(v) for v in row[x:x+n])
            x+=n
        cmd.append(3)
    if kind==0:
        packed=bytearray()
        for i in range(0,len(pix),4):
            q=pix[i:i+4];q+= [0]*(4-len(q));packed.extend(v&255 for v in q);packed.append(sum((v>>8)<<(2*k) for k,v in enumerate(q)))
        tail=struct.pack('<II',len(cmd),len(packed))+cmd+packed
    else:tail=struct.pack('<I',len(cmd))+cmd
    unpacked=32+8*h+len(cmd)+(4*len(pix) if kind==0 else 0)
    return struct.pack('<HHhhII',w,h,*anchor,len(tail)+len(edges),0)+edges+tail,unpacked


def main_layer(data,frame,bit=0):
    l=next(v for v in frame['layers'] if v['bit']==bit);o=l['offset'];end=o+l['length']
    if bit==0:
        x1,y1,x2,y2,fl,u=struct.unpack_from('<4H2B',data,o+4);p=o+14
    else:
        main=next(v for v in frame['layers'] if v['bit']==0)
        x1,y1,x2,y2=struct.unpack_from('<4H',data,main['offset']+4);fl,u=data[o+4:o+6];p=o+6
    if fl&128:raise ValueError('Inherited main not supported')
    if not(0<=x1<x2<=frame['width'] and 0<=y1<y2<=frame['height']):raise ValueError('Bounds')
    if (x2-x1)%4 or (y2-y1)%4:raise ValueError('Alignment')
    n,=struct.unpack_from('<H',data,p);p+=2
    if p+2*n>end:raise ValueError('Gray command bounds')
    cmd=data[p:p+2*n];p+=2*n
    out=np.zeros((frame['height'],frame['width'],4),np.uint8);cols=(x2-x1)//4;b=0
    for j in range(n):
        skip,draw=cmd[2*j:2*j+2];b+=skip
        if b+draw>cols*(y2-y1)//4:raise ValueError('Main block overflow')
        for k in range(draw):
            pix=bc1(data[p:p+8]);p+=8
            bx=x1+(b%cols)*4;by=y1+(b//cols)*4
            out[by:by+4,bx:bx+4]=np.array(pix,np.uint8).reshape(4,4,4);b+=1
    if p!=end:raise ValueError('Main stream end mismatch')
    return out

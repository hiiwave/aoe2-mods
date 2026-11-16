"""Rebuild the selected 2/2/2 110px intact trial from local game files.
No installation, data-mod edits, downloads or network access.
"""
import argparse, hashlib, json, struct, zipfile
from pathlib import Path
import numpy as np
from PIL import Image
from sld_stateful import decode_layer, occupancy
from native_complete_player_safe import write_complete_frames

PROFILES = {
 "dark": {"name":"b_dark_house_age1_x1.sld","size":300,"anchor":133.,"k":.9,"d":3.,
 "seam":[[82,107],[141,133],[180,142],[230,142]],
 "foot":[[60,150],[82,153],[141,176],[180,171],[230,152],[240,150]]},
 "feudal": {"name":"b_west_house_age2_x1.sld","size":400,"anchor":181.,"k":1-15.5/93,"d":29.,
 "seam":[[109,149],[113,155],[145,173],[174,165],[213,180],[237,181],[274,153],[294,148]],
 "foot":[[109,193],[145,211],[174,223],[213,231],[237,220],[274,202],[294,195]]},
 "castle": {"name":"b_west_house_age3_x1.sld","size":400,"anchor":183.,"k":.7,"d":16.6,
 "seam":[[115,151],[133,158],[144,171],[173,157],[205,177],[231,184],[249,174],[282,156],[293,157]],
 "foot":[[115,198],[133,207],[144,215],[173,224],[205,235],[231,230],[249,222],[282,204],[293,202]]}
}

def frames(data):
    if data[:4] != b"SLDX" or struct.unpack_from("<H",data,4)[0] != 4:
        raise ValueError("Only inspected SLD v4 supported")
    count=struct.unpack_from("<H",data,6)[0];pos=struct.unpack_from("<H",data,10)[0];out=[]
    for _ in range(count):
        w,h,ax,ay,flags,u,idx=struct.unpack_from("<HHhhBBH",data,pos);pos+=12
        f={"width":w,"height":h,"hotspot":[ax,ay],"flags":flags,"unknown":u,"index":idx,"layers":[]}
        for bit in range(5):
            if flags & (1<<bit):
                n=struct.unpack_from("<I",data,pos)[0]
                if n<4 or pos+n>len(data): raise ValueError("Layer bounds")
                f["layers"].append({"bit":bit,"offset":pos,"length":n})
                pos+=n;pos+=(4-(pos-16)%4)%4
        out.append(f)
    if pos!=len(data):raise ValueError("Trailing or incomplete data")
    return out

def warp(source,p,age):
    size=p["size"];yy,xx=np.mgrid[:size,:size]
    seam=np.array(p["seam"]);foot=np.array(p["foot"])
    t=np.interp(xx,seam[:,0],seam[:,1]);b=np.interp(xx,foot[:,0],foot[:,1])
    a,k,d=p["anchor"],p["k"],p["d"];nt=a+k*(t-a)+d
    if np.any(b<=nt):raise ValueError("Wall band inverted")
    sy=np.where(yy<nt,a+(yy-a-d)/k,np.where(yy<b,t+(yy-nt)*(b-t)/(b-nt),yy))
    if age=="dark":sy=np.where((xx>=82)&(xx<=230),sy,yy)
    if age=="feudal":sy=np.where(xx>294,yy,sy)
    valid=(sy>=0)&(sy<size);idx=np.clip(np.rint(sy).astype(int),0,size-1)
    result={}
    for bit,img in source.items():
        if age=="dark" and bit==1:out=img.copy()
        else:
            out=np.zeros_like(img);out[valid]=img[idx[valid],xx[valid]]
            if age=="feudal":out[yy>=b]=img[yy>=b]
        result[bit]=out
    return result

def validate(data):
    fs=frames(data)
    if len(fs)!=3:raise ValueError("Expected three slots")
    decoded=[]
    for f in fs:
        images={l["bit"]:decode_layer(data,f,l["bit"]) for l in f["layers"] if l["bit"]!=2}
        box=Image.fromarray(images[0]).getbbox()
        if box is None or box[3]-box[1]!=110:raise ValueError("Output not 110px")
        if not np.array_equal(occupancy(data,f,(0,0,f["width"],f["height"])),images[0][:,:,3]>=128):
            raise ValueError("Outline mismatch")
        decoded.append(images)
    for other in decoded[1:]:
        for bit in decoded[0]:
            if not np.array_equal(decoded[0][bit],other[bit]):raise ValueError("Slots differ")
    return {"frames":3,"height":110,"outline_match":True,"slots_identical":True}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--graphics-dir",type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True)
    args=parser.parse_args()
    source=args.graphics_dir.resolve();output=args.output_dir.resolve()
    if output==source or source in output.parents or output in source.parents:
        raise ValueError("Output must be separate from the input graphics tree")
    mod=output/"hiiwave-Short-Houses-222-110-Intact-Trial"
    graphics=mod/"resources/_common/drs/graphics";graphics.mkdir(parents=True,exist_ok=True)
    reference=json.loads((Path(__file__).resolve().parents[1]/"manifests/v0.2-intact-222-110.json").read_text(encoding="utf-8-sig"))
    expected={x["file"]:x["sha256"] for x in reference["assets"]}
    report={"method":"Roof-Shift Hybrid","selection":"2/2/2","intact_only":True,"assets":[]}
    for age,p in PROFILES.items():
        data=(source/p["name"]).read_bytes();fs=frames(data)
        if len(fs)!=3:raise ValueError("Source static file must have three variants")
        f=fs[1]
        if (f["width"],f["height"])!=(p["size"],p["size"]):raise ValueError("Unexpected canvas")
        decoded={l["bit"]:decode_layer(data,f,l["bit"]) for l in f["layers"] if l["bit"]!=2}
        transformed=warp(decoded,p,age)
        encoded=write_complete_frames(data,[(dict(f,index=i),transformed) for i in range(3)])
        checks=validate(encoded);digest=hashlib.sha256(encoded).hexdigest()
        (graphics/p["name"]).write_bytes(encoded)
        report["assets"].append({"file":p["name"],"source_sha256":hashlib.sha256(data).hexdigest(),
          "sha256":digest,"matches_delivered_trial":digest==expected[p["name"]],**checks})
    info={"Author":"hiiwave","Title":"hiiwave Short Houses 222 110 Intact Trial",
      "Description":"2/2/2, Roof-Shift Hybrid, 110px. Intact-only trial. No DAT. Destruction/rubble not adapted; floating fire remains."}
    (mod/"info.json").write_text(json.dumps(info,indent=2),encoding="utf-8")
    (mod/"README.txt").write_text("Intact-only trial. Disable other house mods, enable this one, restart. Exact package not game-tested. Destruction/rubble remain original; fire can float. Author: hiiwave.\n",encoding="utf-8")
    (output/"verification.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    z=output/"hiiwave-Short-Houses-222-110-Intact-Trial.zip"
    with zipfile.ZipFile(z,"w",zipfile.ZIP_DEFLATED) as archive:
        for path in [mod/"info.json", mod/"README.txt"] + [graphics/p["name"] for p in PROFILES.values()]:
            if path.is_file():archive.write(path,path.relative_to(output))
    with zipfile.ZipFile(z) as archive:
        if archive.testzip() is not None:raise ValueError("ZIP integrity")
    print(json.dumps(report,indent=2))
    if not all(x["matches_delivered_trial"] for x in report["assets"]):
        raise SystemExit("VALIDATED BUT DIFFERS FROM DELIVERED TRIAL: review before distribution")
if __name__=="__main__":main()


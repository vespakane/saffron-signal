# Cuts the reusable pixels out of the reference screenshots and writes src/assets.json (data URIs).
import json, base64, io, numpy as np
from PIL import Image
import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')+'/'   # reference screenshots live in the repo root (not committed)
L=Image.open(P+'IMG_0441.PNG').convert('RGB'); C=Image.open(P+'IMG_0442.PNG').convert('RGB')
out={}
def uri(im, fmt='PNG', **kw):
    b=io.BytesIO(); im.save(b, fmt, **kw); return 'data:image/%s;base64,%s'%(fmt.lower().replace('jpeg','jpeg'), base64.b64encode(b.getvalue()).decode())
def mask(im, bg_l, ink_l=0):
    """monochrome glyph on flat background -> alpha mask (black), alpha from luminance"""
    a=np.array(im.convert('L')).astype(float)
    alpha=np.clip((bg_l-a)/(bg_l-ink_l),0,1); alpha[alpha<0.07]=0
    rgba=np.zeros(a.shape+(4,),np.uint8); rgba[...,3]=(alpha*255).round().astype(np.uint8)
    return Image.fromarray(rgba,'RGBA')
def circle(im, r=None, pad=0):
    w,h=im.size; r=r or min(w,h)/2-pad
    yy,xx=np.mgrid[0:h,0:w]; d=np.sqrt((xx+.5-w/2)**2+(yy+.5-h/2)**2)
    alpha=np.clip(r+0.5-d,0,1)
    rgba=np.dstack([np.array(im),(alpha*255).round().astype(np.uint8)]); return Image.fromarray(rgba,'RGBA')
# --- list screen (white bg) ---
out['status']=uri(mask(L.crop((825,68,1092,126)),255))                  # 89x19.3pt
out['btn_dots']=uri(L.crop((38,176,190,344)))                            # 50.7x56pt opaque
out['btn_cam']=uri(L.crop((848,176,1000,344)))
out['btn_plus']=uri(L.crop((1016,176,1168,344)))
out['avatar']=uri(circle(L.crop((48,692,216,860))))                      # 56pt
out['search']=uri(mask(L.crop((88,544,141,597)),246))                    # 17.7pt
out['ticks']=uri(mask(L.crop((250,766,311,808)),255,114))               # 20.3x14pt mask (blue 52,121,243)
out['lock']=uri(mask(L.crop((106,1204,141,1248)),255,107))              # 11.7x14.7pt
out['meta']=uri(L.crop((980,2150,1206,2410)))                            # 75.3x86.7pt
# tab bar: erase the Chats icon + badge, keeping the pill's rounded edge (240x163 stadium, r=81.5)
tb=np.array(L.crop((0,2330,1206,2622))).astype(float)
X0,X1,Y0,Y1=770,930,2383,2486
def pill_cov(x,y):  # supersampled coverage of the stadium at pixel (x,y) in screenshot coords
    cx1,cx2,cy,r=786.5,863.5,2466.5,81.5
    n=0
    for dx in (0.125,0.375,0.625,0.875):
        for dy in (0.125,0.375,0.625,0.875):
            px,py=x+dx,y+dy
            ccx=min(max(px,cx1),cx2)
            if (px-ccx)**2+(py-cy)**2<=r*r: n+=1
    return n/16
for y in range(Y0,Y1):
    row=tb[y-2330]
    pillcol=np.median(row[705:778][(row[705:778].min(axis=1)>=226)&(row[705:778].max(axis=1)<=240)],axis=0) if y>=2400 else np.median(row[760:770],axis=0)
    barcol=np.median(row[660:700],axis=0)
    for x in range(X0,X1):
        c=pill_cov(x,y); row[x]=pillcol*c+barcol*(1-c)
tb=tb.round().astype(np.uint8)
out['tabbar']=uri(Image.fromarray(tb))                                    # 402x97.3pt
# --- chat screen (beige 243,241,235) ---
out['chevron']=uri(mask(C.crop((76,218,118,286)),249))                   # 14x22.7pt
out['plus']=uri(mask(C.crop((34,2413,106,2485)),243))                    # 24pt
out['sticker']=uri(mask(C.crop((824,2412,898,2486)),255))                # 24.7pt
out['cam']=uri(mask(C.crop((968,2413,1056,2485)),243))                   # 29.3x24pt
out['mic']=uri(circle(C.crop((1083,2402,1179,2498))))                    # 32pt
A=np.array(C.crop((0,976,1206,2365)))                                     # clean wallpaper band
top=A[::-1][-(2054-A.shape[0]):]
wp=Image.fromarray(np.vstack([top,A]))
try:
    out['wallpaper']=uri(wp,'WEBP',quality=82,method=6)
except Exception as e:
    print('webp failed',e); out['wallpaper']=uri(wp,'JPEG',quality=85,optimize=True)
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'assets.json'),'w'))
for k,v in out.items(): print(k, len(v)//1024,'KB')
print('wallpaper size', wp.size)

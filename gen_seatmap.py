#!/usr/bin/env python3
# 깔끔한 넘버링 좌석 배치도 (격자 기반 균일 간격 + 구역 색상 + 중앙 STAGE/양쪽 SCREEN)
import json, os, numpy as np, cv2

HERE=os.path.dirname(os.path.abspath(__file__))
d=json.load(open(os.path.join(HERE,"data.json")))
zmeta=d["zone_meta"]; tzone=d["table_zone"]

W,H=1820,980
cv=np.full((H,W,3),255,np.uint8)
FONT=cv2.FONT_HERSHEY_SIMPLEX

def hex2bgr(h):
    h=h.lstrip("#"); return (int(h[4:6],16),int(h[2:4],16),int(h[0:2],16))
def lighten(bgr,f=0.80):
    return tuple(int(c+(255-c)*f) for c in bgr)
def ctext(s,cx,cy,fs,col,th):
    tw=cv2.getTextSize(s,FONT,fs,th)[0]
    cv2.putText(cv,s,(int(cx-tw[0]/2),int(cy+tw[1]/2)),FONT,fs,col,th)

# --- 격자 좌표 (지그재그/벽돌식: 행마다 반 칸 오프셋) ---
xfull=[0.065+0.84*i/12 for i in range(13)]
off=0.035
ys=np.linspace(0.225,0.93,6)
pos={}; num=1
for ri in range(6):
    if ri==0:
        cols=[xfull[0],xfull[1],xfull[2],xfull[10],xfull[11],xfull[12]]  # 무대 양옆
    else:
        shift=off if ri%2==0 else 0.0   # 교대로 반 칸 밀기
        cols=[x+shift for x in xfull]
    for x in cols:
        pos[num]=(x,ys[ri]); num+=1

# --- 무대(중앙, 실제 14.4m 비율로 넓게) + 양쪽 스크린(떨어져서 크게) ---
sy1,sy2=int(.04*H),int(.145*H)
sx1,sx2=int(.345*W),int(.655*W)
cv2.rectangle(cv,(sx1,sy1),(sx2,sy2),(232,232,232),-1)
cv2.rectangle(cv,(sx1,sy1),(sx2,sy2),(135,135,135),2)
ctext("STAGE",.5*W,(sy1+sy2)/2,1.15,(110,110,110),2)
cv2.rectangle(cv,(int(.483*W),sy2),(int(.517*W),int(.185*H)),(70,70,205),-1)  # 레드카펫
syc1,syc2=int(.05*H),int(.175*H)
for x1,x2 in [(.03*W,.20*W),(.80*W,.97*W)]:
    cv2.rectangle(cv,(int(x1),syc1),(int(x2),syc2),(244,234,214),-1)
    cv2.rectangle(cv,(int(x1),syc1),(int(x2),syc2),(170,130,70),2)
    ctext("SCREEN",(x1+x2)/2,(syc1+syc2)/2,0.72,(150,110,50),2)

# --- 테이블 원 (균일 반지름) ---
R=42
for n,(xr,yr) in pos.items():
    cx,cy=int(xr*W),int(yr*H)
    z=tzone.get(str(n),"일반"); col=hex2bgr(zmeta[z]["c"])
    cv2.circle(cv,(cx,cy),R,lighten(col,.80),-1)
    cv2.circle(cv,(cx,cy),R,col,4)
    ctext(str(n),cx,cy,0.8,(50,50,50),2)

cv2.imwrite(os.path.join(HERE,"assets/seatmap.png"),cv)
print("seatmap 생성:",W,"x",H,"/ 테이블",len(pos))

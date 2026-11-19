import os,json,urllib.request
V={1:100,2:320,3:335,4:500,5:950,6:20000}
D={2:(-33,-31,-18,-14,14,18,31,33),3:(-17,-15,15,17),4:(-16,-1,1,16),5:(-17,-16,-15,-1,1,15,16,17),6:(-17,-16,-15,-1,1,15,16,17)}
def attacked(b,t,s):
 for d in (-1,1):
  i=t-s*16+d
  if not i&136 and b[i]==s:return True
 for d in D[2]:
  i=t+d
  if not i&136 and b[i]==s*2:return True
 for d in D[5]:
  i=t+d;n=1
  while not i&136:
   p=b[i]
   if p:
    if p*s>0 and (abs(p)==5 or abs(p)==(4 if d in D[4] else 3) or abs(p)==6 and n==1):return True
    break
   i+=d;n+=1
 return False
def make(b,m,s,ep):
 i,j,p=m;c=b.copy();v=c[i];c[i]=0;c[j]=p or v
 if abs(v)==1 and j==ep and not b[j]:c[j-s*16]=0
 if abs(v)==6 and abs(j-i)==2:
  r=i+3 if j>i else i-4;c[(i+j)//2]=c[r];c[r]=0
 return c,(i+j)//2 if abs(v)==1 and abs(i-j)==32 else -1
def moves(b,s,ep,captures=False):
 for i,v in enumerate(b):
  if i&136 or v*s<=0:continue
  q=abs(v);out=[]
  if q==1:
   j=i+s*16
   if not j&136 and not b[j]:
    out.append(j)
    k=j+s*16
    if i//16==(1 if s==1 else 6) and not b[k]:out.append(k)
   for j in (i+s*16-1,i+s*16+1):
    if not j&136 and (b[j]*s<0 or j==ep):out.append(j)
  else:
   for d in D[q]:
    j=i+d
    while not j&136:
     if b[j]*s>0:break
     out.append(j)
     if b[j] or q in (2,6):break
     j+=d
  for j in out:
   if captures and not b[j] and j!=ep and not(q==1 and j//16 in (0,7)):continue
   promotions=(5,4,3,2) if q==1 and j//16 in (0,7) else (0,)
   for piece in promotions:
    m=(i,j,s*piece)
    c,e=make(b,m,s,ep)
    if not attacked(c,c.index(s*6),-s):yield m,c,e

def value(b,s):
 z=0;queens=5 in b or -5 in b
 for i,p in enumerate(b):
  if not p or i&136:continue
  q=abs(p);r=i//16 if p>0 else 7-i//16;f=i%16
  center=7-abs(2*f-7)-abs(2*(i//16)-7)
  activity=center*6 if q in (2,3) else r*9 if q==1 else 0
  if q==6:
   activity=-center*4-r*8 if queens else center*5
  z+=(1 if p>0 else -1)*(V[q]+activity)
 return z*s
nodes=0
TT={}
PV={}
def search(b,s,ep,d,a,z,ply=0):
 global nodes
 nodes+=1
 if nodes>40000:raise OverflowError
 key=(tuple(b),s,ep,d);old=a
 if key in TT:return TT[key]
 check=attacked(b,b.index(s*6),-s)
 if d<=0:
  stand=value(b,s)
  if d<=-3:return stand
  if not check:
   if stand>=z:return stand
   a=max(a,stand)
 ms=list(moves(b,s,ep,d<=0 and not check))
 if d<=0 and not ms and not check:return a
 if not ms:return -19000+ply if check else 0
 ms.sort(key=lambda t:(t[0]==PV.get(key[:-1]),V.get(abs(b[t[0][1]]),0)*10-V[abs(b[t[0][0]])]),reverse=True)
 for m,c,e in ms:
  v=-search(c,-s,e,d-1,-z,-a,ply+1)
  if v>=z:PV[key[:-1]]=m;return v
  if v>a:PV[key[:-1]]=m
  a=max(a,v)
 if a>old:TT[key]=a
 return a

def square(t):return ord(t[0])-97+(int(t[1])-1)*16
def choose(fen,legal):
 global nodes
 TT.clear()
 PV.clear()
 f=fen.split();b=[0]*128
 for r,row in enumerate(f[0].split('/')):
  x=0
  for c in row:
   if c.isdigit():x+=int(c)
   else:b[(7-r)*16+x]=(' PNBRQK'.index(c.upper()))*(1 if c.isupper() else -1);x+=1
 s=1 if f[1]=='w' else -1;ep=square(f[3]) if f[3]!='-' else -1
 best=legal[0];nodes=0
 for depth in (1,2,3,4,5):
  alpha=-30000;winner=best
  try:
   for u in sorted(legal,key=lambda u:(u!=best,u)):
    m=(square(u[:2]),square(u[2:4]),s*' PNBRQK'.index(u[4].upper()) if len(u)>4 else 0)
    c,e=make(b,m,s,ep);v=-search(c,-s,e,depth-1,-30000,-alpha)
    if v>alpha:alpha=v;winner=u
  except OverflowError:break
  best=winner
 return best

def post(path,data):
 req=urllib.request.Request(os.environ['MAKEFUN_ENV_URL']+path,json.dumps(data).encode(),{'Content-Type':'application/json'})
 return json.load(urllib.request.urlopen(req))
if __name__=='__main__':
 while True:
  g=post('/game',{})
  if g['status']=='done':break
  while g['status']=='your_move':g=post('/move',{'game':g['game'],'move':choose(g['fen'],g['legal_moves'])})

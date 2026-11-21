import os,json,urllib.request
V={1:100,2:320,3:335,4:500,5:950,6:20000}
D={2:(-33,-31,-18,-14,14,18,31,33),3:(-17,-15,15,17),4:(-16,-1,1,16),5:(-17,-16,-15,-1,1,15,16,17),6:(-17,-16,-15,-1,1,15,16,17)}
def attack_ray(start,step):
 squares=[]
 square=start+step
 while not square&136:
  squares.append(square)
  square+=step
 return tuple(squares)

ATTACK_RAYS={t:tuple((4 if d in D[4] else 3,attack_ray(t,d)) for d in D[5] if not (t+d)&136) for t in range(128) if not t&136}
KNIGHT_SOURCES={t:tuple(t+d for d in D[2] if not (t+d)&136) for t in ATTACK_RAYS}
PAWN_SOURCES={(s,t):tuple(t-s*16+d for d in (-1,1) if not (t-s*16+d)&136) for s in (1,-1) for t in ATTACK_RAYS}

def attacked(b,t,s):
 for i in PAWN_SOURCES[s,t]:
  if b[i]==s:return True
 for i in KNIGHT_SOURCES[t]:
  if b[i]==s*2:return True
 king=s*6
 queen=s*5
 for slider,ray in ATTACK_RAYS[t]:
  for i in ray:
   piece=b[i]
   if piece:
    if piece==queen or piece==s*slider or (piece==king and i==ray[0]):return True
    break
 return False
def make(b,m,s,ep):
 i,j,p=m;c=b.copy();v=c[i];c[i]=0;c[j]=p or v
 if abs(v)==1 and j==ep and not b[j]:c[j-s*16]=0
 if abs(v)==6 and abs(j-i)==2:
  r=i+3 if j>i else i-4;c[(i+j)//2]=c[r];c[r]=0
 return c,(i+j)//2 if abs(v)==1 and abs(i-j)==32 else -1
def castle_options(b,s,rights):
 king,short,long=(4,'K','Q') if s==1 else (116,'k','q')
 if b[king]!=s*6 or attacked(b,king,-s):return
 if short in rights and b[king+3]==s*4 and not (b[king+1] or b[king+2]) and not attacked(b,king+1,-s):yield king+2
 if long in rights and b[king-4]==s*4 and not (b[king-1] or b[king-2] or b[king-3]) and not attacked(b,king-1,-s):yield king-2

CASTLE_CORNERS={0:'Q',7:'K',112:'q',119:'k'}

def castle_rights(b,move,rights):
 if not rights:return ''
 src,dst,_=move
 removed=CASTLE_CORNERS.get(src,'')+CASTLE_CORNERS.get(dst,'')
 if b[src]==6:removed+='KQ'
 if b[src]==-6:removed+='kq'
 return ''.join(right for right in rights if right not in removed) if removed else rights

def moves(b,s,ep,captures=False,rights=''):
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
  if q==6 and rights and not captures:out.extend(castle_options(b,s,rights))
  for j in out:
   if captures and not b[j] and j!=ep and not(q==1 and j//16 in (0,7)):continue
   promotions=(5,4,3,2) if q==1 and j//16 in (0,7) else (0,)
   for piece in promotions:
    m=(i,j,s*piece)
    c,e=make(b,m,s,ep)
    if not attacked(c,c.index(s*6),-s):yield m,c,e

def piece_square_table(queens):
 table=[]
 for square in range(128):
  file,rank=square%16,square//16
  center=7-abs(2*file-7)-abs(2*rank-7)
  values=[0]*13
  for side,advance in ((1,rank),(-1,7-rank)):
   for piece in range(1,7):
    activity=center*6 if piece in (2,3) else advance*9 if piece==1 else 0
    if piece==6:activity=-center*4-advance*8 if queens else center*5
    values[side*piece]=side*(V[piece]+activity)
  table.append(values)
 return table
PIECE_SQUARE=(piece_square_table(False),piece_square_table(True))
BOARD_SQUARES=tuple(i for i in range(128) if not i&136)

PASSED_PAWN_WEIGHT=4
PASSED_SPANS={}
for side in (1,-1):
 for square in BOARD_SQUARES:
  rank,file=divmod(square,16)
  ahead=range(rank+side,8 if side==1 else -1,side)
  PASSED_SPANS[side,square]=tuple(r*16+f for r in ahead for f in range(max(0,file-1),min(7,file+1)+1))

def passed_pawn_bonus(b):
 score=0
 for i in BOARD_SQUARES:
  side=b[i]
  if abs(side)!=1:continue
  rank=i//16 if side==1 else 7-i//16
  if rank<3 or -side in (b[j] for j in PASSED_SPANS[side,i]):continue
  score+=side*PASSED_PAWN_WEIGHT*(rank-2)**2
 return score

def value(b,s):
 queens=5 in b or -5 in b
 table=PIECE_SQUARE[queens]
 score=sum(table[i][b[i]] for i in BOARD_SQUARES if b[i])
 return s*(score+(0 if queens else passed_pawn_bonus(b)))

MAX_SEARCH_NODES=16000
nodes=0
TT={}
PV={}
KILLER={}
HISTORY={}
def search(b,s,ep,d,a,z,ply=0,rights=''):
 global nodes
 nodes+=1
 if nodes>MAX_SEARCH_NODES:raise OverflowError
 position=(tuple(b),s,ep,rights)
 key=(*position,d,ply);old=a
 cached=TT.get(key)
 if cached is not None:
  score,bound=cached
  if bound==0 or (bound<0 and score<=a) or (bound>0 and score>=z):return score
 check=attacked(b,b.index(s*6),-s)
 if d<=0:
  if next(moves(b,s,ep,rights=rights),None) is None:return -19000+ply if check else 0
  stand=value(b,s)
  if d<=-3:return stand
  if not check:
   if stand>=z:return stand
   a=max(a,stand)
 ms=list(moves(b,s,ep,d<=0 and not check,rights))
 if d<=0 and not ms and not check:return a
 if not ms:return -19000+ply if check else 0
 preferred=PV.get(position)
 killer=KILLER.get(ply)
 def priority(child):
  move=child[0];origin,target,promotion=move
  if move==preferred:return 300000
  victim=abs(b[target])
  if victim or promotion or (target==ep and abs(b[origin])==1):
   return 200000+10*V[victim or 1]-V[abs(b[origin])]+V[abs(promotion) or 1]
  if move==killer:return 100000
  return HISTORY.get((s,move),0)
 ms.sort(key=priority,reverse=True)
 for m,c,e in ms:
  v=-search(c,-s,e,d-1,-z,-a,ply+1,castle_rights(b,m,rights))
  if v>=z:
   if d>0 and not b[m[1]] and not m[2] and (m[1]!=ep or abs(b[m[0]])!=1):
    KILLER[ply]=m
    history_key=(s,m)
    HISTORY[history_key]=min(99999,HISTORY.get(history_key,0)+d*d)
   PV[position]=m;TT[key]=(v,1);return v
  if v>a:PV[position]=m
  a=max(a,v)
 TT[key]=(a,0 if a>old else -1)
 return a

def square(t):return ord(t[0])-97+(int(t[1])-1)*16
def choose(fen,legal):
 global nodes
 TT.clear()
 PV.clear()
 KILLER.clear()
 HISTORY.clear()
 f=fen.split();b=[0]*128
 for r,row in enumerate(f[0].split('/')):
  x=0
  for c in row:
   if c.isdigit():x+=int(c)
   else:b[(7-r)*16+x]=(' PNBRQK'.index(c.upper()))*(1 if c.isupper() else -1);x+=1
 s=1 if f[1]=='w' else -1;ep=square(f[3]) if f[3]!='-' else -1
 rights='' if f[2]=='-' else f[2]
 best=legal[0];nodes=0
 for depth in range(1,7):
  alpha=-30000;winner=best
  try:
   for u in sorted(legal,key=lambda u:(u!=best,u)):
    m=(square(u[:2]),square(u[2:4]),s*' PNBRQK'.index(u[4].upper()) if len(u)>4 else 0)
    c,e=make(b,m,s,ep);v=-search(c,-s,e,depth-1,-30000,-alpha,rights=castle_rights(b,m,rights))
    if v==19000:return u
    if v>alpha:alpha=v;winner=u
  except OverflowError:
   # The previous best was searched first. Keep any completed improvement.
   best=winner
   break
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

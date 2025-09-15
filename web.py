import urllib.request,re,os,sys,webbrowser
from html.parser import HTMLParser
from urllib.parse import urljoin

class TextExtractor(HTMLParser):
    def __init__(s): super().__init__();s.t,s.l,s.il,s.ch=[],[],0,None
    def handle_starttag(s,t,a):
        if t in ("p","br","li","div","section"):s.t.append("\n")
        if t=="a":
            for k,v in a:
                if k=="href":s.il,s.ch=1,v
        if t=="img":
            for k,v in a:
                if k=="src":i=len(s.l)+1;s.t.append(f"[Image {i}]");s.l.append(v)
    def handle_endtag(s,t):
        if t=="a"and s.il:s.il,s.ch=0,None
    def handle_data(s,d):
        d=d.strip()
        if d:
            if s.il and s.ch:i=len(s.l)+1;s.t.append(f"{d} [{i}]");s.l.append(s.ch)
            else:s.t.append(d)

def fetch(u):
    if not u.startswith(("http://","https://")):u="https://"+u
    r=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
    h=urllib.request.urlopen(r,timeout=10).read().decode("utf-8","ignore")
    p=TextExtractor();p.feed(h)
    return re.sub(r"\n\s*\n","\n\n","\n".join(p.t)),p.l

hist,idx,inc=[],-1,"--ign"in sys.argv
def navhelp():print("Commands: [n]=open | b=back | f=forward | u=url | r=reload | t=clear | i=incognito | q=quit\n")
def display(u,t,l):
    os.system("cls"if os.name=="nt"else"clear")
    print(f"=== {u} {'(Incognito)'if inc else ''} ===\n{t[:2000]}")
    if l:print("\n--- Links ---",* [f"[{i}] {x}"for i,x in enumerate(l,1)],sep="\n")
    navhelp()

navhelp()
while 1:
    if idx==-1:
        u=input("Enter URL (q to quit): ").strip()
        if u=="q":break
        try:t,l=fetch(u)
        except Exception as e:print("Error:",e);continue
        if not inc:hist=[u];idx=0
        display(u,t,l);continue
    c=input(">> ").strip().lower()
    if c=="q":break
    elif c=="b"and not inc and idx>0:idx-=1;u=hist[idx]
    elif c=="f"and not inc and idx<len(hist)-1:idx+=1;u=hist[idx]
    elif c=="u":
        u=input("New URL: ")
        if u=="q":break
        if not inc:hist=hist[:idx+1]+[u];idx+=1
    elif c=="r":u=hist[idx]if not inc else u
    elif c=="t":os.system("cls"if os.name=="nt"else"clear");continue
    elif c=="i":inc=not inc;print("Incognito:",inc);continue
    elif c.isdigit()and'l'in locals():
        k=int(c)-1
        if 0<=k<len(l):
            u=urljoin(u,l[k])
            if u.lower().endswith((".png",".jpg",".jpeg",".gif",".webp")):webbrowser.open(u);continue
            if not inc:hist=hist[:idx+1]+[u];idx+=1
    else:print("Unknown command");continue
    try:t,l=fetch(u);display(u,t,l)
    except Exception as e:print("Error:",e)

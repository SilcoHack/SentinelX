#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SentinelX - Multi-Tool Cybersecurity Suite. Crafted for Silco."""
import os, sys, ssl, time, json, math, codecs, socket, base64, hashlib
import ipaddress, urllib.parse, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

if os.name == "nt": os.system("")

class C:
    RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
    RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
    BLUE="\033[94m"; MAGENTA="\033[95m"; CYAN="\033[96m"; WHITE="\033[97m"

USER_NAME="Silco"; VERSION="1.0.0"
BANNER=f"""{C.CYAN}{C.BOLD}
 ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗
 ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║
 ███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║
 ╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║
 ███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗
 ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
{C.RESET}{C.MAGENTA}        SentinelX  •  Multi-Tool Cybersecurity Suite  v{VERSION}{C.RESET}
{C.DIM}                       Crafted for {C.BOLD}{USER_NAME}{C.RESET}
"""

def clear(): os.system("cls" if os.name=="nt" else "clear")
def header(t):
    print(f"\n{C.CYAN}{'='*62}{C.RESET}")
    print(f"{C.BOLD}{C.WHITE}  >  {t}{C.RESET}")
    print(f"{C.CYAN}{'='*62}{C.RESET}\n")
def info(m): print(f"{C.BLUE}[i]{C.RESET} {m}")
def ok(m):   print(f"{C.GREEN}[+]{C.RESET} {m}")
def warn(m): print(f"{C.YELLOW}[!]{C.RESET} {m}")
def err(m):  print(f"{C.RED}[-]{C.RESET} {m}")
def prompt(msg):
    try: return input(f"{C.MAGENTA}[{USER_NAME}]{C.RESET} {msg}: ").strip()
    except (KeyboardInterrupt, EOFError): print(); return ""
def pause():
    try: input(f"\n{C.DIM}Devam icin Enter...{C.RESET}")
    except (KeyboardInterrupt, EOFError): print()
def is_ip(s):
    try: ipaddress.ip_address(s); return True
    except ValueError: return False

COMMON_PORTS={20:"FTP-Data",21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",
67:"DHCP",80:"HTTP",110:"POP3",111:"RPCbind",135:"MSRPC",137:"NetBIOS-NS",
138:"NetBIOS-DGM",139:"NetBIOS",143:"IMAP",161:"SNMP",389:"LDAP",443:"HTTPS",
445:"SMB",465:"SMTPS",514:"Syslog",587:"SMTP-Sub",636:"LDAPS",993:"IMAPS",
995:"POP3S",1080:"SOCKS",1433:"MSSQL",1521:"Oracle",1723:"PPTP",2049:"NFS",
3306:"MySQL",3389:"RDP",5432:"PostgreSQL",5900:"VNC",5984:"CouchDB",
6379:"Redis",8080:"HTTP-Alt",8443:"HTTPS-Alt",8888:"HTTP-Alt2",
9200:"Elasticsearch",11211:"Memcached",27017:"MongoDB"}

def _scan_port(host,port,timeout):
    try:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.settimeout(timeout); return port, s.connect_ex((host,port))==0
    except Exception: return port, False

def mod_port_scanner():
    header("Port Scanner")
    target=prompt("Hedef (IP / domain)")
    if not target: warn("Hedef bos."); return
    try: ip=socket.gethostbyname(target)
    except socket.gaierror: err("Cozumlenemedi."); return
    info(f"Hedef -> {target} ({ip})")
    print(f"{C.DIM}  [1] Yaygin  [2] Aralik  [3] Tum (1-65535){C.RESET}")
    ch=prompt("Secim [1]") or "1"
    if ch=="1": ports=sorted(COMMON_PORTS.keys())
    elif ch=="2":
        rng=prompt("Aralik (orn 1-1000)")
        try: a,b=rng.split("-"); ports=list(range(int(a),int(b)+1))
        except Exception: err("Gecersiz."); return
    elif ch=="3": ports=list(range(1,65536))
    else: err("Gecersiz."); return
    try: timeout=float(prompt("Timeout sn [0.5]") or "0.5")
    except ValueError: timeout=0.5
    try: workers=int(prompt("Thread [200]") or "200")
    except ValueError: workers=200
    ok(f"{len(ports)} port taraniyor..."); start=time.time(); open_ports=[]
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures=[ex.submit(_scan_port,ip,p,timeout) for p in ports]
        for fut in as_completed(futures):
            p,is_open=fut.result()
            if is_open:
                svc=COMMON_PORTS.get(p,"?"); open_ports.append((p,svc))
                print(f"  {C.GREEN}[ACIK]{C.RESET} Port {C.BOLD}{p:<6}{C.RESET} {C.DIM}{svc}{C.RESET}")
    print()
    if open_ports: ok(f"{len(open_ports)} acik port. ({time.time()-start:.2f}s)")
    else: warn(f"Acik port yok. ({time.time()-start:.2f}s)")

def mod_dns_lookup():
    header("DNS Lookup")
    t=prompt("Domain veya IP")
    if not t: return
    if is_ip(t):
        try:
            host,aliases,ips=socket.gethostbyaddr(t)
            ok(f"PTR -> {host}")
            if aliases: info(f"Aliases: {', '.join(aliases)}")
            for i in ips: info(f"IP: {i}")
        except Exception as e: err(f"Reverse basarisiz: {e}")
        return
    try: ip=socket.gethostbyname(t); ok(f"A -> {ip}")
    except socket.gaierror as e: err(f"A yok: {e}"); return
    try:
        host,aliases,ips=socket.gethostbyname_ex(t)
        if aliases: info(f"Aliases: {', '.join(aliases)}")
        for i in ips: info(f"IP: {i}")
    except Exception: pass

def _whois_query(server,query,port=43,timeout=6):
    try:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.settimeout(timeout); s.connect((server,port))
            s.sendall((query+"\r\n").encode()); data=b""
            while True:
                chunk=s.recv(4096)
                if not chunk: break
                data+=chunk
                if len(data)>200000: break
        return data.decode(errors="ignore")
    except Exception: return None

def mod_whois():
    header("WHOIS Lookup")
    d=prompt("Domain (orn example.com)").lower()
    if not d: return
    d=urllib.parse.urlparse(d if "://" in d else "http://"+d).netloc or d
    d=d.split("/")[0].split(":")[0]
    info("IANA sorgulaniyor...")
    iana=_whois_query("whois.iana.org",d)
    if not iana: err("IANA yanit vermedi."); return
    refer=None
    for line in iana.splitlines():
        if line.lower().startswith("refer:"): refer=line.split(":",1)[1].strip(); break
    if refer:
        info(f"WHOIS: {refer}")
        result=_whois_query(refer,d)
        if result:
            print(f"\n{C.DIM}{'-'*62}{C.RESET}"); print(result)
            print(f"{C.DIM}{'-'*62}{C.RESET}")
        else: warn("Detay yok, IANA:"); print(iana)
    else: print(iana)

SUBDOMAINS=["www","mail","ftp","webmail","smtp","pop","imap","ns1","ns2","ns3",
"dns","admin","portal","blog","shop","dev","test","staging","api","app","cdn",
"static","media","img","images","secure","vpn","remote","git","gitlab","jenkins",
"db","mysql","sql","oracle","backup","old","new","beta","demo","forum","support",
"help","docs","wiki","mx","cpanel","webdisk","autodiscover","m","mobile",
"intranet","internal"]

def mod_subdomain():
    header("Subdomain Enumeration")
    d=prompt("Domain (orn example.com)").lower().strip()
    if not d: return
    info(f"{len(SUBDOMAINS)} subdomain deneniyor...")
    def check(sub):
        fqdn=f"{sub}.{d}"
        try: return fqdn, socket.gethostbyname(fqdn)
        except socket.gaierror: return None
    found=[]
    with ThreadPoolExecutor(max_workers=30) as ex:
        for res in ex.map(check,SUBDOMAINS):
            if res:
                found.append(res)
                print(f"  {C.GREEN}[+]{C.RESET} {res[0]} -> {C.CYAN}{res[1]}{C.RESET}")
    print()
    if found: ok(f"{len(found)} subdomain.")
    else: warn("Sonuc yok.")

def mod_banner_grab():
    header("Banner Grabber")
    t=prompt("Hedef (IP / domain)")
    if not t: return
    try: port=int(prompt("Port [80]") or "80")
    except ValueError: port=80
    try: ip=socket.gethostbyname(t)
    except socket.gaierror: err("Cozumlenemedi."); return
    try:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.settimeout(6); s.connect((ip,port))
            try: s.sendall(b"HEAD / HTTP/1.0\r\nHost: "+t.encode()+b"\r\n\r\n")
            except Exception: pass
            time.sleep(0.4); s.settimeout(2); data=b""
            try:
                while len(data)<8192:
                    chunk=s.recv(4096)
                    if not chunk: break
                    data+=chunk
            except socket.timeout: pass
        if data:
            print(f"\n{C.DIM}{'-'*62}{C.RESET}")
            print(data.decode(errors="ignore"))
            print(f"{C.DIM}{'-'*62}{C.RESET}")
        else: warn("Banner alinamadi.")
    except Exception as e: err(f"Hata: {e}")

def mod_http_headers():
    header("HTTP Header Analyzer")
    url=prompt("URL (orn https://example.com)")
    if not url: return
    if not url.startswith(("http://","https://")): url="http://"+url
    try:
        req=urllib.request.Request(url,method="GET",
            headers={"User-Agent":f"SentinelX/{VERSION}"})
        with urllib.request.urlopen(req,timeout=10) as r:
            ok(f"Durum: {r.status} {r.reason}")
            print(f"\n{C.DIM}{'-'*62}{C.RESET}")
            for k,v in r.headers.items(): print(f"  {C.CYAN}{k}:{C.RESET} {v}")
            print(f"{C.DIM}{'-'*62}{C.RESET}")
            sec=["Strict-Transport-Security","Content-Security-Policy",
                 "X-Frame-Options","X-Content-Type-Options",
                 "Referrer-Policy","Permissions-Policy"]
            hl={k.lower():v for k,v in r.headers.items()}
            print(f"\n{C.BOLD}Guvenlik Basliklari:{C.RESET}")
            for h in sec:
                if h.lower() in hl: ok(h)
                else: warn(f"{h} -> eksik")
    except urllib.error.HTTPError as e: err(f"HTTP {e.code}: {e.reason}")
    except Exception as e: err(f"Hata: {e}")

def mod_ssl_cert():
    header("SSL Certificate Inspector")
    host=prompt("Host (orn example.com)")
    if not host: return
    try: port=int(prompt("Port [443]") or "443")
    except ValueError: port=443
    cert,version,cipher,verified=None,None,None,False
    try:
        ctx=ssl.create_default_context()
        with socket.create_connection((host,port),timeout=10) as sock:
            with ctx.wrap_socket(sock,server_hostname=host) as ss:
                cert=ss.getpeercert(); version=ss.version()
                cipher=ss.cipher(); verified=True
    except ssl.SSLCertVerificationError as e:
        warn(f"Dogrulama hatasi: {getattr(e,'verify_message',e)}")
        try:
            ctx=ssl.create_default_context(); ctx.check_hostname=False
            ctx.verify_mode=ssl.CERT_NONE
            with socket.create_connection((host,port),timeout=10) as sock:
                with ctx.wrap_socket(sock,server_hostname=host) as ss:
                    version=ss.version(); cipher=ss.cipher()
                    der=ss.getpeercert(binary_form=True)
                    info(f"DER alindi ({len(der)} bayt), dogrulama kapali.")
        except Exception as e2: err(f"Hata: {e2}"); return
    except Exception as e: err(f"Hata: {e}"); return
    print()
    if version: ok(f"Protokol: {version}")
    if cipher: ok(f"Cipher: {cipher[0]} ({cipher[2]} bit)")
    if verified and cert:
        subj=dict(x[0] for x in cert.get("subject",()))
        iss=dict(x[0] for x in cert.get("issuer",()))
        print(f"\n{C.BOLD}Sertifika:{C.RESET}")
        print(f"  Subject  : {subj.get('commonName','?')}")
        print(f"  Issuer   : {iss.get('organizationName',iss.get('commonName','?'))}")
        print(f"  Gecerlilik: {cert.get('notBefore','?')} -> {cert.get('notAfter','?')}")
        sans=cert.get("subjectAltName",())
        if sans:
            names=[s[1] for s in sans[:15]]
            print(f"  SANs     : {', '.join(names)}")
            if len(sans)>15: print(f"             ... (+{len(sans)-15})")

DIRS=["admin","login","wp-admin","administrator","phpmyadmin","backup",
"config","test","dev","staging","api","v1","v2","uploads","images","css","js",
"includes","assets","static","db","sql","private","secret","hidden",
"robots.txt",".git/HEAD",".env",".htaccess","sitemap.xml","crossdomain.xml",
"phpinfo.php","info.php","readme.html","readme.md","license.txt",
"CHANGELOG.md","server-status","web.config","package.json","composer.json"]

def mod_dir_scan():
    header("Directory / File Scanner")
    url=prompt("URL (orn https://example.com)").rstrip("/")
    if not url: return
    if not url.startswith(("http://","https://")): url="http://"+url
    try: workers=int(prompt("Thread [20]") or "20")
    except ValueError: workers=20
    ok(f"{len(DIRS)} yol deneniyor...")
    def check(p):
        full=f"{url}/{p}"
        try:
            req=urllib.request.Request(full,method="HEAD",
                headers={"User-Agent":f"SentinelX/{VERSION}"})
            with urllib.request.urlopen(req,timeout=6) as r: return full, r.status
        except urllib.error.HTTPError as e:
            if e.code not in (404,400): return full, e.code
        except Exception: pass
        return None
    found=[]
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for res in ex.map(check,DIRS):
            if res:
                full,status=res
                color=C.GREEN if 200<=status<300 else C.YELLOW
                found.append(res)
                print(f"  {color}[{status}]{C.RESET} {full}")
    print()
    if found: ok(f"{len(found)} sonuc.")
    else: warn("Sonuc yok.")

def mod_hash_gen():
    header("Hash Generator")
    text=prompt("Metin")
    if not text: return
    data=text.encode(); print()
    for algo in ["md5","sha1","sha224","sha256","sha384","sha512",
                 "sha3_256","sha3_512","blake2b","blake2s"]:
        try:
            h=hashlib.new(algo,data).hexdigest()
            print(f"  {C.CYAN}{algo:<10}{C.RESET} {h}")
        except Exception: pass

WORDLIST=["123456","password","12345678","qwerty","123456789","12345","1234",
"111111","1234567","dragon","123123","baseball","abc123","football","monkey",
"letmein","shadow","master","666666","qwertyuiop","123321","mustang",
"1234567890","michael","654321","superman","1qaz2wsx","7777777","121212",
"000000","qazwsx","123qwe","killer","trustno1","jordan","jennifer","zxcvbnm",
"asdfgh","hunter","buster","soccer","harley","batman","andrew","tigger",
"sunshine","iloveyou","2000","charlie","robert","thomas","hockey","ranger",
"daniel","starwars","112233","george","computer","michelle","jessica",
"pepper","1111","zxcvbn","555555","11111111","131313","freedom","777777",
"pass","maggie","159753","aaaaaa","ginger","princess","joshua","cheese",
"amanda","summer","love","ashley","nicole","chelsea","biteme","matthew",
"access","yankees","987654321","dallas","austin","thunder","taylor",
"matrix","admin","root","toor","test","guest","welcome","login","user",
"changeme","secret","default"]

def mod_hash_crack():
    header("Hash Cracker (Sozluk)")
    target=prompt("Hash").lower()
    if not target: return
    lengths={32:"md5",40:"sha1",56:"sha224",64:"sha256",96:"sha384",128:"sha512"}
    algo=lengths.get(len(target))
    algos=[algo] if algo else ["md5","sha1","sha256","sha512"]
    if not algo: warn("Uzunluk taninmadi, birden fazla denenecek.")
    ok(f"{len(WORDLIST)} kelime x {len(algos)} algo...")
    start=time.time()
    for word in WORDLIST:
        for a in algos:
            if hashlib.new(a,word.encode()).hexdigest()==target:
                print()
                ok(f"BULUNDU -> {C.BOLD}{word}{C.RESET}  ({a}, {time.time()-start:.3f}s)")
                return
    warn("Sozlukte yok.")

def mod_password_strength():
    header("Password Strength Analyzer")
    try:
        import getpass
        pw=getpass.getpass(f"{C.MAGENTA}[{USER_NAME}]{C.RESET} Sifre (gizli): ")
    except Exception: pw=prompt("Sifre")
    if not pw: return
    score=0; fb=[]; n=len(pw)
    if n>=8: score+=1
    if n>=12: score+=1
    if n>=16: score+=1
    else: fb.append("En az 16 karakter onerilir.")
    classes=0
    if any(c.islower() for c in pw): classes+=1
    if any(c.isupper() for c in pw): classes+=1
    if any(c.isdigit() for c in pw): classes+=1
    if any(not c.isalnum() for c in pw): classes+=1
    score+=classes
    if classes<3: fb.append("Buyuk/kucuk harf, rakam ve sembol karistir.")
    common=["password","123456","qwerty","admin","letmein","welcome"]
    if any(c in pw.lower() for c in common):
        score-=2; fb.append("Yaygin kelime/desen iceriyor.")
    import re
    if re.search(r"(.)\1{2,}",pw):
        score-=1; fb.append("Tekrarlanan karakter var.")
    pool=0
    if any(c.islower() for c in pw): pool+=26
    if any(c.isupper() for c in pw): pool+=26
    if any(c.isdigit() for c in pw): pool+=10
    if any(not c.isalnum() for c in pw): pool+=32
    entropy=n*math.log2(pool) if pool else 0
    if score<=2: rating,color="ZAYIF",C.RED
    elif score<=4: rating,color="ORTA",C.YELLOW
    elif score<=6: rating,color="IYI",C.GREEN
    else: rating,color="GUCLU",C.GREEN+C.BOLD
    print()
    print(f"  Uzunluk      : {n}")
    print(f"  Karakter seti: {classes}/4")
    print(f"  Entropi      : ~{entropy:.1f} bit")
    print(f"  Puan         : {score}/7")
    print(f"  Degerlendirme: {color}{rating}{C.RESET}")
    if fb:
        print(f"\n{C.BOLD}Oneriler:{C.RESET}")
        for f in fb: print(f"  {C.YELLOW}*{C.RESET} {f}")

def mod_encoder():
    header("Encoder / Decoder")
    print("  [1] B64 Encode  [2] B64 Decode  [3] Hex Encode  [4] Hex Decode")
    print("  [5] URL Encode  [6] URL Decode  [7] ROT13")
    ch=prompt("Secim"); text=prompt("Metin")
    if not text: return
    try:
        if ch=="1": print(f"\n{C.GREEN}{base64.b64encode(text.encode()).decode()}{C.RESET}")
        elif ch=="2": print(f"\n{C.GREEN}{base64.b64decode(text+'===').decode(errors='ignore')}{C.RESET}")
        elif ch=="3": print(f"\n{C.GREEN}{text.encode().hex()}{C.RESET}")
        elif ch=="4": print(f"\n{C.GREEN}{bytes.fromhex(text).decode(errors='ignore')}{C.RESET}")
        elif ch=="5": print(f"\n{C.GREEN}{urllib.parse.quote(text)}{C.RESET}")
        elif ch=="6": print(f"\n{C.GREEN}{urllib.parse.unquote(text)}{C.RESET}")
        elif ch=="7": print(f"\n{C.GREEN}{codecs.encode(text,'rot_13')}{C.RESET}")
        else: err("Gecersiz.")
    except Exception as e: err(f"Hata: {e}")

def mod_ip_geo():
    header("IP Geolocation")
    ip=prompt("IP (bos = kendin)")
    if not ip:
        try:
            with urllib.request.urlopen("https://api.ipify.org",timeout=6) as r:
                ip=r.read().decode().strip()
            info(f"Genel IP'n: {ip}")
        except Exception as e: err(f"Alinamadi: {e}"); return
    if not is_ip(ip): err("Gecersiz IP."); return
    try:
        url=(f"http://ip-api.com/json/{ip}"
             "?fields=status,message,country,regionName,city,zip,lat,lon,"
             "timezone,isp,org,as,query")
        with urllib.request.urlopen(url,timeout=8) as r:
            data=json.loads(r.read().decode())
        if data.get("status")!="success":
            err(f"Basarisiz: {data.get('message','?')}"); return
        print()
        for label,key in [("IP","query"),("Ulke","country"),("Bolge","regionName"),
                          ("Sehir","city"),("Posta","zip"),("Enlem","lat"),
                          ("Boylam","lon"),("Saat dilimi","timezone"),
                          ("ISP","isp"),("Org","org"),("AS","as")]:
            if data.get(key): print(f"  {C.CYAN}{label:<12}{C.RESET} {data[key]}")
    except Exception as e: err(f"Hata: {e}")

def mod_ping_sweep():
    header("Host Discovery (TCP Ping)")
    net=prompt("Ag (orn 192.168.1.0/24)")
    if not net: return
    try: network=ipaddress.ip_network(net,strict=False)
    except ValueError: err("Gecersiz ag."); return
    hosts=list(network.hosts())
    if not hosts: warn("Host yok."); return
    if len(hosts)>1024: warn(f"{len(hosts)} host, uzun surebilir.")
    probe_ports=[80,443,22,445,3389,8080]
    def probe(ip):
        s=str(ip)
        for p in probe_ports:
            try:
                with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
                    sock.settimeout(0.4)
                    if sock.connect_ex((s,p))==0: return s, p
            except Exception: continue
        return None
    ok(f"{len(hosts)} host taraniyor..."); alive=[]
    with ThreadPoolExecutor(max_workers=100) as ex:
        for res in ex.map(probe,hosts):
            if res:
                alive.append(res)
                print(f"  {C.GREEN}[CANLI]{C.RESET} {res[0]}  {C.DIM}(port {res[1]}){C.RESET}")
    print()
    ok(f"{len(alive)} canli host.")

def mod_mac_vendor():
    header("MAC Vendor Lookup")
    mac = prompt("MAC (00:1A:2B:3C:4D:5E)")
    mac = mac.replace("-","").replace(":","").replace(".","").upper()
    if len(mac) < 6: err("Gecersiz MAC."); return
    oui = mac[:6]
    try:
        url = f"https://api.macvendors.com/{oui}"
        req = urllib.request.Request(url, headers={"User-Agent": f"SentinelX/{VERSION}"})
        with urllib.request.urlopen(req, timeout=8) as r:
            vendor = r.read().decode(errors="ignore").strip()
            ok(f"OUI {oui} -> {vendor}")
    except urllib.error.HTTPError as e:
        if e.code == 404: warn("Bu OUI icin uretici bulunamadi.")
        else: err(f"API hatasi: {e.code}")
    except Exception as e:
        err(f"Hata: {e}")

def mod_http_methods():
    header("HTTP Method Tester")
    url = prompt("URL")
    if not url: return
    if not url.startswith(("http://","https://")): url = "http://" + url
    methods = ["GET","POST","PUT","DELETE","OPTIONS","HEAD","PATCH","TRACE"]
    for m in methods:
        try:
            req = urllib.request.Request(url, method=m,
                headers={"User-Agent": f"SentinelX/{VERSION}"})
            with urllib.request.urlopen(req, timeout=6) as r:
                code = r.status
                color = C.GREEN if code < 300 else C.YELLOW
                print(f"  {color}{m:<8}{C.RESET} {code} {r.reason}")
                if m == "OPTIONS":
                    allow = r.headers.get("Allow", "")
                    if allow: info(f"Allow: {allow}")
        except urllib.error.HTTPError as e:
            color = C.RED if e.code >= 400 else C.YELLOW
            print(f"  {color}{m:<8}{C.RESET} {e.code} {e.reason}")
        except Exception as e:
            print(f"  {C.DIM}{m:<8} hata{C.RESET}")

def mod_tech_finger():
    header("Technology Fingerprinter")
    url = prompt("URL")
    if not url: return
    if not url.startswith(("http://","https://")): url = "http://" + url
    try:
        req = urllib.request.Request(url, headers={"User-Agent": f"SentinelX/{VERSION}"})
        with urllib.request.urlopen(req, timeout=10) as r:
            headers = {k.lower(): v for k, v in r.headers.items()}
            body = r.read(200000).decode(errors="ignore").lower()
            found = []
            if "server" in headers: found.append(f"Server: {headers['server']}")
            if "x-powered-by" in headers: found.append(f"X-Powered-By: {headers['x-powered-by']}")
            if "x-aspnet-version" in headers: found.append(f"ASP.NET {headers['x-aspnet-version']}")
            sigs = [
                ("WordPress", ["wp-content","wp-includes","/wp-json/"]),
                ("Joomla", ["/components/com_","joomla"]),
                ("Drupal", ["drupal","sites/default/files"]),
                ("React", ["data-reactroot","react-dom","_react"]),
                ("Vue.js", ["vue.min.js","v-cloak","vue.js"]),
                ("Angular", ["ng-version","angular.min.js"]),
                ("jQuery", ["jquery.min.js","jquery.js"]),
                ("Bootstrap", ["bootstrap.min.css","bootstrap.min.js"]),
                ("Cloudflare", ["cloudflare"]),
                ("nginx", ["nginx"]),
                ("Apache", ["apache"]),
                ("PHP", ["php"]),
            ]
            for name, keys in sigs:
                if any(k in body for k in keys): found.append(name)
            print()
            if found:
                for f in found: ok(f)
            else: warn("Belirgin teknoloji bulunamadi.")
    except Exception as e:
        err(f"Hata: {e}")

def mod_jwt_decode():
    header("JWT Decoder")
    token = prompt("JWT token")
    if not token: return
    parts = token.split(".")
    if len(parts) != 3: err("Gecersiz JWT (3 kisim olmali)."); return
    def b64d(s):
        s += "=" * (-len(s) % 4)
        return base64.urlsafe_b64decode(s).decode(errors="ignore")
    try:
        hdr = json.loads(b64d(parts[0]))
        pld = json.loads(b64d(parts[1]))
        print(f"\n{C.BOLD}Header:{C.RESET}")
        print(json.dumps(hdr, indent=2, ensure_ascii=False))
        print(f"\n{C.BOLD}Payload:{C.RESET}")
        print(json.dumps(pld, indent=2, ensure_ascii=False))
        print(f"\n{C.BOLD}Signature:{C.RESET} {C.DIM}{parts[2]}{C.RESET}")
        if str(hdr.get("alg","")).lower() == "none":
            print()
            warn("KRITIK: alg=none -> dogrulama yok, guvenlik acigi!")
    except Exception as e:
        err(f"Decode hatasi: {e}")

def mod_pass_gen():
    header("Password Generator")
    try: length = int(prompt("Uzunluk [20]") or "20")
    except ValueError: length = 20
    length = max(4, min(length, 256))
    print(f"{C.DIM}  [1] Harf+rakam  [2] Tum semboller  [3] Kolay okunur{C.RESET}")
    ch = prompt("Secim [2]") or "2"
    import secrets
    if ch == "1":
        alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    elif ch == "3":
        alpha = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    else:
        alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{};:,.<>/?"
    try: count = int(prompt("Kac adet [5]") or "5")
    except ValueError: count = 5
    print()
    for _ in range(count):
        pw = "".join(secrets.choice(alpha) for _ in range(length))
        print(f"  {C.GREEN}{pw}{C.RESET}")

def mod_waf_detect():
    header("WAF Detection")
    url = prompt("URL")
    if not url: return
    if not url.startswith(("http://","https://")): url = "http://" + url
    payload = url + "/?q=<script>alert(1)</script>' OR '1'='1"
    try:
        req = urllib.request.Request(payload, headers={"User-Agent": f"SentinelX/{VERSION}"})
        with urllib.request.urlopen(req, timeout=10) as r:
            code = r.status
            hdrs = {k.lower(): v for k, v in r.headers.items()}
            body = r.read(50000).decode(errors="ignore").lower()
    except urllib.error.HTTPError as e:
        code = e.code
        hdrs = {k.lower(): v for k, v in e.headers.items()}
        try: body = e.read(50000).decode(errors="ignore").lower()
        except Exception: body = ""
    except Exception as e:
        err(f"Hata: {e}"); return
    info(f"Yanit kodu: {code}")
    wafs = {
        "Cloudflare": ["cloudflare","cf-ray"],
        "AWS WAF": ["awselb","x-amz"],
        "Sucuri": ["sucuri","x-sucuri"],
        "Akamai": ["akamai","akamaighost"],
        "Imperva/Incapsula": ["incap_ses","visid_incap","x-iinfo"],
        "F5 BIG-IP": ["bigip"],
        "ModSecurity": ["mod_security","modsecurity"],
        "Barracuda": ["barracuda","barra"],
        "Wordfence": ["wordfence"],
        "Fortinet": ["fortiweb","fortigate"],
    }
    alltxt = " ".join(hdrs.keys()) + " " + " ".join(str(v) for v in hdrs.values()) + " " + body
    found = [n for n, sigs in wafs.items() if any(s in alltxt for s in sigs)]
    print()
    if found:
        for f in found: ok(f"Muhtemel WAF: {f}")
    else: warn("Bilinen WAF imzasi bulunamadi.")
    if code in (403, 406):
        info("403/406 -> buyuk ihtimalle WAF engelledi.")

def mod_redirect_chain():
    header("Redirect Chain")
    url = prompt("URL")
    if not url: return
    if not url.startswith(("http://","https://")): url = "http://" + url
    class NoRedir(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None
    opener = urllib.request.build_opener(NoRedir)
    current = url; seen = set()
    for i in range(15):
        if current in seen:
            warn("Dongu algilandi."); break
        seen.add(current)
        try:
            req = urllib.request.Request(current, headers={"User-Agent": f"SentinelX/{VERSION}"})
            with opener.open(req, timeout=10) as r:
                print(f"  {C.GREEN}[{i+1}]{C.RESET} {r.status} {current}")
                break
        except urllib.error.HTTPError as e:
            if e.code in (301,302,303,307,308):
                loc = e.headers.get("Location", "")
                print(f"  {C.YELLOW}[{i+1}]{C.RESET} {e.code} {current}")
                print(f"      {C.DIM}-> {loc}{C.RESET}")
                if loc.startswith("/"):
                    p = urllib.parse.urlparse(current)
                    current = f"{p.scheme}://{p.netloc}{loc}"
                else: current = loc
            else:
                print(f"  {C.RED}[{i+1}]{C.RESET} {e.code} {current}")
                break
        except Exception as e:
            err(f"Hata: {e}"); break

def mod_email_harvest():
    header("Email Harvester")
    url = prompt("URL")
    if not url: return
    if not url.startswith(("http://","https://")): url = "http://" + url
    try:
        req = urllib.request.Request(url, headers={"User-Agent": f"SentinelX/{VERSION}"})
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read(500000).decode(errors="ignore")
        import re
        emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html))
        emails = {e for e in emails if not e.lower().endswith((".png",".jpg",".gif",".css",".js"))}
        print()
        if emails:
            ok(f"{len(emails)} e-posta bulundu:")
            for e in sorted(emails): print(f"    {C.CYAN}{e}{C.RESET}")
        else: warn("E-posta bulunamadi.")
    except Exception as e:
        err(f"Hata: {e}")

def mod_robots():
    header("robots.txt / sitemap.xml")
    url = prompt("URL").rstrip("/")
    if not url: return
    if not url.startswith(("http://","https://")): url = "http://" + url
    for path in ["/robots.txt", "/sitemap.xml"]:
        full = url + path
        try:
            req = urllib.request.Request(full, headers={"User-Agent": f"SentinelX/{VERSION}"})
            with urllib.request.urlopen(req, timeout=8) as r:
                body = r.read(50000).decode(errors="ignore")
                ok(f"{full}  ({r.status})")
                print(f"{C.DIM}{'-'*62}{C.RESET}")
                print(body[:3000])
                if len(body) > 3000: print(f"{C.DIM}...(+{len(body)-3000} karakter){C.RESET}")
                print(f"{C.DIM}{'-'*62}{C.RESET}")
        except urllib.error.HTTPError as e:
            warn(f"{full} -> {e.code}")
        except Exception as e:
            warn(f"{full} -> hata")

def mod_ssl_versions():
    header("SSL/TLS Version Scanner")
    host = prompt("Host")
    if not host: return
    try: port = int(prompt("Port [443]") or "443")
    except ValueError: port = 443
    versions = [
        ("TLS 1.3", ssl.TLSVersion.TLSv1_3),
        ("TLS 1.2", ssl.TLSVersion.TLSv1_2),
        ("TLS 1.1", ssl.TLSVersion.TLSv1_1),
        ("TLS 1.0", ssl.TLSVersion.TLSv1),
    ]
    for name, ver in versions:
        try:
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            ctx.minimum_version = ver
            ctx.maximum_version = ver
            with socket.create_connection((host, port), timeout=6) as sock:
                with ctx.wrap_socket(sock, server_hostname=host) as ss:
                    ok(f"{name} -> DESTEKLENIYOR ({ss.version()})")
        except Exception:
            warn(f"{name} -> desteklenmiyor")

MENU=[
    ("Port Scanner",              mod_port_scanner),
    ("DNS Lookup",                mod_dns_lookup),
    ("WHOIS Lookup",              mod_whois),
    ("Subdomain Enumeration",     mod_subdomain),
    ("Banner Grabber",            mod_banner_grab),
    ("HTTP Header Analyzer",      mod_http_headers),
    ("SSL Certificate Inspector", mod_ssl_cert),
    ("Directory / File Scanner",  mod_dir_scan),
    ("Hash Generator",            mod_hash_gen),
    ("Hash Cracker",              mod_hash_crack),
    ("Password Strength",         mod_password_strength),
    ("Encoder / Decoder",         mod_encoder),
    ("IP Geolocation",            mod_ip_geo),
    ("Host Discovery (TCP Ping)", mod_ping_sweep),
    ("MAC Vendor Lookup",         mod_mac_vendor),
    ("HTTP Method Tester",        mod_http_methods),
    ("Tech Fingerprinter",        mod_tech_finger),
    ("JWT Decoder",               mod_jwt_decode),
    ("Password Generator",        mod_pass_gen),
    ("WAF Detection",             mod_waf_detect),
    ("Redirect Chain",            mod_redirect_chain),
    ("Email Harvester",           mod_email_harvest),
    ("robots.txt / sitemap.xml",  mod_robots),
    ("SSL/TLS Version Scanner",   mod_ssl_versions),
]

def print_menu():
    clear(); print(BANNER)
    print(f"{C.DIM}{'-'*62}{C.RESET}")
    for i,(name,_) in enumerate(MENU,1):
        print(f"  {C.MAGENTA}[{i:>2}]{C.RESET}  {name}")
    print(f"  {C.RED}[ 0]{C.RESET}  Cikis")
    print(f"{C.DIM}{'-'*62}{C.RESET}")

def main():
    clear(); print(BANNER)
    print(f"{C.GREEN}Hos geldin, {C.BOLD}{USER_NAME}{C.RESET}{C.GREEN}. "
          f"SentinelX v{VERSION} hazir.{C.RESET}")
    print(f"{C.DIM}Yalnizca yetkili oldugun sistemlerde kullan.{C.RESET}")
    try: input(f"\n{C.DIM}Baslamak icin Enter...{C.RESET}")
    except (KeyboardInterrupt, EOFError): return
    while True:
        print_menu()
        try: ch=input(f"\n{C.MAGENTA}[{USER_NAME}]{C.RESET} Secim: ").strip()
        except (KeyboardInterrupt, EOFError): print(); break
        if ch=="0": break
        if not ch.isdigit(): warn("Gecersiz."); time.sleep(1); continue
        idx=int(ch)
        if 1<=idx<=len(MENU):
            name,func=MENU[idx-1]
            try: func()
            except KeyboardInterrupt: warn("Iptal.")
            except Exception as e: err(f"Hata: {e}")
            pause()
        else: warn("Gecersiz."); time.sleep(1)
    print(f"\n{C.CYAN}Gorusuruz, {C.BOLD}{USER_NAME}{C.RESET}{C.CYAN}.{C.RESET}\n")

if __name__=="__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{C.YELLOW}Cikiliyor...{C.RESET}")

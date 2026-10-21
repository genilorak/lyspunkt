#!/usr/bin/env python3
"""Bygger hele Lyspunkt-nettstedet fra data/saker.json.

Kjør fra repoets rot:  python3 verktoy/bygg.py
"""
import os, json, html, hashlib, glob, datetime

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROT, 'data', 'saker.json'), encoding='utf-8'))

KAT = {
    'norge': ('Norge', 'Gode nyheter fra hele landet — fra byene til de minste bygdene.', '#FFF3CC', '#8A6400'),
    'verden': ('Verden', 'Fremskritt, samarbeid og gode historier fra hele kloden.', '#E9E1FF', '#6C4FD6'),
    'vitenskap': ('Vitenskap', 'Oppdagelser og forskning som flytter grensene — med forbeholdene på plass.', '#E2F4F1', '#137A6E'),
    'helse': ('Helse', 'Nye behandlinger, bedre folkehelse og forskning som gir håp.', '#E6EFFD', '#3A64B5'),
    'klima-og-miljo': ('Klima og miljø', 'Løsninger, naturrestaurering og tiltak som faktisk virker.', '#EEF5DC', '#5C7F14'),
    'dyr-og-natur': ('Dyr og natur', 'Arter som kommer tilbake, dyr som blir reddet og natur som leges.', '#E4F5E8', '#2E8A4F'),
    'teknologi': ('Teknologi', 'Oppfinnelser og innovasjon som gjør hverdagen og verden bedre.', '#E3E9F4', '#4F6E9E'),
    'verdensrommet': ('Verdensrommet', 'Teleskoper, satellitter og nye blikk ut i universet.', '#ECE8FD', '#5B47C2'),
    'kultur': ('Kultur', 'Kunst, musikk og fellesskap som løfter hverdagen.', '#FBE6F3', '#A2397F'),
    'sport': ('Sport', 'Idrettsglede, inkludering og lag som vokser.', '#E0F3FA', '#1B7397'),
    'musikk': ('Musikk', 'Nyslupne låter, nye stjerneskudd og gode nyheter fra musikkverdenen.', '#FFEEDB', '#A65300'),
    'sma-gleder': ('Små gleder', 'Hjertevarme, søte og morsomme historier som gjør dagen litt bedre.', '#FFF1B8', '#8A6400'),
}
NAV = ['norge', 'verden', 'vitenskap', 'helse', 'klima-og-miljo', 'dyr-og-natur', 'teknologi', 'verdensrommet', 'musikk', 'kultur', 'sport', 'sma-gleder']
BLOKKER = ['norge', 'verden', 'vitenskap', 'helse', 'klima-og-miljo', 'dyr-og-natur', 'teknologi', 'verdensrommet', 'musikk', 'kultur', 'sport', 'sma-gleder']
STANDARD_VALGT = ['vitenskap', 'dyr-og-natur', 'helse', 'verdensrommet', 'klima-og-miljo', 'norge', 'musikk', 'kultur', 'sport']
MND = ['jan.', 'feb.', 'mars', 'apr.', 'mai', 'juni', 'juli', 'aug.', 'sep.', 'okt.', 'nov.', 'des.']
DAGER = ['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lørdag', 'Søndag']

SAKER = [s for s in DATA['saker'] if s.get('status', 'publisert') == 'publisert' and s.get('kategorier')]
SAKER.sort(key=lambda s: (s.get('kildedato', ''), s.get('publisert', '')), reverse=True)
BY = {s['id']: s for s in SAKER}
SISTE = sorted(SAKER, key=lambda s: (s.get('publisert', ''), s.get('kildedato', '')), reverse=True)
e = html.escape

def dato(iso, aar=False):
    d = datetime.date.fromisoformat(iso[:10])
    return f'{d.day}. {MND[d.month-1]}' + (f' {d.year}' if aar else '')

OPPDATERT = datetime.datetime.fromisoformat(DATA.get('oppdatert', '2026-01-01T00:00:00+00:00'))
I_DAG = f'{DAGER[OPPDATERT.weekday()]} {OPPDATERT.day}. {["januar","februar","mars","april","mai","juni","juli","august","september","oktober","november","desember"][OPPDATERT.month-1]}'

SUN = '<svg width="{s}" height="{s}" viewBox="0 0 32 32" aria-hidden="true"><path d="M9 22a7 7 0 0 1 14 0z" fill="#FFB800"></path><line x1="4" y1="22.5" x2="28" y2="22.5" stroke="#16120F" stroke-width="1.8" stroke-linecap="round"></line><line x1="16" y1="7" x2="16" y2="10.5" stroke="#FFB800" stroke-width="2" stroke-linecap="round"></line><line x1="8" y1="11" x2="10.2" y2="13.4" stroke="#FFB800" stroke-width="2" stroke-linecap="round"></line><line x1="24" y1="11" x2="21.8" y2="13.4" stroke="#FFB800" stroke-width="2" stroke-linecap="round"></line></svg>'

def kat(s):
    return s['kategorier'][0]

def kunst(s, h=260):
    """Abstrakt soloppgang i kategorifargene. Ikke et fotografi av hendelsen."""
    tint, acc = KAT[kat(s)][2], KAT[kat(s)][3]
    hv = int(hashlib.md5(s['id'].encode()).hexdigest(), 16)
    x = 120 + hv % 360
    r1 = 150 + (hv >> 8) % 70
    r2 = int(r1 * 0.62)
    r3 = int(r1 * 0.32)
    sx = 40 + (hv >> 16) % 520
    sy = 30 + (hv >> 24) % 70
    return (f'<svg viewBox="0 0 600 {h}" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" aria-hidden="true" style="display:block;background:{tint}">'
            f'<circle cx="{sx}" cy="{sy}" r="9" fill="{acc}" opacity=".25"></circle>'
            f'<circle cx="{(sx+260)%600}" cy="{sy+40}" r="5" fill="{acc}" opacity=".3"></circle>'
            f'<path d="M{x-r1} {h}a{r1} {r1} 0 0 1 {2*r1} 0z" fill="#FFE08A"></path>'
            f'<path d="M{x-r2} {h}a{r2} {r2} 0 0 1 {2*r2} 0z" fill="#FFC93A"></path>'
            f'<path d="M{x-r3} {h}a{r3} {r3} 0 0 1 {2*r3} 0z" fill="#FFB800"></path>'
            f'<rect x="0" y="{h-6}" width="600" height="6" fill="{acc}" opacity=".35"></rect></svg>')


def kildenavn(s):
    k = (s.get('kilder') or [{}])[0]
    return (k.get('navn') or 'kilden').split(':')[0].split(' (')[0].strip()

def kildeurl(s):
    return (s.get('kilder') or [{}])[0].get('url', '#')

def har_bilde(s):
    b = s.get('bilde')
    return bool(b and b.get('url'))

def bildet(s, h=260, base=''):
    """Kildens bilde hvis lisensen tillater det. Uten lovlig bilde vises ingenting."""
    if not har_bilde(s):
        return ''
    b = s['bilde']
    return f'<img src="{e(b["url"])}" alt="{e(b.get("alt", ""))}" loading="lazy" onerror="var b=this.closest(\'.img,.sgimg\');if(b)b.remove();else this.remove()" style="width:100%;height:100%;object-fit:cover;display:block">'

def bildeboks(s, h, cls='img', stil=''):
    """Bildeboks bare når saken har et lovlig bilde."""
    if not har_bilde(s):
        return ''
    st = f' style="{stil}"' if stil else ''
    return f'<div class="{cls}"{st}>{bildet(s, h)}</div>'


CSS = r"""
body{margin:0;background:#FFFBF2;color:#16120F;font-family:'Hanken Grotesk',sans-serif}
a{color:#16120F;text-decoration:none}a:hover{color:#0E7A4E}
.bri{font-family:'Bricolage Grotesque',sans-serif}
.ser{font-family:'Instrument Serif',Georgia,serif;font-weight:400}
.kick{font-size:11px;letter-spacing:.12em;text-transform:uppercase;font-weight:700}
.meta{font-size:12px;color:#5E665F}
.wrap{width:100%;margin:0;box-sizing:border-box;min-height:100vh;display:flex;flex-direction:column}
.inner{padding:0 56px}
.ticker{background:#FFFFFF;border-bottom:1px solid #EFE6D6;height:40px;display:flex;align-items:center;gap:16px;padding:0 56px;font-size:14px;font-weight:500;white-space:nowrap;overflow:hidden}
.tvindu{flex:1;overflow:hidden;-webkit-mask-image:linear-gradient(to right,transparent,#000 24px,#000 calc(100% - 24px),transparent);mask-image:linear-gradient(to right,transparent,#000 24px,#000 calc(100% - 24px),transparent)}
.tbane{display:inline-flex;gap:20px;align-items:center;padding-left:8px;animation:rull 90s linear infinite}
.tbane:hover,.ticker:focus-within .tbane{animation-play-state:paused}
.tbane .sep{opacity:.35}
@keyframes rull{from{transform:translateX(0)}to{transform:translateX(-50%)}}
@media (prefers-reduced-motion:reduce){.tbane{animation:none}}
.ticker .t{background:#FFE98A;padding:2px 7px;border-radius:6px;margin-right:6px;font-family:'Bricolage Grotesque',sans-serif;font-weight:700}
.pill{display:inline-flex;align-items:center;font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;padding:4px 10px;border-radius:999px}
.hdr{padding:0 56px;border-bottom:1.5px solid #16120F}
.hdr-top{height:118px;display:grid;grid-template-columns:1fr auto 1fr;align-items:center}
.iconbtn{width:44px;height:44px;border:1.5px solid #16120F;background:transparent;border-radius:22px;display:flex;align-items:center;justify-content:center;cursor:pointer;color:#16120F}
.nav{height:56px;border-top:1px solid #EFE6D6;display:flex;align-items:center;justify-content:center;gap:6px;font-size:15px;font-weight:600}
.nav a{padding:9px 14px;border-radius:999px;white-space:nowrap;flex:none}
.nav a.on{background:#16120F;color:#FFFBF2}
.nav a.sg{background:#FFE89A}
.nav a.sg.on{background:#16120F;color:#FFFBF2}
main{flex:1}
.shead{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:24px}
.h2{margin:0;font-family:'Bricolage Grotesque',sans-serif;font-size:40px;font-weight:800;letter-spacing:-0.04em;line-height:1}
.crumb{font-size:14px;font-weight:600;color:#5E665F;padding:28px 0 0}
.crumb a{color:#5E665F;text-decoration:underline;text-underline-offset:3px}
.h1{margin:0;font-family:'Bricolage Grotesque',sans-serif;font-weight:800;letter-spacing:-0.04em;line-height:.98}
.grid3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
.card{border-radius:20px;overflow:hidden;display:flex;flex-direction:column;background:#FFFFFF;box-shadow:0 1px 0 rgba(22,18,15,.06)}
.card .img{height:200px}
.card .txt{padding:20px 22px 24px;display:flex;flex-direction:column;gap:8px;flex:1}
.card h3{margin:0;font-family:'Bricolage Grotesque',sans-serif;font-size:23px;font-weight:700;line-height:1.05;letter-spacing:-0.02em}
.card p{margin:0;font-size:14px;line-height:1.5;color:#3D4540}
.topp{border-radius:22px;overflow:hidden;display:flex;flex-direction:column}
.topp .img{height:170px;flex:none}
.topp .txt{padding:18px 22px 20px;display:flex;flex-direction:column;gap:8px;flex:1}
.topp h3{margin:0;font-family:'Bricolage Grotesque',sans-serif;font-size:24px;font-weight:800;line-height:1.05;letter-spacing:-0.02em}
.topp p{margin:0;font-size:15px;line-height:1.45;color:#3D4540;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.blokk{border-radius:22px;padding:28px;display:flex;flex-direction:column}
.blokk .rad{display:grid;grid-template-columns:1fr auto;gap:16px;align-items:baseline;padding:14px 0;border-bottom:1px solid rgba(22,18,15,.1)}
.blokk .rad:last-child{border-bottom:none;padding-bottom:0}
.foot{background:#FFF3C2;margin-top:64px;display:flex;flex-direction:column}
.foot-in{padding:44px 56px 0;display:flex;flex-direction:column;gap:32px}
.foot-links{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:24px;font-size:14px;line-height:1.8;padding-top:32px;border-top:1.5px solid rgba(22,18,15,.15)}
.foot-links .col{grid-column:span 3;display:flex;flex-direction:column}
.foot-band{background:#FFC93A;padding:18px 56px;text-align:center;font-size:12px;color:#5C4600}
.btn{display:inline-flex;align-items:center;justify-content:center;font:inherit;font-size:16px;font-weight:700;height:52px;padding:0 26px;border-radius:999px;border:none;cursor:pointer}
.prose{max-width:720px}
.prose p{font-size:19px;line-height:1.7;margin:0 0 22px;color:#2A2622}
.prose h2{font-family:'Bricolage Grotesque',sans-serif;font-size:28px;letter-spacing:-0.02em;margin:40px 0 12px}
.prose ul{font-size:18px;line-height:1.7;padding-left:22px;margin:0 0 22px}
.prose a{color:#4F6E9E;text-decoration:underline;text-underline-offset:3px}
.demo{background:#FFF1B8;border-radius:14px;padding:14px 18px;font-size:14px;color:#5C4600}
.tom{border:1.5px dashed rgba(22,18,15,.2);border-radius:16px;padding:22px;font-size:15px;color:#5E665F}
input[type=search],input[type=email],input[type=text],textarea{font:inherit;font-size:16px;border-radius:999px;border:1.5px solid #E6DCC0;background:#FFFFFF;padding:0 20px;height:56px;box-sizing:border-box}
textarea{border-radius:20px;padding:16px 20px;height:160px;width:100%}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
:focus-visible{outline:3px solid #4F6E9E;outline-offset:2px}

.kvalg{position:relative;display:inline-flex}
.kvalg input{position:absolute;opacity:0;width:100%;height:100%;margin:0;cursor:pointer}
.kvalg span{display:inline-flex;align-items:center;gap:6px;font-size:14px;font-weight:600;padding:9px 14px;border-radius:999px;border:1.5px solid var(--a);color:var(--a);background:#FFFFFF}
.kvalg span::before{content:"";width:14px;height:14px;border-radius:4px;border:1.5px solid var(--a);box-sizing:border-box}
.kvalg input:checked+span{background:var(--t);color:#16120F}
.kvalg input:checked+span::before{background:var(--a);box-shadow:inset 0 0 0 2px var(--t)}
.kvalg input:focus-visible+span{outline:3px solid #4F6E9E;outline-offset:2px}
.grid3,[style*="repeat(2,minmax(0,1fr))"],[style*="repeat(3,minmax(0,1fr))"]{align-items:start}
[style*="repeat(12,minmax(0,1fr))"]{align-items:start}
.inner,.hdr,.ticker,.foot-in,.foot-band{padding-left:max(56px,calc((100% - 1328px) / 2))!important;padding-right:max(56px,calc((100% - 1328px) / 2))!important}
img,svg{max-width:100%}
.nav{overflow-x:auto;scrollbar-width:none}
.nav::-webkit-scrollbar{display:none}
@media (max-width:1180px){
  .grid3{grid-template-columns:repeat(2,minmax(0,1fr))}
  .nav{justify-content:flex-start}
  [style*="grid-column:span 8"],[style*="grid-column:span 4"]{grid-column:1 / -1!important}
}
@media (max-width:900px){
  .inner,.hdr,.ticker,.foot-in,.foot-band{padding-left:20px!important;padding-right:20px!important}
  [style*="repeat(12,minmax(0,1fr))"]{grid-template-columns:1fr!important}
  [style*="grid-column:"]{grid-column:1 / -1!important}
  [style*="repeat(2,minmax(0,1fr))"]{grid-template-columns:1fr!important}
  .foot-links{grid-template-columns:repeat(2,minmax(0,1fr))!important}
  .foot-links .col{grid-column:auto!important}
  main section[style*="border-radius"]{padding:28px 22px!important}
  main section[style*="justify-content:space-between"]{flex-wrap:wrap}
  .hdr-top{grid-template-columns:1fr auto;height:auto;padding:16px 0;gap:12px}
  .hdr-top>span:first-child{display:none}
  .hdr-top>div:nth-child(2){align-items:flex-start!important}
  .hdr-top .ser{padding-left:0!important;font-size:16px!important}
  .hdr-top .bri{font-size:32px!important}
  .shead{flex-wrap:wrap;gap:8px}
  [style*="grid-template-columns:110px 200px 1fr"],[style*="grid-template-columns:200px 1fr"]{grid-template-columns:1fr!important;gap:6px!important}
  [style*="height:480px"]{height:260px!important}
  .prose p{font-size:17px}
  .foot-in .bri[style*="font-size:64px"]{font-size:44px!important}
  .foot-in .ser{padding-left:0!important}
  [style*="margin:-8px -56px -32px"]{margin:-8px -20px -32px!important}
  .foot svg[width="600"]{width:100%;height:auto}
}
@media (max-width:640px){
  .grid3{grid-template-columns:1fr}
  [style*="repeat(3,minmax(0,1fr))"]{grid-template-columns:1fr!important}
  .ticker{font-size:13px}
  .topp h3{font-size:22px}
  .h2{font-size:32px}
  form [style*="display:flex;gap:8px"]{flex-direction:column}
}
html.dark{filter:invert(1) hue-rotate(180deg);background:#000}
html.dark img{filter:invert(1) hue-rotate(180deg)}
"""

SISTE_JS = r'''<script>
(function(){
var MND=['jan.','feb.','mars','apr.','mai','juni','juli','aug.','sep.','okt.','nov.','des.'];
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function merke(p,idag){var d=new Date(p);if(isNaN(d))return '';var o=d.toLocaleDateString('sv-SE',{timeZone:'Europe/Oslo'});if(o===idag)return d.toLocaleTimeString('nb-NO',{timeZone:'Europe/Oslo',hour:'2-digit',minute:'2-digit'});var dd=new Date(o+'T12:00:00');return dd.getDate()+'. '+MND[dd.getMonth()]}
function oppdater(){var t=document.querySelector('.ticker');if(!t)return;var base=t.getAttribute('data-base')||'';
fetch(base+'data/siste.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(d){if(!d||!d.saker||!d.saker.length)return;
var idag=new Date().toLocaleDateString('sv-SE',{timeZone:'Europe/Oslo'});
var it=d.saker.slice(0,10).map(function(s){return '<a href="'+base+'artikkel/'+esc(s.id)+'.html"><span class="t">'+esc(merke(s.publisert,idag))+'</span>'+esc(s.tittel)+'</a><span class="sep">/</span>'}).join('');
var b=t.querySelector('.tbane');if(b&&b.getAttribute('data-sig')!==d.oppdatert){b.innerHTML=it+it;b.setAttribute('data-sig',d.oppdatert)}
var l=document.getElementById('siste-liste');if(l){l.innerHTML=d.saker.slice(0,5).map(function(s){return '<a href="'+base+'artikkel/'+esc(s.id)+'.html" style="display:grid;grid-template-columns:70px 1fr;gap:10px;padding:16px 0;border-top:1px solid rgba(14,122,78,.2)"><span class="bri" style="font-weight:700;color:#0E7A4E">'+esc(merke(s.publisert,idag))+'</span><span style="font-size:16px;font-weight:600;line-height:1.35">'+esc(s.tittel)+'</span></a>'}).join('')}
}).catch(function(){})}
document.addEventListener('DOMContentLoaded',function(){oppdater();setInterval(oppdater,120000)});
})();
</script>'''

THEME_JS = """<script>
(function(){var k='lyspunkt-tema';try{if(localStorage.getItem(k)==='dark')document.documentElement.classList.add('dark')}catch(e){}
document.addEventListener('DOMContentLoaded',function(){var b=document.getElementById('tema');if(!b)return;
function lab(){var d=document.documentElement.classList.contains('dark');b.setAttribute('aria-label',d?'Bytt til lyst tema':'Bytt til mørkt tema');b.setAttribute('aria-pressed',d?'true':'false')}lab();
b.addEventListener('click',function(){var d=document.documentElement.classList.toggle('dark');try{localStorage.setItem(k,d?'dark':'light')}catch(e){}lab()})})})();
</script>"""

def head(title, base, desc='Lyspunkt – et lysere blikk på verden. Gode nyheter, ekte historier og dokumenterte fremskritt.'):
    return f'''<!doctype html>
<html lang="no">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{e(desc)}">
<title>{e(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&amp;family=Instrument+Serif:ital@0;1&amp;family=Hanken+Grotesk:wght@400;500;600;700&amp;display=swap">
<link rel="stylesheet" href="{base}stil.css">
{THEME_JS}
{SISTE_JS}
</head>
<body>
<div class="wrap">
'''

def tidsmerke(s):
    """Klokkeslett hvis saken er publisert samme dag som siste oppdatering, ellers dato."""
    pub = s.get('publisert', '')
    if pub[:10] == DATA.get('oppdatert', '')[:10] and len(pub) >= 16:
        return pub[11:16]
    return dato(pub or s['kildedato'])

def ticker(base):
    items = ''.join(f'<a href="{base}artikkel/{s["id"]}.html"><span class="t">{tidsmerke(s)}</span>{e(s["tittel"])}</a><span class="sep">/</span>' for s in SISTE[:10])
    return (f'<div class="ticker" data-base="{base}"><span class="pill" style="background:#FFD23F;flex:none;position:relative;z-index:1">Siste</span>'
            f'<div class="tvindu"><div class="tbane">{items}{items}</div></div></div>\n')

def header(base, active=None):
    nav = f'<a href="{base}index.html"{" class=\"on\"" if active == "forside" else ""}>Forsiden</a>'
    for s in NAV:
        cls = (['sg'] if s == 'sma-gleder' else []) + (['on'] if s == active else [])
        c = f' class="{" ".join(cls)}"' if cls else ''
        nav += f'<a href="{base}kategori/{s}.html"{c}>{KAT[s][0]}</a>'
    return ticker(base) + f'''<header class="hdr">
  <div class="hdr-top">
    <span style="font-size:14px;font-weight:600;color:#5E665F">{I_DAG}</span>
    <div style="display:flex;flex-direction:column;align-items:center;gap:2px">
      <a href="{base}index.html" aria-label="Lyspunkt forside" style="display:flex;align-items:center;gap:10px">{SUN.format(s=40)}<span class="bri" style="font-size:42px;font-weight:800;letter-spacing:-0.045em">lyspunkt</span></a>
      <span class="ser" style="font-size:21px;font-style:italic;color:#4F6E9E;padding-left:50px">Et lysere blikk på verden.</span>
    </div>
    <div style="display:flex;justify-content:flex-end;gap:10px;align-items:center">
      <a href="{base}sok.html" class="iconbtn" aria-label="Søk"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#16120F" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><line x1="16.5" y1="16.5" x2="21" y2="21"></line></svg></a>
      <button id="tema" type="button" class="iconbtn" aria-label="Bytt til mørkt tema"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#16120F" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"></path></svg></button>
    </div>
  </div>
  <nav class="nav" aria-label="Kategorier">{nav}</nav>
</header>
'''

def footer(base):
    k1 = ''.join(f'<a href="{base}kategori/{s}.html">{KAT[s][0]}</a>' for s in ['norge', 'verden', 'vitenskap', 'helse', 'klima-og-miljo', 'dyr-og-natur'])
    k2 = ''.join(f'<a href="{base}kategori/{s}.html">{KAT[s][0]}</a>' for s in ['teknologi', 'verdensrommet', 'musikk', 'kultur', 'sport', 'sma-gleder'])
    return f'''<footer class="foot">
  <div class="foot-in">
    <div style="display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:24px;align-items:center">
      <div style="grid-column:span 6;display:flex;flex-direction:column;gap:6px">
        <a href="{base}index.html" style="display:flex;align-items:center;gap:14px">{SUN.format(s=56)}<span class="bri" style="font-size:clamp(36px,6vw,64px);font-weight:800;letter-spacing:-0.05em;line-height:1">lyspunkt</span></a>
        <span class="ser" style="font-size:28px;font-style:italic;color:#4F6E9E;padding-left:70px">Et lysere blikk på verden.</span>
      </div>
      <form action="{base}nyhetsbrev.html" method="get" style="grid-column:8 / span 5;background:#FFFFFF;border-radius:22px;padding:26px;display:flex;flex-direction:column;gap:12px;box-shadow:0 10px 30px rgba(138,100,0,.12)">
        <span class="bri" style="font-size:24px;font-weight:800;letter-spacing:-0.03em">Ukens lyspunkter, rett i innboksen</span>
        <span style="font-size:14px;color:#3D4540">Hver fredag. Tre gode nyheter og én liten glede. Gratis.</span>
        <div style="display:flex;gap:8px">
          <label for="fepost" class="sr">E-postadresse</label>
          <input id="fepost" name="epost" type="email" required placeholder="din@epost.no" style="flex:1;height:48px;background:#FFFBF2">
          <button type="submit" class="btn" style="height:48px;background:#4F6E9E;color:#FFFFFF;font-size:15px">Meld meg på</button>
        </div>
      </form>
    </div>
    <div class="foot-links">
      <div class="col"><span class="kick" style="color:#8A6400;margin-bottom:8px">Kategorier</span>{k1}</div>
      <div class="col"><span class="kick" style="color:#8A6400;margin-bottom:8px">&#160;</span>{k2}</div>
      <div class="col"><span class="kick" style="color:#8A6400;margin-bottom:8px">Redaksjonen</span><span>Ansvarlig redaktør: Karoline D. Gjeldnes</span><span>Sakene hentes og skrives av KI</span><a href="{base}redaksjonen.html" style="align-self:flex-start;margin-top:8px;background:#16120F;color:#FFFBF2;padding:8px 14px;border-radius:999px;font-weight:700;line-height:1.4">Om redaksjonen →</a><a href="{base}tips.html" style="margin-top:6px">Tips oss</a><a href="{base}om.html">Om Lyspunkt</a></div>
      <div class="col"><span class="kick" style="color:#8A6400;margin-bottom:8px">Slik jobber vi</span><a href="{base}prinsipper.html">Redaksjonelle prinsipper</a><a href="{base}rettelser.html">Rettelser</a><a href="{base}ai.html">Bruk av AI</a><a href="{base}personvern.html">Personvern</a></div>
    </div>
    <div aria-hidden="true" style="display:flex;justify-content:center;margin:-8px -56px -32px">
      <svg width="384" height="160" viewBox="0 0 600 250" style="display:block"><path d="M60 250a240 240 0 0 1 480 0z" fill="#FFE08A"></path><path d="M140 250a160 160 0 0 1 320 0z" fill="#FFC93A"></path><path d="M210 250a90 90 0 0 1 180 0z" fill="#FFB800"></path></svg>
    </div>
  </div>
  <div class="foot-band" style="margin-top:32px">© Lyspunkt · Sist oppdatert {dato(DATA["oppdatert"], True)} kl. {OPPDATERT.strftime("%H:%M")} · <a href="{base}ai.html" style="color:#5C4600;text-decoration:underline">Slik bruker vi AI</a></div>
</footer>
</div>
</body>
</html>
'''

def card(s, base):
    navn, _, _, acc = KAT[kat(s)]
    return f'''<a href="{base}artikkel/{s["id"]}.html" class="card">
  {bildeboks(s, 200)}
  <div class="txt"><span class="kick" style="color:{acc}">{navn}</span><h3>{e(s["tittel"])}</h3><p>{e(s["ingress"])}</p><span class="meta" style="margin-top:auto">{dato(s["kildedato"])}</span></div>
</a>'''

def tom(tekst='Ingen saker her ennå. Redaksjonen leter etter nye lyspunkter flere ganger om dagen.'):
    return f'<div class="tom">{tekst}</div>'

def write(path, s):
    full = os.path.join(ROT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(s)

# ---------------------------------------------------------------- forsiden
def forside():
    base = ''
    topp = [BY[i] for i in DATA.get('topp3', []) if i in BY]
    for s in SAKER:
        if len(topp) >= 3: break
        if s not in topp: topp.append(s)
    toppkort = ''
    for s in topp[:3]:
        navn, _, tint, acc = KAT[kat(s)]
        toppkort += f'''<a href="artikkel/{s["id"]}.html" class="topp" style="background:{tint}">
          {bildeboks(s, 170)}
          <div class="txt"><span class="kick" style="color:{acc}">{navn}</span><h3>{e(s["tittel"])}</h3><p>{e(s["ingress"])}</p><span class="meta" style="margin-top:auto">{dato(s["kildedato"])}</span></div>
        </a>'''
    sg = [s for s in SAKER if 'sma-gleder' in s['kategorier']][:3]
    rot = ['-1.5deg', '1deg', '-0.5deg']
    sgk = ''.join(f'''<a href="artikkel/{s["id"]}.html" style="display:flex;flex-direction:column;gap:12px;background:#FFFFFF;padding:10px 10px 18px;box-shadow:0 8px 22px rgba(22,18,15,.12);transform:rotate({rot[i]})">
            {bildeboks(s, 200, 'sgimg', 'height:200px;overflow:hidden')}
            <span class="bri" style="font-size:20px;font-weight:700;line-height:1.05;letter-spacing:-0.02em;padding:0 4px">{e(s["tittel"])}</span>
          </a>''' for i, s in enumerate(sg)) or tom()
    siste = '<div id="siste-liste">' + ''.join(f'''<a href="artikkel/{s["id"]}.html" style="display:grid;grid-template-columns:70px 1fr;gap:10px;padding:16px 0;border-top:1px solid rgba(14,122,78,.2)"><span class="bri" style="font-weight:700;color:#0E7A4E">{tidsmerke(s)}</span><span style="font-size:16px;font-weight:600;line-height:1.35">{e(s["tittel"])}</span></a>''' for s in SISTE[:5]) + '</div>'
    blokker = ''
    for k in BLOKKER:
        navn, _, tint, acc = KAT[k]
        ss = [s for s in SAKER if k in s['kategorier']][:3]
        if ss:
            first = ss[0]
            rows = f'''<a href="artikkel/{first["id"]}.html" style="display:flex;flex-direction:column;gap:8px;padding:14px 0;{"border-bottom:1px solid rgba(22,18,15,.1)" if len(ss) > 1 else ""}">
            <span class="bri" style="font-size:24px;font-weight:700;line-height:1.05;letter-spacing:-0.02em">{e(first["tittel"])}</span>
            <span class="meta">{dato(first["kildedato"])}</span></a>'''
            rows += ''.join(f'<a href="artikkel/{s["id"]}.html" class="rad"><span style="font-size:17px;font-weight:600;line-height:1.3">{e(s["tittel"])}</span><span class="meta">{dato(s["kildedato"])}</span></a>' for s in ss[1:])
        else:
            rows = '<p style="margin:14px 0 0;font-size:16px;color:#3D4540">Ingen saker ennå. Redaksjonen leter fortløpende.</p>'
        blokker += f'''<div class="blokk" data-kat="{k}" style="background:{tint}">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px">
            <div style="display:flex;align-items:center;gap:10px"><span style="width:12px;height:12px;border-radius:6px;background:{acc}"></span><h3 class="bri" style="margin:0;font-size:26px;font-weight:800;letter-spacing:-0.03em">{navn}</h3></div>
            <a href="kategori/{k}.html" style="font-size:13px;font-weight:700;color:{acc};padding:8px 13px;border-radius:999px;background:#FFFFFF">Se alle →</a>
          </div>
          {rows}
        </div>'''
    valg = ''.join(f'<label class="kvalg" style="--a:{KAT[k][3]};--t:{KAT[k][2]}"><input type="checkbox" value="{k}"{" checked" if k in STANDARD_VALGT else ""}><span>{KAT[k][0]}</span></label>' for k in BLOKKER)
    page = head('Lyspunkt – et lysere blikk på verden', base) + header(base, 'forside') + f'''<main class="inner" style="padding-top:32px;display:flex;flex-direction:column;gap:72px">
  <section aria-labelledby="t3">
    <div class="shead"><h2 id="t3" class="h2">Dagens topp 3</h2><span class="meta">Oppdatert {dato(DATA["oppdatert"])} kl. {OPPDATERT.strftime("%H:%M")}</span></div>
    <div class="grid3">{toppkort}</div>
  </section>
  <section aria-labelledby="kat">
    <div class="shead"><h2 id="kat" class="h2">Utforsk <span class="ser" style="font-style:italic;font-weight:400;letter-spacing:0;color:#4F6E9E">kategoriene</span></h2><span class="meta">Velg hvilke kategorier du vil se. Valget lagres i nettleseren din.</span></div>
    <fieldset style="border:none;margin:0 0 24px;padding:18px 20px;background:#FFFFFF;border-radius:18px;box-shadow:0 1px 0 rgba(22,18,15,.06)">
      <legend class="sr">Velg kategorier</legend>
      <div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center">{valg}
        <button type="button" id="kalle" style="font:inherit;font-size:13px;font-weight:700;background:none;border:none;color:#4F6E9E;text-decoration:underline;cursor:pointer;padding:8px">Vis alle</button>
      </div>
    </fieldset>
    <div id="kblokker" style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px">{blokker}</div>
    <p id="kingen" class="tom" style="display:none">Du har ikke valgt noen kategorier. Kryss av for det du vil se.</p>
    <script>
    (function(){{var K='lyspunkt-kategorier',bx=document.querySelectorAll('.kvalg input'),bl=document.querySelectorAll('#kblokker .blokk');
    try{{var v=JSON.parse(localStorage.getItem(K)||'null');if(Array.isArray(v))bx.forEach(function(b){{b.checked=v.indexOf(b.value)>-1}})}}catch(e){{}}
    function vis(){{var on=[];bx.forEach(function(b){{if(b.checked)on.push(b.value)}});bl.forEach(function(d){{d.style.display=on.indexOf(d.dataset.kat)>-1?'':'none'}});
    var synl=[];bl.forEach(function(d){{d.style.gridColumn='';if(d.style.display!=='none')synl.push(d)}});if(synl.length%2===1)synl[synl.length-1].style.gridColumn='1 / -1';document.getElementById('kingen').style.display=on.length?'none':'block';try{{localStorage.setItem(K,JSON.stringify(on))}}catch(e){{}}}}
    bx.forEach(function(b){{b.addEventListener('change',vis)}});document.getElementById('kalle').addEventListener('click',function(){{bx.forEach(function(b){{b.checked=true}});vis()}});vis();}})();
    </script>
  </section>
  <section style="background:#EAE3FF;border-radius:24px;padding:56px 56px 60px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:16px">
    {SUN.format(s=52)}
    <span class="bri" style="font-size:clamp(30px,6vw,54px);font-weight:800;line-height:.95;letter-spacing:-0.04em">Trenger du et lyspunkt <span class="ser" style="font-style:italic;font-weight:400;letter-spacing:0;color:#6C4FD6">akkurat nå?</span></span>
    <span style="font-size:17px;line-height:1.5;color:#4A4560;max-width:520px">Ett trykk. Én tilfeldig god historie fra hvor som helst i verden.</span>
    <a href="overrask.html" class="btn" style="margin-top:10px;background:#6C4FD6;color:#FFFFFF;box-shadow:0 8px 22px rgba(108,79,214,.28)">Overrask meg</a>
  </section>
  <div style="display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:24px">
    <section aria-labelledby="sg" style="grid-column:span 8;background:#FFF1B8;border-radius:20px;padding:36px 36px 44px">
      <div class="shead" style="margin-bottom:32px"><h2 id="sg" class="h2">Små <span class="ser" style="font-style:italic;font-weight:400;letter-spacing:0">gleder</span></h2><a href="kategori/sma-gleder.html" style="font-size:15px;font-weight:700">Se alle →</a></div>
      <div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px">{sgk}</div>
    </section>
    <aside aria-labelledby="siste" style="grid-column:span 4;background:#DFF3E7;border-radius:20px;padding:36px;display:flex;flex-direction:column">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:18px"><span style="width:10px;height:10px;border-radius:5px;background:#FFD23F;box-shadow:0 0 0 3px #FFF3C2"></span><h2 id="siste" class="bri" style="margin:0;font-size:28px;font-weight:800;letter-spacing:-0.03em">Siste nytt</h2></div>
      {siste}
      <a href="siste.html" style="margin-top:auto;align-self:flex-start;background:#0E7A4E;color:#FFFFFF;padding:12px 18px;border-radius:999px;font-size:14px;font-weight:700">Alle saker →</a>
    </aside>
  </div>
</main>
''' + footer(base)
    write('index.html', page)

# ---------------------------------------------------------------- kategorier
def kategorier():
    base = '../'
    for k, (navn, desc, tint, acc) in KAT.items():
        ss = [s for s in SAKER if k in s['kategorier']]
        cards = '\n'.join(card(s, base) for s in ss)
        innhold = f'<div class="grid3">{cards}</div>' if ss else tom()
        write(f'kategori/{k}.html', head(f'{navn} – Lyspunkt', base, desc) + header(base, k) + f'''<main class="inner">
  <div class="crumb"><a href="{base}index.html">Forsiden</a> / {navn}</div>
  <section style="background:{tint};border-radius:24px;padding:48px 56px;margin:20px 0 40px;display:flex;align-items:center;justify-content:space-between;gap:40px">
    <div style="display:flex;flex-direction:column;gap:12px;max-width:760px">
      <span class="kick" style="color:{acc}">Kategori</span>
      <h1 class="h1" style="font-size:clamp(36px,6vw,64px)">{navn}</h1>
      <p style="margin:0;font-size:19px;line-height:1.5;color:#3D4540">{desc}</p>
    </div>
    <span class="bri" style="font-size:15px;font-weight:700;color:{acc};background:#FFFFFF;padding:12px 18px;border-radius:999px;white-space:nowrap">{len(ss)} {"sak" if len(ss) == 1 else "saker"}</span>
  </section>
  {innhold}
</main>
''' + footer(base))

# ---------------------------------------------------------------- artikler
def artikler():
    base = '../'
    for f in glob.glob(os.path.join(ROT, 'artikkel', '*.html')):
        os.remove(f)
    for s in SAKER:
        k = kat(s)
        navn, _, tint, acc = KAT[k]
        rel = [b for b in SAKER if b['id'] != s['id'] and k in b['kategorier']][:3]
        rel += [b for b in SAKER if b['id'] != s['id'] and b not in rel][:3 - len(rel)]
        body = ''
        for p in s.get('brodtekst', []):
            body += f'<h2>{e(p[3:])}</h2>' if p.startswith('## ') else f'<p>{e(p)}</p>'
        usikkert = f'<p style="margin:0;font-size:15px;line-height:1.6;color:#3D4540"><strong>Dette vet vi ikke ennå:</strong> {e(s["usikkert"])}</p>' if s.get('usikkert') else ''
        kilder = ''.join(f'<li><a href="{e(q["url"])}" target="_blank" rel="noopener">{e(q["navn"])}</a></li>' for q in s.get('kilder', []))
        tags = ' '.join(f'<a href="{base}kategori/{c}.html" style="font-size:13px;font-weight:700;color:{KAT[c][3]};background:{KAT[c][2]};padding:8px 14px;border-radius:999px;text-decoration:none">{KAT[c][0]}</a>' for c in s['kategorier'] if c in KAT)
        ai = ''
        if s.get('ai_assistert', True):
            ai = f'''<p style="margin:40px 0 0;padding-top:20px;border-top:1px solid #EFE6D6;font-size:14px;line-height:1.6;color:#5E665F"><strong style="color:#16120F">KI-assistert sak.</strong> Saken er funnet, kontrollert mot kildene over og skrevet av Lyspunkts KI-agenter. Det er også KI som har vurdert at saken skulle publiseres. Ansvarlig redaktør er Karoline D. Gjeldnes, som følger med på sakene og kan rette eller fjerne dem. Ser du en feil? <a href="{base}tips.html">Gi oss beskjed</a>. <a href="{base}redaksjonen.html">Les mer om redaksjonen</a>.</p>'''
        b = s.get('bilde')
        if b and b.get('url'):
            figur = f'''<figure style="margin:14px 0 0"><div style="height:480px;border-radius:24px;overflow:hidden;background:{tint}"><img src="{e(b['url'])}" alt="{e(b.get('alt',''))}" onerror="var f=this.closest('figure');if(f)f.remove()" style="width:100%;height:100%;object-fit:cover;display:block"></div><figcaption class="meta" style="margin-top:10px;font-size:13px">{"Illustrasjonsfoto" if b.get("illustrasjon") else "Foto"}: {e(b.get('kreditt',''))} · {e(b.get('lisens',''))} · <a href="{e(b.get('kilde_url') or kildeurl(s))}" target="_blank" rel="noopener" style="color:#4F6E9E;text-decoration:underline">Bildets kilde</a></figcaption></figure>'''
        else:
            figur = ''
        rettelse = f'<div class="demo" style="margin-bottom:24px"><strong>Rettelse:</strong> {e(s["rettelse"])}</div>' if s.get('rettelse') else ''
        write(f'artikkel/{s["id"]}.html', head(f'{s["tittel"]} – Lyspunkt', base, s['ingress']) + header(base, k) + f'''<main class="inner">
  <div class="crumb"><a href="{base}index.html">Forsiden</a> / <a href="{base}kategori/{k}.html">{navn}</a></div>
  <article style="display:flex;flex-direction:column;align-items:center;padding-top:36px">
    <div style="width:100%;max-width:880px;display:flex;flex-direction:column;gap:18px">
      <span style="display:flex;gap:10px;align-items:center;flex-wrap:wrap"><span class="kick" style="color:{acc}">{navn}</span><a href="{base}redaksjonen.html" class="pill" style="background:#EAE3FF;color:#4B3AA8;text-decoration:none">KI-skrevet sak</a></span>
      <h1 class="h1" style="font-size:clamp(34px,6vw,58px)">{e(s["tittel"])}</h1>
      <p style="margin:0;font-size:22px;line-height:1.5;color:#3D4540;font-weight:500">{e(s["ingress"])}</p>
      <div style="display:flex;gap:16px;align-items:center;padding:14px 0;border-top:1px solid #EFE6D6;border-bottom:1px solid #EFE6D6;font-size:14px;color:#5E665F">
        <span style="width:40px;height:40px;border-radius:20px;background:{tint};display:flex;align-items:center;justify-content:center">{SUN.format(s=22)}</span>
        <span><strong style="color:#16120F">Hentet fra <a href="{e(kildeurl(s))}" target="_blank" rel="noopener" style="color:#16120F;text-decoration:underline;text-underline-offset:3px">{e(kildenavn(s))}</a></strong> · Funnet og skrevet av KI<br>Publisert {dato(s["publisert"], True)} · Kilden er datert {dato(s["kildedato"], True)} · <a href="{base}redaksjonen.html" style="color:#4F6E9E;text-decoration:underline">Om redaksjonen</a></span>
      </div>
      {figur}
    </div>
    <div class="prose" style="width:100%;max-width:720px;margin-top:36px">
      {rettelse}{body}
      <aside style="background:{tint};border-radius:20px;padding:26px 28px;margin:36px 0">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">{SUN.format(s=26)}<span class="bri" style="font-size:22px;font-weight:800;letter-spacing:-0.02em">Hvorfor dette gir håp</span></div>
        <p style="margin:0 0 10px;font-size:17px;line-height:1.6">{e(s.get("hvorfor_hap", ""))}</p>
        {usikkert}
      </aside>
      <h2>Kilder</h2>
      <ul>{kilder}</ul>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:28px">{tags}</div>
      {ai}
    </div>
  </article>
  <section style="margin-top:72px">
    <h2 class="bri" style="font-size:34px;font-weight:800;letter-spacing:-0.03em;margin:0 0 20px">Les også</h2>
    <div class="grid3">{"".join(card(b, base) for b in rel)}</div>
  </section>
</main>
''' + footer(base))

# ---------------------------------------------------------------- siste, søk, overrask
def lister():
    rows = ''.join(f'''<a href="artikkel/{s["id"]}.html" style="display:grid;grid-template-columns:110px 200px 1fr;gap:20px;align-items:baseline;padding:20px 0;border-top:1px solid #EFE6D6">
  <span class="bri" style="font-weight:700;font-size:15px;background:#FFE98A;padding:3px 10px;border-radius:7px;justify-self:start">{dato(s["kildedato"])}</span>
  <span class="kick" style="color:{KAT[kat(s)][3]}">{KAT[kat(s)][0]}</span>
  <span style="display:flex;flex-direction:column;gap:4px"><span class="bri" style="font-size:24px;font-weight:700;letter-spacing:-0.02em;line-height:1.1">{e(s["tittel"])}</span><span style="font-size:15px;color:#3D4540">{e(s["ingress"])}</span></span>
</a>''' for s in SAKER) or tom()
    write('siste.html', head('Siste nytt – Lyspunkt', '') + header('') + f'''<main class="inner">
  <div class="crumb"><a href="index.html">Forsiden</a> / Siste nytt</div>
  <div style="display:flex;align-items:center;gap:14px;margin:28px 0 24px"><span style="width:14px;height:14px;border-radius:7px;background:#FFD23F;box-shadow:0 0 0 4px #FFF3C2"></span><h1 class="h1" style="font-size:clamp(36px,6vw,64px)">Siste nytt</h1></div>
  <div style="max-width:1100px">{rows}</div>
</main>
''' + footer(''))

    idx = json.dumps([{'s': s['id'], 't': s['tittel'], 'i': s['ingress'], 'k': KAT[kat(s)][0], 'c': KAT[kat(s)][3]} for s in SAKER], ensure_ascii=False)
    write('sok.html', head('Søk – Lyspunkt', '') + header('') + f'''<main class="inner">
  <div class="crumb"><a href="index.html">Forsiden</a> / Søk</div>
  <h1 class="h1" style="font-size:clamp(36px,6vw,64px);margin:28px 0 24px">Søk i <span class="ser" style="font-style:italic;font-weight:400;letter-spacing:0;color:#4F6E9E">gode nyheter</span></h1>
  <form role="search" onsubmit="return false" style="display:flex;gap:10px;max-width:760px">
    <label for="q" class="sr">Søkeord</label>
    <input id="q" type="search" placeholder="Prøv «elbil», «natur» eller «Norge»" style="flex:1" autofocus>
  </form>
  <p id="antall" class="meta" style="font-size:14px;margin:18px 0 8px" aria-live="polite"></p>
  <div id="treff" style="max-width:1100px"></div>
</main>
<script>
var A={idx};
var q=document.getElementById('q'),t=document.getElementById('treff'),n=document.getElementById('antall');
function esc(s){{return s.replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]}})}}
function vis(){{var v=q.value.trim().toLowerCase();var r=A.filter(function(a){{return !v||(a.t+' '+a.i+' '+a.k).toLowerCase().indexOf(v)>-1}});
n.textContent=v?(r.length+' treff for «'+q.value.trim()+'»'):('Alle '+r.length+' saker');
t.innerHTML=r.map(function(a){{return '<a href="artikkel/'+a.s+'.html" style="display:grid;grid-template-columns:200px 1fr;gap:20px;align-items:baseline;padding:18px 0;border-top:1px solid #EFE6D6"><span class="kick" style="color:'+a.c+'">'+esc(a.k)+'</span><span style="display:flex;flex-direction:column;gap:4px"><span class="bri" style="font-size:24px;font-weight:700;letter-spacing:-0.02em;line-height:1.1">'+esc(a.t)+'</span><span style="font-size:15px;color:#3D4540">'+esc(a.i)+'</span></span></a>'}}).join('')||'<p style="font-size:18px">Ingen treff — prøv et annet ord.</p>';
try{{history.replaceState(null,'',v?('?q='+encodeURIComponent(q.value.trim())):location.pathname)}}catch(e){{}}}}
try{{var p=new URLSearchParams(location.search).get('q');if(p)q.value=p}}catch(e){{}}
q.addEventListener('input',vis);vis();
</script>
''' + footer(''))

    slugs = json.dumps([s['id'] for s in SAKER])
    first = SAKER[0]['id'] if SAKER else ''
    write('overrask.html', head('Overrask meg – Lyspunkt', '') + header('') + f'''<main class="inner">
  <section style="background:#EAE3FF;border-radius:24px;padding:72px 56px;margin:40px 0;display:flex;flex-direction:column;align-items:center;text-align:center;gap:16px">
    {SUN.format(s=60)}
    <h1 class="h1" style="font-size:clamp(32px,6vw,56px)">Finner et lyspunkt <span class="ser" style="font-style:italic;font-weight:400;letter-spacing:0;color:#6C4FD6">til deg …</span></h1>
    <p style="margin:0;font-size:17px;color:#4A4560">Du sendes videre til en tilfeldig god historie.</p>
    <a id="lenke" href="artikkel/{first}.html" class="btn" style="background:#6C4FD6;color:#FFFFFF;margin-top:10px">Ta meg dit</a>
  </section>
</main>
<script>
var S={slugs};if(S.length){{var u='artikkel/'+S[Math.floor(Math.random()*S.length)]+'.html';document.getElementById('lenke').href=u;setTimeout(function(){{location.replace(u)}},900)}}
</script>
''' + footer(''))

# ---------------------------------------------------------------- statiske sider
def statiske():
    write('nyhetsbrev.html', head('Nyhetsbrev – Lyspunkt', '') + header('') + f'''<main class="inner">
  <div class="crumb"><a href="index.html">Forsiden</a> / Nyhetsbrev</div>
  <section style="background:#FFF3C2;border-radius:24px;padding:64px 56px;margin:24px 0;display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:24px;align-items:center">
    <div style="grid-column:span 6;display:flex;flex-direction:column;gap:14px">
      <h1 class="h1" style="font-size:clamp(34px,6vw,60px)">Ukens lyspunkter, <span class="ser" style="font-style:italic;font-weight:400;letter-spacing:0;color:#4F6E9E">rett i innboksen</span></h1>
      <p style="margin:0;font-size:19px;line-height:1.55;color:#3D4540">Hver fredag: ukens tre viktigste gode nyheter, et par saker tilpasset deg og én liten glede. Gratis, uten reklame — og du kan melde deg av når du vil.</p>
    </div>
    <div style="grid-column:8 / span 5;background:#FFFFFF;border-radius:22px;padding:30px">
      <form id="nf" style="display:flex;flex-direction:column;gap:12px">
        <label for="epost" class="bri" style="font-size:20px;font-weight:700">Din e-postadresse</label>
        <input id="epost" name="epost" type="email" required placeholder="din@epost.no">
        <button type="submit" class="btn" style="background:#4F6E9E;color:#FFFFFF">Meld meg på</button>
        <p class="meta" style="margin:0">Nyhetsbrevet er ikke i gang ennå, så påmeldingen lagres ikke.</p>
      </form>
      <div id="takk" style="display:none;flex-direction:column;gap:10px;align-items:flex-start">
        {SUN.format(s=48)}
        <span class="bri" style="font-size:28px;font-weight:800;letter-spacing:-0.03em">Takk!</span>
        <p id="takktekst" style="margin:0;font-size:16px;line-height:1.5;color:#3D4540"></p>
        <a href="index.html" style="font-weight:700;color:#4F6E9E">Tilbake til forsiden →</a>
      </div>
    </div>
  </section>
</main>
<script>
var f=document.getElementById('nf'),e=document.getElementById('epost'),t=document.getElementById('takk');
function takk(v){{f.style.display='none';t.style.display='flex';document.getElementById('takktekst').textContent='Når nyhetsbrevet starter, sender vi ukens lyspunkter til '+v+'. Foreløpig lagres ingenting.'}}
try{{var p=new URLSearchParams(location.search).get('epost');if(p)takk(p)}}catch(x){{}}
f.addEventListener('submit',function(ev){{ev.preventDefault();if(e.value)takk(e.value)}});
</script>
''' + footer(''))

    def info(fil, tittel, tint, intro, innhold):
        write(fil, head(f'{tittel} – Lyspunkt', '') + header('') + f'''<main class="inner">
  <div class="crumb"><a href="index.html">Forsiden</a> / {tittel}</div>
  <section style="background:{tint};border-radius:24px;padding:48px 56px;margin:20px 0 40px">
    <h1 class="h1" style="font-size:clamp(34px,6vw,60px)">{tittel}</h1>
    <p style="margin:12px 0 0;font-size:19px;line-height:1.5;color:#3D4540;max-width:760px">{intro}</p>
  </section>
  <div class="prose">{innhold}</div>
</main>
''' + footer(''))


    info('redaksjonen.html', 'Om redaksjonen', '#EAE3FF', 'Lyspunkt er en KI-assistert nettavis. Her forklarer vi hvem som gjør hva.',
         '''<div class="demo" style="font-size:16px;line-height:1.6;margin-bottom:28px"><strong>Kort fortalt:</strong> Sakene på Lyspunkt blir funnet, kontrollert, skrevet og publisert av kunstig intelligens (KI). Også de redaksjonelle vurderingene, som hvilke saker som publiseres og hva som havner i Dagens topp 3, gjøres av KI. Ansvarlig redaktør Karoline D. Gjeldnes har det redaksjonelle ansvaret, setter reglene KI-en jobber etter og kan rette eller fjerne saker.</div>
<h2>Ansvarlig redaktør</h2>
<p><strong>Karoline D. Gjeldnes</strong> er ansvarlig redaktør og nyhetsredaktør. Hun bestemmer de redaksjonelle prinsippene, følger med på det som publiseres, og retter, skjuler eller overstyrer saker ved behov.</p>
<h2>Hva KI-en gjør</h2>
<ul><li><strong>Finner saker:</strong> KI-agenter søker gjennom nyhetskilder, forskningsinstitusjoner og myndigheter hver time.</li><li><strong>Vurderer saker:</strong> KI-en avgjør om en sak er ny, positiv, troverdig og godt nok dokumentert til å publiseres.</li><li><strong>Kontrollerer fakta:</strong> KI-en åpner og leser kildene, og tar bare med tall og påstander som står der.</li><li><strong>Skriver saken:</strong> Teksten skrives på norsk med egne ord, med lenke til kildene og en egen boks om hva som fortsatt er usikkert.</li><li><strong>Velger bilder:</strong> KI-en bruker kildens bilde bare når lisensen tillater det. Ellers velges et gratis illustrasjonsbilde, merket «Illustrasjonsfoto».</li><li><strong>Publiserer:</strong> Sakene legges ut automatisk, uten at et menneske leser dem først.</li></ul>
<h2>Hva KI-en ikke gjør</h2>
<ul><li>Den finner ikke på saker, personer, sitater eller tall.</li><li>Den gjengir ikke sangtekster eller kopierer lengre tekst fra kildene.</li><li>Den bruker ikke bilder den ikke har lov til å bruke.</li></ul>
<h2>Hvor kommer sakene fra?</h2>
<p>Hver sak viser øverst hvilken kilde den er hentet fra, og alle kildene er listet nederst i saken. Gå gjerne til originalkilden for å lese mer.</p>
<h2>Feil kan skje</h2>
<p>KI kan misforstå eller ta feil. Ser du noe som ikke stemmer, <a href="tips.html">gi oss beskjed</a>, så retter vi det og merker rettelsen åpent. Se også <a href="rettelser.html">rettelser</a>, <a href="prinsipper.html">redaksjonelle prinsipper</a> og <a href="ai.html">bruk av KI</a>.</p>''')

    info('om.html', 'Om Lyspunkt', '#E3E9F4', 'Et lysere blikk på verden — positiv journalistikk som er til å stole på.',
         '''<p>Lyspunkt er en norsk nyhetsplattform som samler og formidler positive nyheter, gode historier, dokumenterte fremskritt og konstruktive løsninger fra hele verden.</p>
<p>Vi ignorerer ikke verdens problemer. Men det skjer også utrolig mye fint, viktig og meningsfullt — og det fortjener å bli fortalt like godt.</p>
<h2>To typer saker</h2>
<ul><li><strong>Viktige fremskritt:</strong> medisinske gjennombrudd, naturrestaurering, teknologiske løsninger og samfunnsendringer som gjør verden bedre.</li><li><strong>Ekte gladnyheter:</strong> dyr som blir reddet, mennesker som hjelper hverandre og små øyeblikk som gjør dagen litt bedre.</li></ul>
<h2>Redaksjonen</h2>
<p>Ansvarlig redaktør og nyhetsredaktør er Karoline D. Gjeldnes. Sakene blir funnet, vurdert, skrevet og publisert av KI-agenter etter våre redaksjonelle prinsipper. Redaktøren følger med og kan rette eller fjerne saker. <a href="redaksjonen.html">Les mer om redaksjonen</a>.</p>
<h2>Gratis og åpent</h2>
<p>Lyspunkt er gratis å lese, uten betalingsmur og uten reklame.</p>''')

    info('prinsipper.html', 'Redaksjonelle prinsipper', '#E2F4F1', 'Positivt uten å være naivt. Slik sørger vi for at du kan stole på det som står på Lyspunkt.',
         '''<p>Lyspunkt skal være positivt uten å være naivt. Vi fremstiller aldri noe som bedre enn det faktisk er.</p>
<h2>Vi skiller tydelig mellom</h2>
<ul><li>En dokumentert positiv utvikling.</li><li>Et lovende forskningsresultat som ennå er usikkert.</li><li>En inspirerende menneskelig historie.</li><li>En hyggelig hendelse som gjør folk glade.</li></ul>
<h2>Slik jobber vi</h2>
<ul><li>Faktabasert journalistikk og troverdige kilder — originalkilder når det er mulig.</li><li>Åpenhet om usikkerhet: hver sak sier hva vi ikke vet ennå.</li><li>Ingen oppdiktede nyheter, ingen clickbait og ingen overdreven positiv vinkling.</li><li>Ingen politisk propaganda og ingen manipulering av bilder.</li><li>Tydelig merking av AI-assistanse.</li><li>Åpenhet om rettelser og respekt for personvern.</li></ul>
<h2>Om illustrasjonene</h2>
<p>Vi bruker bare bilder vi har lov til å bruke: bilder fra offentlige etater som NASA, fritt lisensierte bilder og pressebilder som er frigitt for media. Alle krediteres med fotograf og lisens. Bilder fra aviser og bildebyråer bruker vi ikke. Finnes det ikke et bilde vi har lov til å bruke, publiserer vi saken uten bilde. Kildene står alltid nederst i saken.</p>''')

    info('rettelser.html', 'Rettelser og oppdateringer', '#FFF3CC', 'Feil skjer — da skal du få vite om det.',
         '<p>Når vi gjør feil, retter vi dem åpent. Rettelser merkes øverst i saken det gjelder, og samles her.</p>'
         + (''.join(f'<p><a href="artikkel/{s["id"]}.html">{e(s["tittel"])}</a>: {e(s["rettelse"])}</p>' for s in SAKER if s.get('rettelse')) or '<div class="demo">Ingen rettelser er registrert.</div>')
         + '<h2>Fant du en feil?</h2><p>Gi oss beskjed via <a href="tips.html">Tips oss</a>.</p>')

    info('ai.html', 'Bruk av AI', '#EAE3FF', 'Hvordan vi bruker kunstig intelligens — og hvor grensene går.',
         '''<p>Lyspunkt bruker AI-agenter til å finne, kontrollere og skrive gode nyheter. Agentene går gjennom nyhetskilder fortløpende, hver time.</p>
<h2>Slik jobber agentene</h2>
<ul><li>De leter etter positive nyheter fra troverdige kilder: forskningsinstitusjoner, myndigheter, fagtidsskrifter og etablerte medier.</li><li>Hver sak kontrolleres mot kilden før den publiseres. Tall og påstander som ikke kan bekreftes, tas ikke med.</li><li>Sakene skrives med egne ord på norsk, med lenke til kildene.</li><li>Hver sak sier tydelig hva som fortsatt er usikkert.</li><li>Agentene finner aldri på sitater, personer eller tall.</li></ul>
<h2>Redaktørens rolle</h2>
<ul><li>Ansvarlig redaktør Karoline D. Gjeldnes kan når som helst endre, skjule eller overstyre saker og Dagens topp 3.</li><li>Alle saker er merket «KI-skrevet sak» øverst og har en forklaring nederst. Saker publiseres automatisk, uten at et menneske leser dem først.</li><li>AI-genererte bilder brukes aldri som om de var ekte fotografier.</li></ul>''')

    info('personvern.html', 'Personvern', '#E6EFFD', 'Minst mulig data, mest mulig åpenhet.',
         '''<p>Lyspunkt skal være personvernvennlig. Du trenger ikke konto for å lese, og vi samler inn minst mulig informasjon.</p>
<h2>Det vi lagrer</h2>
<ul><li>Valget ditt av lyst eller mørkt tema lagres bare i din egen nettleser.</li><li>Vi bruker ikke sporingsverktøy eller reklame.</li><li>Påmelding til nyhetsbrev og tips lagres ikke ennå.</li></ul>''')

    write('tips.html', head('Tips oss – Lyspunkt', '') + header('') + '''<main class="inner">
  <div class="crumb"><a href="index.html">Forsiden</a> / Tips oss</div>
  <section style="background:#E4F5E8;border-radius:24px;padding:48px 56px;margin:20px 0 40px">
    <h1 class="h1" style="font-size:clamp(34px,6vw,60px)">Tips oss om <span class="ser" style="font-style:italic;font-weight:400;letter-spacing:0;color:#2E8A4F">et lyspunkt</span></h1>
    <p style="margin:12px 0 0;font-size:19px;line-height:1.5;color:#3D4540;max-width:760px">Vet du om noe fint som skjer — eller har du sett en feil i en sak? Vi vil gjerne høre om det.</p>
  </section>
  <form id="tf" style="max-width:100%;max-width:720px;display:flex;flex-direction:column;gap:14px">
    <label for="tnavn" class="bri" style="font-size:18px;font-weight:700">Navn (valgfritt)</label>
    <input id="tnavn" type="text">
    <label for="ttips" class="bri" style="font-size:18px;font-weight:700">Hva vil du fortelle oss?</label>
    <textarea id="ttips" required></textarea>
    <button type="submit" class="btn" style="background:#2E8A4F;color:#FFFFFF;align-self:flex-start">Send tips</button>
    <p class="meta" style="margin:0">Tipsskjemaet er ikke koblet til ennå, så ingenting sendes.</p>
  </form>
  <p id="ttakk" class="demo" style="display:none;max-width:100%;max-width:720px;font-size:16px">Takk! Skjemaet er ikke koblet til ennå, så tipset ble ikke sendt.</p>
</main>
<script>document.getElementById('tf').addEventListener('submit',function(e){e.preventDefault();this.style.display='none';document.getElementById('ttakk').style.display='block'})</script>
''' + footer(''))

if __name__ == '__main__':
    with open(os.path.join(ROT, 'stil.css'), 'w', encoding='utf-8') as f:
        f.write(CSS)
    forside(); kategorier(); artikler(); lister(); statiske()
    with open(os.path.join(ROT, 'data', 'siste.json'), 'w', encoding='utf-8') as f:
        json.dump({'oppdatert': DATA.get('oppdatert'), 'saker': [{'id': s['id'], 'tittel': s['tittel'], 'publisert': s.get('publisert') or s['kildedato']} for s in SISTE[:15]]}, f, ensure_ascii=False)
    print(f'Bygget nettstedet: {len(SAKER)} publiserte saker.')

import asyncio
import socket
import threading
import time
import webbrowser
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI(title="Roman Numerals Converter")


def int_to_roman(num: int) -> str:
    mapping = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]
    res = []
    for val, sym in mapping:
        while num >= val:
            res.append(sym)
            num -= val
    return "".join(res)


def roman_to_int(s: str) -> int:
    s = s.strip().upper()
    if not s:
        raise ValueError("Boş giriş yapılamaz.")
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    if any(ch not in values for ch in s):
        raise ValueError("Geçersiz karakter! Sadece I, V, X, L, C, D, M.")
    total = 0
    for i in range(len(s)):
        curr = values[s[i]]
        if i + 1 < len(s) and curr < values[s[i + 1]]:
            total -= curr
        else:
            total += curr
    if not (1 <= total <= 4999):
        raise ValueError("Sayı 1 ile 4999 arasında olmalıdır.")
    if int_to_roman(total) != s:
        raise ValueError(f"Hatalı dizilim: '{s}' (Doğrusu: {int_to_roman(total)})")
    return total


HTML_UI = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>Roman Numerals Converter</title>
<script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex items-center justify-center p-4 font-sans">
<div class="w-full max-w-lg bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl space-y-5">
  <div class="flex justify-between items-center border-b border-slate-800 pb-3">
    <h1 class="text-lg font-bold text-cyan-400">Roman Numerals Converter</h1>
    <span class="text-xs px-2.5 py-1 rounded-full bg-slate-800 text-cyan-300">1 - 4999</span>
  </div>
  <div class="flex gap-2">
    <input id="inp" type="text" placeholder="Örn: MCMXCIV" oninput="this.value=this.value.toUpperCase();run()" class="w-full bg-slate-950 border border-slate-700 focus:border-cyan-400 focus:outline-none rounded-xl px-4 py-2.5 text-lg font-mono tracking-widest uppercase">
    <button onclick="clr()" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 rounded-xl text-sm">Temizle</button>
  </div>
  <div class="grid grid-cols-7 gap-1.5" id="keypad"></div>
  <div class="bg-slate-950 border border-slate-800 rounded-xl p-4 flex items-center justify-between">
    <div>
      <div class="text-xs text-slate-400">Sayısal Karşılık</div>
      <div id="val" class="text-3xl font-bold text-slate-500 mt-0.5">—</div>
    </div>
    <div id="badge" class="text-xs px-3 py-1.5 rounded-lg bg-slate-900 text-slate-400 border border-slate-800">Giriş bekleniyor</div>
  </div>
  <div class="pt-2 border-t border-slate-800 flex flex-wrap gap-1.5" id="examples"></div>
</div>
<script>
const keys = [['I',1],['V',5],['X',10],['L',50],['C',100],['D',500],['M',1000]];
document.getElementById('keypad').innerHTML = keys.map(([k,v]) =>
  `<button onclick="add('${k}')" class="bg-slate-800 hover:border-cyan-400 border border-slate-700 rounded-xl py-2 text-center"><div class="font-bold text-cyan-300">${k}</div><div class="text-[10px] text-slate-400">${v}</div></button>`
).join('');

const exs = [['IV',1],['XIV',1],['MCMXCIV',1],['MMMMCMXCIX',1],['IIII',0],['VIIII',0]];
document.getElementById('examples').innerHTML = exs.map(([t,ok]) =>
  `<button onclick="setEx('${t}')" class="px-2.5 py-1 rounded-lg text-xs font-mono border ${ok?'bg-emerald-950/60 border-emerald-700/50 text-emerald-300':'bg-rose-950/60 border-rose-700/50 text-rose-300'}">${t}</button>`
).join('');

function add(c){ const i=document.getElementById('inp'); i.value+=c; run(); }
function setEx(t){ document.getElementById('inp').value=t; run(); }
function clr(){
  document.getElementById('inp').value='';
  const v=document.getElementById('val'), b=document.getElementById('badge');
  v.innerText='—'; v.className='text-3xl font-bold text-slate-500 mt-0.5';
  b.innerText='Giriş bekleniyor'; b.className='text-xs px-3 py-1.5 rounded-lg bg-slate-900 text-slate-400 border border-slate-800';
}
async function run(){
  const q=document.getElementById('inp').value.trim();
  if(!q){ clr(); return; }
  const r=await fetch('/convert?roman='+encodeURIComponent(q));
  const d=await r.json();
  const v=document.getElementById('val'), b=document.getElementById('badge');
  if(r.ok){
    v.innerText=d.number; v.className='text-3xl font-bold text-emerald-400 mt-0.5';
    b.innerText='Geçerli ✓'; b.className='text-xs px-3 py-1.5 rounded-lg bg-emerald-950 text-emerald-300 border border-emerald-700';
  } else {
    v.innerText='Geçersiz'; v.className='text-2xl font-bold text-rose-400 mt-0.5';
    b.innerText=d.detail; b.className='text-xs px-3 py-1.5 rounded-lg bg-rose-950 text-rose-300 border border-rose-700';
  }
}
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_UI


@app.get("/convert")
def convert(roman: str):
    try:
        return {"roman": roman.strip().upper(), "number": roman_to_int(roman)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def find_free_port(default_port: int = 8000) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("127.0.0.1", default_port)) != 0:
            return default_port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


if __name__ == "__main__":
    port = find_free_port(8000)
    threading.Thread(
        target=lambda: (time.sleep(1.0), webbrowser.open(f"http://127.0.0.1:{port}")),
        daemon=True,
    ).start()
    try:
        asyncio.get_running_loop()
        threading.Thread(
            target=lambda: uvicorn.run(app, host="127.0.0.1", port=port, log_level="error"),
            daemon=True,
        ).start()
    except RuntimeError:
        uvicorn.run(app, host="127.0.0.1", port=port)

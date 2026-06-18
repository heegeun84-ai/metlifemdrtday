#!/usr/bin/env python3
# 2026 MetLife MDRT Day 준비 대시보드 생성기 (v2 — 9 tabs)
import json, os

_HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(_HERE, "data.json")))
OUT = os.path.join(_HERE, "index.html")

# 안정적 고정 id 부여 (렌더마다 id가 바뀌어 체크가 엉뚱하게 매칭되는 버그 방지)
for i, it in enumerate(DATA["checklist"]):
    it.setdefault("id", "c%d" % i)
for ci, c in enumerate(DATA["budget"]["cats"]):
    for ii, it in enumerate(c["items"]):
        it.setdefault("id", "b%d_%d" % (ci, ii))
        it.setdefault("fund", "본사" if "본사" in c["name"] else "회비")

TPL = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>2026 MDRT Day 준비 대시보드</title>
<link rel="stylesheet" href="https://fastly.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<style>
:root{
  --blue:#0c6b4f; --blue-d:#06281d; --green:#18996d; --amber:#c98a2a; --red:#c0492f; --purple:#7B5EA7;
  --gold:#b88a3e; --gold-br:#d8b367;
  --bg:#eef2f0; --card:#fff; --ink:#16241d; --muted:#5f7068; --line:#e0e7e3;
  --shadow:0 1px 3px rgba(10,40,30,.06),0 6px 20px rgba(10,40,30,.07);
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Pretendard,-apple-system,system-ui,sans-serif;background:var(--bg);color:var(--ink);
  -webkit-font-smoothing:antialiased;line-height:1.5;padding-bottom:70px}
.wrap{max-width:1180px;margin:0 auto;padding:0 18px}
header{background:linear-gradient(125deg,#04211a 0%,#0a4936 55%,#0c5e46 100%);color:#fff;padding:18px 0 15px;position:relative;overflow:hidden}
header::before{content:"";position:absolute;top:-70%;left:-8%;width:55%;height:220%;
  background:radial-gradient(closest-side,rgba(216,179,103,.30),transparent 72%);transform:rotate(20deg);pointer-events:none}
header::after{content:"";position:absolute;bottom:-90%;right:-4%;width:50%;height:220%;
  background:radial-gradient(closest-side,rgba(216,179,103,.22),transparent 72%);pointer-events:none}
header .wrap{display:flex;flex-wrap:wrap;align-items:center;gap:12px 18px;justify-content:space-between;position:relative;z-index:1}
.brand{display:flex;align-items:center;gap:15px;min-width:0}
.brand .logo-ml{height:25px;width:auto;display:block}
.brand .sep{width:1px;height:30px;background:rgba(255,255,255,.25);flex:none}
.htitle{display:flex;flex-direction:column;gap:3px;min-width:0}
.htitle .logo-wio{height:33px;width:auto;display:block;cursor:pointer}
.htitle .logo-wio:hover{opacity:.85}
.htitle span{font-size:12px;opacity:.82;letter-spacing:.02em}
.hright{display:flex;align-items:center;gap:14px}
.logo-mdrt{height:46px;width:auto;opacity:.96}
.dday{display:flex;align-items:baseline;gap:8px;background:rgba(216,179,103,.13);
  border:1px solid rgba(216,179,103,.45);padding:8px 16px;border-radius:12px}
.dday em{font-style:normal;font-size:12px;opacity:.9;color:var(--gold-br)}
.dday b{font-size:26px;font-weight:800;letter-spacing:-.03em;color:var(--gold-br)}
.hmeta{font-size:12.5px;opacity:.92;width:100%;display:flex;flex-wrap:wrap;gap:6px 18px;margin-top:2px}
.hmeta span::before{content:"·";margin-right:6px;opacity:.5}
.hmeta span:first-child::before{content:none}
nav.tabs{position:sticky;top:0;z-index:30;background:rgba(255,255,255,.92);backdrop-filter:blur(8px);
  border-bottom:1px solid var(--line);box-shadow:0 2px 8px rgba(10,40,30,.04)}
nav.tabs .wrap{display:flex;gap:2px;overflow-x:auto}
nav.tabs button{flex:none;background:none;border:none;font:inherit;font-size:13.5px;font-weight:600;color:var(--muted);
  padding:13px 12px;cursor:pointer;border-bottom:2.5px solid transparent;white-space:nowrap}
nav.tabs button.on{color:var(--blue);border-color:var(--blue)}
nav.tabs button .b{display:inline-block;min-width:17px;font-size:11px;background:var(--line);color:var(--muted);
  border-radius:9px;padding:1px 6px;margin-left:4px;font-weight:700}
nav.tabs button.on .b{background:var(--blue);color:#fff}
nav.tabs button.tabadmin{color:var(--gold);font-weight:700;margin-left:auto}
nav.tabs button.tabadmin.on{color:var(--gold);border-color:var(--gold)}
main{padding-top:22px}
.panel{display:none;animation:fade .25s ease}.panel.on{display:block}
@keyframes fade{from{opacity:0;transform:translateY(4px)}to{opacity:1}}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow)}
h2.sec{font-size:15px;font-weight:800;margin:26px 4px 12px;letter-spacing:-.01em;display:flex;align-items:center;gap:8px}
h2.sec:first-child{margin-top:4px}
.muted{color:var(--muted)}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.kpi{padding:16px}.kpi .k{font-size:12px;color:var(--muted);font-weight:600}
.kpi .v{font-size:27px;font-weight:800;letter-spacing:-.03em;margin-top:3px;line-height:1.1}
.kpi .s{font-size:11.5px;color:var(--muted);margin-top:2px}
.kpi .v.blue{color:var(--blue)}.kpi .v.green{color:var(--green)}.kpi .v.amber{color:var(--amber)}
.bar{height:8px;background:#eef2f7;border-radius:6px;overflow:hidden}
.bar>i{display:block;height:100%;background:linear-gradient(90deg,var(--green),#36c97f);border-radius:6px;transition:width .4s}
.grid2{display:grid;grid-template-columns:1.3fr 1fr;gap:14px;align-items:start}
.areas{padding:6px 4px}
.arow{display:grid;grid-template-columns:128px 1fr 52px;gap:12px;align-items:center;padding:8px 12px;cursor:pointer}
.arow:hover{background:#fafbfd}.arow .an{font-size:13px;font-weight:600}
.arow .ap{font-size:12px;color:var(--muted);text-align:right;font-variant-numeric:tabular-nums}
.mile{padding:6px 4px}
.mrow{display:flex;gap:12px;align-items:center;padding:9px 14px;border-bottom:1px solid var(--line)}
.mrow:last-child{border:none}
.mdot{width:9px;height:9px;border-radius:50%;background:var(--blue);flex:none}
.mrow.past .mdot{background:var(--line)}.mrow.goal .mdot{background:var(--red);box-shadow:0 0 0 4px rgba(214,69,69,.15)}
.mrow .md{font-size:12px;color:var(--muted);width:74px;flex:none;font-variant-numeric:tabular-nums}
.mrow .ml{font-size:13.5px;font-weight:600}.mrow.past .ml{color:var(--muted);font-weight:500}
.mrow .mdd{margin-left:auto;font-size:11.5px;font-weight:700;color:var(--blue)}
.toolbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:14px}
.seg{display:inline-flex;background:#e7ecf3;border-radius:10px;padding:3px}
.seg button{border:none;background:none;font:inherit;font-size:13px;font-weight:700;color:var(--muted);
  padding:6px 14px;border-radius:8px;cursor:pointer}
.seg button.on{background:#fff;color:var(--blue);box-shadow:0 1px 3px rgba(0,0,0,.08)}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font-size:12.5px;font-weight:600;padding:6px 12px;border-radius:20px;border:1px solid var(--line);
  background:#fff;cursor:pointer;color:var(--muted)}
.chip.on{background:var(--blue);color:#fff;border-color:var(--blue)}
.search{flex:1;min-width:160px;padding:8px 13px;border:1px solid var(--line);border-radius:10px;font:inherit;font-size:13.5px}
.areablock{margin-bottom:14px}
.areahd{display:flex;align-items:center;gap:10px;padding:11px 15px}
.areahd .nm{font-size:14.5px;font-weight:800}
.areahd .dp{font-size:11px;font-weight:700;color:var(--blue);background:#e7f1ec;padding:2px 8px;border-radius:7px}
.areahd .cnt{margin-left:auto;font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}
.areahd .mini{width:70px;height:6px}
.items{border-top:1px solid var(--line)}
.it{display:flex;gap:11px;padding:11px 15px;border-bottom:1px solid var(--line);align-items:flex-start}
.it:last-child{border:none}.it:hover{background:#fafbfd}.it.done{background:#f3faf5}
.cb{flex:none;width:20px;height:20px;border:2px solid #c6d2df;border-radius:6px;cursor:pointer;margin-top:1px;
  display:grid;place-items:center;transition:.15s}
.cb.ck{background:var(--green);border-color:var(--green)}.cb.ck::after{content:"✓";color:#fff;font-size:13px;font-weight:800}
.it .body{flex:1;min-width:0}.it .nm{font-size:14px;font-weight:600}
.it.done .nm{text-decoration:line-through;color:var(--muted)}
.it .ct{font-size:12.5px;color:var(--muted);margin-top:2px}
.it .tags{display:flex;flex-wrap:wrap;gap:5px;margin-top:6px}
.tag{font-size:11px;padding:2px 8px;border-radius:6px;background:#f0f3f7;color:#5a6b7d;font-weight:600}
.tag.o{background:#fff3e0;color:#a9701a}.tag.c{background:#e7f1ec;color:#0c6b4f}.tag.s{background:#fdeaea;color:#b23b3b}
.editing-cl .cef{border-bottom:1px dashed var(--gold);padding:0 2px;min-width:12px;display:inline-block;outline:none;font-weight:400}
.editing-cl .it .nm .cef{font-weight:600}
.editing-cl .cef:focus{background:#fffaef;box-shadow:0 0 0 2px rgba(216,179,103,.35)}
.editing-cl .cef:empty::before{content:"＋";color:var(--gold);opacity:.6}
.itrm{flex:none;background:none;border:none;color:var(--muted);cursor:pointer;font-size:14px;padding:2px 4px;align-self:flex-start}
.itrm:hover{color:var(--red)}
.itadd{padding:10px 15px;font-size:12.5px;font-weight:700;color:var(--blue);cursor:pointer;border-top:1px dashed var(--line)}
.itadd:hover{background:#f3faf5}
.imv{display:inline-flex;flex-direction:column;flex:none;align-self:center}
.imv button{background:none;border:1px solid var(--line);border-radius:4px;cursor:pointer;color:var(--muted);font-size:9px;line-height:1;padding:2px 4px;margin:1px 0}
.imv button:hover{color:var(--blue);border-color:var(--blue)}
/* depts */
.dgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:14px}
.dcard{padding:16px}
.dcard .dh{display:flex;align-items:center;gap:9px;margin-bottom:10px}
.dcard .dh b{font-size:16px;font-weight:800}
.dcard .dh .pct{margin-left:auto;font-size:13px;font-weight:800;color:var(--green)}
.dcard .areaslist{display:flex;flex-wrap:wrap;gap:5px;margin:10px 0}
.dcard .achip{font-size:11.5px;font-weight:600;padding:3px 9px;border-radius:7px;background:#f0f3f7;color:#5a6b7d;cursor:pointer}
.dcard .achip:hover{background:#e7f1ec;color:var(--blue)}
.dcard .ppl{border-top:1px solid var(--line);margin-top:10px;padding-top:8px}
.dcard .cp{display:flex;justify-content:space-between;gap:8px;padding:4px 0;font-size:13px}
.cp .nm b{font-weight:700}.cp .nm em{font-style:normal;color:var(--muted);font-size:11.5px;margin-left:5px}
.cp a{color:var(--blue);font-weight:600;font-size:12.5px;text-decoration:none;white-space:nowrap}
.role-lead{color:var(--green)}
/* timetable */
.ttbar{display:flex;align-items:center;gap:8px;margin-bottom:12px;flex-wrap:wrap}
.ttsec{font-size:13px;font-weight:800;margin:20px 4px 8px;padding:8px 14px;border-radius:9px;letter-spacing:.01em;display:flex;align-items:center;gap:8px}
.ttsec:first-child{margin-top:2px}
.ttsec.main{color:#fff;background:linear-gradient(100deg,#0a4936,#0c6b4f)}
.ttsec.prep{color:var(--gold-br);background:#262b27;border:1px solid rgba(216,179,103,.3)}
.ttsec .badge{font-size:10.5px;font-weight:700;padding:1px 8px;border-radius:20px;background:rgba(255,255,255,.18)}
.tt{overflow:hidden}
.ttr{display:grid;grid-template-columns:108px 1fr;border-bottom:1px solid var(--line);background:#fff}
.ttr.alt{background:#f4f8f5}
.ttr:last-child{border:none}
.ttr .tm{padding:11px 12px;border-right:1px solid var(--line);text-align:center}
.ttr .tmt{font-size:13px;font-weight:800;color:var(--blue);font-variant-numeric:tabular-nums;letter-spacing:-.01em}
.ttr .tms{font-size:11px;color:var(--muted);margin-top:3px;font-weight:600;text-align:center}
.ttr .tc{padding:10px 14px}
.ttr .tt-t{font-size:14px;font-weight:700}
.ttr .tt-m{font-size:12.5px;color:var(--muted);margin-top:3px}
.ttr .tt-m .spk{color:#3a4a42;font-weight:600}
.ttr.rest{background:linear-gradient(90deg,#faf2dd,#fdfbf3)}
.ttr.rest .tm{border-right-color:#eee0bf}
.ttr.rest .tmt{color:var(--gold)}.ttr.rest .tms{color:#b09042}
.ttr.rest .tt-t{color:#977829;font-weight:700;letter-spacing:.04em}
.dept{font-size:10.5px;font-weight:700;padding:1px 7px;border-radius:6px;background:#e7f1ec;color:var(--blue);margin-left:6px;vertical-align:middle}
.ef{outline:none;border-radius:3px}
.editing .ef{border-bottom:1px dashed var(--gold);min-width:10px;display:inline-block;padding:0 2px}
.editing .ef:empty::before{content:"＋";color:var(--gold);opacity:.6;font-weight:700}
.editing .ef:focus{background:#fffaef;box-shadow:0 0 0 2px rgba(216,179,103,.35)}
.adminbtn{font-size:12px;font-weight:700;border-radius:9px;padding:7px 13px;cursor:pointer;border:1px solid var(--line);background:#fff;color:var(--muted)}
.adminbtn.on{background:var(--gold);color:#fff;border-color:var(--gold)}
/* videos */
.vrow{display:flex;gap:11px;padding:11px 15px;border-bottom:1px solid var(--line);align-items:flex-start}
.vrow:last-child{border:none}.vrow .vt{flex:1;min-width:0}
.vrow .vn{font-size:13.5px;font-weight:600}.vrow.done .vn{text-decoration:line-through;color:var(--muted)}
.vrow .vm{font-size:11.5px;color:var(--muted);margin-top:2px}
.rtbadge{font-size:11px;font-weight:700;color:var(--blue);background:#e7f1ec;padding:2px 7px;border-radius:6px;flex:none;font-variant-numeric:tabular-nums}
/* seating */
.zgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}
.zone{padding:14px 15px;text-align:center}
.zone .zn{font-size:13px;color:var(--muted);font-weight:600}
.zone .zv{font-size:24px;font-weight:800;color:var(--blue);margin-top:3px}
.placeholder{padding:34px 24px;text-align:center;color:var(--muted)}
.placeholder .pi{font-size:34px}.placeholder h3{font-size:16px;color:var(--ink);margin:8px 0 4px}
/* resources */
.addbtn{font-size:13px;font-weight:700;color:#fff;background:var(--blue);border:none;border-radius:10px;
  padding:9px 15px;cursor:pointer}
.rescat{margin-bottom:16px}
.rescat h4{font-size:13px;font-weight:800;color:var(--blue);margin:0 4px 8px}
.rcard{display:flex;align-items:center;gap:12px;padding:12px 15px;border-bottom:1px solid var(--line)}
.rcard:last-child{border:none}.rcard .ri{font-size:18px;flex:none}
.rcard .rl{flex:1;min-width:0}.rcard .rl b{font-size:14px;font-weight:600;display:block}
.rcard .rl a{font-size:12px;color:var(--blue);text-decoration:none;word-break:break-all}
.rcard .del{background:none;border:none;color:var(--muted);cursor:pointer;font-size:16px;flex:none;padding:4px}
.rcard .del:hover{color:var(--red)}
/* issues */
.iadd{display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap}
.iadd input{flex:1;min-width:180px;padding:10px 13px;border:1px solid var(--line);border-radius:10px;font:inherit;font-size:14px}
.iadd select{padding:10px;border:1px solid var(--line);border-radius:10px;font:inherit;font-size:13px}
.irow{display:flex;gap:11px;padding:12px 15px;border-bottom:1px solid var(--line);align-items:center}
.irow:last-child{border:none}.irow.done .itx{text-decoration:line-through;color:var(--muted)}
.irow .itx{flex:1;font-size:14px;font-weight:500}
.prio{font-size:10.5px;font-weight:800;padding:2px 8px;border-radius:6px;flex:none}
.prio.high{background:#fdeaea;color:var(--red)}.prio.mid{background:#fff3e0;color:var(--amber)}.prio.low{background:#eef2f7;color:var(--muted)}
.irow .del{background:none;border:none;color:var(--muted);cursor:pointer;font-size:16px;padding:4px}
.irow .del:hover{color:var(--red)}
/* budget */
.bcat{margin-bottom:14px;overflow:hidden}
.bch{display:flex;justify-content:space-between;align-items:center;padding:13px 16px;background:linear-gradient(100deg,#0a4936,#0c6b4f);color:#fff}
.bch b{font-size:15px;font-weight:800}.bch .bct{font-size:15px;font-weight:800;color:var(--gold-br);font-variant-numeric:tabular-nums}
.bi{display:flex;gap:11px;padding:10px 16px;border-bottom:1px solid var(--line);align-items:flex-start}
.bi:last-child{border:none}
.bcb{flex:none;width:19px;height:19px;border:2px solid #c6d2df;border-radius:5px;cursor:pointer;display:grid;place-items:center;margin-top:1px}
.bcb.ck{background:var(--green);border-color:var(--green)}.bcb.ck::after{content:"✓";color:#fff;font-size:12px;font-weight:800}
.bi.spent{background:#f3faf5}.bi.spent .bis{color:var(--muted)}.bi.spent .bia{color:var(--green)}
.bdone{font-size:11.5px;font-weight:700;padding:6px 13px;border-radius:8px;cursor:pointer;border:1.5px solid;white-space:nowrap;align-self:center;flex:none}
.bdone.no{background:#fff;border-color:#c6d2df;color:var(--muted)}
.bdone.no:hover{border-color:var(--green);color:var(--green)}
.bdone.yes{background:var(--green);border-color:var(--green);color:#fff}
.bfund{font-size:11px;font-weight:700;padding:6px 11px;border-radius:8px;cursor:pointer;border:1.5px solid;white-space:nowrap;align-self:center;flex:none}
.bfund.hq{background:#eaf3fb;border-color:#0061A0;color:#0061A0}
.bfund.fee{background:#fff3e0;border-color:#c98a2a;color:#a9701a}
.fundsum{display:flex;gap:12px;margin-top:12px;flex-wrap:wrap}
.fundsum .fs{flex:1;min-width:160px;display:flex;justify-content:space-between;align-items:center;padding:11px 16px;border-radius:12px;border:1px solid;font-size:13px;font-weight:600}
.fundsum .fs.hq{background:#eaf3fb;border-color:#bcd9ef;color:#0061A0}
.fundsum .fs.fee{background:#fff6e8;border-color:#f0d9b0;color:#a9701a}
.fundsum .fs b{font-size:17px;font-weight:800}
.bis{font-size:13.5px;font-weight:500;flex:1}.bic{font-size:11.5px;color:var(--muted);margin-top:2px}
.bia{font-size:13.5px;font-weight:700;font-variant-numeric:tabular-nums;white-space:nowrap;text-align:right}
.bef{outline:none}
.editing-bud .bef{border-bottom:1px dashed var(--gold);padding:0 2px;min-width:10px;display:inline-block}
.editing-bud .bef:focus{background:#fffaef;box-shadow:0 0 0 2px rgba(216,179,103,.35)}
.editing-bud .bef:empty::before{content:"＋";color:var(--gold);opacity:.6}
.birm{flex:none;background:none;border:none;color:var(--muted);cursor:pointer;font-size:15px;padding:0 2px;margin-left:6px;line-height:1}
.birm:hover{color:var(--red)}
.biadd{padding:9px 16px;font-size:12.5px;font-weight:700;color:var(--blue);cursor:pointer;border-top:1px dashed var(--line)}
.biadd:hover{background:#f3faf5}
/* seating tool — card grid + static numbered map */
.seatsum{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px;font-size:13px;font-weight:600}
.seatsum .ss{background:#fff;border:1px solid var(--line);border-radius:10px;padding:8px 13px}
.seatsum .ss b{color:var(--blue);font-size:15px}
.seatmap-img{width:100%;display:block;border-radius:8px}
.zlegend{display:flex;flex-wrap:wrap;gap:8px 16px;margin:11px 4px 2px;font-size:12.5px;font-weight:600}
.zlegend .zl{display:flex;align-items:center;gap:6px}
.zlegend .zl i{width:14px;height:14px;border-radius:50%;display:inline-block;border:2px solid}
.tcard .zb{font-size:10px;font-weight:800;padding:1px 6px;border-radius:5px;margin-left:5px;color:#fff}
.seattool{display:grid;grid-template-columns:290px 1fr;gap:14px;align-items:start}
.pool{padding:12px;max-height:660px;overflow:auto;position:sticky;top:58px}
.pool .pgh{font-size:12px;font-weight:700;color:var(--muted);padding:7px 2px 3px;display:flex;justify-content:space-between;border-top:1px solid var(--line);margin-top:4px}
.pchip{display:inline-block;font-size:12.5px;font-weight:600;padding:5px 10px;margin:3px 3px 0 0;border-radius:8px;
  background:#eef3f0;border:1px solid var(--line);cursor:grab;user-select:none;-webkit-user-select:none}
.pchip.sel{background:var(--gold);color:#fff;border-color:var(--gold)}
.tables{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}
.tcard{border:1px solid var(--line);border-radius:10px;background:#fff;padding:10px;min-height:84px;transition:.15s}
.tcard .tch{display:flex;justify-content:space-between;align-items:center;font-size:12px;font-weight:800;margin-bottom:6px}
.tcard .tcn{color:var(--blue)}.tcard .tcc{color:var(--muted);font-weight:700;font-variant-numeric:tabular-nums}
.tcard.full{background:#f3faf5;border-color:var(--green)}.tcard.full .tcc{color:var(--green)}
.tcard.tgt{border-color:var(--gold);box-shadow:0 0 0 2px rgba(216,179,103,.30);cursor:pointer}
.tcard.blk{background:#f0f1f0;border-color:#c4ccc6;opacity:.8}.tcard.blk .tcn{color:#7a857e}
.tm{display:flex;flex-wrap:wrap;gap:3px}
.tname{font-size:11.5px;padding:2px 7px;border-radius:6px;background:#eef3f0;cursor:pointer}
.tname:hover{background:#fdeaea;color:var(--red)}
@media(max-width:820px){.seattool{grid-template-columns:1fr}.pool{position:static;max-height:300px}}
.note{font-size:12px;color:var(--muted);margin-top:10px;padding:0 4px;line-height:1.6}
.reset{font-size:11.5px;color:var(--muted);background:none;border:1px solid var(--line);border-radius:8px;padding:5px 10px;cursor:pointer;font-weight:600}
@media(max-width:820px){.kpis{grid-template-columns:1fr 1fr}.grid2{grid-template-columns:1fr}.arow{grid-template-columns:104px 1fr 46px}}
</style>
</head>
<body>
<header><div class="wrap">
  <div class="brand">
    <img class="logo-ml" src="data:image/png;base64,__METLIFE__" alt="MetLife">
    <span class="sep"></span>
    <div class="htitle"><img class="logo-wio" src="data:image/png;base64,__WIO__" alt="Whole In One"><span id="mSub"></span></div>
  </div>
  <div class="hright">
    <img class="logo-mdrt" src="data:image/png;base64,__MDRT__" alt="MDRT">
    <div class="dday"><em>D-DAY</em><b id="ddayBig"></b></div>
  </div>
  <div class="hmeta" id="hmeta"></div>
</div></header>
<nav class="tabs"><div class="wrap" id="tabbar"></div></nav>
<main class="wrap">
  <section class="panel on" id="p-overview">
    <div class="kpis">
      <div class="card kpi"><div class="k">행사까지</div><div class="v blue" id="kDday"></div><div class="s" id="kDate"></div></div>
      <div class="card kpi"><div class="k">전체 준비 진행률</div><div class="v green" id="kProg"></div><div class="s" id="kProgs"></div></div>
      <div class="card kpi"><div class="k">행사 규모</div><div class="v">698<span style="font-size:15px">명</span></div><div class="s">라운드 70테이블 · 테이블당 10석</div></div>
      <div class="card kpi"><div class="k">준비 영역 / 영상</div><div class="v amber" id="kArea"></div><div class="s" id="kVid"></div></div>
    </div>
    <div class="grid2" style="margin-top:16px">
      <div><h2 class="sec">영역별 준비 현황</h2><div class="card areas" id="areaProg"></div></div>
      <div>
        <h2 class="sec">주요 일정 (마일스톤)</h2><div class="card mile" id="mileList"></div>
        <h2 class="sec">행사 당일 핵심</h2><div class="card mile" id="dayHi"></div>
      </div>
    </div>
  </section>

  <section class="panel" id="p-checklist">
    <div class="toolbar">
      <div class="seg" id="clView"><button data-v="area" class="on">영역별</button><button data-v="dept">분과별</button></div>
      <input class="search" id="clSearch" placeholder="항목·내용·담당 검색…">
      <button class="adminbtn" id="clAdmin">🔒 관리자 편집</button>
      <button class="reset" id="clReset">체크 초기화</button>
      <button class="reset" id="clRestore" style="display:none">원본 복원</button>
    </div>
    <div class="chips" id="clChips" style="margin-bottom:14px"></div>
    <div id="clBody"></div>
    <p class="note">※ 체크 상태는 이 브라우저에 자동 저장됩니다(localStorage). 비어 있는 담당·수량은 추후 채워주세요.</p>
  </section>

  <section class="panel" id="p-depts">
    <h2 class="sec">분과별 업무 · 진행률 · 연락처</h2>
    <div class="dgrid" id="dBody"></div>
    <p class="note">※ 진행률은 해당 분과가 주관하는 체크리스트 항목 기준입니다. 영역 칩을 누르면 체크리스트로 이동합니다. (개인 연락처 포함 — 외부 공유 주의)</p>
  </section>

  <section class="panel" id="p-timetable">
    <div class="ttbar">
      <div class="muted" style="font-size:13px;font-weight:600">전날 리허설 · 당일 행사 전 · 본행사 순</div>
      <button class="adminbtn" id="ttAdmin" style="margin-left:auto">🔒 관리자 편집</button>
      <button class="reset" id="ttRestore" style="display:none">원본 복원</button>
    </div>
    <div id="ttBody"></div>
    <p class="note">※ ‘관리자 편집’은 권한자 전용입니다(비밀번호). 켜면 시간·소요·내용·발표자를 직접 고칠 수 있고, 수정분은 이 브라우저에 저장됩니다.</p>
  </section>

  <section class="panel" id="p-seating">
    <h2 class="sec">좌석 · 배치 개요</h2>
    <div class="kpis" style="grid-template-columns:repeat(3,1fr)">
      <div class="card kpi"><div class="k">참석 인원</div><div class="v blue">698<span style="font-size:15px">명</span></div><div class="s">확정 기준</div></div>
      <div class="card kpi"><div class="k">라운드 테이블</div><div class="v">70<span style="font-size:15px">개</span></div><div class="s">테이블당 10석</div></div>
      <div class="card kpi"><div class="k">무대</div><div class="v amber">14.4<span style="font-size:15px">m</span></div><div class="s">레드카펫 · 스크린 3ea</div></div>
    </div>
    <h2 class="sec">테이블 배치도 <span class="muted" style="font-weight:500;font-size:12px">(좌상단부터 1~71 · 71번 스텝용)</span></h2>
    <div class="card" style="padding:10px;overflow:hidden"><img class="seatmap-img" src="data:image/png;base64,__SEATMAP__" alt="테이블 넘버링 배치도"></div>
    <div class="zlegend" id="zlegend"></div>
    <h2 class="sec">테이블별 인원 배정 <span class="muted" style="font-weight:500;font-size:12px">(이름을 테이블로 드래그 · 아이패드는 이름 탭 → 테이블 탭)</span></h2>
    <div class="seatsum" id="seatSum"></div>
    <div class="seattool">
      <div class="card pool">
        <input class="search" id="poolSearch" placeholder="이름·지점 검색…" style="width:100%">
        <div id="poolBody"></div>
      </div>
      <div class="tables" id="tableBox"></div>
    </div>
    <p class="note">※ 테이블 칸은 <b>넘버링 순(1~71)</b>으로 정렬됩니다. <b>71번은 스텝용으로 블락</b>(참석 70테이블 · 698명). 배정된 이름을 탭하면 해제되고, 상태는 브라우저에 저장됩니다.</p>
    <h2 class="sec">구역 구성 <span class="muted" style="font-weight:500;font-size:12px">(2025 참고 — 2026 확정 시 갱신)</span></h2>
    <div class="zgrid" id="zoneBox"></div>
  </section>

  <section class="panel" id="p-videos">
    <div class="toolbar"><div class="muted" id="vidSum" style="font-size:13px;font-weight:600"></div>
      <button class="reset" id="vidReset" style="margin-left:auto">체크 초기화</button></div>
    <div class="card" id="vidBody"></div>
    <p class="note">※ 제작/확보 완료된 영상을 체크하세요. 총 러닝타임과 진행률이 갱신됩니다.</p>
  </section>

  <section class="panel" id="p-resources">
    <div class="toolbar"><div class="muted" style="font-size:13px;font-weight:600">영상·PPT·문서·드라이브 링크를 한곳에</div>
      <button class="addbtn" id="resAdd" style="margin-left:auto">+ 링크 추가</button></div>
    <div id="resBody"></div>
    <p class="note">※ 링크는 이 브라우저에 저장됩니다(localStorage). 구글드라이브·유튜브·노션 등 어떤 URL이든 등록할 수 있습니다.</p>
  </section>

  <section class="panel" id="p-issues">
    <div class="iadd">
      <input id="isText" placeholder="할 일 · 이슈를 입력하고 Enter…">
      <select id="isPrio"><option value="high">🔴 긴급</option><option value="mid" selected>🟡 보통</option><option value="low">⚪ 참고</option></select>
      <button class="addbtn" id="isAdd">추가</button>
    </div>
    <div class="card" id="isBody"></div>
    <p class="note">※ 미결 이슈·회의 결정·확인 필요사항을 메모하세요. 이 브라우저에 저장됩니다.</p>
  </section>

  <section class="panel" id="p-budget">
    <div id="budGate" class="card placeholder">
      <div class="pi">🔒</div><h3>예산은 관리자 전용입니다</h3>
      <p>관리자 비밀번호를 입력하면 예산 내역이 표시됩니다.</p>
      <button class="addbtn" id="budUnlock" style="margin-top:12px">비밀번호 입력</button>
    </div>
    <div id="budContent" style="display:none">
    <div class="ttbar">
      <div class="muted" style="font-size:13px;font-weight:600">2026 예상 예산 · 지출 완료 항목 체크</div>
      <button class="adminbtn" id="budAdmin" style="margin-left:auto">✏️ 금액·내용 편집</button>
      <button class="reset" id="budLock">🔒 잠금</button>
    </div>
    <div class="kpis">
      <div class="card kpi"><div class="k">등록 입금</div><div class="v green" id="bIn"></div><div class="s" id="bAtt"></div></div>
      <div class="card kpi"><div class="k">지출 예산</div><div class="v" id="bSp"></div><div class="s">대관·제작·운영 합</div></div>
      <div class="card kpi"><div class="k">집행 완료</div><div class="v blue" id="bDone"></div><div class="s" id="bRate"></div></div>
      <div class="card kpi"><div class="k">잔액</div><div class="v amber" id="bBal"></div><div class="s">입금 − 지출예산</div></div>
    </div>
    <div class="fundsum">
      <div class="fs hq"><span>본사지급 합계</span><b id="fHq">—</b></div>
      <div class="fs fee"><span>회비지급 합계</span><b id="fFee">—</b></div>
    </div>
    <div id="bCats" style="margin-top:6px"></div>
    <p class="note">※ <b id="bAsof"></b> 기준 예상 예산. <b>금액·내용 편집</b>으로 항목을 수정·추가·삭제하고, 항목 왼쪽 <b>체크박스로 지출 완료</b>를 표시합니다. 변경분은 브라우저에 저장됩니다.</p>
    </div>
  </section>
</main>

<script>
const DATA = /*__DATA__*/;
const EVENT_DATE=new Date(DATA.meta.date+"T09:00:00+09:00");
const $=s=>document.querySelector(s), ce=(t,c)=>{const e=document.createElement(t);if(c)e.className=c;return e;};
function dday(){return Math.ceil((EVENT_DATE-new Date())/86400000);}
const KEY="mdrt2026_checks"; let CK=JSON.parse(localStorage.getItem(KEY)||"{}");
function save(){localStorage.setItem(KEY,JSON.stringify(CK));}
function toggle(id){CK[id]=!CK[id];save();}
function lsGet(k,d){try{return JSON.parse(localStorage.getItem(k))??d}catch(e){return d}}
function lsSet(k,v){localStorage.setItem(k,JSON.stringify(v));}

/* header */
$("#mSub").textContent=DATA.meta.title+" · 22기";
const dd0=dday();$("#ddayBig").textContent=dd0>0?("D-"+dd0):(dd0===0?"D-DAY":("D+"+(-dd0)));
$("#hmeta").innerHTML=[`📅 ${DATA.meta.date.replace(/-/g,'.')} (금) ${DATA.meta.time}`,`📍 ${DATA.meta.venue}`,
  `👥 ${DATA.meta.scale}`,`기획·진행 ${DATA.meta.agency}`]
  .map(t=>`<span>${t}</span>`).join("");

/* ── checklist data model (id 기반 · 편집/추가/삭제) ── */
let clAdmin=false, _cluid=0;
const CLKEY="mdrt2026_checklist_data", CLDONE="mdrt2026_cl_done";
function cluid(){_cluid++;return "ck"+_cluid+"_"+String(EVENT_DATE.getTime()).slice(-3);}
function clData(){let c=lsGet(CLKEY,null);if(!c)c=JSON.parse(JSON.stringify(DATA.checklist));c.forEach(it=>{if(!it.id)it.id=cluid();});return c;}
function clSave(c){lsSet(CLKEY,c);}
function clDoneMap(){return lsGet(CLDONE,{})}
function clToggle(id){const D=clDoneMap();D[id]?delete D[id]:D[id]=true;lsSet(CLDONE,D);}
function clFind(c,id){return c.find(x=>x.id===id);}
function getAreas(){return [...new Set(clData().map(c=>c.area))];}
function getDepts(){const c=clData();const ord=DATA.dept_order.filter(d=>c.some(x=>x.deptN===d));
  const extra=[...new Set(c.map(x=>x.deptN).filter(d=>d&&!DATA.dept_order.includes(d)))];return [...ord,...extra];}
function keyOf(c,mode){return mode==="dept"?(c.deptN||"미분류"):c.area;}
function groupStat(val,mode){const D=clDoneMap();const items=clData().filter(c=>keyOf(c,mode)===val);
  const done=items.filter(x=>D[x.id]).length;return {total:items.length,done,pct:items.length?Math.round(done/items.length*100):0};}
function overallStat(){const c=clData(),D=clDoneMap();const done=c.filter(x=>D[x.id]).length;
  return {done,total:c.length,pct:c.length?Math.round(done/c.length*100):0};}

function renderOverview(){
  const dd=dday();$("#kDday").textContent=dd>0?("D-"+dd):"D-DAY";
  $("#kDate").textContent=DATA.meta.date.replace(/-/g,'.')+" (금)";
  const o=overallStat();$("#kProg").textContent=o.pct+"%";$("#kProgs").textContent=`${o.done} / ${o.total} 항목 완료`;
  $("#kArea").textContent=getAreas().length+"개";$("#kVid").textContent=`영상 ${DATA.videos.length}컷`;
  const ap=$("#areaProg");ap.innerHTML="";
  getAreas().map(a=>({a,s:groupStat(a,"area")})).sort((x,y)=>x.s.pct-y.s.pct).forEach(({a,s})=>{
    const r=ce("div","arow");
    r.innerHTML=`<div class="an">${a}</div><div class="bar"><i style="width:${s.pct}%"></i></div><div class="ap">${s.done}/${s.total}</div>`;
    r.onclick=()=>{goTab("checklist");clMode="area";setGroup(a);};ap.appendChild(r);
  });
  const ml=$("#mileList");ml.innerHTML="";
  DATA.milestones.forEach(m=>{
    const md=new Date(m.date+"T00:00:00+09:00"),diff=Math.ceil((md-new Date())/86400000);
    const past=diff<0,goal=m.label.includes("MDRT Day");
    const r=ce("div","mrow"+(past?" past":"")+(goal?" goal":""));
    r.innerHTML=`<div class="md">${m.date.slice(5).replace("-",".")}</div><div class="mdot"></div>
      <div class="ml">${m.label}</div><div class="mdd">${past?"완료":(diff===0?"오늘":"D-"+diff)}</div>`;
    ml.appendChild(r);
  });
  const hi=$("#dayHi");hi.innerHTML="";
  DATA.timetable.filter(t=>t.sec==="본행사"&&/CEO|희노애락|Ceremony|Japan|기부|부의 심리학|회장 인사|클로징|Lunch|미래와 전망/.test(t.content)).slice(0,8).forEach(t=>{
    const r=ce("div","mrow");
    r.innerHTML=`<div class="md">${(t.time||'').split('~')[0]}</div><div class="mdot"></div>
      <div class="ml">${t.content}${t.speaker?` <span class="muted" style="font-weight:500">· ${t.speaker}</span>`:''}</div>`;
    hi.appendChild(r);
  });
}

/* checklist */
let clMode="area", curGroup="전체", curSearch="";
function setGroup(g){curGroup=g;renderChips();renderChecklist();}
function renderChips(){
  const box=$("#clChips");box.innerHTML="";const groups=clMode==="dept"?getDepts():getAreas();
  ["전체",...groups].forEach(a=>{
    const c=ce("button","chip"+(a===curGroup?" on":""));
    const s=a==="전체"?overallStat():groupStat(a,clMode);
    c.innerHTML=`${a} <span style="opacity:.8">${s.done}/${s.total}</span>`;
    c.onclick=()=>setGroup(a);box.appendChild(c);
  });
}
function clRerender(){renderChecklist();renderChips();renderOverview();renderDepts();}
function moveChk(id,dir){const c=clData();const it=c.find(x=>x.id===id);if(!it)return;
  const g=keyOf(it,clMode);const idxs=c.map((x,i)=>keyOf(x,clMode)===g?i:-1).filter(i=>i>=0);
  const cur=idxs.indexOf(c.indexOf(it));const tp=cur+dir;if(tp<0||tp>=idxs.length)return;
  const a=idxs[cur],b=idxs[tp];const t=c[a];c[a]=c[b];c[b]=t;clSave(c);clRerender();}
function renderChecklist(){
  const body=$("#clBody");body.className=clAdmin?"editing-cl":"";body.innerHTML="";
  const C=clData(), D=clDoneMap();
  const groups=curGroup==="전체"?(clMode==="dept"?getDepts():getAreas()):[curGroup];
  const q=curSearch.trim().toLowerCase();let shown=0;
  groups.forEach(g=>{
    let items=C.filter(c=>keyOf(c,clMode)===g);
    if(q)items=items.filter(c=>(c.item+c.content+c.owner+c.sit+c.area).toLowerCase().includes(q));
    if(!items.length && !(clAdmin&&!q&&curGroup!=="전체"))return;shown+=items.length;
    const s=groupStat(g,clMode);const block=ce("div","areablock card");const hd=ce("div","areahd");
    const sub=clMode==="dept"?"":(items[0]&&items[0].deptN?`<span class="dp">${items[0].deptN}</span>`:"");
    hd.innerHTML=`<span class="nm">${g}</span>${sub}<span class="cnt">${s.done}/${s.total}</span><div class="bar mini"><i style="width:${s.pct}%"></i></div>`;
    block.appendChild(hd);const list=ce("div","items");
    items.forEach(c=>{
      const on=!!D[c.id];const it=ce("div","it"+(on?" done":""));const tags=[];
      if(clMode==="dept"&&c.area)tags.push(`<span class="tag c">${c.area}</span>`);
      if(!clAdmin){
        if(c.owner)tags.push(`<span class="tag">담당 ${c.owner}</span>`);
        if(c.coop)tags.push(`<span class="tag c">협조 ${c.coop}</span>`);
        if(c.extra)tags.push(`<span class="tag o">${c.extra}</span>`);
        if(c.sit)tags.push(`<span class="tag s">${c.sit}</span>`);
      }
      const ef=(f,v)=>`<span class="cef" data-id="${c.id}" data-f="${f}" contenteditable="true">${v||''}</span>`;
      const nm=clAdmin?ef('item',c.item):(c.item||c.content||'(항목)');
      const ctLine=clAdmin?`<div class="ct">${ef('content',c.content)}</div>`:(c.content&&c.item?`<div class="ct">${c.content}</div>`:'');
      const ownerLine=clAdmin?`<div class="ct">담당 ${ef('owner',c.owner)} · 협조 ${ef('coop',c.coop)}</div>`:'';
      it.innerHTML=`<div class="cb${on?' ck':''}" data-id="${c.id}"></div>
        <div class="body"><div class="nm">${nm}</div>${ctLine}${ownerLine}
        ${(!clAdmin&&c.check)?`<div class="ct">☑ ${c.check}</div>`:''}<div class="tags">${tags.join('')}</div></div>
        ${clAdmin?`<span class="imv"><button class="ciup" data-id="${c.id}">▲</button><button class="cidn" data-id="${c.id}">▼</button></span><button class="itrm" data-id="${c.id}" title="행 삭제">✕</button>`:''}`;
      list.appendChild(it);
    });
    if(clAdmin){const add=ce("div","itadd");add.textContent="＋ 항목 추가";add.dataset.g=g;list.appendChild(add);}
    block.appendChild(list);body.appendChild(block);
  });
  if(!shown && !clAdmin)body.innerHTML=`<div class="card" style="padding:28px;text-align:center;color:var(--muted)">검색 결과가 없습니다.</div>`;
  body.querySelectorAll(".cb").forEach(cb=>cb.onclick=()=>{clToggle(cb.dataset.id);clRerender();});
  if(clAdmin){
    body.querySelectorAll(".cef").forEach(e=>e.addEventListener("blur",()=>{
      const c=clData(),it=clFind(c,e.dataset.id);if(!it)return;it[e.dataset.f]=e.innerText.trim();clSave(c);renderOverview();renderDepts();renderChips();}));
    body.querySelectorAll(".itrm").forEach(b=>b.onclick=()=>{const c=clData().filter(x=>x.id!==b.dataset.id);clSave(c);clRerender();});
    body.querySelectorAll(".ciup").forEach(b=>b.onclick=()=>moveChk(b.dataset.id,-1));
    body.querySelectorAll(".cidn").forEach(b=>b.onclick=()=>moveChk(b.dataset.id,1));
    body.querySelectorAll(".itadd").forEach(b=>b.onclick=()=>{
      const c=clData(),g=b.dataset.g,ni={id:cluid(),item:"새 항목",content:"",owner:"",coop:"",extra:"",sit:"",check:""};
      if(clMode==="dept"){ni.deptN=g;ni.area="기타";}else{ni.area=g;const f=c.find(x=>x.area===g);ni.deptN=f?f.deptN:"";}
      c.push(ni);clSave(c);clRerender();});
  }
}

/* depts */
function renderDepts(){
  const body=$("#dBody");body.innerHTML="";const C=clData();
  getDepts().forEach(d=>{
    const s=groupStat(d,"dept");const card=ce("div","card dcard");
    const areasIn=[...new Set(C.filter(c=>c.deptN===d).map(c=>c.area))];
    const ppl=DATA.contacts.filter(c=>c.divN===d);
    let h=`<div class="dh"><b>${d}</b><span class="muted" style="font-size:12px">${s.done}/${s.total}</span><span class="pct">${s.pct}%</span></div>
      <div class="bar"><i style="width:${s.pct}%"></i></div>
      <div class="areaslist">${areasIn.map(a=>`<span class="achip" data-a="${a}">${a}</span>`).join('')}</div>`;
    if(ppl.length){h+=`<div class="ppl">`;ppl.forEach(c=>{
      const lead=/위원장|회장/.test(c.role);
      h+=`<div class="cp"><div class="nm"><b class="${lead?'role-lead':''}">${c.name}</b><em>${c.role}${c.branch?' · '+c.branch:''}</em></div></div>`;});h+=`</div>`;}
    card.innerHTML=h;
    card.querySelectorAll(".achip").forEach(ch=>ch.onclick=()=>{goTab("checklist");clMode="area";updateViewSeg();setGroup(ch.dataset.a);});
    body.appendChild(card);
  });
}

/* timetable (with admin inline edit) */
const TTKEY="mdrt2026_ttedit", ADMIN_PW="2026", CL_PW="mdrt";
let ttAdmin=false;
function renderTT(){
  const ed=lsGet(TTKEY,{});const body=$("#ttBody");body.classList.toggle("editing",ttAdmin);body.innerHTML="";
  const SEC_BADGE={"D-1 리허설 (전날)":"전날 저녁","당일 행사 전":"당일 오전","본행사":"09:00–18:00"};
  [...new Set(DATA.timetable.map(t=>t.sec))].forEach(sec=>{
    const isMain=sec==="본행사";
    const h=ce("div","ttsec "+(isMain?"main":"prep"));
    h.innerHTML=`${sec}<span class="badge">${SEC_BADGE[sec]||''}</span>`;body.appendChild(h);
    const card=ce("div","card tt");
    DATA.timetable.forEach((t0,gi)=>{
      if(t0.sec!==sec)return;
      const t={...t0,...(ed[gi]||{})};
      const r=ce("div","ttr"+(t.rest?" rest":(gi%2?" alt":"")));
      const F=(f,v,cls)=>ttAdmin?`<span class="ef ${cls||''}" data-id="${gi}" data-f="${f}" contenteditable="true">${v||''}</span>`:(v||'');
      const meta=(t.dept&&!t.rest)?`<span class="dept">${t.dept}</span>`:'';
      const hasM=ttAdmin||t.speaker||t.note;
      const subDisp=ttAdmin?F('sub',t.sub):(t.sub?(t.sec==="본행사"?`(${t.sub})`:t.sub):'');
      r.innerHTML=`<div class="tm"><div class="tmt">${F('time',t.time)}</div><div class="tms">${subDisp}</div></div>
        <div class="tc"><div class="tt-t">${F('content',t.content)}${meta}</div>
        ${hasM?`<div class="tt-m">${F('speaker',t.speaker,'spk')}${(t.speaker&&t.note)?' · ':''}${F('note',t.note)}</div>`:''}</div>`;
      card.appendChild(r);
    });
    body.appendChild(card);
  });
  if(ttAdmin)body.querySelectorAll(".ef").forEach(e=>e.addEventListener("blur",()=>{
    const m=lsGet(TTKEY,{});(m[e.dataset.id]=m[e.dataset.id]||{})[e.dataset.f]=e.innerText.trim();lsSet(TTKEY,m);
  }));
}
$("#ttAdmin").onclick=()=>{
  if(ttAdmin){ttAdmin=false;$("#ttAdmin").textContent="🔒 관리자 편집";$("#ttAdmin").classList.remove("on");$("#ttRestore").style.display="none";renderTT();return;}
  const pw=prompt("관리자 비밀번호를 입력하세요");
  if(pw===null)return;
  if(pw===ADMIN_PW){ttAdmin=true;$("#ttAdmin").textContent="✏️ 편집 중 (끄기)";$("#ttAdmin").classList.add("on");$("#ttRestore").style.display="";renderTT();}
  else alert("비밀번호가 올바르지 않습니다.");
};
$("#ttRestore").onclick=()=>{if(confirm("식순 수정 내용을 모두 원본으로 되돌릴까요?")){localStorage.removeItem(TTKEY);renderTT();}};

/* videos */
function rt2sec(s){if(!s)return 0;const p=s.split(':').map(Number);return p.length===3?p[0]*3600+p[1]*60+p[2]:(p.length===2?p[0]*60+p[1]:0);}
function fmt(t){const m=Math.floor(t/60),s=t%60;return m+":"+String(s).padStart(2,'0');}
function renderVid(){
  const body=$("#vidBody");body.innerHTML="";let part="";
  DATA.videos.forEach((v,i)=>{
    if(v.part!==part){part=v.part;const h=ce("div");h.style.cssText="padding:9px 15px;font-size:12px;font-weight:800;color:var(--blue);background:#f7f9fc;border-bottom:1px solid var(--line)";h.textContent=v.part;body.appendChild(h);}
    const id="vid"+i,on=!!CK[id];const r=ce("div","vrow"+(on?" done":""));
    r.innerHTML=`<div class="cb${on?' ck':''}" data-id="${id}" style="margin-top:0"></div>
      <div class="vt"><div class="vn">${v.title}</div>${(v.cue||v.note)?`<div class="vm">${v.cue||''}${v.cue&&v.note?' · ':''}${v.note||''}</div>`:''}</div>
      ${v.rt?`<span class="rtbadge">${v.rt}</span>`:''}`;
    body.appendChild(r);
  });
  const done=DATA.videos.filter((v,i)=>CK["vid"+i]).length;
  const tot=DATA.videos.reduce((a,v)=>a+rt2sec(v.rt),0);
  $("#vidSum").textContent=`${done}/${DATA.videos.length}컷 준비 · 총 러닝타임 ${fmt(tot)}`;
  body.querySelectorAll(".cb").forEach(cb=>cb.onclick=()=>{toggle(cb.dataset.id);renderVid();});
}

/* seating */
function renderSeating(){
  const box=$("#zoneBox");box.innerHTML="";
  DATA.seating_ref.zones.forEach(([n,v])=>{
    const z=ce("div","card zone");z.innerHTML=`<div class="zn">${n}</div><div class="zv">${v??'—'}</div>`;box.appendChild(z);
  });
}
/* seating assignment tool — floorplan overlay (drag&drop + tap-to-place) */
const SEATKEY="mdrt2026_seats", CAP=10, NTABLE=70;
const BLOCK=new Set(DATA.seating_ref.block||[]);
let seatSel=null, tableView=null;
const ROSTER_BYID={}; DATA.roster.forEach(p=>ROSTER_BYID[p.id]=p);
function seatGet(){const s=lsGet(SEATKEY,null);return s||Object.assign({},DATA.seat_default||{});}
function tcount(a,n){return Object.values(a).filter(t=>t==n).length}
function assignSeat(pid,n){
  if(BLOCK.has(n)){alert(`테이블 ${n}은 스텝용으로 블락되어 있습니다.`);return;}
  const a=seatGet();
  if(tcount(a,n)>=CAP && a[pid]!=n){alert(`테이블 ${n}은 정원(${CAP}석)입니다.`);return;}
  a[pid]=n;lsSet(SEATKEY,a);seatSel=null;tableView=n;renderSeatTool();
}
function unassignSeat(pid){const a=seatGet();delete a[pid];lsSet(SEATKEY,a);renderSeatTool();}
const TZ=DATA.table_zone||{}, ZM=DATA.zone_meta||{};
function light(hex,f){const h=hex.replace('#','');const r=parseInt(h.slice(0,2),16),g=parseInt(h.slice(2,4),16),b=parseInt(h.slice(4,6),16);
  return `rgb(${Math.round(r+(255-r)*f)},${Math.round(g+(255-g)*f)},${Math.round(b+(255-b)*f)})`;}
function renderSeatTool(){
  const a=seatGet();
  $("#zlegend").innerHTML=Object.entries(ZM).map(([k,m])=>`<span class="zl"><i style="background:${light(m.c,.78)};border-color:${m.c}"></i>${m.label}</span>`).join('');
  const asgN=Object.keys(a).filter(p=>ROSTER_BYID[p]).length, used=new Set(Object.values(a)).size, tot=DATA.roster.length;
  $("#seatSum").innerHTML=`<div class="ss">배치 <b>${asgN}</b>/${tot}명</div><div class="ss">미배치 <b>${tot-asgN}</b></div>
    <div class="ss">사용 테이블 <b>${used}</b>/${NTABLE}</div>
    ${seatSel?`<div class="ss" style="color:var(--gold);border-color:var(--gold)">✋ ${ROSTER_BYID[seatSel].name} — 테이블 탭</div>`:''}`;
  // 테이블 카드 (넘버링 순 1~71)
  const tb=$("#tableBox");tb.innerHTML="";
  for(let n=1;n<=DATA.tables.length;n++){
    const blk=BLOCK.has(n);
    const z=TZ[String(n)]||"일반", zc=ZM[z]?ZM[z].c:null;
    const mem=Object.keys(a).filter(pid=>a[pid]==n).map(pid=>ROSTER_BYID[pid]).filter(Boolean);
    const card=ce("div","tcard"+(blk?" blk":(mem.length>=CAP?" full":""))+((seatSel&&!blk)?" tgt":""));
    if(zc&&z!=="일반"&&z!=="스텝")card.style.borderLeft=`4px solid ${zc}`;
    const zb=(z!=="일반"&&z!=="스텝")?`<span class="zb" style="background:${zc}">${z}</span>`:'';
    card.innerHTML=`<div class="tch"><span class="tcn">테이블 ${n}${blk?' 🔧':''}${zb}</span><span class="tcc">${blk?'스텝용':mem.length+'/'+CAP}</span></div>
      <div class="tm">${mem.map(p=>`<span class="tname" data-pid="${p.id}" title="${p.branch} · ${p.name} (탭하면 해제)">${p.name}</span>`).join('')}</div>`;
    if(!blk){
      card.onclick=e=>{if(e.target.classList.contains("tname")){unassignSeat(e.target.dataset.pid);return;}if(seatSel)assignSeat(seatSel,n);};
      card.addEventListener("dragover",e=>e.preventDefault());
      card.addEventListener("drop",e=>{e.preventDefault();const pid=e.dataTransfer.getData("pid");if(pid)assignSeat(pid,n);});
    }
    tb.appendChild(card);
  }
  const q=($("#poolSearch").value||"").trim().toLowerCase();
  const pool=DATA.roster.filter(p=>!a[p.id]);
  const NONMEM=["강사","본사","본부장","컴퍼니체어","운영진","협회","일본·RGA"];
  const TYPECOL={"강사":"#7B5EA7","본사":"#0061A0","본부장":"#c98a2a","컴퍼니체어":"#b5527e","운영진":"#1f8a8a","협회":"#5a8f3a","일본·RGA":"#c0563a"};
  const gkey=p=>(p.type&&p.type!=="회원")?p.type:p.branch;
  const groups={};pool.forEach(p=>{const k=gkey(p);(groups[k]=groups[k]||[]).push(p)});
  const keys=[...NONMEM.filter(k=>groups[k]), ...Object.keys(groups).filter(k=>!NONMEM.includes(k)).sort((x,y)=>x.localeCompare(y,'ko'))];
  const pb=$("#poolBody");pb.innerHTML="";
  keys.forEach(br=>{
    let ppl=groups[br]; if(q)ppl=ppl.filter(p=>(p.name+p.branch+(p.type||'')+(p.bonbu||'')).toLowerCase().includes(q));
    if(!ppl.length)return;
    const isNM=NONMEM.includes(br), col=TYPECOL[br];
    const g=ce("div");g.innerHTML=`<div class="pgh"${col?` style="color:${col}"`:''}><span>${isNM?'◆ '+br:br}</span><span>${ppl.length}</span></div>`;const wrap=ce("div");
    ppl.forEach(p=>{
      const c=ce("span","pchip"+(seatSel===p.id?" sel":""));c.textContent=p.name;c.draggable=true;c.dataset.pid=p.id;
      if(col&&seatSel!==p.id){c.style.borderColor=col;c.style.color=col;c.style.background="#fff";}
      c.onclick=()=>{seatSel=(seatSel===p.id?null:p.id);renderSeatTool();};
      c.addEventListener("dragstart",e=>e.dataTransfer.setData("pid",p.id));
      wrap.appendChild(c);
    });
    g.appendChild(wrap);pb.appendChild(g);
  });
  if(!pb.children.length)pb.innerHTML=`<p class="muted" style="font-size:13px;padding:12px 4px">${q?'검색 결과가 없습니다.':'모든 인원이 배치되었습니다 🎉'}</p>`;
}

/* resources */
const RKEY="mdrt2026_resources";const ICON={"영상":"🎬","PPT·스크립트":"📑","디자인·포스터":"🎨","운영계획·문서":"📋","명단·좌석":"🪑","기타":"🔗"};
function renderRes(){
  const body=$("#resBody");body.innerHTML="";const list=lsGet(RKEY,[]);
  if(!list.length){body.innerHTML=`<div class="card placeholder"><div class="pi">🔗</div><h3>등록된 링크가 없습니다</h3><p>‘+ 링크 추가’로 영상·PPT·운영계획서·구글드라이브 링크를 모아두세요.</p></div>`;return;}
  DATA.resource_cats.forEach(cat=>{
    const items=list.filter(r=>r.cat===cat);if(!items.length)return;
    const sec=ce("div","rescat");sec.innerHTML=`<h4>${ICON[cat]||'🔗'} ${cat}</h4>`;const card=ce("div","card");
    items.forEach(r=>{
      const row=ce("div","rcard");
      row.innerHTML=`<div class="ri">${ICON[cat]||'🔗'}</div><div class="rl"><b>${r.label}</b>
        <a href="${r.url}" target="_blank" rel="noopener">${r.url}</a></div><button class="del" data-id="${r.id}">✕</button>`;
      card.appendChild(row);
    });
    sec.appendChild(card);body.appendChild(sec);
  });
  body.querySelectorAll(".del").forEach(b=>b.onclick=()=>{lsSet(RKEY,lsGet(RKEY,[]).filter(x=>x.id!=b.dataset.id));renderRes();});
}
$("#resAdd").onclick=()=>{
  const label=prompt("자료 이름 (예: 2026 운영계획서, 오프닝 영상)");if(!label)return;
  let url=prompt("링크 URL (https://…)");if(!url)return;if(!/^https?:\/\//.test(url))url="https://"+url;
  const cats=DATA.resource_cats;const cat=prompt("분류 — "+cats.map((c,i)=>`${i+1}.${c}`).join("  "),"1");
  const ci=parseInt(cat)-1;const c=cats[ci]||"기타";
  const list=lsGet(RKEY,[]);list.push({id:Date.now(),cat:c,label,url});lsSet(RKEY,list);renderRes();
};

/* issues */
const IKEY="mdrt2026_issues";
function renderIssues(){
  const body=$("#isBody");body.innerHTML="";const list=lsGet(IKEY,[]);
  if(!list.length){body.innerHTML=`<div class="placeholder"><div class="pi">📝</div><h3>등록된 이슈가 없습니다</h3><p>미결 사항·회의 결정·확인 필요건을 적어두세요.</p></div>`;return;}
  const ord={high:0,mid:1,low:2};
  list.sort((a,b)=>(a.done-b.done)||(ord[a.prio]-ord[b.prio]));
  list.forEach(it=>{
    const on=it.done;const r=ce("div","irow"+(on?" done":""));const pl={high:"긴급",mid:"보통",low:"참고"}[it.prio];
    r.innerHTML=`<div class="cb${on?' ck':''}" data-id="${it.id}"></div>
      <span class="prio ${it.prio}">${pl}</span><div class="itx">${it.text}</div><button class="del" data-id="${it.id}">✕</button>`;
    body.appendChild(r);
  });
  body.querySelectorAll(".cb").forEach(b=>b.onclick=()=>{const l=lsGet(IKEY,[]);const it=l.find(x=>x.id==b.dataset.id);it.done=!it.done;lsSet(IKEY,l);renderIssues();});
  body.querySelectorAll(".del").forEach(b=>b.onclick=()=>{lsSet(IKEY,lsGet(IKEY,[]).filter(x=>x.id!=b.dataset.id));renderIssues();});
}
function addIssue(){
  const t=$("#isText").value.trim();if(!t)return;
  const l=lsGet(IKEY,[]);l.push({id:Date.now(),text:t,prio:$("#isPrio").value,done:false});lsSet(IKEY,l);
  $("#isText").value="";renderIssues();
}
$("#isAdd").onclick=addIssue;
$("#isText").addEventListener("keydown",e=>{if(e.key==="Enter")addIssue();});

/* budget — inline edit (admin) + 지출완료 체크 */
function won(n){return n?(n).toLocaleString('ko-KR')+'원':'—';}
function eok(n){return (n/100000000).toFixed(2)+'억';}
const BKEY="mdrt2026_budget_data", BS="mdrt2026_budget_spent", BFUND="mdrt2026_budget_fund";
let budAdmin=false, budUnlocked=false, _uidc=0;
function fundOf(it){const F=lsGet(BFUND,{});return F[it.id]!==undefined?F[it.id]:(it.fund||"회비");}
function budView(){const u=budUnlocked;$("#budGate").style.display=u?"none":"";$("#budContent").style.display=u?"":"none";if(u)renderBudget();}
function uid(){_uidc++;return "bi"+_uidc+"_"+String(EVENT_DATE.getTime()).slice(-4)+_uidc;}
function parseWon(s){return Number(String(s).replace(/[^0-9]/g,''))||0;}
function bData(){
  let b=lsGet(BKEY,null);
  if(!b) b=JSON.parse(JSON.stringify(DATA.budget));
  b.cats.forEach(c=>c.items.forEach(it=>{if(!it.id)it.id=uid();}));
  return b;
}
function bSave(b){lsSet(BKEY,b);}
function findItem(b,id){for(const c of b.cats)for(const it of c.items)if(it.id===id)return it;return null;}
function renderBudget(){
  const b=bData(), S=lsGet(BS,{});
  let spend=0, done=0, hq=0, fee=0;
  b.cats.forEach(c=>c.items.forEach(it=>{const a=parseWon(it.a);spend+=a;if(S[it.id])done+=a;
    if(fundOf(it)==="본사")hq+=a;else fee+=a;}));
  $("#fHq").textContent=won(hq);$("#fFee").textContent=won(fee);
  $("#bIn").textContent=eok(b.income);$("#bAtt").textContent=won(b.income)+" · 총원 "+b.attendees;
  $("#bSp").textContent=eok(spend);
  $("#bDone").textContent=eok(done);$("#bRate").textContent="예산 대비 "+(spend?Math.round(done/spend*100):0)+"%";
  $("#bBal").textContent=eok(b.income-spend);
  $("#bAsof").textContent=b.as_of;
  const box=$("#bCats");box.className=budAdmin?"editing-bud":"";box.innerHTML="";
  b.cats.forEach((c,ci)=>{
    const ctot=c.items.reduce((s,it)=>s+parseWon(it.a),0);
    const card=ce("div","card bcat");
    let h=`<div class="bch"><b>${c.name}</b><span class="bct">${won(ctot)}</span></div>`;
    c.items.forEach(it=>{
      const sp=!!S[it.id], a=parseWon(it.a);
      const sEdit=budAdmin?`<span class="bef" data-id="${it.id}" data-f="s" contenteditable="true">${it.s||''}</span>`:(it.s||'');
      const aEdit=budAdmin?`<span class="bef amt" data-id="${it.id}" data-f="a" contenteditable="true">${a||''}</span>원`:(a?won(a):'<span class="muted">—</span>');
      const del=budAdmin?`<span class="imv"><button class="biup" data-id="${it.id}">▲</button><button class="bidn" data-id="${it.id}">▼</button></span><button class="birm" data-id="${it.id}" title="행 삭제">✕</button>`:'';
      const chip=`<button class="bdone ${sp?'yes':'no'}" data-id="${it.id}">${sp?'✓ 집행완료':'미집행'}</button>`;
      const f=fundOf(it);
      const fundChip=`<button class="bfund ${f==='본사'?'hq':'fee'}" data-id="${it.id}">${f==='본사'?'본사지급':'회비지급'}</button>`;
      h+=`<div class="bi${sp?' spent':''}">
        <div class="bis">${sEdit}${it.d?`<span class="dept" style="margin-left:7px">${it.d}</span>`:''}${it.c?`<div class="bic">${it.c}</div>`:''}</div>
        <div class="bia">${aEdit}</div>${fundChip}${chip}${del}</div>`;
    });
    if(budAdmin)h+=`<div class="biadd" data-ci="${ci}">＋ 항목 추가</div>`;
    card.innerHTML=h;box.appendChild(card);
  });
  box.querySelectorAll(".bdone").forEach(cb=>cb.onclick=()=>{const s=lsGet(BS,{});const id=cb.dataset.id;s[id]?delete s[id]:s[id]=true;lsSet(BS,s);renderBudget();});
  box.querySelectorAll(".bfund").forEach(cb=>cb.onclick=()=>{const F=lsGet(BFUND,{});const id=cb.dataset.id;
    const it=findItem(bData(),id);const cur=F[id]!==undefined?F[id]:(it?it.fund:"회비");F[id]=cur==="본사"?"회비":"본사";lsSet(BFUND,F);renderBudget();});
  if(budAdmin){
    box.querySelectorAll(".bef").forEach(e=>e.addEventListener("blur",()=>{
      const b=bData(),it=findItem(b,e.dataset.id);if(!it)return;
      it[e.dataset.f]=e.dataset.f==='a'?parseWon(e.innerText):e.innerText.trim();bSave(b);renderBudget();}));
    box.querySelectorAll(".birm").forEach(btn=>btn.onclick=()=>{
      const b=bData();b.cats.forEach(c=>c.items=c.items.filter(it=>it.id!==btn.dataset.id));bSave(b);renderBudget();});
    box.querySelectorAll(".biadd").forEach(btn=>btn.onclick=()=>{
      const b=bData();b.cats[+btn.dataset.ci].items.push({id:uid(),s:"새 항목",a:0,c:"",d:""});bSave(b);renderBudget();});
    box.querySelectorAll(".biup").forEach(b=>b.onclick=()=>moveBud(b.dataset.id,-1));
    box.querySelectorAll(".bidn").forEach(b=>b.onclick=()=>moveBud(b.dataset.id,1));
  }
}
function moveBud(id,dir){const b=bData();for(const c of b.cats){const i=c.items.findIndex(x=>x.id===id);
  if(i>=0){const j=i+dir;if(j>=0&&j<c.items.length){const t=c.items[i];c.items[i]=c.items[j];c.items[j]=t;bSave(b);renderBudget();}return;}}}
$("#budUnlock").onclick=()=>{const pw=prompt("관리자 비밀번호를 입력하세요");if(pw===null)return;
  if(pw===ADMIN_PW){budUnlocked=true;budView();}else alert("비밀번호가 올바르지 않습니다.");};
$("#budLock").onclick=()=>{budUnlocked=false;budAdmin=false;$("#budAdmin").textContent="✏️ 금액·내용 편집";$("#budAdmin").classList.remove("on");
  const bt=document.querySelector('[data-t="budget"]');if(bt)bt.style.display="none";goTab("overview");};
$("#budAdmin").onclick=()=>{
  budAdmin=!budAdmin;
  $("#budAdmin").textContent=budAdmin?"✏️ 편집 중 (끄기)":"✏️ 금액·내용 편집";
  $("#budAdmin").classList.toggle("on",budAdmin);
  renderBudget();
};

/* tabs */
const TABS=[["overview","개요",null],["checklist","체크리스트",()=>clData().length],["depts","분과별",()=>getDepts().length],
  ["timetable","당일 식순",null],["seating","좌석·배치",null],["videos","영상",()=>DATA.videos.length],
  ["resources","자료실",null],["issues","이슈·메모",null],["budget","예산",null]];
function goTab(id){
  document.querySelectorAll(".panel").forEach(p=>p.classList.remove("on"));$("#p-"+id).classList.add("on");
  document.querySelectorAll("#tabbar button").forEach(b=>b.classList.toggle("on",b.dataset.t===id));
  if(id==="budget")budView();
  window.scrollTo({top:0,behavior:"smooth"});
}
const tb=$("#tabbar");
TABS.forEach(([id,label,cnt])=>{const b=ce("button");b.dataset.t=id;b.innerHTML=label+(cnt?` <span class="b">${cnt()}</span>`:"");if(id==="overview")b.classList.add("on");if(id==="budget")b.style.display="none";b.onclick=()=>goTab(id);tb.appendChild(b);});
// 예산은 관리자 전용 — 평소 숨김, 자물쇠 버튼으로 비번 입력 시 노출
const admBtn=ce("button");admBtn.className="tabadmin";admBtn.textContent="🔒 관리자";
admBtn.onclick=()=>{
  if(budUnlocked){goTab("budget");return;}
  const pw=prompt("관리자 비밀번호를 입력하세요");if(pw===null)return;
  if(pw===ADMIN_PW){budUnlocked=true;const bt=document.querySelector('[data-t="budget"]');if(bt)bt.style.display="";goTab("budget");}
  else alert("비밀번호가 올바르지 않습니다.");
};
tb.appendChild(admBtn);

function updateViewSeg(){document.querySelectorAll("#clView button").forEach(b=>b.classList.toggle("on",b.dataset.v===clMode));}
document.querySelectorAll("#clView button").forEach(b=>b.onclick=()=>{clMode=b.dataset.v;updateViewSeg();curGroup="전체";renderChips();renderChecklist();});
$("#clSearch").oninput=e=>{curSearch=e.target.value;renderChecklist();};
$("#clReset").onclick=()=>{if(confirm("체크리스트 완료 체크를 모두 초기화할까요?")){localStorage.removeItem(CLDONE);clRerender();}};
$("#clRestore").onclick=()=>{if(confirm("체크리스트 내용 수정·추가·삭제를 모두 원본으로 되돌릴까요? (완료 체크는 유지)")){localStorage.removeItem(CLKEY);clRerender();}};
$("#clAdmin").onclick=()=>{
  if(clAdmin){clAdmin=false;$("#clAdmin").textContent="🔒 관리자 편집";$("#clAdmin").classList.remove("on");$("#clRestore").style.display="none";clRerender();return;}
  const pw=prompt("관리자 비밀번호를 입력하세요");if(pw===null)return;
  if(pw===CL_PW){clAdmin=true;$("#clAdmin").textContent="✏️ 편집 중 (끄기)";$("#clAdmin").classList.add("on");$("#clRestore").style.display="";clRerender();}
  else alert("비밀번호가 올바르지 않습니다.");
};
$("#vidReset").onclick=()=>{if(confirm("영상 체크를 초기화할까요?")){Object.keys(CK).filter(k=>k.startsWith("vid")).forEach(k=>delete CK[k]);save();renderVid();}};

$("#poolSearch").oninput=()=>renderSeatTool();
document.querySelector(".logo-wio").addEventListener("click",()=>location.reload());
renderOverview();renderChips();renderChecklist();renderDepts();renderTT();renderSeating();renderSeatTool();renderVid();renderRes();renderIssues();renderBudget();
</script>
</body>
</html>"""

import base64
ASSET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
def b64(name): return base64.b64encode(open(os.path.join(ASSET, name), "rb").read()).decode()
html = TPL.replace("/*__DATA__*/", json.dumps(DATA, ensure_ascii=False))
html = (html.replace("__METLIFE__", b64("metlife.png"))
            .replace("__WIO__", b64("wholeinone.png"))
            .replace("__MDRT__", b64("mdrt.png"))
            .replace("__SEATMAP__", b64("seatmap.png")))
open(OUT, "w", encoding="utf-8").write(html)
print("written:", OUT, len(html), "bytes")

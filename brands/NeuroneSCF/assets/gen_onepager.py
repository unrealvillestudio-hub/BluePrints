"""Generate NSCF B2B kit pricing one-pager: dark + print versions."""
import base64, os, sys

BASE    = r"C:\Users\black\GitHub\BluePrints\brands\NeuroneSCF\assets"
BRAND   = os.path.join(BASE, "brand")
PROD    = os.path.join(BASE, "products")
DARK    = os.path.join(PROD, "dark_versions")
ALPHA   = os.path.join(PROD, "alpha_dark")
OUT     = BASE


def b64(path):
    if not path or not os.path.exists(path):
        print(f"  MISSING: {path}", file=sys.stderr)
        return ""
    ext  = os.path.splitext(path)[1].lower()
    mime = {".png":"image/png",".jpg":"image/jpeg",".jpeg":"image/jpeg",
            ".webp":"image/webp",".svg":"image/svg+xml"}.get(ext,"image/png")
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    print(f"  OK  {os.path.basename(path)} ({len(data)//1024}KB b64)")
    return f"data:{mime};base64,{data}"


# ── load images ──────────────────────────────────────────────────────────────
LOGOS = os.path.join(BRAND, "NeuroneSCF")
print("Loading images…")
logo_w     = b64(os.path.join(LOGOS, "NSCF_Logo_WT_TC.png"))   # white+alpha, dark bg
logo_cy    = b64(os.path.join(LOGOS, "NSCF_Logo_CY_TC.png"))   # color+alpha, light bg

dk_tinte   = b64(os.path.join(DARK,  "NCOLOR_dark.png"))
dk_shampoo = b64(os.path.join(ALPHA, "HUMIT_SH_1L_alpha.png"))
dk_mask    = b64(os.path.join(ALPHA, "humitmask_400_web_alpha.png"))
dk_perox   = b64(os.path.join(DARK,  "NACDR_dark.png"))
dk_liso    = b64(os.path.join(DARK,  "NTLISOTH-1-1_dark.png"))
dk_kerasin = b64(os.path.join(DARK,  "NTKHBMK-1-1_dark.png"))
dk_dyf     = b64(os.path.join(ALPHA, "dyfensorsh_400_web_alpha.png"))

pt_tinte   = b64(os.path.join(PROD,  "NCOLOR.png"))
pt_shampoo = b64(os.path.join(PROD,  "HUMIT_SH_1L.png"))
pt_mask    = b64(os.path.join(PROD,  "humitmask_400_web.png"))
pt_perox   = b64(os.path.join(PROD,  "NACDR.png"))
pt_liso    = b64(os.path.join(PROD,  "NTLISOTH-1-1.png"))
pt_kerasin = b64(os.path.join(PROD,  "NTKHBMK-1-1.png"))
pt_dyf     = b64(os.path.join(PROD,  "dyfensorsh_400_web.png"))


# ── helpers ──────────────────────────────────────────────────────────────────
def kit_imgs_dark(*srcs, h=64):
    imgs = [s for s in srcs if s]
    if not imgs:
        return ""
    tags = "".join(
        f'<img src="{s}" style="max-height:{h}px;object-fit:contain;opacity:0.9;">'
        for s in imgs
    )
    return (
        f'<div style="display:flex;justify-content:center;align-items:center;'
        f'gap:8px;padding:7px 14px;background:transparent;">{tags}</div>'
    )


def kit_imgs_print(*srcs, h=72):
    imgs = [s for s in srcs if s]
    if not imgs:
        return ""
    tags = "".join(
        f'<img src="{s}" style="max-height:{h}px;object-fit:contain;">'
        for s in imgs
    )
    return (
        f'<div style="background:#FFFFFF!important;border-top:1px solid #C9A55A;'
        f'border-bottom:1px solid #C9A55A;padding:9px;text-align:center;'
        f'display:flex;justify-content:center;align-items:center;gap:8px;">{tags}</div>'
    )


def pr_row(src, name, fmt, price):
    img = (
        f'<img src="{src}" style="width:26px;height:26px;object-fit:contain;flex-shrink:0;">'
        if src else '<div style="width:26px;flex-shrink:0;"></div>'
    )
    return (
        f'<div style="display:flex;align-items:center;gap:8px;'
        f'padding:4px 0;border-bottom:1px solid #1e2535;">'
        f'{img}'
        f'<div style="flex:1;">'
        f'<div style="font-size:8.5px;color:#9ca3af;">{name}</div>'
        f'<div style="font-size:7px;color:#6b7280;">{fmt}</div>'
        f'</div>'
        f'<div style="font-size:10.5px;font-weight:700;color:#F8FAFB;'
        f'text-align:right;flex-shrink:0;">{price}</div>'
        f'</div>'
    )


def pc_cell(src, name, price, note):
    if src:
        top = (
            f'<div style="background:#FFFFFF!important;padding:7px;'
            f'text-align:center;border-bottom:1px solid #C9A55A;'
            f'display:flex;align-items:center;justify-content:center;height:74px;">'
            f'<img src="{src}" style="max-height:58px;object-fit:contain;"></div>'
        )
    else:
        ini = name[0] if name else "?"
        top = (
            f'<div style="background:#FFFFFF!important;padding:7px;'
            f'text-align:center;border-bottom:1px solid #C9A55A;'
            f'display:flex;align-items:center;justify-content:center;height:74px;">'
            f'<span style="font-size:22px;color:#C9A55A;font-weight:300;">{ini}</span></div>'
        )
    return (
        f'<div style="border:1px solid #C9A55A;border-radius:2px;overflow:hidden;">'
        f'{top}'
        f'<div style="background:#F5F0E8!important;padding:5px 6px;">'
        f'<div style="font-size:8.5px;font-weight:600;color:#0A0D14;">{name}</div>'
        f'<div style="font-size:11.5px;font-weight:700;color:#0A0D14;">{price}</div>'
        f'<div style="font-size:7px;color:#555555;">{note}</div>'
        f'</div></div>'
    )


def logo_tag(h=40):
    """Always use the color (CY) logo — NSCF_Logo_CY_TC.png"""
    if logo_cy:
        return f'<img src="{logo_cy}" style="height:{h}px;" alt="Neurone South &amp; Central FL">'
    return '<span style="font-size:14px;font-weight:700;color:#F8FAFB;">NEURONE<br><span style="font-size:7px;letter-spacing:3px;color:#B8892A;">SOUTH &amp; CENTRAL FL</span></span>'


def logo_ftr(h=28):
    """Always use the color (CY) logo — NSCF_Logo_CY_TC.png"""
    if logo_cy:
        return f'<img src="{logo_cy}" style="height:{h}px;" alt="Neurone South &amp; Central FL">'
    return ''


# ─────────────────────────────────────────────────────────────────────────────
#  DARK CSS
# ─────────────────────────────────────────────────────────────────────────────
DARK_CSS = """
*{margin:0;padding:0;box-sizing:border-box;}
@page{size:Letter;margin:0;}
@media print{*{-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important;}}
body{
  width:215.9mm;background:#0A0D14;color:#F8FAFB;
  font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;
  -webkit-print-color-adjust:exact;print-color-adjust:exact;
}
.hdr{background:#0A0D14;padding:20px 28px;display:flex;justify-content:space-between;align-items:center;}
.hl{display:flex;flex-direction:column;gap:4px;}
.hsub{font-size:7px;color:#B8892A;letter-spacing:4px;text-transform:uppercase;font-weight:500;}
.hr{display:flex;flex-direction:column;align-items:flex-end;gap:4px;}
.bpro{border:1px solid #B8892A;color:#B8892A;padding:3px 8px;font-size:8px;font-weight:600;letter-spacing:1px;text-transform:uppercase;}
.hlnch{font-size:7.5px;color:rgba(255,255,255,0.3);}
.gbar{background:#B8892A;padding:8px 28px;display:flex;justify-content:space-between;align-items:center;}
.gtl{font-style:italic;color:#0A0D14;font-size:11px;font-family:Georgia,'Times New Roman',serif;}
.bship{background:#0A0D14;color:#B8892A;font-size:8px;font-weight:700;padding:4px 9px;white-space:nowrap;}
.kg{padding:15px 18px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;}
.kc{border:1px solid #1e2535;background:#111420;display:flex;flex-direction:column;}
.kc.fl{border:2px solid #B8892A;}
.flb{background:#B8892A;color:#0A0D14;font-size:7px;font-weight:700;letter-spacing:2px;text-transform:uppercase;text-align:center;padding:3px 0;}
.kh{padding:13px 13px 10px;border-bottom:1px solid #1e2535;}
.kl{font-size:7px;color:#B8892A;letter-spacing:3px;text-transform:uppercase;font-weight:600;margin-bottom:3px;}
.kn{font-size:20px;font-weight:300;color:#F8FAFB;line-height:1.1;margin-bottom:3px;}
.kpr{display:flex;align-items:baseline;gap:7px;}
.kp{font-size:28px;font-weight:700;color:#F8FAFB;line-height:1;}
.ks{font-size:8px;color:#6b7280;}
.ki-list{padding:10px 13px;flex:1;display:flex;flex-direction:column;gap:4px;}
.ki{display:flex;align-items:flex-start;gap:6px;}
.bul{width:4px;height:4px;min-width:4px;border-radius:50%;background:#3d4455;margin-top:4px;}
.bul.g{background:#B8892A;}
.im{font-size:9px;font-weight:500;color:#F8FAFB;line-height:1.3;}
.in{font-size:7.5px;color:#6b7280;line-height:1.2;}
.kft{padding:8px 13px;border-top:1px solid #1e2535;}
.ktg{font-size:8px;color:#6b7280;font-style:italic;}
.ktg.g{color:#B8892A;}
.div{height:1px;margin:0 18px;background:linear-gradient(to right,transparent,#1e2535,transparent);}
.bot{padding:12px 18px;display:grid;grid-template-columns:1fr 1fr;gap:18px;}
.st{font-size:7px;font-weight:700;letter-spacing:3px;color:#B8892A;text-transform:uppercase;margin-bottom:8px;}
.abox{border:1px dashed #B8892A;background:rgba(184,137,42,0.04);padding:11px 13px;}
.al{font-size:7px;font-weight:700;color:#B8892A;letter-spacing:2px;text-transform:uppercase;margin-bottom:5px;}
.at{font-size:13px;font-weight:700;color:#F8FAFB;margin-bottom:4px;}
.ad{font-size:8px;color:#6b7280;line-height:1.4;margin-bottom:7px;}
.ap{font-size:21px;font-weight:700;color:#B8892A;}
.onote{margin:0 18px 13px;padding:9px 13px;border-left:2px solid #1e2535;background:rgba(255,255,255,0.02);}
.onote p{font-size:7.5px;color:#6b7280;line-height:1.5;}
.ftr{background:#060810;border-top:1px solid #1e2535;padding:11px 28px;display:flex;justify-content:space-between;align-items:center;}
.fb{font-size:10px;font-weight:700;letter-spacing:3px;color:#F8FAFB;text-transform:uppercase;}
.fc{display:flex;flex-direction:column;align-items:center;gap:2px;font-size:7.5px;color:#6b7280;}
.fw{display:flex;flex-direction:column;align-items:flex-end;gap:2px;font-size:7.5px;color:#6b7280;}
"""

# ─────────────────────────────────────────────────────────────────────────────
#  PRINT CSS
# ─────────────────────────────────────────────────────────────────────────────
PRINT_CSS = """
*{margin:0;padding:0;box-sizing:border-box;}
@page{size:Letter;margin:0;}
@media print{*{-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important;}}
body{
  width:215.9mm;background:#FFFFFF!important;color:#0A0D14;
  font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;
  -webkit-print-color-adjust:exact;print-color-adjust:exact;
}
.hdr{background:#0A0D14!important;padding:20px 28px;display:flex;justify-content:space-between;align-items:center;}
.hl{display:flex;flex-direction:column;gap:4px;}
.hsub{font-size:7px;color:#B8892A;letter-spacing:4px;text-transform:uppercase;font-weight:500;}
.hr{display:flex;flex-direction:column;align-items:flex-end;gap:4px;}
.bpro{border:1px solid #B8892A;color:#B8892A;padding:3px 8px;font-size:8px;font-weight:600;letter-spacing:1px;text-transform:uppercase;}
.hlnch{font-size:7.5px;color:rgba(255,255,255,0.3);}
.gbar{background:#B8892A!important;padding:8px 28px;display:flex;justify-content:space-between;align-items:center;}
.gtl{font-style:italic;color:#0A0D14;font-size:11px;font-family:Georgia,'Times New Roman',serif;}
.bship{background:#FFFFFF!important;color:#B8892A;font-size:8px;font-weight:700;padding:4px 9px;white-space:nowrap;border:1px solid #B8892A;}
.kg{padding:15px 18px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;background:#FFFFFF!important;}
.kc{border:1px solid #C9A55A;border-radius:2px;background:#FFFFFF!important;display:flex;flex-direction:column;overflow:hidden;}
.kc.fl{border:2px solid #B8892A;border-top-width:4px;}
.kh{background:#B8892A!important;padding:12px 13px 9px;}
.kl{font-size:7px;font-weight:700;letter-spacing:3px;color:rgba(255,255,255,0.9);text-transform:uppercase;margin-bottom:3px;}
.kn{font-size:20px;font-weight:600;color:#FFFFFF;line-height:1.1;margin-bottom:3px;font-family:Georgia,'Times New Roman',serif;}
.kpr{display:flex;align-items:baseline;gap:7px;}
.kp{font-size:26px;font-weight:700;color:#FFFFFF;line-height:1;}
.ks{font-size:8px;color:rgba(255,255,255,0.85);}
.ki-list{padding:9px 13px;flex:1;display:flex;flex-direction:column;gap:3px;background:#FFFFFF!important;}
.ki{display:flex;align-items:flex-start;gap:6px;padding-bottom:4px;border-bottom:1px solid rgba(201,165,90,0.25);}
.ki:last-child{border-bottom:none;padding-bottom:0;}
.bsq{font-size:7px;color:#B8892A;margin-top:2px;flex-shrink:0;line-height:1;}
.im{font-size:9px;font-weight:500;color:#0A0D14;line-height:1.3;}
.in{font-size:7.5px;color:#555555;line-height:1.2;}
.kft{background:#F5F0E8!important;border-top:1px solid #C9A55A;padding:7px 13px;}
.ktg{font-size:8px;color:#8B6520;font-style:italic;}
.div{height:1px;margin:0 18px;background:#C9A55A;}
.bot{padding:12px 18px;display:grid;grid-template-columns:1fr 1fr;gap:18px;background:#FFFFFF!important;}
.st{font-size:7px;font-weight:700;letter-spacing:3px;color:#B8892A;text-transform:uppercase;margin-bottom:8px;}
.vg{display:grid;grid-template-columns:1fr 1fr 1fr;gap:7px;}
.abox{border:1px dashed #B8892A;background:#FFFBF5!important;padding:11px 13px;}
.al{font-size:7px;font-weight:700;color:#8B6520;letter-spacing:2px;text-transform:uppercase;margin-bottom:5px;}
.at{font-size:13px;font-weight:700;color:#0A0D14;margin-bottom:4px;}
.ad{font-size:8px;color:#555555;line-height:1.4;margin-bottom:7px;}
.ap{font-size:21px;font-weight:700;color:#B8892A;}
.onote{margin:0 18px 13px;padding:9px 13px;border-left:3px solid #B8892A;background:#F5F0E8!important;}
.onote p{font-size:7.5px;color:#555555;line-height:1.5;}
.ftr{background:#0A0D14!important;padding:11px 28px;display:flex;justify-content:space-between;align-items:center;}
.fb{font-size:10px;font-weight:700;letter-spacing:3px;color:#F8FAFB;text-transform:uppercase;}
.fc{display:flex;flex-direction:column;align-items:center;gap:2px;font-size:7.5px;color:#9ca3af;}
.fw{display:flex;flex-direction:column;align-items:flex-end;gap:2px;font-size:7.5px;color:#9ca3af;}
"""


# ─────────────────────────────────────────────────────────────────────────────
#  SHARED FOOTER/HEADER FRAGMENTS
# ─────────────────────────────────────────────────────────────────────────────
def header_html():
    return f"""
<div class="hdr">
  <div class="hl">
    {logo_tag(40)}
    <span class="hsub">South &amp; Central Florida</span>
  </div>
  <div class="hr">
    <span class="bpro">Professional Channel</span>
    <span class="hlnch">Florida · Launch Pricing · 2026</span>
  </div>
</div>

<div class="gbar">
  <span class="gtl">Laboratory-grade professional haircare — delivered to your door.</span>
  <span class="bship">✦ Free Shipping on All Kits</span>
</div>"""


def footer_html():
    return """
<div class="onote">
  <p><strong>How to order:</strong> Contact Patricia directly via WhatsApp to place your
  first order. Shade selection confirmed at time of order.
  Delivery within South &amp; Central Florida.
  pro.neuronescflorida.com — Online portal coming soon.</p>
</div>

<div class="ftr">
  <div class="fb">{logo_ftr()}</div>
  <div class="fc">
    <span>WhatsApp · Patricia / +1 (305) 748-9101</span>
    <span>Email / hello-pro@neuronescflorida.com</span>
  </div>
  <div class="fw">
    <span style="font-style:italic;">Professional use only</span>
    <span>pro.neuronescflorida.com</span>
  </div>
</div>"""


# ─────────────────────────────────────────────────────────────────────────────
#  DARK HTML
# ─────────────────────────────────────────────────────────────────────────────
def make_dark():
    ka = kit_imgs_dark(dk_tinte)
    kb = kit_imgs_dark(dk_tinte, dk_shampoo)
    kc = kit_imgs_dark(dk_tinte, dk_mask)

    pr = (
        pr_row(dk_tinte,   "Neurone Color Tube",    "90ml · min. 12 tubes",   "$8.99")
      + pr_row(dk_shampoo, "Professional Shampoo",  "1L · base line",          "$28.99")
      + pr_row(dk_perox,   "Neuroactive Developer", "1L · any VOL",            "$13.99")
      + pr_row(dk_mask,    "Humit Mask",            "1L · treatment",          "$34.99")
      + pr_row(dk_liso,    "Lisothermic",           "1L · treatment",          "$35.99")
      + pr_row(dk_kerasin, "Kerasin HB Mask",       "1L · premium treatment",  "$39.99")
    )

    dyf_img = (
        f'<div style="margin-bottom:8px;"><img src="{dk_dyf}" '
        f'style="max-height:52px;object-fit:contain;opacity:0.9;"></div>'
        if dk_dyf else ""
    )

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>{DARK_CSS}</style>
</head>
<body>

{header_html()}

<div class="kg">

  <div class="kc">
    <div class="kh">
      <div class="kl">KIT A · COLOR STARTER</div>
      <div class="kn">Color<br>Starter</div>
      <div class="kpr"><span class="kp">$99</span><span class="ks">free shipping</span></div>
    </div>
    {ka}
    <div class="ki-list">
      <div class="ki"><div class="bul"></div><div><div class="im">12 Neurone Color Tubes (90ml)</div><div class="in">Shade selection yours</div></div></div>
      <div class="ki"><div class="bul"></div><div><div class="im">Neuroactive Developer 1L</div><div class="in">VOL to choose: 10, 20, 30 or 40</div></div></div>
    </div>
    <div class="kft"><span class="ktg">Start the system · zero risk</span></div>
  </div>

  <div class="kc fl">
    <div class="flb">★ Most Popular</div>
    <div class="kh">
      <div class="kl">KIT B · SALON SYSTEM</div>
      <div class="kn">Salon<br>System</div>
      <div class="kpr"><span class="kp">$169</span><span class="ks">free shipping</span></div>
    </div>
    {kb}
    <div class="ki-list">
      <div class="ki"><div class="bul g"></div><div><div class="im">12 Neurone Color Tubes (90ml)</div><div class="in">Shade selection yours</div></div></div>
      <div class="ki"><div class="bul g"></div><div><div class="im">Neuroactive Developer 1L</div><div class="in">VOL to choose</div></div></div>
      <div class="ki"><div class="bul g"></div><div><div class="im">2 Professional Shampoos 1L</div><div class="in">Total Violet + Depura, or choose</div></div></div>
      <div class="ki"><div class="bul g"></div><div><div class="im">Humit Mask 1L</div><div class="in">Professional deep treatment</div></div></div>
    </div>
    <div class="kft"><span class="ktg g">Everything your salon needs — one order</span></div>
  </div>

  <div class="kc">
    <div class="kh">
      <div class="kl">KIT C · COLOR PRO</div>
      <div class="kn">Color<br>Pro</div>
      <div class="kpr"><span class="kp">$229</span><span class="ks">free shipping</span></div>
    </div>
    {kc}
    <div class="ki-list">
      <div class="ki"><div class="bul"></div><div><div class="im">24 Neurone Color Tubes (90ml)</div><div class="in">Shade selection yours</div></div></div>
      <div class="ki"><div class="bul"></div><div><div class="im">2× Neuroactive Developer 1L</div><div class="in">VOL to choose</div></div></div>
      <div class="ki"><div class="bul"></div><div><div class="im">2 Professional Shampoos 1L</div><div class="in">Choose your line</div></div></div>
      <div class="ki"><div class="bul"></div><div><div class="im">Humit Mask 1L</div><div class="in">Professional deep treatment</div></div></div>
    </div>
    <div class="kft"><span class="ktg">For the salon that&apos;s ready to commit</span></div>
  </div>

</div>

<div class="div"></div>

<div class="bot">
  <div>
    <div class="st">Individual Pricing</div>
    {pr}
  </div>
  <div>
    <div class="st">Add-On</div>
    <div class="abox">
      <div class="al">Sulfate-Free Upgrade</div>
      {dyf_img}
      <div class="at">Dyfensor Sulfate-Free Shampoo</div>
      <div class="ad">Add the sulfate-free line to any order. Extends color vibrancy and reduces fade for color-treated clients.</div>
      <div class="ap">$33.99</div>
    </div>
  </div>
</div>

{footer_html()}

</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
#  PRINT HTML
# ─────────────────────────────────────────────────────────────────────────────
def make_print():
    ka = kit_imgs_print(pt_tinte)
    kb = kit_imgs_print(pt_tinte, pt_shampoo)
    kc = kit_imgs_print(pt_tinte, pt_mask)

    vc = (
        pc_cell(pt_tinte,   "Neurone Color",  "$8.99",  "90ml · min. 12")
      + pc_cell(pt_shampoo, "Pro Shampoo",    "$28.99", "1L · base line")
      + pc_cell(pt_perox,   "Developer",      "$13.99", "1L · any VOL")
      + pc_cell(pt_mask,    "Humit Mask",     "$34.99", "1L · treatment")
      + pc_cell(pt_liso,    "Lisothermic",    "$35.99", "1L · treatment")
      + pc_cell(pt_kerasin, "Kerasin HB",     "$39.99", "1L · premium")
    )

    dyf_img = (
        f'<div style="margin-bottom:8px;text-align:center;">'
        f'<img src="{pt_dyf}" style="max-height:52px;object-fit:contain;"></div>'
        if pt_dyf else ""
    )

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>{PRINT_CSS}</style>
</head>
<body>

{header_html()}

<div class="kg">

  <div class="kc">
    <div class="kh">
      <div class="kl">KIT A · COLOR STARTER</div>
      <div class="kn">Color Starter</div>
      <div class="kpr"><span class="kp">$99</span><span class="ks">free shipping</span></div>
    </div>
    {ka}
    <div class="ki-list">
      <div class="ki"><div class="bsq">&#9632;</div><div><div class="im">12 Neurone Color Tubes (90ml)</div><div class="in">Shade selection yours</div></div></div>
      <div class="ki"><div class="bsq">&#9632;</div><div><div class="im">Neuroactive Developer 1L</div><div class="in">VOL to choose: 10, 20, 30 or 40</div></div></div>
    </div>
    <div class="kft"><span class="ktg">Start the system · zero risk</span></div>
  </div>

  <div class="kc fl">
    <div class="kh">
      <div class="kl">KIT B · SALON SYSTEM ★</div>
      <div class="kn">Salon System</div>
      <div class="kpr"><span class="kp">$169</span><span class="ks">free shipping</span></div>
    </div>
    {kb}
    <div class="ki-list">
      <div class="ki"><div class="bsq">&#9632;</div><div><div class="im">12 Neurone Color Tubes (90ml)</div><div class="in">Shade selection yours</div></div></div>
      <div class="ki"><div class="bsq">&#9632;</div><div><div class="im">Neuroactive Developer 1L</div><div class="in">VOL to choose</div></div></div>
      <div class="ki"><div class="bsq">&#9632;</div><div><div class="im">2 Professional Shampoos 1L</div><div class="in">Total Violet + Depura, or choose</div></div></div>
      <div class="ki"><div class="bsq">&#9632;</div><div><div class="im">Humit Mask 1L</div><div class="in">Professional deep treatment</div></div></div>
    </div>
    <div class="kft"><span class="ktg">Everything your salon needs — one order</span></div>
  </div>

  <div class="kc">
    <div class="kh">
      <div class="kl">KIT C · COLOR PRO</div>
      <div class="kn">Color Pro</div>
      <div class="kpr"><span class="kp">$229</span><span class="ks">free shipping</span></div>
    </div>
    {kc}
    <div class="ki-list">
      <div class="ki"><div class="bsq">&#9632;</div><div><div class="im">24 Neurone Color Tubes (90ml)</div><div class="in">Shade selection yours</div></div></div>
      <div class="ki"><div class="bsq">&#9632;</div><div><div class="im">2× Neuroactive Developer 1L</div><div class="in">VOL to choose</div></div></div>
      <div class="ki"><div class="bsq">&#9632;</div><div><div class="im">2 Professional Shampoos 1L</div><div class="in">Choose your line</div></div></div>
      <div class="ki"><div class="bsq">&#9632;</div><div><div class="im">Humit Mask 1L</div><div class="in">Professional deep treatment</div></div></div>
    </div>
    <div class="kft"><span class="ktg">For the salon that&apos;s ready to commit</span></div>
  </div>

</div>

<div class="div"></div>

<div class="bot">
  <div>
    <div class="st">Individual Pricing</div>
    <div class="vg">{vc}</div>
  </div>
  <div>
    <div class="st">Add-On</div>
    <div class="abox">
      <div class="al">Sulfate-Free Upgrade</div>
      {dyf_img}
      <div class="at">Dyfensor Sulfate-Free Shampoo</div>
      <div class="ad">Add the sulfate-free line to any order. Extends color vibrancy and reduces fade for color-treated clients.</div>
      <div class="ap">$33.99</div>
    </div>
  </div>
</div>

{footer_html()}

</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
#  WRITE FILES
# ─────────────────────────────────────────────────────────────────────────────
print("\nGenerating HTML…")

dark_path = os.path.join(OUT, "NSCF_Kit_Pricing_Orlando.html")
with open(dark_path, "w", encoding="utf-8") as f:
    f.write(make_dark())
print(f"  Wrote {dark_path}  ({os.path.getsize(dark_path)//1024}KB)")

print_path = os.path.join(OUT, "NSCF_Kit_Pricing_Orlando_PRINT.html")
with open(print_path, "w", encoding="utf-8") as f:
    f.write(make_print())
print(f"  Wrote {print_path}  ({os.path.getsize(print_path)//1024}KB)")

print("\nDone.")

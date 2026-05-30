"""
Generate NSCF_Kit_Pricing_PRINT.html + .pdf  (Legal 8.5×14")
Run: python gen_legal_print.py
"""
import base64, io, os, pathlib, sys

BASE    = pathlib.Path(r"C:\Users\black\GitHub\BluePrints\brands\NeuroneSCF\assets")
BRAND   = BASE / "brand"
PROD    = BASE / "products"
ALPHA   = PROD / "alpha_dark"
OUT     = BASE


# ── image loader ─────────────────────────────────────────────────────────────
def b64(path):
    p = pathlib.Path(path)
    if not p.exists():
        print(f"  MISSING  {p.name}", file=sys.stderr)
        return ""
    ext  = p.suffix.lower().lstrip(".")
    mime = {"png":"image/png","jpg":"image/jpeg","jpeg":"image/jpeg",
            "webp":"image/webp"}.get(ext, "image/png")
    data = base64.b64encode(p.read_bytes()).decode()
    print(f"  OK  {p.name}  ({len(data)//1024} KB)")
    return f"data:{mime};base64,{data}"


LOGOS    = BRAND / "NeuroneSCF"

print("── Loading images ──────────────────────────────────────────")
logo_w   = b64(LOGOS / "NSCF_Logo_WT_TC.png")   # white + alpha → dark backgrounds
logo_cy  = b64(LOGOS / "NSCF_Logo_CY_TC.png")   # color + alpha → light backgrounds
tinte    = b64(PROD  / "NCOLOR.png")
shampoo  = b64(ALPHA / "HUMIT_SH_1L_alpha.png")
mask     = b64(ALPHA / "humitmask_400_web_alpha.png")
kerasin  = b64(ALPHA / "kerasinsh_400_web_alpha.png")
dyfensor = b64(ALPHA / "dyfensorsh_400_web_alpha.png")
liso     = b64(PROD  / "NTLISOTH-1-1.png")


# ── QR code (WhatsApp https://wa.me/13057489101) ─────────────────────────────
def make_qr():
    try:
        import qrcode
        from PIL import Image as PILImage
        qr = qrcode.QRCode(
            version=3,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=3,
            border=2,
        )
        qr.add_data("https://wa.me/13057489101")
        qr.make(fit=True)
        img = qr.make_image(fill_color="#0A0D14", back_color="#F2EDE4")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        data = base64.b64encode(buf.getvalue()).decode()
        print("  OK  QR code generated")
        return f"data:image/png;base64,{data}"
    except Exception as e:
        print(f"  SKIP QR ({e})")
        return ""

qr_uri = make_qr()


# ── helpers ──────────────────────────────────────────────────────────────────
def img_tag(src, style):
    if not src: return ""
    return f'<img src="{src}" style="{style}" alt="">'

def badge(text, extra=""):
    return (f'<span style="display:inline-block;background:#EFE5D0;color:#6B4E1A;'
            f'border:1px solid #C9A55A;font-size:6px;padding:2px 5px;border-radius:20px;'
            f'margin:1px 1px 0 0;font-weight:700;text-transform:uppercase;'
            f'letter-spacing:.4px;{extra}">{text}</span>')

def item(main, sub="", is_flagship=False):
    col = "#B8892A" if is_flagship else "#C9A55A"
    return (
        f'<div style="display:flex;align-items:flex-start;gap:5px;'
        f'padding-bottom:4px;">'
        f'<div style="width:5px;height:5px;min-width:5px;background:{col};'
        f'border-radius:1px;margin-top:3px;"></div>'
        f'<div><div style="font-size:8.5px;font-weight:700;color:#0A0D14;'
        f'line-height:1.2;">{main}</div>'
        + (f'<div style="font-size:6.5px;color:#666;line-height:1.3;">{sub}</div>' if sub else "")
        + f'</div></div>'
    )

def stacked_imgs(*srcs, h=44, dark=False):
    """Return a vertical stack of images in a side panel."""
    imgs = [s for s in srcs if s]
    if not imgs: return ""
    bg = "#0A0D14" if dark else "#FAFAF8"
    border_col = "#3d4455" if dark else "#C9A55A"
    tags = "".join(
        f'<div style="border:1px solid {border_col};margin-bottom:4px;">'
        f'<img src="{s}" style="display:block;width:72px;max-height:{h}px;'
        f'object-fit:contain;"></div>'
        for s in imgs
    )
    return (
        f'<div style="width:80px;min-width:80px;background:{bg}!important;'
        f'border-left:1px solid rgba(201,165,90,.22);'
        f'padding:8px 4px;display:flex;flex-direction:column;'
        f'align-items:center;justify-content:center;">'
        f'{tags}</div>'
    )

def price_card(price, name, sub, img_uri):
    img_html = (
        f'<div style="width:42px;min-width:42px;height:42px;'
        f'background:#EFE5D0!important;border:1px solid #C9A55A;'
        f'display:flex;align-items:center;justify-content:center;">'
        + (f'<img src="{img_uri}" style="max-width:38px;max-height:38px;object-fit:contain;">'
           if img_uri else "")
        + f'</div>'
    )
    return (
        f'<div style="border:1px solid #C9A55A;overflow:hidden;">'
        f'<div style="background:#B8892A!important;padding:5px 8px;">'
        f'<span style="font-family:\'Arial Black\',Arial,sans-serif;font-size:16px;'
        f'font-weight:900;color:#0A0D14;">{price}</span>'
        f'</div>'
        f'<div style="display:flex;align-items:center;gap:6px;'
        f'padding:7px 8px;background:#F2EDE4!important;">'
        f'<div style="flex:1;">'
        f'<div style="font-size:8.5px;font-weight:700;color:#0A0D14;">{name}</div>'
        f'<div style="font-size:6px;color:#666;margin-top:1px;">{sub}</div>'
        f'</div>'
        f'{img_html}'
        f'</div></div>'
    )

def wa_card(qr):
    qr_html = (
        f'<img src="{qr}" style="display:block;width:52px;height:52px;'
        f'image-rendering:pixelated;border:2px solid #F2EDE4;">'
        if qr else
        '<div style="width:52px;height:52px;border:2px solid #B8892A;'
        'display:flex;align-items:center;justify-content:center;">'
        '<span style="font-size:7px;color:#B8892A;text-align:center;'
        'font-weight:700;">WA<br>QR</span></div>'
    )
    return (
        f'<div style="border:1px solid #C9A55A;overflow:hidden;">'
        f'<div style="background:#B8892A!important;padding:5px 8px;">'
        f'<span style="font-family:\'Arial Black\',Arial,sans-serif;font-size:13px;'
        f'font-weight:900;color:#0A0D14;letter-spacing:.5px;">ORDER NOW</span>'
        f'</div>'
        f'<div style="display:flex;align-items:center;gap:8px;'
        f'padding:8px;background:#0A0D14!important;">'
        f'<div style="flex:1;">'
        f'<div style="font-size:8.5px;font-weight:700;color:#F8FAFB;">WhatsApp · Patricia</div>'
        f'<div style="font-size:10px;font-weight:900;color:#B8892A;margin:2px 0;">+1 (305) 748-9101</div>'
        f'<div style="font-size:6px;color:#9ca3af;margin-top:3px;">Scan to chat on WhatsApp</div>'
        f'</div>'
        f'{qr_html}'
        f'</div></div>'
    )


# ── CSS ──────────────────────────────────────────────────────────────────────
CSS = """
*{margin:0;padding:0;box-sizing:border-box;}
@page{size:8.5in 14in;margin:0;}
@media print{
  *{-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important;}
  body{background:#F2EDE4!important;}
}
body{
  width:215.9mm;
  background:#F2EDE4;
  font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;
  -webkit-print-color-adjust:exact;
  print-color-adjust:exact;
  font-size:10px;
}

/* HEADER */
.hdr{background:#0A0D14!important;padding:18px 24px;
     display:flex;justify-content:space-between;align-items:center;}
.hl{display:flex;flex-direction:column;gap:5px;}
.hr{display:flex;flex-direction:column;align-items:flex-end;gap:4px;}
.bpro{border:1px solid #B8892A;color:#B8892A;padding:3px 9px;
      font-size:7.5px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;}
.hlnch{font-size:7.5px;color:rgba(255,255,255,.3);}

/* GOLD BAR */
.gbar{background:#B8892A!important;padding:8px 24px;
      display:flex;justify-content:space-between;align-items:center;}
.gtl{font-style:italic;color:#0A0D14;font-size:12px;
     font-family:Georgia,'Times New Roman',serif;}
.bship{background:#FFFFFF!important;color:#B8892A;font-size:8px;font-weight:700;
       padding:4px 11px;white-space:nowrap;border:1px solid #B8892A;}

/* KITS GRID 2×2 */
.kg{padding:11px 14px 0;display:grid;grid-template-columns:1fr 1fr;gap:10px;}

/* each kit card */
.kc{display:flex;flex-direction:column;background:#FFFFFF!important;
    border:1.5px solid #C9A55A;overflow:hidden;}
.kc.fl{border:2px solid #B8892A;border-top:4px solid #B8892A;}

/* strip */
.strip{background:#B8892A!important;color:#0A0D14;
       font-size:7px;font-weight:900;letter-spacing:1.5px;text-transform:uppercase;
       text-align:center;padding:4px 0;}

/* kit header */
.kh{background:#B8892A!important;padding:10px 14px;
    display:flex;justify-content:space-between;align-items:flex-start;gap:8px;}
.khl{flex:1;}
.kl{font-size:6px;font-weight:700;letter-spacing:3px;
    color:rgba(255,255,255,.85);text-transform:uppercase;margin-bottom:3px;}
.kn{font-size:21px;font-weight:600;color:#FFFFFF;line-height:1.08;
    font-family:Georgia,'Times New Roman',serif;}
.khr{text-align:right;flex-shrink:0;}
.kp{font-family:'Arial Black',Arial,sans-serif;font-size:35px;
    font-weight:900;color:#0A0D14;line-height:1;}
.kbship{display:inline-block;background:#0A0D14!important;color:#D4A84B;
        font-size:7px;font-weight:700;padding:3px 7px;
        letter-spacing:.5px;margin-top:4px;}

/* kit body */
.kb{display:flex;flex:1;}
.kitems{flex:1;padding:9px 13px 9px;display:flex;flex-direction:column;}
.kimgs-light{width:80px;min-width:80px;background:#FAFAF8!important;
  border-left:1px solid rgba(201,165,90,.22);
  padding:8px 4px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;}
.kimgs-dark{width:80px;min-width:80px;background:#0A0D14!important;
  border-left:1px solid rgba(201,165,90,.22);
  padding:8px 4px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:4px;}
.kimg-wrap{border:1px solid #C9A55A;margin-bottom:4px;
           display:flex;align-items:center;justify-content:center;}
.kimg-wrap-dark{border:1px solid #3d4455;margin-bottom:4px;}
.kft{background:#F8F3EB!important;border-top:1px solid #C9A55A;padding:7px 14px;}
.kftag{font-size:8px;font-style:italic;
       font-family:Georgia,'Times New Roman',serif;color:#6B4E1A;}

/* divider */
.divider{height:1px;background:#C9A55A;margin:8px 14px;}

/* individual pricing */
.pricing{background:#DDD5C8!important;padding:10px 14px 12px;}
.plabel{font-size:6.5px;font-weight:700;color:#6B5A3E;
        text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;}
.pgrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;}

/* order note */
.onote{margin:8px 14px 10px;padding:9px 13px;
       border-left:3px solid #B8892A;background:#E8DFCC!important;}
.onote p{font-size:7.5px;color:#4A3A28;line-height:1.55;}

/* footer */
.ftr{background:#0A0D14!important;padding:10px 24px;
     display:flex;justify-content:space-between;align-items:center;}
.fb{font-size:10px;font-weight:700;letter-spacing:3px;
    color:#F8FAFB;text-transform:uppercase;}
.fc{display:flex;flex-direction:column;align-items:center;gap:2px;
    font-size:7.5px;color:#9ca3af;}
.fw{display:flex;flex-direction:column;align-items:flex-end;gap:2px;
    font-size:7.5px;color:#9ca3af;}
"""


# ── KIT CARDS ────────────────────────────────────────────────────────────────
def kita():
    items_html = (
        item("12 Neurone Color Tubes (90ml)", "Shade selection yours · Pro Salón")
      + item("Neuroactive Developer 1L", "VOL: 10 · 20 · 30 · 40")
      + f'<div style="margin-top:6px;line-height:1.8;">'
      + badge("Quinoa Protein")
      + badge("Nano Tribology")
      + badge("Formula 1+1½")
      + badge("Ammonia-Free")
      + f'</div>'
    )
    img_html = ""
    if tinte:
        img_html += (f'<div class="kimg-wrap">'
                     f'<img src="{tinte}" style="width:70px;max-height:46px;object-fit:contain;"></div>')
    if shampoo:
        img_html += (f'<div class="kimg-wrap" style="opacity:.18;">'
                     f'<img src="{shampoo}" style="width:70px;max-height:46px;object-fit:contain;"></div>')

    return f"""
<div class="kc" style="border-top:4px solid #C9A55A;">
  <div class="kh">
    <div class="khl">
      <div class="kl">KIT A · COLOR STARTER</div>
      <div class="kn">Color<br>Starter</div>
    </div>
    <div class="khr">
      <div class="kp">$99</div>
      <div class="kbship">✦ FREE SHIPPING</div>
    </div>
  </div>
  <div class="kb">
    <div class="kitems">{items_html}</div>
    <div class="kimgs-light">{img_html}</div>
  </div>
  <div class="kft"><span class="kftag">Start the system — zero risk</span></div>
</div>"""


def kitb():
    items_html = (
        item("12 Neurone Color Tubes (90ml)", "Shade selection yours", True)
      + item("Neuroactive Developer 1L", "VOL to choose", True)
      + item("2 Professional Shampoos 1L", "Total Violet + Depura (or choose)", True)
      + item("Humit Mask 1L", "High Moisturizing · Dry &amp; Damaged Hair", True)
    )
    img_html = ""
    for src in [tinte, shampoo, mask]:
        if src:
            img_html += (f'<div class="kimg-wrap">'
                         f'<img src="{src}" style="width:70px;max-height:44px;object-fit:contain;"></div>')

    return f"""
<div class="kc fl">
  <div class="strip">★ MOST POPULAR · RECOMMENDED ★</div>
  <div class="kh">
    <div class="khl">
      <div class="kl">KIT B · SALON SYSTEM</div>
      <div class="kn">Salon<br>System</div>
    </div>
    <div class="khr">
      <div class="kp">$169</div>
      <div class="kbship">✦ FREE SHIPPING</div>
    </div>
  </div>
  <div class="kb">
    <div class="kitems">{items_html}</div>
    <div class="kimgs-light">{img_html}</div>
  </div>
  <div class="kft"><span class="kftag">Everything your salon needs — one order</span></div>
</div>"""


def kitc():
    items_html = (
        item("24 Neurone Color Tubes (90ml)", "Shade selection yours")
      + item("2× Neuroactive Developer 1L", "VOL to choose")
      + item("2 Professional Shampoos 1L", "Choose your line")
      + item("Humit Mask 1L", "Professional deep treatment")
      + f'<div style="margin-top:6px;line-height:1.8;">'
      + badge("Monthly Reorder")
      + badge("Best Value")
      + badge("28-Unit Batch")
      + f'</div>'
    )
    img_html = ""
    for src in [tinte, shampoo, mask]:
        if src:
            img_html += (f'<div class="kimg-wrap">'
                         f'<img src="{src}" style="width:70px;max-height:44px;object-fit:contain;"></div>')

    return f"""
<div class="kc" style="border-top:4px solid #C9A55A;">
  <div class="kh">
    <div class="khl">
      <div class="kl">KIT C · COLOR PRO</div>
      <div class="kn">Color<br>Pro</div>
    </div>
    <div class="khr">
      <div class="kp">$229</div>
      <div class="kbship">✦ FREE SHIPPING</div>
    </div>
  </div>
  <div class="kb">
    <div class="kitems">{items_html}</div>
    <div class="kimgs-light">{img_html}</div>
  </div>
  <div class="kft"><span class="kftag">For the salon that&apos;s ready to commit</span></div>
</div>"""


def kitd():
    items_html = (
        item("Dyfensor Sulfate-Free Shampoo 1L", "Color Rescue · Protección del Color", True)
      + item("Extends color vibrancy up to 40%", "Locks in dye · reduces fade", True)
      + item("No minimum — add to any kit", "Recommend after every color service", True)
      + f'<div style="margin-top:6px;line-height:1.8;">'
      + badge("Sulfate-Free")
      + badge("Color-Safe")
      + badge("pH Balanced")
      + badge("Paraben-Free")
      + f'</div>'
    )
    # dark images panel + save block
    dyf_img = (
        f'<div class="kimg-wrap-dark">'
        f'<img src="{dyfensor}" style="width:70px;max-height:52px;object-fit:contain;">'
        f'</div>'
        if dyfensor else ""
    )
    save_block = (
        f'<div style="background:#B8892A!important;padding:5px 4px;text-align:center;margin-top:2px;">'
        f'<div style="font-family:\'Arial Black\',Arial,sans-serif;font-size:13px;'
        f'font-weight:900;color:#0A0D14;line-height:1;">Save $16</div>'
        f'<div style="font-size:7px;color:#0A0D14;font-weight:700;">vs retail</div>'
        f'</div>'
    )

    # Header price: retail crossed + promo
    price_html = f"""
      <div style="text-align:right;">
        <div style="font-size:9px;color:rgba(0,0,0,.5);
             text-decoration:line-through;font-weight:600;">$49.99</div>
        <div class="kp" style="font-size:32px;">$33.99</div>
        <div class="kbship">WITH ANY KIT</div>
      </div>"""

    return f"""
<div class="kc fl">
  <div class="strip">✦ SPECIAL ADD-ON · SAVE $16 VS. RETAIL ✦</div>
  <div class="kh">
    <div class="khl">
      <div class="kl">DYFENSOR SPECIAL</div>
      <div class="kn">Sulfate-Free<br>Upgrade</div>
    </div>
    {price_html}
  </div>
  <div class="kb">
    <div class="kitems">{items_html}</div>
    <div class="kimgs-dark">{dyf_img}{save_block}</div>
  </div>
  <div class="kft"><span class="kftag">For your color-treated clients — their most loyal visit</span></div>
</div>"""


# ── FULL HTML ─────────────────────────────────────────────────────────────────
# Header: white logo on dark bg
logo_hdr = (
    f'<img src="{logo_w}" style="height:44px;" alt="Neurone South &amp; Central FL">'
    if logo_w else
    f'<img src="{logo_cy}" style="height:44px;filter:brightness(10);" alt="Neurone South &amp; Central FL">'
    if logo_cy else
    '<span style="font-size:16px;font-weight:700;letter-spacing:1px;color:#F8FAFB;">NEURONE<br>'
    '<span style="font-size:9px;color:#B8892A;letter-spacing:3px;">SOUTH &amp; CENTRAL FL</span></span>'
)
# Footer: white logo, smaller
logo_ftr = (
    f'<img src="{logo_w}" style="height:30px;opacity:.9;" alt="Neurone South &amp; Central FL">'
    if logo_w else
    f'<img src="{logo_cy}" style="height:30px;filter:brightness(10);opacity:.9;" alt="">'
    if logo_cy else ''
)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>{CSS}</style>
</head>
<body>

<!-- HEADER -->
<div class="hdr">
  <div class="hl">
    {logo_hdr}
  </div>
  <div class="hr">
    <span class="bpro">Professional Channel</span>
    <span class="hlnch">Florida · Launch Pricing · 2026</span>
  </div>
</div>

<!-- GOLD BAR -->
<div class="gbar">
  <span class="gtl">Laboratory-grade professional haircare — delivered to your salon.</span>
  <span class="bship">✦ FREE SHIPPING ON ALL KITS</span>
</div>

<!-- KITS 2×2 -->
<div class="kg">
  {kita()}
  {kitb()}
  {kitc()}
  {kitd()}
</div>

<!-- DIVIDER -->
<div class="divider"></div>

<!-- INDIVIDUAL PRICING -->
<div class="pricing">
  <div class="plabel">Individual Pricing</div>
  <div class="pgrid">
    {price_card("$8.99",  "Neurone Color Tube",   "90ml · min.12 tubes", tinte)}
    {price_card("$28.99", "Professional Shampoo", "1L · MOISTURE C", shampoo)}
    {price_card("$34.99", "Humit Mask",           "1L · Pro-Hydration", mask)}
    {price_card("$35.99", "Lisothermic",          "1L · Thermal Protective", liso)}
    {price_card("$39.99", "Kerasin HB Mask",      "1L · Keratin + Hyaluronic + Biotin", kerasin)}
    {wa_card(qr_uri)}
  </div>
</div>

<!-- ORDER NOTE -->
<div class="onote">
  <p><strong>How to order:</strong> Contact Patricia directly via WhatsApp.
  Shade selection confirmed at order time. Delivery within South &amp; Central Florida.
  pro.neuronescflorida.com — Online ordering portal coming soon.</p>
</div>

<!-- FOOTER -->
<div class="ftr">
  <div class="fb">{logo_ftr}</div>
  <div class="fc">
    <span>WhatsApp · Patricia / +1 (305) 748-9101</span>
    <span>hello-pro@neuronescflorida.com</span>
  </div>
  <div class="fw">
    <span style="font-style:italic;">Professional use only</span>
    <span>pro.neuronescflorida.com</span>
  </div>
</div>

</body>
</html>"""


# ── WRITE HTML ────────────────────────────────────────────────────────────────
html_path = OUT / "NSCF_Kit_Pricing_PRINT.html"
html_path.write_text(html, encoding="utf-8")
print(f"\n  Wrote {html_path.name}  ({html_path.stat().st_size // 1024} KB)")


# ── GENERATE PDF WITH PLAYWRIGHT ──────────────────────────────────────────────
pdf_path = str(OUT / "NSCF_Kit_Pricing_PRINT.pdf")
print("\n── Generating PDF with Playwright ──────────────────────────")
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html, wait_until="networkidle")
        page.pdf(
            path=pdf_path,
            width="8.5in",
            height="14in",
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
            print_background=True,
        )
        browser.close()
    size = pathlib.Path(pdf_path).stat().st_size // 1024
    print(f"  Wrote {pathlib.Path(pdf_path).name}  ({size} KB)")
except Exception as e:
    print(f"  Playwright failed ({e}), falling back to Chrome headless…")
    import subprocess
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    subprocess.run([
        chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
        f"--print-to-pdf={pdf_path}",
        "--print-to-pdf-no-header", "--no-pdf-header-footer",
        f"--paper-width=8.5", f"--paper-height=14",
        "--margin-top=0", "--margin-bottom=0",
        "--margin-left=0", "--margin-right=0",
        str(html_path),
    ], check=True)
    print(f"  Chrome fallback OK → {pdf_path}")

print("\n✓ Done.")

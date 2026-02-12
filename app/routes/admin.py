from fastapi import APIRouter, UploadFile, File, Query, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.services.catalog_service import catalog_path
from app.services.key_service import get_key
from app.core.config import settings
from app.db.database import SessionLocal
from app.db.models import Lead

router = APIRouter()

def require_admin(token: str):
    if not settings.admin_token:
        # If not set, treat as insecure dev mode
        return
    if token != settings.admin_token:
        raise HTTPException(status_code=401, detail="Invalid admin token")

def detect_base_url(request: Request) -> str:
    return str(request.base_url).rstrip("/")

@router.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request, bid: str = Query(default="default"), token: str = Query(default="")):
    require_admin(token)
    business_id = (bid or "default").strip()
    base = detect_base_url(request)

    biz_key = get_key(business_id)
    key_q = f"&key={biz_key}" if biz_key else ""

    webhook_url = f"{base}/whatsapp?bid={business_id}{key_q}"
    leads_url = f"{base}/leads?bid={business_id}"

    db: Session = SessionLocal()
    try:
        leads = (
            db.query(Lead)
            .filter(Lead.business_id == business_id)
            .order_by(Lead.updated_at.desc())
            .limit(50)
            .all()
        )
    finally:
        db.close()

    rows = ""
    for l in leads:
        rows += f"""
        <tr>
          <td>{l.id}</td>
          <td>{l.phone}</td>
          <td>{l.status}</td>
          <td style="white-space:pre-wrap; max-width:420px;">{l.last_message}</td>
          <td style="white-space:pre-wrap; max-width:420px;">{l.last_reply}</td>
          <td>{l.updated_at}</td>
        </tr>
        """

    cat_file = catalog_path(business_id)
    cat_exists = "YES" if cat_file.exists() else "NO"

    html = f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Admin - {business_id}</title>
  <style>
    body {{ font-family: -apple-system, system-ui, Arial; margin: 24px; }}
    code {{ background:#f2f2f2; padding:2px 6px; border-radius:6px; }}
    .box {{ border:1px solid #ddd; border-radius:12px; padding:16px; margin-bottom:16px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border:1px solid #ddd; padding:10px; vertical-align: top; }}
    th {{ background:#fafafa; }}
    input[type=text] {{ padding:8px; width: 320px; }}
    button {{ padding:10px 14px; border-radius:10px; border:0; background:#111; color:#fff; cursor:pointer; }}
    .muted {{ color:#555; }}
  </style>
</head>
<body>
  <h2>WhatsApp AI Sales Agent — Admin</h2>

  <div class="box">
    <form method="get" action="/admin">
      <input type="hidden" name="token" value="{token}"/>
      <label><b>Business ID</b></label><br/>
      <input type="text" name="bid" value="{business_id}" />
      <button type="submit">Open</button>
      <div class="muted" style="margin-top:8px;">Catalog file exists: <b>{cat_exists}</b> (data/catalog_{business_id}.csv)</div>
      <div class="muted" style="margin-top:6px;">Business key exists: <b>{"YES" if biz_key else "NO"}</b></div>
    </form>
  </div>

  <div class="box">
    <div><b>Webhook URL (paste into Twilio Sandbox)</b></div>
    <div style="margin-top:8px;"><code>{webhook_url}</code></div>

    <div style="margin-top:14px;"><b>Leads JSON</b></div>
    <div style="margin-top:8px;"><code>{leads_url}</code></div>
  </div>

  <div class="box">
    <div><b>Upload / Replace Catalog CSV for {business_id}</b></div>
    <div class="muted" style="margin-top:6px;">
      CSV headers must be: <code>sku,name,category,price_inr,details</code>
    </div>
    <form method="post" action="/admin/upload?bid={business_id}&token={token}" enctype="multipart/form-data" style="margin-top:10px;">
      <input type="file" name="file" accept=".csv" required />
      <button type="submit">Upload</button>
    </form>
  </div>

  <div class="box">
    <div><b>Latest 50 Leads ({business_id})</b></div>
    <div class="muted" style="margin-top:6px;">Refresh page to update.</div>
    <div style="overflow:auto; margin-top:10px;">
      <table>
        <thead>
          <tr>
            <th>ID</th><th>Phone</th><th>Status</th><th>Last Message</th><th>Last Reply</th><th>Updated</th>
          </tr>
        </thead>
        <tbody>
          {rows if rows else "<tr><td colspan='6'>No leads yet.</td></tr>"}
        </tbody>
      </table>
    </div>
  </div>

</body>
</html>
"""
    return HTMLResponse(content=html)

@router.post("/admin/upload")
async def upload_catalog(bid: str = Query(default="default"), token: str = Query(default=""), file: UploadFile = File(...)):
    require_admin(token)
    business_id = (bid or "default").strip()
    dest = catalog_path(business_id)
    dest.parent.mkdir(parents=True, exist_ok=True)

    content = await file.read()
    dest.write_bytes(content)

    return RedirectResponse(url=f"/admin?bid={business_id}&token={token}", status_code=303)

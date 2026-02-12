from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
      <head>
        <title>WhatsApp AI Sales Agent</title>
        <meta charset="utf-8" />
        <style>
          body { font-family: -apple-system, system-ui, Arial; margin: 40px; max-width: 820px; }
          code { background: #f3f3f3; padding: 2px 6px; border-radius: 6px; }
          a { text-decoration: none; }
          .card { padding: 16px; border: 1px solid #ddd; border-radius: 12px; margin: 12px 0; }
        </style>
      </head>
      <body>
        <h1>WhatsApp AI Sales Agent</h1>
        <p>Status: <b>running</b></p>

        <div class="card">
          <h3>Useful endpoints</h3>
          <ul>
            <li><a href="/health">/health</a></li>
            <li><code>/whatsapp?bid=default&key=defaultkey123</code> (Twilio webhook)</li>
            <li><a href="/admin?bid=default">/admin?bid=default</a> (Admin panel)</li>
            <li><a href="/leads?bid=default">/leads?bid=default</a> (Leads JSON)</li>
            <li><a href="/dbinfo">/dbinfo</a> (DB backend)</li>
            <li><a href="/docs">/docs</a> (API docs)</li>
          </ul>
        </div>

        <div class="card">
          <h3>Quick test</h3>
          <p>POST to <code>/whatsapp</code> with form fields <code>Body</code> and <code>From</code>.</p>
        </div>
      </body>
    </html>
    """

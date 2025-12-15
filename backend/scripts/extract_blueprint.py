"""Extract blueprint from upload response and save to file."""
import sys, json, mimetypes, uuid, urllib.request
from pathlib import Path

path = Path('test-image.png')
url = 'http://127.0.0.1:8000/upload/'

try:
    import requests
    r = requests.post(url, files={'file': open(path,'rb')})
    resp = r.json()
except Exception as e:
    boundary = '----WebKitFormBoundary' + uuid.uuid4().hex
    CRLF = '\r\n'
    parts = []
    parts.append('--' + boundary)
    parts.append(f'Content-Disposition: form-data; name="file"; filename="{path.name}"')
    ctype = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
    parts.append(f'Content-Type: {ctype}')
    parts.append('')
    body_start = CRLF.join(parts).encode() + CRLF.encode()
    body = body_start + path.read_bytes() + CRLF.encode() + ('--' + boundary + '--').encode() + CRLF.encode()
    req = urllib.request.Request(url, data=body)
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    with urllib.request.urlopen(req) as resp_obj:
        resp = json.loads(resp_obj.read().decode())

# Save blueprint to file
with open('improved_bp.json', 'w') as f:
    json.dump(resp['blueprint'], f, indent=2)
print("Saved blueprint to improved_bp.json")

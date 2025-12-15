import sys
from pathlib import Path
path=Path('test-image.png')
if not path.exists():
    print('ERROR: test-image.png not found', file=sys.stderr)
    sys.exit(2)
url='http://127.0.0.1:8000/upload/'
try:
    import requests
    r=requests.post(url, files={'file': open(path,'rb')})
    print(r.status_code)
    print(r.text)
except Exception as e:
    import mimetypes, uuid, urllib.request
    boundary='----WebKitFormBoundary'+uuid.uuid4().hex
    CRLF='\r\n'
    parts=[]
    parts.append('--'+boundary)
    parts.append(f'Content-Disposition: form-data; name="file"; filename="{path.name}"')
    ctype=mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
    parts.append(f'Content-Type: {ctype}')
    parts.append('')
    data = CRLF.join(parts).encode() + CRLF.encode() + path.read_bytes() + CRLF.encode() + ('--'+boundary+'--').encode() + CRLF.encode()
    req=urllib.request.Request(url, data=data)
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    with urllib.request.urlopen(req) as resp:
        print(resp.status)
        print(resp.read().decode())

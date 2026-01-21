from starlette.requests import Request

def get_real_ip(request: Request):
    cf_ip = request.headers.get("CF-Connecting-IP")
    if cf_ip:
        return cf_ip
    
    xff = request.headers.get("X-Forwarded-For")
    if xff:
        first = xff.split(",")[0].strip()
        if first:
            return first
    
    return request.client.host

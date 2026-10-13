from checker import build_url, is_https, retry_check, show_response, check_site, scan_sites, check_headers, retry_check

# Partea 1: apeluri pentru build_url și is_https
print ("Partea 1", build_url("example.com", "login")) 
# Partea 2: apeluri pentru show_response
print ("Partea 2", show_response("https://httpbin.org/get"))
# Partea 3: apeluri pentru check_site
print ("Partea 3", check_site("https://httpbin.org/get"))
# Partea 4: apelul scan_sites()
print ("Partea 4", scan_sites())
# Partea 5: apeluri pentru check_headers
print ("Partea 5", check_headers("https://httpbin.org/get"))
# Partea 6: apeluri pentru retry_check
print ("Partea 6", retry_check("https://httpbin.org/status/200,500", retries=5, delay=1))
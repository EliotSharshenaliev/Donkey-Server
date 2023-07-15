import http.cookies

from requests.cookies import RequestsCookieJar


def cookie_to_dict(cookie: RequestsCookieJar):
    cookie_str = ""
    for key, value in cookie.items():
        cookie_str += "%s=%s;" % (key, value)

    return cookie_str

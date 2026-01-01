# This program is created by Al9912.

def pagination(links):
    next_url = None
    for link in links.split(","):
        if 'rel="next"' in link:
            next_url = link[link.find("<")+1 : link.find(">")]
            break
    return next_url
import os
import re
import requests
import json
yetToCrawl = []
linkstotal = []
Host = ''

def main():
    global yetToCrawl
    global linkstotal
    global Host

    a = input('enter mode: listpage, scrapepage, listhost, scrapehost, quit\n').rstrip()
    if a == 'quit':
        quit()
    if a == 'listpage':
        b = input('Enter url:\n').rstrip()
        req = requests.get(b)
        if req.status_code != 200:
            print('Failure grabbing page\n')
            main()
        else:
            bdy = req.text
            c = pullLinks(bdy)
            for x in c:
                print(x)
            main()

    if a == 'scrapepage':
        b = input('Enter url:\n').rstrip()
        b = b.replace('www.', '')

        sc = input('Gather out of scope links? y/n\n').rstrip()
        if b.startswith('http://'):
            Host = b.split('http://')[1]
            Host = Host.split('/')[0]

        if b.startswith('https://'):
            Host = b.split('https://')[1]
            Host = b.split('/')[0]

        req = requests.get(b)
        if req.status_code != 200:
            print('Failure grabbing page\n')
            main()
        else:
            bdy = req.text
            c = pullLinks(bdy)
            for x in c:
                x = x.replace('www.', '')
                if sc == 'y':
                    if x.endswith('/'):
                        y = x.split('/')
                        pathname = y[len(y) - 2]
                        dl = dlFile(x, os.getcwd() + '/' + pathname)
                        print(dl)
                    else:
                        y = x.split('/')
                        pathname = y[len(y) - 1]
                        dl = dlFile(x, os.getcwd() + '/' + pathname)
                        print(dl)
                elif sc == 'n':
                    if x.startswith('http://'):
                        scHost = x.split('http://')[1]
                        scHost = scHost.split('/')[0]
                    if x.startswith('https://'):
                        scHost = x.split('https://')[1]
                        scHost = scHost.split('/')[0]
                    if Host == scHost:
                        if x.endswith('/'):
                            y = x.split('/')
                            pathname = y[len(y) - 2]
                            dl = dlFile(x, os.getcwd() + '/' + pathname)
                            print(dl)
                        else:
                            y = x.split('/')
                            pathname = y[len(y) - 1]
                            dl = dlFile(x, os.getcwd() + '/' + pathname)
                            print(dl)
                    else:
                        print('skipping(out of scope): ' + x + '\n')
    if a == 'scrapehost':
        b = input('enter URL:\n').rstrip()
        b = b.replace('www.', '')
        if b.startswith('http://'):
            Host = b.split('http://')[1]
            Host = Host.split('/')[0]
        if b.startswith('https://'):
            Host = b.split('https://')[1]
            Host = Host.split('/')[0]
        req = requests.get(b)
        if req.status_code != 200:
            print('Error retrieving...\n')
            main()
        else:
            c = pullLinks(req.text)
            for x in c:
                if x not in yetToCrawl:
                    yetToCrawl.append(x)
            if len(yetToCrawl) > 0:
                ret = recursiveCrawl(Host, True)

    main()


def recursiveCrawl(Host, hostonlytf):
    yetHost = ''
    if len(yetToCrawl) <= 0:
        print('Done.')
        return()

    url = yetToCrawl.pop(0)
    if hostonlytf == True:
        if url.startswith('http://'):
            yetHost = url.split('http://')[1]
            yetHost = yetHost.split('/')[0]
        elif url.startswith('https://'):
            yetHost = url.split('https://')[1]
            yetHost = yetHost.split('/')[0]
        ##set the filename
        filename = ''
        if url.endswith('/'):
            filename = url.split('/')
            filename = filename[len(filename) - 2]
        else:
            filename = url.split('/')
            filename = filename[len(filename) - 1]
        if url.endswith('/') or url.endswith('.htm') or url.endswith('.html') or url.endswith('.php'):
            req = requests.get(url)
            if req.status_code != 200:
                recursiveCrawl(Host, hostonlytf)
            else:
                links = pullLinks(req.text)
                if len(links) > 0:
                    for x in links:
                        if x not in yetToCrawl:
                            yetToCrawl.append(x)
                    recursiveCrawl(Host, hostonlytf)

    else: ##meaning we grab eveerything
        filename = ''
        if url.endswith('/'):
            filename = url.split('/')
            filename = filename[len(filename) -2]
        else:
            filename = url.split('/')
            filename = filename[len(filename) - 1]
        dl = dlFile(url, filename)
        print(dl)
        if len(yetToCrawl) > 0:
            recursiveCrawl(Host, hostonlytf)
        else:
            return('done\n')


def dlFile(link, path):
    req = requests.get(link, stream=True)
    if req.ok:
        with open(path, 'wb') as f:
            f.write(req.content)
        del f
        return('Written to: ' + path)
    else:
        return(req.status_code)

def pullLinks(str):
    linksfound = []
    if str.find('"') > -1 and str.find("'") > -1:
        linksplit = str.split('"')
        linksplit2 = str.split("'")
        for x in linksplit:
            strsplit = x.split('"')[0]
            strsplit = strsplit.replace('u002F', '')
            if strsplit.startswith('https://') or strsplit.startswith('http://'):
                if strsplit not in linksfound:
                    linksfound.append(strsplit)
        for x in linksplit2:
            strsplit = x.split("'")[0]
            if strsplit.startswith('https://') or strsplit.startswith('http://'):
                if strsplit not in linksfound:
                    linksfound.append(strsplit)
    if len(linksfound) > 0:
        return(linksfound)
    elif len(linksfound) == 0:
        return('No links found..\n')

if __name__ == '__main__':
    print('Welcome to the 5pyd3r\n\n')
    main()

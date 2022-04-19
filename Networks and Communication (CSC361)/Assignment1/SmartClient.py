## Name: Vedant Manawat
## VNum: V00904582
## Date: January 29 2021
## CSC361 Assignment1 Spring 2021

import socket
import ssl
import sys
import re

# Using sys to parse the command line to find the URI to connect to 
# Checks to see if URI has "www.", if not then prepend URI with "www."
# Checks to see whether URI is valid, that is, it does not have the form www..twitter.com or www.twitter..com
def parseURIAndPort():
    URI = sys.argv[1]
    if ".." in URI:
        print("Please Enter a Valid URI.")
        sys.exit(1)
    elif "www." not in URI:
        URI = "www." + URI
        return URI
    else:
        return URI

# Parameters: URI, socketObj s and list of final cookies
# Connects to the webserver using socket library, sends a GET request and gives back a response 
# This response is then parsed to check the response header; if returned HTTP/1.0 or HTTP/1.1 with a response code between 1xx-4xx
#  http/1.1 is supported
# The response is then further parsed to get the cookie name, expiry time and domain name and appened to cookieList
# Return yes if protocol is supported and no if its not
def HTTP11Request(URI,s,cookieList):
    message = "GET http://" + URI + "/ HTTP/1.1\r\nHost:" + URI + "\r\n\r\n"
    try:
        s.connect((URI, 80))
    except:
        print("\nCould not establish connection")
        return "no"
    else:
        s.send(message.encode())
        data = s.recv(10000)
        data = data.decode(encoding="utf-8", errors="ignore")
        print(data)

        responseList = data.split("\n")
        responseList = [x.lower() for x in responseList]

        text = responseList[0]
        if re.search("^http/1.0 3", text) or re.search("^http/1.1 2|3", text):
            for i in responseList:
                c = re.search("^set-cookie:",i)
                if c:
                    setCookieText = responseList[responseList.index(i)]
                    tempCookieText = setCookieText.strip("set-cookie:").strip()
                    cookieName = re.split(' |;|=', tempCookieText)
                    if "domain" and "expires" in cookieName:
                        cookieFinal = cookieName[0] + " Expires: " + cookieName[cookieName.index('expires')+1] + " " + cookieName[cookieName.index('expires')+2] + " " + cookieName[cookieName.index('expires')+3] + " " + cookieName[cookieName.index('expires')+4] + " Domain Name: " + cookieName[cookieName.index('domain')+1]
                        cookieList.append(cookieFinal)
                    elif "domain" in cookieName:
                        cookieFinal = cookieName[0] + " Domain Name: " + cookieName[cookieName.index('domain')+1]
                        cookieList.append(cookieFinal)

            return "yes"
        else:
            return "no"


# Parameters: URI
# Connects to the webserver using the TLS_APLN method to check whether http2 is supported
# If the selected_apln_protocol() returns "h2", http2 is supported
# Return yes if protocol is supported and no if its not
def HTTP2Request(URI,s,cookieList):
    message = "GET http://" + URI + "/ HTTP/2.0\r\nHost:" + URI + "\r\n\r\n"
    ctx = ssl.create_default_context()
    ctx.set_alpn_protocols(['h2','http/1.1'])

    conn = ctx.wrap_socket(s, server_hostname=URI)
    try:
        conn.connect((URI, 443))
        temp = conn.selected_alpn_protocol()
    except:
        print("\nCould not establish connection")
        return "no"
    else:
        conn.send(message.encode())
        data = conn.recv(10000)
        data = data.decode(encoding="utf-8", errors="ignore")
        print(data)

        responseList = data.split("\n")
        responseList = [x.lower() for x in responseList]

        text = responseList[0]
        if re.search("^http/1.0 3", text) or re.search("^http/1.1 2|3", text):
            for i in responseList:
                c = re.search("^set-cookie:",i)
                if c:
                    setCookieText = responseList[responseList.index(i)]
                    tempCookieText = setCookieText.strip("set-cookie:").strip()
                    cookieName = re.split(' |;|=', tempCookieText)
                    if "domain" and "expires" in cookieName:
                        cookieFinal = cookieName[0] + " Expires: " + cookieName[cookieName.index('expires')+1] + " " + cookieName[cookieName.index('expires')+2] + " " + cookieName[cookieName.index('expires')+3] + " " + cookieName[cookieName.index('expires')+4] + " Domain Name: " + cookieName[cookieName.index('domain')+1]
                        cookieList.append(cookieFinal)
                    elif "domain" in cookieName:
                        cookieFinal = cookieName[0] + " Domain Name: " + cookieName[cookieName.index('domain')+1]
                        cookieList.append(cookieFinal)
        
    if temp=="h2":
        return "yes"
    else:
        return "no"

# Parameters: URI, socketObj s and list of final cookies
# Connects to the webserver after the socket is wrapped to be able to connect via HTTPS, sends a GET request and gives back a response 
# This response is then parsed to check the response header; if returned HTTP/1.0 or HTTP/1.1 with a response code between 1xx-4xx
#  https is supported
# The response is then further parsed to get the cookie name, expiry time and domain name and appened to cookieList
# Return yes if protocol is supported and no if its not
def HTTPSRequest(URI,s,cookieList):
    message = "GET https://" + URI + "/ HTTP/1.1\r\nHost:" + URI + "\r\n\r\n"
    soc = ssl.wrap_socket(s)
    try:
        soc.connect((URI, 443))
    except:
        print("\nCould not establish connection")
        return "no"
    else:
        soc.send(message.encode())
        data = soc.recv(10000)
        data = data.decode(encoding="utf-8", errors="ignore")
        print(data)

        responseList = data.split("\n")
        responseList = [x.lower() for x in responseList]

        text = responseList[0]
        if re.search("^http/1.0 3", text) or re.search("^http/1.1 2|3", text):
            for i in responseList:
                c = re.search("^set-cookie:",i)
                if c:
                    setCookieText = responseList[responseList.index(i)]
                    tempCookieText = setCookieText.strip("set-cookie:").strip()
                    cookieName = re.split(' |;|=', tempCookieText)
                    if "domain" and "expires" in cookieName:
                        cookieFinal = cookieName[0] + " Expires: " + cookieName[cookieName.index('expires')+1] + " " + cookieName[cookieName.index('expires')+2] + " " + cookieName[cookieName.index('expires')+3] + " " + cookieName[cookieName.index('expires')+4] + " Domain Name: " + cookieName[cookieName.index('domain')+1]
                        cookieList.append(cookieFinal)
                    elif "domain" in cookieName:
                        cookieFinal = cookieName[0] + " Domain Name: " + cookieName[cookieName.index('domain')+1]
                        cookieList.append(cookieFinal)
                        
            return "yes"
        else:
            return "no"

# Main function used to create socketObj's and calling functions for each of the protocols
# Final output printout is also handled by this function
def main():
    URI = parseURIAndPort()
    cookieList = []
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


    print("\n#####################HTTP1.1#####################")
    http11Response = HTTP11Request(URI,s,cookieList)
    
    
    print("\n#####################HTTP2#####################")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    http2Response = HTTP2Request(URI,s,cookieList)
    
    
    print("\n#####################HTTPS#####################")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    httpsResponse = HTTPSRequest(URI,s,cookieList)
    
    s.close()

    print("\n\n\nwebsite: " + URI)
    print("1. Supports HTTPS: " + httpsResponse)
    print("2. Supports http1.1: " + http11Response)
    print("3. Supports http2: " + str(http2Response))
    print("4. List of Cookies: ")
    for i in cookieList:
        print("\tCookie Name: " + i)

if __name__ == "__main__":
    main()
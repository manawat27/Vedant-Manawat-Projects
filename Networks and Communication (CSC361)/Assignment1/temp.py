# import socket
# import ssl
# import sys
import re

# def parseURIAndPort():
#     URI = sys.argv[1]
#     return URI

# def HTTP11Request(URI,s,cookieList):
#     message = "GET http://" + URI + "/index.html HTTP/1.1\n\n"
#     try:
#         s.connect((URI, 80))
#     except:
#         print("Could not establish connection")
#     else:
#         s.send(message.encode())
#         data = s.recv(10000)
#         data = data.decode()
#         print(data)

#         responseList = data.split("\n")
#         responseList = [x.lower() for x in responseList]

#         text = responseList[0]
#         x = re.search("^1|2|3", text)
        
#         for i in responseList:
#             c = re.search("^set-cookie:",i)
#             if c:
#                 cookieList.append(responseList[responseList.index(i)])

#         if x:
#             return "yes"
#         else:
#             return "no"


# def HTTP2Request(URI,s,cookieList):
#     message = "GET http://" + URI + "/index.html HTTP/2\n\n"
#     ctx = ssl.create_default_context()
#     ctx.set_alpn_protocols(['h2','http/1.1'])

#     conn = ctx.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=URI)
#     try:
#         conn.connect((URI, 443))
#         temp = conn.selected_alpn_protocol()
#     except:
#         print("Could not establish connection")
#     else:
#         conn.send(message.encode())
#         data = conn.recv(10000)
#         data = data.decode()
#         print(data)

#         responseList = data.split("\n")
#         responseList = [x.lower() for x in responseList]

#         for i in responseList:
#             c = re.search("^set-cookie:",i)
#             if c:
#                 cookieList.append(responseList[responseList.index(i)])
        
#         if temp=="h2":
#             return "yes"
#         else:
#             return "no"

# def HTTPSRequest(URI,s,cookieList):
#     message = "GET https://" + URI + "/index.html\n\n"
#     soc = ssl.wrap_socket(s)
#     try:
#         soc.connect((URI, 443))
#     except:
#         print("Could not establish connection")
#         sys.exit(1)
#     else:
#         soc.send(message.encode())
#         data = soc.recv(10000)
#         data = data.decode()
#         print(data)

#         responseList = data.split("\n")
#         responseList = [x.lower() for x in responseList]

#         text = responseList[0]
#         x = re.search("^1|2|3", text)
#         print(x)
        
#         for i in responseList:
#             c = re.search("^set-cookie:",i)
#             if c:
#                 cookieList.append(responseList[responseList.index(i)])

#         if x:
#             return "yes"
#         else:
#             return "no"


# def main():
#     URI = parseURIAndPort()
#     cookieList = []
#     s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


#     print("\n*******HTTP1.1***********\n")
#     http11Response = HTTP11Request(URI,s,cookieList)
    
    
#     print("\n*******HTTP2***********\n")
#     s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#     http2Response = HTTP2Request(URI,s,cookieList)
    
    
#     print("\n*********HTTPS*********\n")
#     s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#     httpsResponse = HTTPSRequest(URI,s,cookieList)
    
    
#     s.close()

#     print("website: " + URI)
#     print("1. Supports HTTPS: " + httpsResponse)
#     print("2. Supports http1.1: " + http11Response)
#     print("3. Supports http2: " + http2Response)
#     print("4. List of Cookies: ")
#     for i in cookieList:
#         print("\tcookie name: " + i + "\n")

# if __name__ == "__main__":
#     main()

cookieList = []

text = "set-cookie: session-id=130-4480152-4218623; domain=.amazon.com; expires=sun, 30-jan-2022 00:16:18 gmt; path=/; secure"
textTemp = text.strip("set-cookie:").strip()
print(textTemp)
cookieName = re.split(' |;|=', text)
# print(cookieName)
# print(cookieName[cookieName.index('expires')+1:cookieName.index('gmt')+1])
if "domain" and "expires" in cookieName:
    cookieFinal = cookieName[0] + " Expires: " + cookieName[cookieName.index('expires')+1] + " " + cookieName[cookieName.index('expires')+2] + " " + cookieName[cookieName.index('expires')+3] + " " + cookieName[cookieName.index('expires')+4] + " Domain Name: " + cookieName[cookieName.index('domain')+1]
    cookieList.append(cookieFinal)

# print(cookieList)





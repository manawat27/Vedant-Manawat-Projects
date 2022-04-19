Vedant Manawat V00904582
CSC 361 Assignment1 Spring 2021

### How to run the code 
Run the code with: 
1) python3 SmartClient.py www.example.com 
2) python3 SmartClient.py example.com

When running replace 'www.example.com' with and actual URL, for example, www.uvic.ca or www.google.com

If while running the program the user doesn't add a www. to the URI (example.com), then my implementation will append the URI with a www. before building a connection. 
However, if the web server is actually located at example.com and "www.example.com" gives a redirect code, then the connection will be verified but no cookies will be returned. 

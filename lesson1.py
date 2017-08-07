
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

#HTTPRequestHandler class
class webServerHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        if self.path.endswith("/hello"):
            #Send get status
            self.send_response(200)

            #send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            #send message back to client
            output = ""
            output += "<html><body>"
            output += "<h1>Hello!</h1>"
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            
            #write content as utf-8 data
            #use this if you running at python2
            #self.wfile.write(message)
            #use this if you running python3
            self.wfile.write(bytes(output, "UTF-8"))
            print (output)
            return

        if self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<h1>Hello!</h1>"
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
        
            self.wfile.write(bytes(output, "UTF-8"))
            print (output)
            return

        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> "
            self.wfile.write(bytes(output, "UTF-8"))
            self.wfile.write(messagecontent[0])
            output = ""
            output += "</h1>"
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"

            self.wfile.write(bytes(output, "UTF-8"))
            print (output)

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print ("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()

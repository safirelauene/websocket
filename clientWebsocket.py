#!/usr/bin/python2
import tornado.web
import tornado.websocket
import tornado.ioloop

from tornado.options import define, options, parse_command_line
define("port", default=8887, help="run on the given port", type=int)

chatTexto = "Chat Server Prj BDD"
connections = set()

def clientUDP():
    HOST = '127.0.0.1'
    PORT = 5002
    udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    dest = (HOST, PORT)
    print 'Para sair use CTRL+X\n'
    ##abro o arquivo com a chave
    arq = open('chavesSafirePub.txt','r')
    ##carrego a chave
    txt = ''
    for linha in arq:
       txt = txt + linha
    arq.close()
    #decodifico para o formato expoente e modulo
    pub = rsa.PublicKey.load_pkcs1(txt, format='PEM')

    msg = raw_input()

    #cifro a msg
    msgc = rsa.encrypt(msg,pub)

    while msg <> '\x18':
        msgc = rsa.encrypt(msg,pub)
        udp.sendto(msgc, dest)
    udp.close()

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("chat.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		global connections
		connections.add(self)
		self.write_message(chatTexto)

	def on_message(self, message):
		global chatTexto
		global connections
		chatTexto += "<br>"
		chatTexto += message
		print chatTexto
		for con in connections:
			con.write_message(chatTexto)

	def on_close(self):
		global connections
		connections.remove(self)

app = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/websocket", WebSocketHandler),
])

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    thread_server = Thread(target=clientUDP)
    tornado.ioloop.IOLoop.instance().start()

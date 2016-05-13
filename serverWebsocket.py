import rsa
import socket
import thread
import tornado.web
import tornado.websocket
import tornado.ioloop

from tornado.options import define, options, parse_command_line
define("port", default=8887, help="run on the given port", type=int)

chatTexto = "Chat Server Prj BDD"
connections = set()

def serverUDP():
    HOST1 = ''               # Endereco IP do Servidor
    PORT1 = 5002             # Porta que o Servidor esta
    udp1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    orig = (HOST1, PORT1)
    udp1.bind(orig)
    arq1 = open('chavesSafirePri.txt','r')
    ##carrego a chave
    txt1 = ''
    for linha in arq1:
       txt1 = txt1 + linha
    arq1.close()
    #decodifico para o formato expoente e modulo
    pri1 = rsa.PrivateKey.load_pkcs1(txt1, format='PEM')
    while True:
        msgc1, cliente = udp1.recvfrom(1024)
        msg1 = rsa.decrypt(msgc1,pri1)
        chatTexto += "<br>"
		chatTexto += mesg1
        for con in connections:
            con.send(chatTexto)
    udp.close()

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("serverChat.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		global connections
		connections.add(self)
		self.write_message(chatTexto)

	def on_message(self, message):
		global chatTexto
		global connections


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
    thread_server = Thread(target=serverUDP)
    tornado.ioloop.IOLoop.instance().start()

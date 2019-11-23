import pygame
from pygame.locals import *
import random
import sys
import inspect




#Colores
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)
CAFE = (140, 70, 0)
GRIS = (75, 75, 75)

def cargar_fondo(archivo, ancho, alto):
    imagen=pygame.image.load(archivo).convert()
    imagen_ancho, imagen_alto=imagen.get_size() #Doble return es decir (return ancho, return alto)
    #print (imagen_ancho)
    #print (imagen_alto)
    tabla_fondos=[]
    for fondo_y in range(0, int(imagen_alto/alto)):
        linea=[]
        tabla_fondos.append(linea)
        for fondo_x in range(0, int(imagen_ancho/ancho)):
            cuadro=(fondo_x*ancho, fondo_y*alto, ancho, alto)
            color=imagen.get_at((0,0))
            imagen.set_colorkey(color, RLEACCEL)
            linea.append(imagen.subsurface(cuadro))
    return tabla_fondos
class Opcion:
	ver=False
	def __init__(self, text, pos, menu_font, pantalla):
		self.text=text
		self.pos=pos
		self.menu_font=menu_font
		self.pantalla=pantalla
		self.set_rect()
		self.draw()

	def draw(self):
		self.set_rect()
		self.pantalla.blit(self.rend, self.rect)

	def set_rend(self):
		self.rend=self.menu_font.render(self.text, True, self.get_color())

	def get_color(self):
		if(self.ver):
			return (255, 255, 255)
		else:
			return (100, 100, 100)

	def set_rect(self):
		self.set_rend()
		self.rect=self.rend.get_rect()
		self.rect.topleft=self.pos
class cosa(pygame.sprite.Sprite):
	#Carga de Sprites
	tipoCosa=0
	
	#Lista de elementos con los cuales chocar
	entorno = None
	#perceptor de entorno
	mundo = None
	#si esta o no siendo buscada por una hormiga
	buscada= False
	def __init__(self, tipo, x, y):
		pygame.sprite.Sprite.__init__(self)
		if(tipo==1):#hoja
			self.image = pygame.image.load("resources/sLeaf_40x40.png").convert_alpha()
		elif(tipo==2):#dulce navideño
			self.image = pygame.image.load("resources/candy1.png").convert_alpha()
		elif(tipo==3):#dulce naranja
			self.image = pygame.image.load("resources/candy2.png").convert_alpha()
		elif(tipo==4):#frutita de mora
			self.image = pygame.image.load("resources/fruit.png").convert_alpha()
		
		self.tipoCosa=tipo
		self.rect=self.image.get_rect()
		self.rect.x=55+(int(x/50)-1)*50
		self.rect.y=55+(int(y/50)-1)*50
		print(self.rect.x, self.rect.y)
		self.timeframes=0
	
	def update(self):
				
		bloque_col_list = pygame.sprite.spritecollide(self, self.entorno, False)
		for bloque in bloque_col_list:
			#Si nos movemos a la derecha
			#Ubicar jugador a la izquiera del objeto golpeado
			if(not bloque==self):
				if self.vel_x > 0:
					self.rect.right = bloque.rect.left
				elif self.vel_x < 0:
					#De otra forma nos movemos a la izquierda
					self.rect.left = bloque.rect.right
		
		#Revisamos si chocamos
		bloque_col_list = pygame.sprite.spritecollide(self, self.entorno, False)
		for bloque in bloque_col_list:
			if(not bloque==self):            
				#Reiniciamos posicion basado en el arriba/abajo del objeto
				if self.vel_y > 0:
					self.rect.bottom = bloque.rect.top
				elif self.vel_y < 0:
					self.rect.top = bloque.rect.bottom
			
	def getPosMatriz(self):#posicion de matriz mundo apartir de posición en pantalla
		#print("cosa pixel pos", self.rect.x, self.rect.x)
		posC=int(self.rect.x/50)-1
		posF=int(self.rect.y/50)-1
		return (posF, posC)
	def setPos(self, x, y):#establecer posición en pantalla
		self.rect.x=x
		self.rect.y=y
		

	
	
	
	#def __del__(self):
		# print("Destruido")
		
class hormiga(pygame.sprite.Sprite):
	#Carga de Sprites
	hormigaMovimiento=cargar_fondo("resources/hormiga movimientos.png", 40, 40)
	hormigaMovimientoCargada=cargar_fondo("resources/hormiga movimientos cargada.png", 40, 40)
	vel_y=0
	vel_x=0
	movement=0
	caminado=0
	caminando=0
	cooldown=0
	mundo= None
	cargada=None
	cosaObjetivo=None
	moment=0#1 arriba | 2 derecha | 3 abajo | 4 izquierda
	#Lista de elementos con los cuales chocar
	entorno = None
	modoSoltar=False
	def __init__(self, tipo, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("resources/hormiga alone.png").convert_alpha()
		self.rect=self.image.get_rect()
		self.rect.x=55+(int(x/50)-1)*50
		self.rect.y=55+(int(y/50)-1)*50
		print(self.rect.x, self.rect.y)
		self.timeframes=0
		# Number of move iterations for wait a move to target (problem of bloqueant ants)
		self.limitTargetWait=10
		self.iterationsTargetWait=0
	tiempoMov=0#variable que controla el tiempo de movimiento; el mas rapido es 0
	def update(self):
		#Mover izq/der
		if(self.caminando>=self.tiempoMov):
			self.rect.x += self.vel_x
		
		#Revisar si golpeamos con algo (bloques de colision)
		bloque_col_list = pygame.sprite.spritecollide(self, self.entorno, False)
		for bloque in bloque_col_list:
			#Si nos movemos a la derecha
			#Ubicar jugador a la izquiera del objeto golpeado
			if(not bloque==self):
				if self.vel_x > 0:
					self.rect.right = bloque.rect.left
				elif self.vel_x < 0:
					#De otra forma nos movemos a la izquierda
					self.rect.left = bloque.rect.right
		
                
		#Mover arriba/abajo
		if(self.caminando>=self.tiempoMov):
			self.rect.y += self.vel_y
		
		if(self.caminando>=self.tiempoMov):
			self.caminando=0
			
			self.caminado+=1
		else:
			self.caminando+=1
		#Revisamos si chocamos
		bloque_col_list = pygame.sprite.spritecollide(self, self.entorno, False)
		for bloque in bloque_col_list:
			if(not bloque==self):            
				#Reiniciamos posicion basado en el arriba/abajo del objeto
				if self.vel_y > 0:
					self.rect.bottom = bloque.rect.top
				elif self.vel_y < 0:
					self.rect.top = bloque.rect.bottom
			
			#Detener movimento vertical
			#self.vel_y = 0
		
		if(self.timeframes==0):#control de visual
			self.movement+=1
			if(self.movement<0 or self.movement>2):
				self.movement=0
			if(self.vel_x<0):#Izquierda
				if(self.cargada is None):
					self.image=self.hormigaMovimiento[1][self.movement].convert_alpha()
				else:
					self.image=self.hormigaMovimientoCargada[1][self.movement].convert_alpha()
			if(self.vel_x>=0):#Derecha
				if(self.cargada is None):
					self.image=self.hormigaMovimiento[0][self.movement].convert_alpha()
				else:
					self.image=self.hormigaMovimientoCargada[0][self.movement].convert_alpha()
			if(self.vel_y<0):#Arriba
				if(self.cargada is None):
					self.image=self.hormigaMovimiento[3][self.movement].convert_alpha()
				else:
					self.image=self.hormigaMovimientoCargada[3][self.movement].convert_alpha()
			if(self.vel_y>0):#Abajo
				if(self.cargada is None):
					self.image=self.hormigaMovimiento[2][self.movement].convert_alpha()
				else:
					self.image=self.hormigaMovimientoCargada[2][self.movement].convert_alpha()
			
			#print("aca")
		self.timeframes+=1
		if(self.timeframes>45):#Controla la velocidad visual,e ntre menos mas rápido
			#print("aca")
			self.timeframes=0
		
		# 50 is the number of pixels to move for place in the next cell
		if(self.caminado>50):#cantidad
			self.vel_x = 0
			self.vel_y=0
			# Number of cells moved to start searching for new item (this prevent to take the same dropped item)
			if(self.cooldown<=0):
				if((self.cargada is None) and (self.cosaObjetivo is None) and (not self.modoSoltar)):
					# Get a list of items that can see the ant (around him)
					percepcion=self.percibirCosas()
					if(len(percepcion)>0):
						# take a random from percepcion list 
						percibido=random.randint(0, (len(percepcion)-1))
						percibe=percepcion[percibido]
						# check if perception item are not already will taken for another ant
						if(not percibe.buscada):#asegurar que no esta siendo buscado el objeto por otra hormiga
							# Set item for searching
							percibe.buscada=True
							# Make item target for search by ant
							self.cosaObjetivo=percibe
							print("percibí!", self.cosaObjetivo.getPosMatriz())
					else:
						if(not self.modoSoltar):
							self.moverse()
					#print("aqui")
				# Case when have a target item
				elif(self.cosaObjetivo is not None):
					print("trato de moverme")
					# move to respective rarget
					self.moverseObjetivo()
					if(self.iterationsTargetWait>self.limitTargetWait):
						self.cosaObjetivo.buscada=False
						self.cosaObjetivo=None

					
				elif((self.cargada is not None) and (self.mundo.getPosStatusCosas(self.getPosMatriz()) is None)):
					print("intento soltar")
					self.soltar()
				elif((self.cargada is not None) and (self.mundo.getPosStatusCosas(self.getPosMatriz()) is not None)):
					self.moverse()
				elif(self.modoSoltar):#en caso de modo soltar para terminar el algoritmo
					self.mundo.removeHormiga((self.rect.x, self.rect.y))
			else:
				self.cooldown-=1
				self.moverse()
				
			
			self.caminado=0
			#print("accion:", accion, "posicion:", pos)
		
	#Control de movimiento
	def ir_izq(self):
		self.vel_x = -1
		self.vel_y=0
		self.mundo.moverHormiga(self.getPosMatriz(), "izquierda", self)
	
	def ir_der(self):
		self.vel_x = 1
		self.vel_y=0
		self.mundo.moverHormiga(self.getPosMatriz(), "derecha", self)
	def ir_arr(self):
		self.vel_y = -1
		self.vel_x=0
		self.mundo.moverHormiga(self.getPosMatriz(), "arriba", self)
	
	def ir_aba(self):
		self.vel_y = 1
		self.vel_x=0
		self.mundo.moverHormiga(self.getPosMatriz(), "abajo", self)
		
	def no_mover(self):
		self.vel_x = 0
		self.vel_y = 0
	# Fix visual position for ant respective to logical position
	def fixPos(self):# arrega la posición (en caso de que hayan ligeros descuadres)
		pos=self.getPosMatriz()
		self.rect.x=55+pos[1]*50
		self.rect.y=55+pos[0]*50
		
		
	def moverse(self):
		pos=self.getPosMatriz()
		self.fixPos()
		while True:
			accion=random.randint(1, 5)# Get a random movement
			if(accion==1 and pos[1]>0 and self.percibirHormigas("izquierda")):
				self.ir_izq()
				break
			if(accion==2 and pos[1]<13 and self.percibirHormigas("derecha")):
				self.ir_der()
				break
			if(accion==3 and pos[0]<9 and self.percibirHormigas("abajo")):
				self.ir_aba()
				break
			if(accion==4 and pos[0]>0 and self.percibirHormigas("arriba")):
				self.ir_arr()
				break
			if(accion==5):
				self.no_mover()
				break
	
	def moverseObjetivo(self):
		pos=self.getPosMatriz()
		posCosa=self.cosaObjetivo.getPosMatriz()

		self.fixPos()

		# direction of row and col movement for ant to reach the object
		moverseFila=0
		moverseColumna=0
		
		# Check row move
		if(pos[0]<posCosa[0]):
			moverseFila=1
		elif(pos[0]>posCosa[0]):
			moverseFila=-1
		else:
			moverseFila=0

		# Check col move
		if(pos[1]<posCosa[1]):
			moverseColumna=1
		elif(pos[1]>posCosa[1]):
			moverseColumna=-1
		else:
			moverseColumna=0
		# print(moverseFila, moverseColumna)
		# If required movments are Row and Col
		if((not moverseFila==0) and (not moverseColumna==0)):
			# Reset target wait
			
			# Random action for first move Row or Col
			accion=random.randint(1, 2)
			if(accion==1):
				if(moverseFila==1 and self.percibirHormigas("abajo")):
					self.ir_aba()
					self.iterationsTargetWait=0
					return
				elif(moverseFila==-1 and self.percibirHormigas("arriba")):
					self.ir_arr()
					self.iterationsTargetWait=0
					return
			else:
				if(moverseColumna==1 and self.percibirHormigas("derecha")):
					self.ir_der()
					self.iterationsTargetWait=0
					return
				elif(moverseColumna==-1 and self.percibirHormigas("izquierda")):
					self.ir_izq()
					self.iterationsTargetWait=0
					return
			
		elif(not moverseFila==0):
			# Reset target wait
			self.iterationsTargetWait=0
			if(moverseFila==1 and self.percibirHormigas("abajo")):
				self.ir_aba()
				self.iterationsTargetWait=0
				return
			elif(moverseFila==-1 and self.percibirHormigas("arriba")):
				self.ir_arr()
				self.iterationsTargetWait=0
				return
			# print(self.percibirHormigas("derecha"), self.percibirHormigas("izquierda"))
			# print(self.mundo.mapaCosas)
			# print("---")
			# print(self.mundo.mapaHormigas)
		elif(not moverseColumna==0):
			# Reset target wait
			if(moverseColumna==1 and self.percibirHormigas("derecha")):
				self.ir_der()
				self.iterationsTargetWait=0
				return
			elif(moverseColumna==-1 and self.percibirHormigas("izquierda")):
				self.ir_izq()
				self.iterationsTargetWait=0
				return
			# print(self.percibirHormigas("derecha"), self.percibirHormigas("izquierda"))
			# print(self.mundo.mapaCosas)
			# print("---")
			# print(self.mundo.mapaHormigas)
		
		else:#caso e que esta sobre el objeto
			
			self.recoger()
			print("intento recoger")
			return
		# Stop Movement because is not possible Yet make a movement
		self.no_mover()
		# Sum times target wait
		self.iterationsTargetWait+=1
		return
	# Return Row, Col position index, (Y,X)
	def getPosMatriz(self):
		posC=int(self.rect.x/50)-1
		posF=int(self.rect.y/50)-1
		return (posF, posC)
	# Verify if are not ant on position (possible movements), this grants not double ants on same cell
	def percibirHormigas(self, lado):
		fila, columna=self.getPosMatriz()
		if(lado=="izquierda" and columna>0):
			if(self.mundo.getPosStatusHormigas((self.rect.x-50, self.rect.y)) is None):
				return True
		if(lado=="derecha" and columna<13):
			if(self.mundo.getPosStatusHormigas((self.rect.x+50, self.rect.y)) is None):
				return True
		if(lado=="abajo" and fila<9):
			if(self.mundo.getPosStatusHormigas((self.rect.x, self.rect.y+50)) is None):
				return True
		if(lado=="arriba" and fila>0):
			if(self.mundo.getPosStatusHormigas((self.rect.x, self.rect.y-50)) is None):
				return True
	
	def percibirCosas(self):
		fila, columna=self.getPosMatriz()
		cosas=[]
		#Fila superior
		fila-=1
		columna-=1
		if(fila>=0 and fila<=9 and columna>=0 and columna<=13):
			if(self.mundo.mapaCosas[fila][columna] is not None):
				cosas.append(self.mundo.mapaCosas[fila][columna])
		columna+=1
		if(fila>=0 and fila<=9 and columna>=0 and columna<=13):
			if(self.mundo.mapaCosas[fila][columna] is not None):
				cosas.append(self.mundo.mapaCosas[fila][columna])
		columna+=1
		if(fila>=0 and fila<=9 and columna>=0 and columna<=13):
			if(self.mundo.mapaCosas[fila][columna] is not None):
				cosas.append(self.mundo.mapaCosas[fila][columna])
		
		#Fila intermedio
		fila+=1
		columna-=2
		if(fila>=0 and fila<=9 and columna>=0 and columna<=13):
			if(self.mundo.mapaCosas[fila][columna] is not None):
				cosas.append(self.mundo.mapaCosas[fila][columna])
		columna+=2
		if(fila>=0 and fila<=9 and columna>=0 and columna<=13):
			if(self.mundo.mapaCosas[fila][columna] is not None):
				cosas.append(self.mundo.mapaCosas[fila][columna])
		
		#Fila inferior
		fila+=1
		columna-=2
		if(fila>=0 and fila<=9 and columna>=0 and columna<=13):
			if(self.mundo.mapaCosas[fila][columna] is not None):
				cosas.append(self.mundo.mapaCosas[fila][columna])
		columna+=1
		if(fila>=0 and fila<=9 and columna>=0 and columna<=13):
			if(self.mundo.mapaCosas[fila][columna] is not None):
				cosas.append(self.mundo.mapaCosas[fila][columna])
		columna+=1
		if(fila>=0 and fila<=9 and columna>=0 and columna<=13):
			if(self.mundo.mapaCosas[fila][columna] is not None):
				cosas.append(self.mundo.mapaCosas[fila][columna])
				
		return cosas
	
	## HERE a formule
	def recoger(self):
		# Quantity of number of same objects
		parecidos=0
		listaPercibidos=self.percibirCosas()
		# Get number of same objects from vision range  of perception
		for i in listaPercibidos:
			if(i.tipoCosa==self.cosaObjetivo.tipoCosa):
				parecidos+=1
		
		diferentes=8-parecidos
		valorAlpha=8#maximo de diferentes posibles

		# At more different values, lesser posibility
		valorF=1-(diferentes/valorAlpha)
		# Constant 
		constanteK1=1
		recogerProb=(constanteK1/(constanteK1+valorF))

		suerte=random.uniform(0, 1.0)
		if(recogerProb>=suerte):
			self.cosaObjetivo.buscada=False
			self.cargada=self.cosaObjetivo
			fila, columna=self.cargada.getPosMatriz()
			self.mundo.removeCosa(fila, columna)
			self.cosaObjetivo=None
			self.cooldown=15
			self.iterationsTargetWait=0
		else:
			self.cooldown=10
			self.cosaObjetivo.buscada=False
			self.cosaObjetivo=None
	
	def soltar(self):
		parecidos=0
		listaPercibidos=self.percibirCosas()
		for i in listaPercibidos:
			if(i.tipoCosa==self.cargada.tipoCosa):
				parecidos+=1
		diferentes=8-parecidos
		valorAlpha=8#maximo de diferentes posibles

		valorF=1-(diferentes/valorAlpha)
		constanteK2=0.1
		soltarProb=(valorF/(constanteK2+valorF))

		suerte=random.uniform(0, 1)
		if(soltarProb>=suerte):
			self.cargada.setPos(self.rect.x, self.rect.y)
			self.mundo.addCosa(self.cargada)
			self.cargada=None
			self.cooldown=15
		else:
			self.cooldown=10
	#def __del__(self):
		# print("Destruido")
		
		
class Bloque(pygame.sprite.Sprite):#Buscar operaciones para el ciruculo
	def __init__(self, color, largo, alto, x, y):
		pygame.sprite.Sprite. __init__(self)
		self.image=pygame.Surface([largo, alto])
		self.image.fill(color)
		self.color=color
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
	"""#usando imagen
	def __init__(self, color, archivo):
		pygame.sprite.Sprite. __init__(self)
		self.image=pygame.image.load(archivo).convert_alpha()
		self.rect=self.image.get_rect()
	"""
	def Color(self):
		color=self.image.get_at([0, 0])

	def Dimension(self, alto, ancho):
		self.image=pygame.Surface([ancho, alto])
		self.image.fill(self.color)
		self.rect=self.image.get_rect()

class Mundo():
	mapaHormigas=[[None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None]]#Matriz 14x10
	mapaCosas=[[None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None]]#Matriz 14x10
	def __init__(self, groupHormigas, groupCosas):
		self.hormigas=groupHormigas
		self.cosas=groupCosas
		#self.activos=groupActivos
		
	
	def addHormiga(self, hormiga):
		pos=hormiga.getPosMatriz()
		if(self.mapaHormigas[pos[0]][pos[1]] is None):
			try:
				self.mapaHormigas[pos[0]][pos[1]]=hormiga
				self.hormigas.add(hormiga)
				#self.activos.add(hormiga)
				print("añadida hormiga:", pos)
			except:
				print("Unexpected error:", sys.exc_info(), "line number", inspect.currentframe().f_back.f_lineno)
		else:
			print("ya hay hormiga")
	
	def addCosa(self, cosa):
		pos=cosa.getPosMatriz()
		if(self.mapaCosas[pos[0]][pos[1]] is None):
			try:
				self.mapaCosas[pos[0]][pos[1]]=cosa
				self.cosas.add(cosa)
				#self.activos.add(cosa)
				print("añadida cosa:", pos)
			except:
				print("Unexpected error:", sys.exc_info())
		else:
			print("ya hay cosa")
			
	def removeHormiga(self, pos):
		pos=self.getPosMatriz(pos)
		if(self.mapaHormigas[pos[0]][pos[1]] is not None):
			print(pos)
			hormiga=self.mapaHormigas[pos[0]][pos[1]]
			self.mapaHormigas[pos[0]][pos[1]]=None
			self.hormigas.remove(hormiga)
			#self.activos.remove(hormiga)
			print("borrada hormiga:", pos)
		else:
			print("no hay hormiga para borrar")
	
	def removeCosaPix(self, pos):
		pos=self.getPosMatriz(pos)
		if(self.mapaCosas[pos[0]][pos[1]] is not None):
			print(pos)
			cosa=self.mapaCosas[pos[0]][pos[1]]
			self.mapaCosas[pos[0]][pos[1]]=None
			self.cosas.remove(cosa)
			#self.activos.remove(hormiga)
			print("borrada cosa:", pos)
		else:
			print("no hay cosa para borrar", pos)
	
	def removeCosa(self, fila, columna):
		if(self.mapaCosas[fila][columna] is not None):
			cosa=self.mapaCosas[fila][columna]
			self.mapaCosas[fila][columna]=None
			self.cosas.remove(cosa)
			#self.activos.remove(hormiga)
			print("borrada cosa:", fila, columna)
		else:
			print("no hay cosa para borrar", fila, columna)
			
	def moverHormiga(self, pos, accion, hormiga):
		#print("accion:", accion, "posicion:", pos)
		self.mapaHormigas[pos[0]][pos[1]]=None
		if(accion=="izquierda"):
			self.mapaHormigas[pos[0]][pos[1]-1]=hormiga
		if(accion=="arriba"):
			self.mapaHormigas[pos[0]-1][pos[1]]=hormiga
		if(accion=="derecha"):
			self.mapaHormigas[pos[0]][pos[1]+1]=hormiga
		if(accion=="abajo"):
			self.mapaHormigas[pos[0]+1][pos[1]]=hormiga
	def getPosStatusHormigas(self, pos):
		posC=int(pos[0]/50)-1
		posF=int(pos[1]/50)-1
		return self.mapaHormigas[posF][posC]
	def getPosStatusCosas(self, pos):
		posF, posC=pos
		return self.mapaCosas[posF][posC]
	def getPosMatriz(self, pos):
		posC=int(pos[0]/50)-1
		posF=int(pos[1]/50)-1
		return (posF, posC)
	def soltarModo(self):
		for i in self.hormigas:
			i.modoSoltar=True
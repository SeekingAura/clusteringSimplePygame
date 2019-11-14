import pygame
import sys

LEFT = 1
RIGHT = 3
#Dimensiones de la pantalla
ANCHO = 800
ALTO = 600

if __name__=="__main__":
	pygame.init()
	#Set the height and width of the screen
	tam = [ANCHO, ALTO]
	pantalla = pygame.display.set_mode(tam)
	pygame.display.set_caption("Blanda")
	from libreria import *
	
	
	
	#opciones=[Opcion("NUEVO", (140, 105), pygame.font.Font(None, 40), pantalla), Opcion("CARGAR", (135, 155), pygame.font.Font(None, 40), pantalla), Opcion("OPCIONES", (145, 205), pygame.font.Font(None, 40), pantalla)]
	
	#Listas de sprites
	activosSprites= pygame.sprite.Group()
	hormigasActivos=pygame.sprite.Group()
	cosasActivos=pygame.sprite.Group()
	murosActivos=pygame.sprite.Group()
	mallas=pygame.sprite.Group()
	
	#Creación de murosActivos
	muro=Bloque(GRIS, 800, 48, 0, 0)
	murosActivos.add(muro)
	activosSprites.add(muro)
	
	muro=Bloque(GRIS, 800, 48, 0, 552)
	murosActivos.add(muro)
	activosSprites.add(muro)
	
	muro=Bloque(GRIS, 48, 504, 0, 48)
	murosActivos.add(muro)
	activosSprites.add(muro)
	
	muro=Bloque(GRIS, 48, 504, 752, 48)
	murosActivos.add(muro)
	activosSprites.add(muro)
	
	for i in range(50, 800, 50):#creación de malla
		malla=Bloque(BLANCO, 4, 500, i-2, 50)
		mallas.add(malla)
		#activosSprites.add(malla)
		
		malla=Bloque(BLANCO, 700, 4, 50, i-2)
		mallas.add(malla)
		#activosSprites.add(malla)
	
	Salida=False
	#ejecucion=True
	mousex=0
	mousey=0
	creacion="hormiga"
	world=Mundo(hormigasActivos, cosasActivos)
	#pantalla.fill((0, 0, 0))
	
	while True:
		pantalla.fill((0, 0, 0))
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type==KEYDOWN and event.key == K_ESCAPE:
				print(event.key)
			elif event.type==KEYDOWN and event.key == K_1:
				creacion="hormiga"
			elif event.type==KEYDOWN and event.key == K_2:
				creacion="hoja"
			elif event.type==KEYDOWN and event.key == K_3:
				creacion="caramelo1"
			elif event.type==KEYDOWN and event.key == K_4:
				creacion="caramelo2"
			elif event.type==KEYDOWN and event.key == K_5:
				creacion="fruta"
			elif(event.type==KEYDOWN) and event.key == K_9:
				world.soltarModo()
			
			elif(event.type==MOUSEBUTTONDOWN and event.button == RIGHT):
				mousex, mousey = event.pos
				if(mousex>=50 and mousex<750 and mousey>=50 and mousey<550):
					if(creacion=="hormiga"):
						world.removeHormiga(event.pos)
					else:
						world.removeCosaPix(event.pos)
			elif event.type==MOUSEBUTTONDOWN and event.button == LEFT:
				mousex, mousey = event.pos
				if(mousex>=50 and mousex<750 and mousey>=50 and mousey<550):
					if(creacion=="hormiga"):
						hormigas=hormiga(0, mousex, mousey)
						hormigas.entorno=murosActivos
						hormigas.mundo=world
						world.addHormiga(hormigas)
					if(creacion=="hoja"):
						cosas=cosa(1, mousex, mousey)
						cosas.entorno=murosActivos
						cosas.mundo=world
						world.addCosa(cosas)
					if(creacion=="caramelo1"):
						cosas=cosa(2, mousex, mousey)
						cosas.entorno=murosActivos
						cosas.mundo=world
						world.addCosa(cosas)
					if(creacion=="caramelo2"):
						cosas=cosa(3, mousex, mousey)
						cosas.entorno=murosActivos
						cosas.mundo=world
						world.addCosa(cosas)
					if(creacion=="fruta"):
						cosas=cosa(4, mousex, mousey)
						cosas.entorno=murosActivos
						cosas.mundo=world
						world.addCosa(cosas)
				
		"""	for opcion in opciones:
				if opcion.rect.collidepoint(pygame.mouse.get_pos()) and event.type==MOUSEBUTTONDOWN and event.button == LEFT:
					print (opcion.text)
		for opcion in opciones:
			if opcion.rect.collidepoint(pygame.mouse.get_pos()):
				opcion.ver=True
				#Aqui se llega cuando se asoma el cursor sobre la opción
			else:
				opcion.ver=False
			opcion.draw()
		"""
		#control de hormigas
		for i in hormigasActivos:
			if(i.rect.x>ANCHO+10 or i.rect.x<-10 or i.rect.y>ALTO+10 or i.rect.y<-10):
				activosSprites.remove(i)
				hormigasActivos.remove(i)
				
			
		mallas.update()
		mallas.draw(pantalla)
		cosasActivos.update()
		cosasActivos.draw(pantalla)
		hormigasActivos.update()
		hormigasActivos.draw(pantalla)
		murosActivos.update()
		murosActivos.draw(pantalla)
		#activosSprites.update()
		#activosSprites.draw(pantalla)
		pygame.display.flip()
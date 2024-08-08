import pygame
import random
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy the Bird")

POLE_WIDTH = 70
GAP = 100

BLACK = (0,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)

POLE = pygame.Rect(WIDTH, 0, POLE_WIDTH, HEIGHT)
POLE_GROUP = []


POLE_IMAGE = pygame.image.load(os.path.join("sprites", "pipe-green.png"))
POLE_IMAGE_UP = pygame.transform.rotate(pygame.transform.scale(POLE_IMAGE, (POLE_WIDTH, HEIGHT-GAP-10)), 180)
POLE_IMAGE_DOWN = pygame.transform.scale(POLE_IMAGE, (POLE_WIDTH, HEIGHT-GAP-10))

BACKGROUND_IMAGE = pygame.image.load(os.path.join("sprites", "background-day.png"))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

GAME_OVER_IMAGE = pygame.image.load(os.path.join("sprites", "gameover.png"))

BIRD_IMAGE = [pygame.image.load(os.path.join("sprites", "yellowbird-upflap.png")), pygame.image.load(os.path.join("sprites", "yellowbird-midflap.png")), pygame.image.load(os.path.join("sprites", "yellowbird-downflap.png"))]
BIRD_BODY = [pygame.transform.scale(BIRD_IMAGE[0], (30,20)), pygame.transform.scale(BIRD_IMAGE[1], (30,20)), pygame.transform.scale(BIRD_IMAGE[2], (30,20))]


HIT_AUDIO = pygame.mixer.Sound(os.path.join("audio", "hit.wav"))
SCORE_AUDIO = pygame.mixer.Sound(os.path.join("audio", "point.wav"))
FLAP_AUDIO = pygame.mixer.Sound(os.path.join("audio", "swoosh.wav"))
FLAP_AUDIO.set_volume(0.4)
DIE_AUDIO = pygame.mixer.Sound(os.path.join("audio", "die.wav"))


BIRD = pygame.Rect(WIDTH//2-20, HEIGHT//2-20, 32, 20)
BIRD_HIT = pygame.USEREVENT + 1

VEL = 2
GRAVITY = 6
JUMP = 7
PUSH = 0

LOOP = 0
ROTATE = 0
SCORE = 0

SCORE_FONT = pygame.font.SysFont("comicsans", 25)
END_FONT = pygame.font.SysFont("comicsans", 50)


def die_animation():
	global ROTATE
	DIE_AUDIO.play()
	while BIRD.y <= HEIGHT-30:
		BIRD.y += GRAVITY

		WIN.blit(BACKGROUND, (0,0))
		
		for pole in POLE_GROUP:
			WIN.blit(POLE_IMAGE_UP, (pole.x,-HEIGHT+pole.height+GAP+10))
			WIN.blit(POLE_IMAGE_DOWN, (pole.x,pole.height+GAP))

		WIN.blit(pygame.transform.rotate(BIRD_BODY[1], -ROTATE), (BIRD.x, BIRD.y))
		scoring = SCORE_FONT.render("SCORE: "+str(SCORE), 1, YELLOW)
		WIN.blit(scoring, (10, 10))
		if ROTATE < 90:
			ROTATE += 15
		pygame.display.update()
	

def end_game(end_text):
	HIT_AUDIO.play()
	WIN.blit(GAME_OVER_IMAGE, (WIDTH//2-100, HEIGHT//2))
	pygame.display.update()
	pygame.time.delay(2000)

def handle_poles():
	global SCORE
	for pole in POLE_GROUP:
		pole.x -= VEL
		if pole.x <= -POLE_WIDTH:
			POLE_GROUP.remove(pole)
		if pole.x == WIDTH//2+50:
			POLE_GROUP.append(pygame.Rect(WIDTH, 0, POLE_WIDTH, random.randint(10, HEIGHT-GAP)))
		if BIRD.colliderect(pole) or BIRD.colliderect(pygame.Rect(pole.x, pole.height+GAP, POLE_WIDTH, HEIGHT-pole.height-GAP)):
			pygame.event.post(pygame.event.Event(BIRD_HIT))
		elif pole.x == BIRD.x:
			SCORE_AUDIO.play()
			SCORE += 1

def handle_bird():
	global PUSH, LOOP
	if PUSH  == 0:
		BIRD.y += GRAVITY
	else:
		LOOP += 1
		PUSH-=1
		BIRD.y -= JUMP
	if BIRD.y >= HEIGHT-10 or BIRD.y <= -75:
		pygame.event.post(pygame.event.Event(BIRD_HIT))
	if LOOP == 3:
		LOOP = 0

def draw_window():
	global LOOP
	WIN.blit(BACKGROUND, (0,0))
	
	for pole in POLE_GROUP:
		WIN.blit(POLE_IMAGE_UP, (pole.x,-HEIGHT+pole.height+GAP+10))
		WIN.blit(POLE_IMAGE_DOWN, (pole.x,pole.height+GAP))

	WIN.blit(BIRD_BODY[LOOP], (BIRD.x, BIRD.y))

	scoring = SCORE_FONT.render("SCORE: "+str(SCORE), 1, YELLOW)
	WIN.blit(scoring, (10, 10))
	pygame.display.update()


def main():
	global PUSH
	POLE_GROUP.append(pygame.Rect(WIDTH, 0, POLE_WIDTH, HEIGHT//2-GAP//2))
	run = True
	clock = pygame.time.Clock()
	while run:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				break

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					PUSH = 4
					FLAP_AUDIO.play()
					start = True
			end_text = ""
			if event.type == BIRD_HIT:
				end_text = "GAME OVER"
		if end_text != "":
			die_animation()
			end_game(end_text)
			break
			

		handle_poles()
		handle_bird()
		draw_window()
	pygame.quit()

if __name__ == "__main__":
	pygame.time.delay(5000)
	main()
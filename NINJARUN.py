import msvcrt #for getting keyboard pressed button
import os #to clear screen
from time import sleep #for frame per second





#some initial variables
ENEMIES_KILLED=0
LIVES_LEFT=3

WON=False
import pygame
pygame.init()
pygame.mixer.music.load('C:\\Users\\acer\\Desktop\\ninjamusic.mp3')
pygame.mixer.music.play(-1)


MAX_WORLD_WIDTH=80-1
MAX_WORLD_HEIGHT=25

HATTORI_LOCATION_X=0
HATTORI_LOCATION_Y=0
HATTORI_ALIVE = True
HATTORI_CAN_DOUBLE_JUMP = True
HATTORI_JUMPED_ONCE = True

ENEMY_LOCATION_X=0
ENEMY_LOCATION_Y=0
ENEMY_SHOULD_MOVE_TO_RIGHT=False

LAST_PRESSED_KEY=b''

CHARACTER_HATTORI_REPLACED=''


WORLD_MAP=list()

#load file into variable
def prepare_world():
    global WORLD_MAP
    with open('1-1.txt') as f:
        WORLD_MAP = f.read().splitlines()
        
        
prepare_world()


WORLD_MAP_WIDTH=0
WORLD_MAP_HEIGHT=0


HATTORI_SPRITE=[
" ▄████▄▄",
"▄▀█▀▐└─┐",
"█▄▐▌▄█▄┘",
"└▄▄▄▄▄┘ ",
"██▒█▒██ ",
]

HATTORI_SPRITE_WIDTH=len(HATTORI_SPRITE[0])
HATTORI_SPRITE_HEIGHT=len(HATTORI_SPRITE)

ENEMY_SPRITE=[
"  ▓▓▓   ",
" ▓▒▓▒▓  ",
"▓▓▓▓▓▓▓ ",
" █████  ",
"▒▒███▒▒▒"
]

ENEMY_SPRITE_WIDTH=len(ENEMY_SPRITE[0])
ENEMY_SPRITE_HEIGHT=len(ENEMY_SPRITE)

AREA_HATTORI_REPLACED=list()
AREA_ENEMY_REPLACED=list()


#prints world into cmd
def print_world(world):
    for line in world:

        camera_trigger_index=20
        if HATTORI_LOCATION_X >camera_trigger_index:
            print(line[HATTORI_LOCATION_X-camera_trigger_index:HATTORI_LOCATION_X + (MAX_WORLD_WIDTH-camera_trigger_index)])
        else:
            print(line[:MAX_WORLD_WIDTH])

#prints HUD
def print_hud():
    print ((" "*3)+"Enemies killed: "+str(ENEMIES_KILLED)+(" "*15)+"[1;40;31mH[40;32mA[40;33mT[40;34mT[40;35mO[40;36mR[40;31mI [40;32mC[40;33mO[40;34mN[40;35mS[40;36mO[40;37mL[40;38mE[40;39m"+(" "*15)+"Lives left: "+str(LIVES_LEFT))
         
#cleans screen and prints world           
def refresh_screen():
    global ENEMIES_KILLED
    global LIVES_LEFT
    
    print_hud()
    
    print_world(WORLD_MAP)
    os.system('cls')

#checks if world is properly formated
def check_the_world():
    global WORLD_MAP_WIDTH
    global WORLD_MAP_HEIGHT

    
    for i in range(1,len(WORLD_MAP)):
        #check if all lines are the same size
        
        if(len(WORLD_MAP[i]) != len(WORLD_MAP[i-1])):
            print("Line size not equal at line:",i,"and",i-1)
            
    WORLD_MAP_WIDTH=len(WORLD_MAP[0])
    WORLD_MAP_HEIGHT=len(WORLD_MAP)


#creates HATTORI in a world, using x and y coordinates
def create_2d_HATTORI(x,y):
    global HATTORI_LOCATION_X
    global HATTORI_LOCATION_Y
    global AREA_HATTORI_REPLACED

    

    for i in range(HATTORI_SPRITE_HEIGHT):
        AREA_HATTORI_REPLACED.append(WORLD_MAP[y-i][x-HATTORI_SPRITE_WIDTH:x])

        WORLD_MAP[y-i]=WORLD_MAP[y-i][:x-HATTORI_SPRITE_WIDTH]+ HATTORI_SPRITE[HATTORI_SPRITE_HEIGHT-i-1] +WORLD_MAP[y-i][x:]

    
    HATTORI_LOCATION_X=x
    HATTORI_LOCATION_Y=y

#creates enemy in a world, using x and y coordinates
def create_2d_enemy(x,y):
    global ENEMY_LOCATION_X
    global ENEMY_LOCATION_Y
    global AREA_ENEMY_REPLACED

    

    for i in range(ENEMY_SPRITE_HEIGHT):
        AREA_ENEMY_REPLACED.append(WORLD_MAP[y-i][x-ENEMY_SPRITE_WIDTH:x])

        WORLD_MAP[y-i]=WORLD_MAP[y-i][:x-ENEMY_SPRITE_WIDTH]+ ENEMY_SPRITE[ENEMY_SPRITE_HEIGHT-i-1] +WORLD_MAP[y-i][x:]

    
    ENEMY_LOCATION_X=x
    ENEMY_LOCATION_Y=y

#deletes HATTORI in a world
def delete_2d_HATTORI():
    global HATTORI_LOCATION_X
    global HATTORI_LOCATION_Y
    global CHARACTER_HATTORI_REPLACED

    for i in range(HATTORI_SPRITE_HEIGHT):
        WORLD_MAP[HATTORI_LOCATION_Y-i]=WORLD_MAP[HATTORI_LOCATION_Y-i][:HATTORI_LOCATION_X-HATTORI_SPRITE_WIDTH]+ AREA_HATTORI_REPLACED[i] +WORLD_MAP[HATTORI_LOCATION_Y-i][HATTORI_LOCATION_X:]

    AREA_HATTORI_REPLACED.clear()
    HATTORI_LOCATION_X=-1
    HATTORI_LOCATION_Y=-1

#deletes enemy in a world
def delete_2d_enemy():
    global ENEMY_LOCATION_X
    global ENEMY_LOCATION_Y
    global CHARACTER_ENEMY_REPLACED

    for i in range(ENEMY_SPRITE_HEIGHT):
        WORLD_MAP[ENEMY_LOCATION_Y-i]=WORLD_MAP[ENEMY_LOCATION_Y-i][:ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH]+ AREA_ENEMY_REPLACED[i] +WORLD_MAP[ENEMY_LOCATION_Y-i][ENEMY_LOCATION_X:]

    AREA_ENEMY_REPLACED.clear()
    ENEMY_LOCATION_X=-1
    ENEMY_LOCATION_Y=-1

#checks if HATTORI can be moved to an x,y coordinates
def can_be_moved_HATTORI(x,y):
    if(((x-HATTORI_SPRITE_WIDTH) >= 0) and (x < WORLD_MAP_WIDTH) and ((y-(HATTORI_SPRITE_HEIGHT-2)) > 0) and (y<WORLD_MAP_HEIGHT-1) ) :
        return True
    return False

#checks if enemy can be moved to an x,y coordinates
def can_be_moved_enemy(x,y):
    if(((x-ENEMY_SPRITE_WIDTH) >= 0) and (x < WORLD_MAP_WIDTH) and ((y-(ENEMY_SPRITE_HEIGHT-2)) > 0) and (y<WORLD_MAP_HEIGHT-1) ) :
        return True
    return False

#moves HATTORI in 2d dimensions
def move_2d_HATTORI(to_x,to_y):
    global HATTORI_LOCATION_X
    global HATTORI_LOCATION_Y
    if(can_be_moved_HATTORI(to_x,to_y)):
        delete_2d_HATTORI()

        #create a new HATTORI
        create_2d_HATTORI(to_x,to_y)
        
        HATTORI_LOCATION_X=to_x
        HATTORI_LOCATION_Y=to_y
        
#moves enemy in 2d dimensions
def move_2d_enemy(to_x,to_y):
    global ENEMY_LOCATION_X
    global ENEMY_LOCATION_Y
    if(can_be_moved_enemy(to_x,to_y)):
        delete_2d_enemy()

        #create a new enemy
        create_2d_enemy(to_x,to_y)
        
        ENEMY_LOCATION_X=to_x
        ENEMY_LOCATION_Y=to_y

def get_char_at(x,y):
    global WORLD_MAP
    return WORLD_MAP[y][x]


#gets characters surrounding HATTORI, it gets these characters from the WORLD_MAP variable   
def get_characters_around_HATTORI():
    global HATTORI_LOCATION_X
    global HATTORI_LOCATION_Y
    global HATTORI_SPRITE_WIDTH
    global HATTORI_SPRITE_HEIGHT
    
    characters_below_HATTORI=list()
    for i in range(HATTORI_LOCATION_X-HATTORI_SPRITE_WIDTH,HATTORI_LOCATION_X):
        characters_below_HATTORI.append(get_char_at(HATTORI_LOCATION_X-HATTORI_SPRITE_WIDTH+(i-(HATTORI_LOCATION_X-HATTORI_SPRITE_WIDTH)),HATTORI_LOCATION_Y+1))
    
    characters_above_HATTORI=list()
    for i in range(HATTORI_LOCATION_X-HATTORI_SPRITE_WIDTH,HATTORI_LOCATION_X):
        characters_above_HATTORI.append(get_char_at(HATTORI_LOCATION_X-HATTORI_SPRITE_WIDTH+(i-(HATTORI_LOCATION_X-HATTORI_SPRITE_WIDTH)),HATTORI_LOCATION_Y-HATTORI_SPRITE_HEIGHT))
    
    characters_left_of_HATTORI=list()
    for i in range(HATTORI_SPRITE_HEIGHT):
        characters_left_of_HATTORI.append(get_char_at(HATTORI_LOCATION_X-HATTORI_SPRITE_WIDTH-1,HATTORI_LOCATION_Y-i))
    
    characters_right_of_HATTORI=list()
    for i in range(HATTORI_SPRITE_HEIGHT):
        characters_right_of_HATTORI.append(get_char_at(HATTORI_LOCATION_X,HATTORI_LOCATION_Y-i))
    
    return [characters_below_HATTORI,characters_left_of_HATTORI,characters_above_HATTORI,characters_right_of_HATTORI]

	  
#gets characters surrounding HATTORI, it gets these characters from the WORLD_MAP variable   
def get_characters_around_enemy():
    global ENEMY_LOCATION_X
    global ENEMY_LOCATION_Y
    global ENEMY_SPRITE_WIDTH
    global ENEMY_SPRITE_HEIGHT

    characters_below_enemy=list()
    for i in range(ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH,ENEMY_LOCATION_X):
        characters_below_enemy.append(get_char_at(ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH+(i-(ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH)),ENEMY_LOCATION_Y+1))

    characters_above_enemy=list()
    for i in range(ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH,ENEMY_LOCATION_X):
        characters_above_enemy.append(get_char_at(ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH+(i-(ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH)),ENEMY_LOCATION_Y-ENEMY_SPRITE_HEIGHT))

    characters_left_of_enemy=list()
    for i in range(ENEMY_SPRITE_HEIGHT):
        characters_left_of_enemy.append(get_char_at(ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH-1,ENEMY_LOCATION_Y-i))

    characters_right_of_enemy=list()
    for i in range(ENEMY_SPRITE_HEIGHT):
        characters_right_of_enemy.append(get_char_at(ENEMY_LOCATION_X,ENEMY_LOCATION_Y-i))

    return [characters_below_enemy,characters_left_of_enemy,characters_above_enemy,characters_right_of_enemy]

#if HATTORI touched the rigid body		
def is_collided_with_ridgid(char_list):
    for i in range(len(char_list)):
        if char_list[i] == '|':
            return True
    return False
    
	
#this function knows what to do with keys a user press key	
def process_key(key):
    global HATTORI_LOCATION_X
    global HATTORI_LOCATION_Y
    global HATTORI_JUMPED_ONCE
    global HATTORI_CAN_DOUBLE_JUMP
    global LAST_PRESSED_KEY
	
    global ENEMY_LOCATION_X
    global ENEMY_LOCATION_Y


    #left arrow
    if key == b'K':
        for i in range(3):
            if not is_collided_with_ridgid(get_characters_around_HATTORI()[1]):
                move_2d_HATTORI(HATTORI_LOCATION_X-1,HATTORI_LOCATION_Y)
                refresh_screen()
        pass

    #down arrow
    elif key == b'P':
        if not is_collided_with_ridgid(get_characters_around_HATTORI()[0]):
            move_2d_HATTORI(HATTORI_LOCATION_X,HATTORI_LOCATION_Y+1)
        pass
    
    #up arrow
    elif key == b'H':
        if not HATTORI_JUMPED_ONCE or HATTORI_CAN_DOUBLE_JUMP:
            HATTORI_JUMPED_ONCE=True

            HATTORI_CAN_DOUBLE_JUMP=not HATTORI_CAN_DOUBLE_JUMP
                
            for i in range(10):
                if not is_collided_with_ridgid(get_characters_around_HATTORI()[2]):
                    
                    move_2d_HATTORI(HATTORI_LOCATION_X,HATTORI_LOCATION_Y-1)
                refresh_screen()


        pass
    
    #right arrow
    elif key == b'M':
        
        for i in range(6):
            if not is_collided_with_ridgid(get_characters_around_HATTORI()[3]):
                move_2d_HATTORI(HATTORI_LOCATION_X+1,HATTORI_LOCATION_Y)
                refresh_screen()
        pass
    
    LAST_PRESSED_KEY=key


#this function moves the enemy to the left until the enemy collides with a wall,
#in that case it will be moving to the right
def move_enemy_left_and_right():
    global ENEMY_LOCATION_X
    global ENEMY_LOCATION_Y
    global ENEMY_SHOULD_MOVE_TO_RIGHT
    
    if is_collided_with_ridgid(get_characters_around_enemy()[3]):
        ENEMY_SHOULD_MOVE_TO_RIGHT=False
    elif is_collided_with_ridgid(get_characters_around_enemy()[1]):
        ENEMY_SHOULD_MOVE_TO_RIGHT=True
    
    if ENEMY_SHOULD_MOVE_TO_RIGHT:
        move_2d_enemy(ENEMY_LOCATION_X+1,ENEMY_LOCATION_Y)
    else:
        move_2d_enemy(ENEMY_LOCATION_X-1,ENEMY_LOCATION_Y)
        
#if HATTORI collides with enemy on left or right kill HATTORI    
#if HATTORI collides with enemy on top kill enemy    
def deal_with_HATTORI_and_enemy_collisions():
    global ENEMY_LOCATION_X
    global ENEMY_LOCATION_Y
    global ENEMY_SPRITE_WIDTH
    global ENEMY_SPRITE_HEIGHT
    
    global HATTORI_LOCATION_X
    global HATTORI_LOCATION_Y 
    global HATTORI_SPRITE_WIDTH
    global HATTORI_SPRITE_HEIGHT
    
    
    #if HATTORI hit the top of enemy
    if (HATTORI_LOCATION_Y > (ENEMY_LOCATION_Y-ENEMY_SPRITE_HEIGHT)) and (HATTORI_LOCATION_Y < (ENEMY_LOCATION_Y-ENEMY_SPRITE_HEIGHT+2)) and (HATTORI_LOCATION_X >= (ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH)) and ((HATTORI_LOCATION_X <= (ENEMY_LOCATION_X) or (HATTORI_LOCATION_X-HATTORI_SPRITE_WIDTH) <= ENEMY_LOCATION_X)):
        #print("TOP collision detected")
        kill_enemy()
        pass
        
        
    #if side collision is detected
    left_of_enemy_collided_with_HATTORI=(HATTORI_LOCATION_X >= (ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH)) and (HATTORI_LOCATION_X <= (ENEMY_LOCATION_X-ENEMY_SPRITE_WIDTH+2)) and (HATTORI_LOCATION_Y>(ENEMY_LOCATION_Y-ENEMY_SPRITE_HEIGHT))
    right_of_enemy_collided_with_HATTORI=(ENEMY_LOCATION_X > (HATTORI_LOCATION_X-HATTORI_SPRITE_WIDTH)) and ENEMY_LOCATION_X < (HATTORI_LOCATION_X-(HATTORI_SPRITE_WIDTH-2)) and (HATTORI_LOCATION_Y>(ENEMY_LOCATION_Y-ENEMY_SPRITE_HEIGHT))
    
    if left_of_enemy_collided_with_HATTORI or right_of_enemy_collided_with_HATTORI:
        kill_HATTORI()
        #print("SIDE Collision detected")
        pass

#this function kills HATTORI
def kill_HATTORI():
    global HATTORI_ALIVE
    global LIVES_LEFT
    
    HATTORI_ALIVE = False
    LIVES_LEFT=LIVES_LEFT -1
    make_hud()

    pass

#this function kills enemy
def kill_enemy():
    global ENEMY_LOCATION_X
    global ENEMY_LOCATION_Y
    global AREA_ENEMY_REPLACED
    global ENEMY_SHOULD_MOVE_TO_RIGHT
    global ENEMIES_KILLED
    global SHOULD_CREATE_MORE_ENEMIES
    
    ENEMIES_KILLED=ENEMIES_KILLED+1
    ENEMY_SHOULD_MOVE_TO_RIGHT=False

    if HATTORI_LOCATION_X < 400:
        move_2d_enemy(440,18)
        
    elif HATTORI_LOCATION_X > 400 and HATTORI_LOCATION_X < 650:
        move_2d_enemy(700,18)
    
    else:
        delete_2d_enemy()
    
    prepare_world()
    pass


#responsible for printing the HUD, colors are made using ANSI codea
def make_hud():
    print_hud()
    print_world(WORLD_MAP) 

#kills HATTORI if he falls
def deal_with_out_of_bounds_collisions():
    global HATTORI_LOCATION_X
    global HATTORI_LOCATION_Y 
    
    if HATTORI_LOCATION_Y > 18:
        kill_HATTORI()
    
#shows scores
def display_score():
    global ENEMIES_KILLED
    global MAX_WORLD_WIDTH

    print("")
    print(("SCORE: "+str(ENEMIES_KILLED*ENEMIES_KILLED)).center(MAX_WORLD_WIDTH))        

#this is where the magic happens
def main():
    global HATTORI_ALIVE
    global HATTORI_JUMPED_ONCE
    global HATTORI_CAN_DOUBLE_JUMP
    global AREA_HATTORI_REPLACED
    global AREA_ENEMY_REPLACED
    global WON
    

    
    check_the_world()   
    
    create_2d_HATTORI(15,11)
    create_2d_enemy(210,18)
    
    HATTORI_KILLING_LIFTED=False
    
    while True:
        sleep(0.05)#so it is not CPU intensive
        os.system('cls')#to clear cmd
        
        
        if HATTORI_ALIVE:
            move_enemy_left_and_right()
            deal_with_HATTORI_and_enemy_collisions()
            deal_with_out_of_bounds_collisions()
            
            
            if HATTORI_LOCATION_X > 1166 and not WON:
                #if HATTORI passed the flag, he wins
                print("**** CONGRATULATIONS, YOU HAVE SUCCESSFULLY COMPLETED THE LEVEL ****".center(MAX_WORLD_WIDTH))

                WON=True
                
                display_score()
                exit()
                
                
            #this is gravity
            if not is_collided_with_ridgid(get_characters_around_HATTORI()[0]):
                    move_2d_HATTORI(HATTORI_LOCATION_X,HATTORI_LOCATION_Y+1)
            else:
                HATTORI_CAN_DOUBLE_JUMP=False
                HATTORI_JUMPED_ONCE=False
                    
        
                    
            if msvcrt.kbhit():
                process_key(msvcrt.getch())
            
            
        else:
            
            #HATTORI is dead, so play dead animation
            if HATTORI_LOCATION_Y > 10 and not HATTORI_KILLING_LIFTED:
                #lift HATTORI up
                move_2d_HATTORI(HATTORI_LOCATION_X,HATTORI_LOCATION_Y-1)
            elif HATTORI_KILLING_LIFTED:
                #take HATTORI down
                move_2d_HATTORI(HATTORI_LOCATION_X,HATTORI_LOCATION_Y+1)
                
                
                if not can_be_moved_HATTORI(HATTORI_LOCATION_X,HATTORI_LOCATION_Y+1):
                #restart game
                    AREA_HATTORI_REPLACED=list()
                    AREA_ENEMY_REPLACED=list()
                    
                    prepare_world()
                    if LIVES_LEFT > 0:
                        HATTORI_ALIVE=True
                        
                        main()
                    else:
                        break
                
                
                
            elif HATTORI_LOCATION_Y == 10:
                HATTORI_KILLING_LIFTED=True
            

                
            
        
        
        #print(HATTORI_LOCATION_X,HATTORI_LOCATION_Y)
        
        
        make_hud()

    display_score()
    exit()

main()
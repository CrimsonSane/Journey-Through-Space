import random, pygame

import engine, game_objects

PLAYER_SPD = 12
STAR_AMOUNT = 100
PLANET_AMOUNT = 5
GALAXY_AMOUNT = 2

GAME_RESOLUTION=[1200, 900]
FPS = 30

def main():
    g_eng = engine.Game_engine(game_res=GAME_RESOLUTION, current_scene="start scene", fps=FPS)
    
    set_vars(g_eng)
    
    add_scenes(g_eng)
    
    g_eng.add_global_event("play music", "Gaze Upon the Stars")
    running = True
    while running:
        pygame.display.update()
        g_eng.update_current()
        g_eng.draw_current()
        
        running = g_eng.get_running()

def set_vars(g_engine):
    g_engine.add_global_var("game_status", "unloaded") 
    g_engine.add_global_var("player_speed", PLAYER_SPD) 
    g_engine.add_global_var("space_sprite_group", pygame.sprite.Group())
    g_engine.globl_vars["space_sprite_group"].add(get_space_decor(g_engine))
    g_engine.add_global_var("bullet_sprite_group", pygame.sprite.Group())

def add_scenes(g_engine):
    start_scene = engine.Scene()
    g_engine.add_scene("start scene", start_scene)
    g_engine.scenes["start scene"].workspace.append(g_engine.globl_vars["space_sprite_group"])
    g_engine.scenes["start scene"].workspace.append(g_engine.globl_vars["bullet_sprite_group"])

def get_space_decor(g_engine):
    decor = []
        
    for i in range(STAR_AMOUNT):
        decor.append(game_objects.Space_decor_sprite(images=[g_engine.get_image_surf("Assets/Background/Star0.png"), g_engine.get_image_surf("Assets/Background/Star1.png"), g_engine.get_image_surf("Assets/Background/Star2.png"), g_engine.get_image_surf("Assets/Background/Star3.png")], layer="background", pos=[random.randint(0, g_engine.game_res[0]), random.randint(0, g_engine.game_res[1])], angle=random.randint(-360, 360)))
    
    for i in range(PLANET_AMOUNT):
        decor.append(game_objects.Space_decor_sprite(images=[g_engine.get_image_surf("Assets/Background/Planet1.png"), g_engine.get_image_surf("Assets/Background/Planet2.png"), g_engine.get_image_surf("Assets/Background/Planet3.png"), g_engine.get_image_surf("Assets/Background/Planet4.png"), g_engine.get_image_surf("Assets/Background/Planet5.png")], layer="background", pos=[random.randint(0, g_engine.game_res[0]), random.randint(0, g_engine.game_res[1])], angle=random.randint(-360, 360)))
    
    for i in range(GALAXY_AMOUNT):
        decor.append(game_objects.Space_decor_sprite(images=[g_engine.get_image_surf("Assets/Background/Galaxy1.png"), g_engine.get_image_surf("Assets/Background/Galaxy2.png"), g_engine.get_image_surf("Assets/Background/Galaxy3.png")], layer="background", pos=[random.randint(0, g_engine.game_res[0]), random.randint(0, g_engine.game_res[1])], angle=random.randint(-360, 360)))
    return decor

if __name__ == "__main__":
    print("-----------------------------------------------")
    print("""                                                  
       &                                          
                                                  
      @&@&@@&                                     
       %#(@@@@@/                                  
         .%@@@@@@(*#          /#***/,             
            %//./.*((//, ((/,   (  ,/             
             *%/// //./.   .#@@(&/*               
            */(%,  ( .*   ///. %  ./.             
     ,*###,    *#@&@*   /@@@@@@@*                 
  ,#.       &(@%#* ,       %@@@@@#(.              
    *(@,,,,,&@@&&@& #@@(,,,        /*             
                           ##%@@@###&@..          
                                       #%#        
                                          /%@@    
""")
    print("       Journey Through Space Arcade Game       ")
    print("-------------- By Crimson Sane ----------------")
    print()
    print("              Made using Pygame!               ")
    main()
pygame.quit()

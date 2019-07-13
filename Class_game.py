import pygame as pg
import time , random
import sqlite3 as sql


class Race_game :
    """
    this is about to create a racer game with some obstacles , 
    to avoid and increase your score 
    """
    def __init__(self , dw , dh , bg_col , race , rcw , usr_nm, volacity = 60   , save = None ) :
        """
        dw : display width
        dh : display height 
        bg_col : background color
        race : the image of race 
        rcw : race width
        usr_nm : user_name 
        volacity : faces in second
        """

        pg.init()

        self.crach_sound = pg.mixer.Sound("images_races/7827.wav")
        self.save = save
        self.volacity = volacity
        self.dw = dw 
        self.dh = dh
        self.bg_col = bg_col
        self.race = pg.image.load(race)
        self.race_width = rcw
        self.game = pg.display.set_mode((dw , dh))
        self.intro_text ="Hi "+ usr_nm
        self.usr_nm = usr_nm
        

        self.col = {
         "black" : (0 , 0 , 0)  ,
         "red" : (255,0,0), 
         "blue" : (0,0,255) ,
         "green" : (0 , 255 , 0) ,
         "black-green" : (0 , 200 , 0) ,
         "black-red" : (180 , 0 , 0) , 
         "black-blue" : (0 , 0 , 200)
         }
        pg.mixer.music.load("images_races/Boss_Race.mp3")
        self.game.fill(self.col["black"])
        pg.display.set_caption("A bit Racey")
        icon  = pg.image.load("images_races/race2.tga")
        pg.display.set_icon(icon)
        self.clock = pg.time.Clock()

        self.game_intro()
    def __dir__(self) :
        return 'a game racer'

    def game_loop(self) :
        pg.mixer.music.play(-1)

        self.x_car = self.dw*0.45
        self.y_car = self.dh*0.8

        self.db1 = -30
        self.db2 = -30 - self.dh //3
        self.db3 = -30 - (2*self.dh) //3

        dx = 0
        thing = {
        "startx" : random.randrange(0 , self.dw) ,
        "starty" :-600 , 
        "speed" : 10 ,
        "width" : 30 , 
        "heigth": 30 ,
        "color" : (44 , 55 , 22)
        }
        
        self.score = 0

        self.GameExit = False 

        while not self.GameExit :
            for event in pg.event.get() : 
                if event.type == pg.QUIT :
                    self.GameExit = True

                if event.type == pg.KEYDOWN : 
                    if event.key == pg.K_LEFT:
                        dx = -5
                    elif event.key == pg.K_RIGHT : 
                        dx = 5
                    elif event.key == pg.K_p :
                        self.pause()

                if event.type == pg.KEYUP : 
                    if event.key in (pg.K_LEFT , pg.K_RIGHT) : 
                        dx = 0

            self.x_car += dx
            self.game.fill(self.bg_col)

            pg.draw.rect(self.game , (255 , 255 , 255) , (0 , 0 , 10 , self.dh))
            pg.draw.rect(self.game , (255 , 255 , 255) , (self.dw - 10  , 0 , self.dw ,self.dh ))

            self.Things(thing["startx"] , thing["starty"] , thing["width"] , thing["heigth"] , thing["color"])
            thing["starty"] += thing["speed"]

            self.draw_whi_rect()
            self.draw_whi_rect()

            self.car(self.x_car , self.y_car)
            
            self.thing_dodged(self.score)

            if self.x_car> self.dw - self.race_width or self.x_car<10 : 
                self.crash()


            if thing["starty"] > self.dh : 
                thing["starty"] = 0- thing["heigth"]
                thing["startx"] = random.randrange(int(thing["width"]) , self.dw -int( thing["width"]))
                self.score += 1
                thing["speed"] += 0.5

            # the collision between the thing and the car

            if self.y_car<thing["starty"]+thing["heigth"]-20 : 
            # y cross over
                if (self.x_car>thing["startx"] and self.x_car < thing["startx"] + thing["width"]) or (self.x_car+self.race_width > thing["startx"] and self.x_car+self.race_width < thing["startx"] + thing["width"]) or self.x_car<thing["startx"]<self.x_car + self.race_width :
                    self.crash()

            pg.display.update()  #pg.display.flip()

            self.clock.tick(self.volacity)
        
    def game_intro(self) :
        intro = True 
        while intro : 
            for event in pg.event.get() :
                if event.type == pg.QUIT :
                    self.exit()

            self.game.fill(self.col["blue"])

            self.LargeText = pg.font.Font("freesansbold.ttf" , 60) 
            self.smallText = pg.font.Font("freesansbold.ttf" , 20)
            TextSurf , TextRect = self.text_objects("A bit Racey : " , 
                self.LargeText , 
                self.col["black"])
            TextRect.center = ((self.dw/2 ) , self.dh/2 - self.dh *0.1)
            self.game.blit(TextSurf , TextRect)
            

            TextSurf , TextRect = self.text_objects(self.intro_text , 
                self.LargeText , 
                self.col["black"])
            TextRect.center = ((self.dw/2 ) , self.dh/2)
            self.game.blit(TextSurf , TextRect)

            rec1 = (self.dw*0.2  , self.dh*0.8 , self.dw*0.1 , self.dh*0.08)
            rec2 = (self.dw*0.7  , self.dh*0.8 , self.dw*0.1 , self.dh*0.08)

            self.button(rec1 , "green" , "black-green" , "Go!" , self.game_loop)
            self.button(rec2 , "red" , "black-red" , "Quit"  , self.exit)

            pg.display.update()
            self.clock.tick(30)

    def pause(self) :
        TextSurf , TextRect = self.text_objects("Paused" , self.LargeText , self.col["red"])

        TextRect.center = ((self.dw/2 ) , self.dh/2)
        
        
        self.pausee = True 
        pg.mixer.music.pause()
        
        while self.pausee : 
            for event in pg.event.get() :
                if event.type == pg.QUIT :
                    self.exit()

            self.game.fill(self.col["blue"])
            self.game.blit(TextSurf , TextRect)


            rec1 = (self.dw*0.2  , self.dh*0.8 , self.dw*0.1 , self.dh*0.08)
            rec2 = (self.dw*0.7  , self.dh*0.8 , self.dw*0.1 , self.dh*0.08)

            self.button(rec1 , "green" , "black-green" , "Continue" , self.unpause )
            self.button(rec2 , "red" , "black-red" , "Quit"  , self.exit)

            pg.display.update()
            self.clock.tick(30)
            
    def car(self , x , y) : 
        self.game.blit( self.race , (x , y ))


    def unpause(self) :
        pg.mixer.music.unpause()
        self.pausee = False 

    def thing_dodged(self , count) :
        font = pg.font.SysFont(None , 25)
        text = font.render("Score : " + str(count) , True , self.col["red"])
        self.game.blit(text , (10 , 0))


    def Things(self , x , y , w , h, color) : 
        pg.draw.rect(self.game , color , (x , y , w , h))


    def text_objects(self , text , font , col) :
        textSurface = font.render(text , True , col)
        return textSurface , textSurface.get_rect()


    def crash(self ) : 

        pg.mixer.music.stop()
        self.crach_sound.play()
        self.safe(self.score)
        text = "Game Over"
        TextSurf , TextRect = self.text_objects(text , self.LargeText , self.col["black-red"])
        TextRect.center = ((self.dw/2 ) , self.dh/2)
        self.game.blit(TextSurf , TextRect)
        pg.display.update()
        time.sleep(3)
        self.intro_text = "Try again"
        self.game_intro()

        self.exit()

    def button(self , rec  , col_light , color_over , text  ,action = None) :

        """
        the two button :
            rec : the prameters 
            col_light : the color when the button is prssed
            col_over ; the color of the button when the button is not pressed
        """

        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()


        if rec[0] + rec[2] > mouse[0] > rec[0] and rec[1] + rec[3] > mouse[1] >rec[1] :
            pg.draw.rect(self.game , self.col[col_light] ,rec)
            if click[0] and action:
                action()
        else : 
            pg.draw.rect(self.game , self.col[color_over] ,rec)

        TextSurf , TextRect = self.text_objects(text  ,
         self.smallText , 
         self.col["black"])

        TextRect.center = (rec[0] + rec[2]/2 , rec[1] + rec[3]/2 )
        
        self.game.blit(TextSurf , TextRect)

    def safe(self , sc) :
        """ sc : score 
        goal  : to save the data in database 
        """
        if self.save :
            con = sql.connect("score.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM Pets Where Name=?" , (self.usr_nm ,) )
            data = cur.fetchall()
            if not data : 
                cur.execute("INSERT INTO Pets VALUES(? , ? , ?)" , (self.usr_nm , sc, 1))

            elif sc>data[0][1] :
                games = data[0][2] + 1
                cur.execute("DELETE From Pets Where Name=? " , (self.usr_nm ,))
                cur.execute("INSERT INTO Pets VALUES(? , ? , ?)" , (self.usr_nm , sc,games ))
            elif sc<data[0][1]:
                sc = data[0][1]
                games = data[0][2] + 1
                cur.execute("DELETE From Pets Where Name=? " , (self.usr_nm ,))
                cur.execute("INSERT INTO Pets VALUES(? , ? , ?)" , (self.usr_nm , sc,games ))

            con.commit()
            cur.execute("SELECT * From Pets")
            data = cur.fetchall()
            # print(data)
            con.close()

    def draw_whi_rect(self) :
        pg.draw.rect(self.game ,(255 , 255 , 255)  , (self.dw//2 ,self.db1 , 10 , 30 ))
        pg.draw.rect(self.game ,(255 , 255 , 255)  , (self.dw//2 ,self.db2 , 10 , 30 ))
        pg.draw.rect(self.game ,(255 , 255 , 255)  , (self.dw//2 ,self.db3 , 10 , 30 ))
        self.db1 += 10
        self.db2 += 10
        self.db3 +=10
        if self.db1 > self.dh :
            self.db1 = -30

        elif self.db2 > self.dh :
            self.db2 = -30

        elif self.db3 > self.dh : 
            self.db3 = -30

    def exit(self) :
        pg.quit()
        quit()

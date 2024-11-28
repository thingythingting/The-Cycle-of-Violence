from cmu_graphics import *
from PIL import*
import random 

def onAppStart(app):
    app.phase = 0
    app.height = 500
    app.width = 1000
    app.recttop = 0
    app.rectleft = 450
    app.rectwidth = 1000
    app.rectheight = 50
    app.label = ''
    app.attack = False
    app.defend = False
    app.ignore = False
    app.apologize = False
    app.rectborder = 2

    app.barX = 10
    app.barY = 160
    app.barHeight = 100
    app.barWidth = 50

    app.resourcesbarX = 70
    app.resourcesbarY = 160
    app.resourcesbarHeight = 100
    app.resourcesbarWidth = 50

    app.resourcesPlayer = 10
    app.resourcesAI = 10

    app.maxTrust = 100
    
    # Initialize game state and scenes
    app.gameState = {"trust": 10, "COV": 20, "current_scene": "Intro", "player_choices": []}
    app.scenes = {
        "Intro": IntroScene(),
        "PrologueScene": PrologueScene(),
        "Level1": Level1Scene(),
        "Level2": Level2Scene(),
        "GameOver": GameOverScene(),
    }
    app.current_scene = app.scenes["Intro"]
    #trim_image("box.png")
    app.elite_box = Image.open("elite_box.png")
    app.elite_box = CMUImage(app.elite_box)
    app.peep = CMUImage(Image.open("good_peep.png"))
    app.peep_open_eyes = CMUImage(Image.open("open_eyes.png"))
    app.ai_peep = CMUImage(Image.open("ai_peep.png"))
    app.ai_open_eyes = CMUImage(Image.open("ai_open_eyes.png"))
    app.url_score_box = "https://github.com/thingythingting/The-Cycle-of-Violence/blob/main/final%20score.png?raw=true"
    app.player = "https://raw.githubusercontent.com/thingythingting/The-Cycle-of-Violence/main/Player.png"
    app.choice_box = "https://github.com/thingythingting/The-Cycle-of-Violence/blob/main/Untitled_Artwork.png?raw=true"
    
    #from chatgpt
    app.timer = 0  # Time tracker for transitions
    app.lineLength = 0  # Line grows dynamically
    app.textAlpha = 0  # Text fades in
    app.circleRadius = 1  # Circle grows dynamically

def trim_image(image):   
    with Image.open(image) as im:
        rgba = im.convert("RGBA")
        data = rgba.getdata()
        new_data = []
        for pixel in data:
            if pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255:
                new_data.append((255,255,255,0))
            else:
                new_data.append(pixel)
        rgba.putdata(new_data)
        rgba.save("{image}.png", "PNG")
        return rgba

def set_scene(app, scene_name):
    if scene_name in app.scenes:
        app.current_scene = app.scenes[scene_name]
        app.gameState["current_scene"] = scene_name
    else:
        print(f"Scene '{scene_name}' not found!")

def attack(app):
    app.label = "attack"
    app.gameState["player_choices"].append(app.label)
    if app.gameState['trust'] > 0:
        app.gameState['trust'] -= 10
    if app.gameState.get('ai_action') == 'attack':
        if app.resourcesAI > app.resourcesPlayer:
            app.resourcesPlayer -= 5
            app.resourcesAI += 5
        elif app.resourcesAI < app.resourcesPlayer:
            app.resourcesPlayer += 5
            app.resourcesAI = -5
        else:
            random_num = random.randint(-5,5)
            app.resourcesPlayer += random_num
            app.resourcesAI -= random_num
    elif app.gameState.get("ai_action") == 'defend':
        app.resourcesAI -= 1
        app.resourcesPlayer += 2
    elif app.gameState.get('ai_action') == 'apologize':
        app.resourcesPlayer += 3
        app.resourcesAI -= 3
    elif app.gameState.get("ai_action") == 'ignore':
        app.resourcesAI += 0
        app.resourcesPlayer += 3



def defend(app):
    app.label = 'defend'
    app.gameState["player_choices"].append(app.label)
    app.gameState["trust"] += 0
    if app.gameState.get("ai_action") == 'attack':
        app.resourcesAI += 2
        app.resourcesPlayer -= 1
    elif app.gameState.get("ai_action") == 'defend':
        app.resourcesAI += 0
        app.resourcesPlayer += 0
    elif app.gameState.get("ai_action") == 'apologize':
        app.resourcesPlayer += 2
        app.resourcesAI -= 1
    elif app.gameState.get("ai_action") == 'ignore':
        app.resourcesAI += 0
        app.resourcesPlayer -= 1

def apologize(app):
    app.label = 'apologize'
    app.gameState["player_choices"].append(app.label)
    app.gameState["trust"] += 10
    if app.gameState.get("ai_action") == 'attack':
        app.resourcesAI += 3
        app.resourcesPlayer -= 3
    elif app.gameState.get("ai_action") == 'defend':
        app.resourcesAI += 2
        app.resourcesPlayer -= 1
    elif app.gameState.get("ai_action") == 'apologize':
        app.resourcesAI += 1
        app.resourcesPlayer += 1
    elif app.gameState.get("ai_action") == 'ignore':
        app.resourcesAI -= 1
        app.resourcesPlayer += 0


def ignore(app):
    app.label = 'ignore'
    app.gameState["player_choices"].append(app.label)
    app.gameState["trust"] += 5
    if app.gameState.get("ai_action") == 'attack':
        app.resourcesAI += 3
        app.resourcesPlayer += 0
    elif app.gameState.get("ai_action") == 'defend':
        app.resourcesAI -= 1
        app.resourcesPlayer += 0
    elif app.gameState.get("ai_action") == 'apologize':
        app.resourcesAI += 0
        app.resourcesPlayer -= 1
    elif app.gameState.get("ai_action") == 'ignore':
        app.resourcesAI += 0
        app.resourcesPlayer += 0

def onKeyPress(app, key):
    app.current_scene.handle_input_keys(app, key)

def onMousePress(app, mouseX, mouseY):
    app.current_scene.handle_input_mouse_press(app, mouseX, mouseY)
    
def onStep(app):
    app.current_scene.Step(app)

def redrawAll(app):
    app.current_scene.render(app)
    # circle_edge = (1/5)*app.width
    # delta = 0
    # num = 7
    # for circles in range(num):
    #     drawCircle((1/(num+1))*app.width + delta ,app.height - ((1/2)*app.rectheight), 10, fill = 'white')
    #     delta += (1/(num+1))*app.rectwidth


# Base Scene class
class Scene:
    def __init__(self, name):
        self.name = name
    
    def Step(self, app):
        pass

    def render(self, app):
        """Draw the scene on the screen."""
        raise NotImplementedError
    
    def handle_input(self, app, key):
        """Handle user input for this scene."""
        raise NotImplementedError

# Intro Scene
class IntroScene(Scene):
    def __init__(self):
        super().__init__("Intro")
    
    def render(self, app):
        drawLabel("The Circle of Violence", app.width // 2, app.height // 2, size=30, align="center", font = '')
        drawLabel("Press 'Enter' to start.", app.width // 2, app.height // 2 + 50, size=20, align="center")

        drawRect(0, 0, app.width, app.height, fill="black")

        # Phase 1: Growing line
        if app.phase >= 0:
            drawLine(0, app.height // 2, app.lineLength, app.height // 2, fill="white", lineWidth=3)

        # Phase 2: Fade-in text
        if app.phase >= 1:
            drawLabel("The Circle of Violence", app.width // 2, app.height // 2 - 50,
                    size=30, fill=rgb(255, 255, 255), opacity = app.textAlpha, align="center")
            drawLabel("Press 'Enter' to start.", app.width // 2, app.height // 2 + 50,
                    size=20, fill=rgb(255, 255, 255), opacity = app.textAlpha, align="center")

        # Phase 3: Growing circle
        if app.phase >= 2:
            drawCircle(app.width // 2, app.height // 2 + 100, app.circleRadius, fill="white")

        # Debug: Display phase number
        drawLabel(f"Phase: {app.phase}", 10, 10, size=15, fill="white")

    def Step(self,app):
        app.timer += 1
        
        # Phase 1: Line grows
        if app.phase == 0:
            app.lineLength += 10
            if app.lineLength >= app.width:  # Move to next phase when line is complete
                app.phase += 1
                app.timer = 0

        # Phase 2: Text fades in
        elif app.phase == 1:
            if app.textAlpha + 5 <= 100:
                app.textAlpha = min(255, app.textAlpha + 5)  # Gradually increase opacity
            if app.timer >= 50:  # Stay in this phase for 50 steps
                app.phase += 1
                app.timer = 0

        # Phase 3: Circle grows
        elif app.phase == 2:
            app.circleRadius += 5
            # if app.circleRadius >= 100:  # Circle fully expanded
            #     app.phase += 1
            #     app.timer = 0

    def handle_input_keys(self, app, key):
        if key == "enter":
            set_scene(app, "PrologueScene")

# Level 1 Scene
class PrologueScene(Scene):
    def __init__(self):
        super().__init__("PrologueScene")
    def render(self, app):
        drawLabel("Prologue", 500, 40, align = 'center', size = 30)
        drawLabel("In an alternate universe (much like our own) people", 500, 80, align = 'center', size = 20)
        drawLabel("have gone on rampages of war, violence, and destruction.", 500, 110, align = 'center', size = 20)
        drawLabel("Desperate to seperate from those norms, your tribe,", 500, 140, align = 'center', size = 20)
        drawLabel("among many others, sought to move past these", 500, 170, align = 'center', size = 20)
        drawLabel("violent ideals. Now you must play as a representative", 500, 200, align = 'center', size = 20)
        drawLabel("for your tribe, aiming to grow your tribe's level of ", 500, 230, align = 'center', size = 20)
        drawLabel("resources. Aim to prevent the next wars by keeping", 500, 260, align = 'center', size = 20)
        drawLabel("the 'cycle of violence' meter low and the 'trust'", 500, 290, align = 'center', size = 20)
        drawLabel("meter high. Because if you don't, the repercussions", 500, 320, align = 'center', size = 20)
        drawLabel("will be felt for generations to come...", 500, 350, align = 'center', size = 20)
        drawRect(400, 380, 200, 50, fill = None, borderWidth = 2, border = 'black')
        drawLabel("Next...", 500, 405, align = 'center', size = 20)
    def handle_input_mouse_press(self,app, mouseX, mouseY):
        if mouseX < 600 and mouseX > 400 and mouseY < 430 and mouseY > 380:
            set_scene(app, "Level1")
class Level1Scene(Scene):
    def __init__(self):
        super().__init__("Level1")
        self.ai_agent = Revenger(resources = 10)
    
    # drawings for level1
    def render(self, app):
        #drawLabel("Level 1", 50,30, size=30, align="center")
        #drawLabel("Press 'Q' to quit or 'N' for next level.", 450,10, size=20, align="left")
        drawLabel("First, you be playing with a representative from another tribe. You will ", 500, 30, align = 'center', size = 15)
        drawLabel("play againt 4 tribes, with each representative having a different", 500, 50, align = 'center', size = 15)
        drawLabel("playing philosphy. It is up to you to maintain relationships and garner resources ", 500, 70, align = 'center', size = 15)
        drawLabel("for your tribe. Based on you and your fellow representative's answers, it",500, 90, align = 'center', size = 15)
        drawLabel("will affect the amount of resources each of you get.", 500, 130, align = "center", size = 15)
        #drawLabel(f"AI Action: {app.gameState.get('ai_action', '')}", 300, 50, size=20, align="center")
        #drawLabel(f"Player Action: {app.label}", 150, 100, size=20, align="center")
        drawLabel("Trust",35, 155)
        drawLabel("Resources",95, 155)
        

        drawLine(230, 280, 230,270)
        drawLine(230,280,238,277)
        drawLine(230, 280, 239, 265)
        drawLabel("you", 241, 263, align = 'left')

        drawLine(775, 280, 775, 268)
        drawLine(775, 280, 768, 273)
        drawLine(775, 280, 767,260)
        drawLabel("AI Rep", 768, 253, align = 'right')
        #Navigation tools
        drawRect(app.recttop ,app.rectleft,app.rectwidth, app.rectheight, fill = rgb(30,30,30))

        drawRect(10, 160, 50, 100, fill = None, border = 'black', borderWidth = 2)
        currentHeight = app.gameState['trust'] / app.maxTrust * app.barHeight
        drawRect(app.barX, app.barY + app.barHeight - currentHeight, app.barWidth, currentHeight, fill="red", border = 'black', borderWidth = 2)
        
        drawRect(70, 160, 50, 100, fill = None, border = 'black', borderWidth = 2)
        currentHeight = app.resourcesPlayer / 100 * app.resourcesbarHeight
        drawRect(app.resourcesbarX, app.resourcesbarY + app.resourcesbarHeight - currentHeight, app.resourcesbarWidth, currentHeight, fill="red", border = 'black', borderWidth = 2)
        

        choices = ["Attack", "Defend", "Apologize", "Ignore"]
        delta = 0
        for box in range(4):
            drawRect((1/7)*app.width + delta, (4/5)*app.height, 100, 50, fill = None, border = "black", borderWidth = app.rectborder, align = 'center')
            drawLabel(choices[0], (1/7)*app.width + delta, (4/5)*app.height)
            choices.remove(choices[0])
            delta += (1/4)*app.width

        delta = 0
        num = 7
        for circles in range(num):
            drawCircle((1/(num+1))*app.width + delta ,app.height - ((1/2)*app.rectheight), 10, fill = 'white')
            delta += (1/(num+1))*app.rectwidth
        #drawImage(app.elite_box, 200, 400, width = 700, height = 700, align = 'center')
        #score coin machine
        drawImage(app.url_score_box, 500, 350, width = 800, height = 1000, align = 'center')

        #peep tools
        drawImage(app.peep, 200, 325, width = 90, height = 100, align = 'center')
        drawImage(app.peep_open_eyes, 210, 315, width = 45, height = 25, align = 'center')
        drawImage(app.ai_peep, 800, 325, width = 90, height = 100, align = 'center')
        drawImage(app.ai_open_eyes, 790, 315, width = 45, height = 25, align = 'center')



    def handle_input_keys(self, app, key):
    
        if key == "n":
            set_scene(app, "Level2")
        elif key == "q":
            set_scene(app, "GameOver")

    def handle_input_mouse_move(self, app, mouseX, mouseY):
        if mouseX < 193 and mouseX > 93 and mouseY > 375 and mouseY < 425:
            attack(app)
            app.attack = True
            app.defend = False
            app.apologize = False
            app.ignore = False
        if mouseX < 443 and mouseX > 343 and mouseY > 375 and mouseY < 425:
            defend(app)
            app.defend = True
            app.attack = False
            app.apologize = False
            app.ignore = False

        if mouseX < 693 and mouseX > 593 and mouseY > 375 and mouseY < 425:
            apologize(app)
            app.apologize = True
            app.attack = False
            app.defend = False
            app.ignore = False

        if mouseX < 943 and mouseX > 843 and mouseY > 375 and mouseY < 425:
            ignore(app)
            app.ignore = True
            app.defend = False
            app.attack = False
            app.apologize = False

    def handle_input_mouse_press(self, app, mouseX, mouseY):
        if mouseX < 193 and mouseX > 93 and mouseY > 375 and mouseY < 425:
            attack(app)
            app.attack = True
            app.defend = False
            app.apologize = False
            app.ignore = False
        if mouseX < 443 and mouseX > 343 and mouseY > 375 and mouseY < 425:
            defend(app)
            app.defend = True
            app.attack = False
            app.apologize = False
            app.ignore = False

        if mouseX < 693 and mouseX > 593 and mouseY > 375 and mouseY < 425:
            apologize(app)
            app.apologize = True
            app.attack = False
            app.defend = False
            app.ignore = False

        if mouseX < 943 and mouseX > 843 and mouseY > 375 and mouseY < 425:
            ignore(app)
            app.ignore = True
            app.defend = False
            app.attack = False
            app.apologize = False
        self.ai_agent.update_state(app.label)
        app.gameState['ai_action'] = self.ai_agent.choice()
    def Step(self,app):
        pass
    def handle_input_keys(self,app, key):
        pass
# Level 2 Scene
class Level2Scene(Scene):
    def __init__(self):
        super().__init__("Level2")
    
    def render(self, app):
        drawLabel("Level 2", app.width // 2, app.height // 2, size=30, align="center")
        drawLabel("Press 'Q' to quit or 'R' to restart.", app.width // 2, app.height // 2 + 50, size=20, align="center")
        
    def handle_input(self, app, key):
        if key == "q":
            set_scene(app, "GameOver")
        elif key == "r":
            set_scene(app, "Intro")
    
# Game Over Scene
class GameOverScene(Scene):
    def __init__(self):
        super().__init__("GameOver")
    
    def render(self, app):
        drawLabel("Game Over!", app.width // 2, app.height // 2, size=40, align="center")
        drawLabel("Press 'R' to restart.", app.width // 2, app.height // 2 + 50, size=20, align="center")
    
    def handle_input_keys(self, app, key):
        if key == "r":
            set_scene(app, "Intro")
            
class Joker:
    
    def __init__(self, resources):
        self.default_weights = {attack:.25, defend:.25, apologize:.25, ignore:.25}
        self.resources = resources
        
    def choice(self):
        choice = random.choices(
            list(self.default_weights.keys()), 
            weights=list(self.default_weights.values()), 
            k=1)
        return choice[0]
        
class Revenger:
    def __init__(self, resources):
        self.default_weights = {'defend':3, 'apologize': 3, 'ignore': 4}
        self.has_been_attacked = False
        self.revenge_mode = False
        
    def update_state(self, player_action):
        if player_action == 'attack':
            self.has_been_attacked = True
            self.revenge_mode = True
    
    def choice(self):
        if self.revenge_mode == True:
            return 'attack'
        else:
            weighted_list = []
            for option in self.default_weights:
                weighted_list.extend([option] * self.default_weights[option])  # Use list extend to add multiple items
            choice_index = random.randint(0, len(weighted_list) - 1)  # Fixed random index
            return weighted_list[choice_index]
    #     answer = choice(self)    

class Detective:
    def __init__(self, resources):
        self.resources = resources
        self.world_state = {
            "ai_resources": app.resourcesAI,
            "player_resources": app.resourcesPlayer
        }
        self.goals = [
            {"name": "Maximize AI Resources", "priority": 1, "target":{"ai_resources":100}}
        ]
        self.actions = [
            {
                "name": "Attack",
                "preconditions": {"ai_resources": 15},
                "effects": {"player_resources":-5}
            }
        ]
runApp()

     
     
     
     
     
     
     
     
     
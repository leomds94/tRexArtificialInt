from PIL import Image
from PIL import ImageGrab
from datetime import datetime
from time import sleep
import pykeyboard

dino_color = (83, 83, 83)

def screenshot(x, y, w, h):
    box = (x, y, w, h)
    ImageGrab.grab().crop(box).save("tmp.png", "PNG")
    # os.system("screencapture -R{},{},{},{} tmp.png".format(x, y, w, h))
    img = Image.open("tmp.png")
    return img

def is_dino_color(pixel):
    return pixel == dino_color

def obstacle(distance, length, speed, time):
    return { 'distance': distance, 'length': length, 'speed': speed, 'time': time }

class Scanner:
    def __init__(self):
        self.game_start = (0,0)
        self.game_end = (0,0)
        self.game_dimension = (599,109)
        self.dino_start_x = 0
        self.last_obs = {}
        self.curr_fitness = 0
        self.change_fitness = False
        self.image = None

    def find_game(self):
        xstart = 0
        image = screenshot(0, 0, 1920, 1080)
        size = image.size
        
        for y in range(0, size[1]):
            dino_ground = 0
            for x in range(0, size[0]):
                color = image.getpixel((x, y))
                if is_dino_color(color):
                    if dino_ground == 0:
                        xstart = x
                    dino_ground += 1
                    
            if dino_ground > 500:
                self.game_start = (xstart, y - self.game_dimension[1])
                self.game_end = (xstart + self.game_dimension[0], y)
                self.image = screenshot(self.game_start[0], self.game_start[1], self.game_end[0], self.game_end[1])
                print("x0: {}, y0: {}, x1: {}, y1: {}").format(self.game_start[0], self.game_start[1], self.game_end[0], self.game_end[1])
                return True
            
        raise Exception("Game not found!")

    def find_dino(self):
        for x in range(0, self.game_dimension[0]):
            sum = 0
            for y in range(88, 99):
                color = self.image.getpixel((x, y))
                if is_dino_color(color):
                    sum += 1
                    if(sum == 11):
                        self.dino_start_x = x + 40
                        return True
    

    def find_next_obstacle(self, down_pressed):
        self.image = screenshot(self.game_start[0], self.game_start[1], self.game_end[0], self.game_end[1])
        self.is_game_over(self.image)
        sleep(0.05)
        if down_pressed:
            x_diff = self.dino_start_x + 17
        else:
            x_diff = self.dino_start_x

        obs_param = self.next_obs_params(self.image, x_diff)

        dist = obs_param[0]
        length = obs_param[1]
        time = obs_param[2]
        speed = 0.0

        #print dist, x_diff, down_pressed

        if self.last_obs:
            self.verify_change_fitness(dist)
            delta_dist = float(self.last_obs['distance'] - dist)
            delta_time = float(time - self.last_obs['time'])
            speed = abs(delta_dist / delta_time) * 10000
            if speed > 10.0:
                speed = 3.5
        self.last_obs = obstacle(dist, length, speed, time)
        return self.last_obs

    def next_obs_params(self, image, x_diff):
        time = 0
        for x in range(x_diff, image.size[0], 2):
            for y in range(0, image.size[1] - 6, 2):
                color = image.getpixel((x, y))
                time = datetime.now().microsecond
                if is_dino_color(color):
                    return [(x-x_diff), (110 - y), time]

        return [1000, 0, time]

    def is_game_over(self, image):
        s = 0
        for y in range(55, 84):
            for x in range(285, 289):
                color = image.getpixel((x, y))
                if is_dino_color(color):
                    s += 1
        if s > 110:
            print('Game over! Fitness: {}, Last dist: {}, Length: {}').format(self.curr_fitness,self.last_obs['distance'], self.last_obs['length'])
            sleep(1)
            raise Exception('Game over!')

    def reset(self):
        self.last_obs = {}
        self.curr_fitness = 0
        self.change_fitness = False

    def verify_change_fitness(self, dist):
        if dist > self.last_obs['distance'] and not self.change_fitness:
            self.curr_fitness += 1
            self.change_fitness = True
        else:
            self.change_fitness = False

    def get_fitness(self):
        return self.curr_fitness

import simplegui
import math

"""d
Contains useful functions for clamping values for use various color spaces.
"""
class Color:
    """d
    Casts values to integers and clamps them between 0 and 255.
    :param value :- The value to clamp :- number
    :return The value after the clamping :- int
    """
    def clamp8Bit(value):
        return max(0, min(int(value), 255))
    
    """d
    Clamps values between 0 and 1.
    :param value :- The value to clamp :- number
    :return The value after the clamping :- float
    """
    def clampDecimal(value):
        return max(0.0, min(float(value), 1.0))
    
    """d
    Clamps values between 0 and 100.
    :param value :- The value to clamp :- number
    :return The value after the clamping :- number
    """
    def clampPercent(value):
        return max(0, min(value, 100))
    
    """d
    Clamps values between 0 and 360.
    :param value :- The value to clamp :- number
    :return The value after the clamping :- number
    """
    def clampDegrees(value):
        return max(0, min(value, 360))
    
"""d
Represents a color in the RGB color space.
"""
class RGB:
    """d
    Constructs an RGB color.
    :param r :- The red value of the color, clamped using Color.clamp8Bit() :- number
    :param g :- The greed value of the color, clamped using Color.clamp8Bit() :- number
    :param b :- The blue value of the color, clamped using Color.clamp8Bit() :- number
    """
    def __init__(self, r, g, b):
        self.r = Color.clamp8Bit(r)
        self.g = Color.clamp8Bit(g)
        self.b = Color.clamp8Bit(b)

    """d
    [CAST] Converts the color to a valid HTML color string in format rgb(r, g, b)
    """
    def __str__(self):
        return f"rgb({self.r}, {self.g}, {self.b})"
"""d
Represents a color in the RGB color space while allowing for transparency.
"""
class RGBA:
    """d
    Constructs an RGBA color.
    :param r :- The red value of the color, clamped using Color.clamp8Bit() :- number
    :param g :- The greed value of the color, clamped using Color.clamp8Bit() :- number
    :param b :- The blue value of the color, clamped using Color.clamp8Bit() :- number
    :param a :- The alpha, or opacity, of the color, clamped using Color.clampDecimal() :- float
    """
    def __init__(self, r, g, b, a):
        self.r = Color.clamp8Bit(r)
        self.g = Color.clamp8Bit(g)
        self.b = Color.clamp8Bit(b)
        self.a = Color.clampDecimal(a)
        
    """d
    [CAST] Converts the color to a valid HTML color string in format rgba(r, g, b, a)
    """
    def __str__(self):
        return f"rgba({self.r}, {self.g}, {self.b}, {self.a})"
"""d
Represents a color in the HSL color space.
"""
class HSL:
    """d
    Constructs an HSL color.
    :param h :- The hue of the color, clamped using Color.clampDegrees() :- number
    :param s :- The saturation of the color, clamped using Color.clampPercent() :- number
    :param l :- The luminosity of the color, clamped using Color.clampPercent() :- number
    """
    def __init__(self, h, s, l):
        self.h = Color.clampDegrees(h)
        self.s = Color.clampPercent(s)
        self.l = Color.clampPercent(l)
    """d
    [CAST] Converts the color to a valid HTML color string in format hsl(h, s, l)
    """
    def __str__(self):
        return f"HSL({self.h}, {self.s}%, {self.l}%)"    
"""d
Represents a color in the HSL color space while allowing for transparency.
"""
class HSLA:
    """d
    Constructs an HSL color.
    :param h :- The hue of the color, clamped using Color.clampDegrees() :- number
    :param s :- The saturation of the color, clamped using Color.clampPercent() :- number
    :param l :- The luminosity of the color, clamped using Color.clampPercent() :- number
    :param a :- The alpha, or opacity, of the color, clamped using Color.clampDecimal() :- float
    """
    def __init__(self, h, s, l, a):
        self.h = Color.clampDegrees(h)
        self.s = Color.clampPercent(s)
        self.l = Color.clampPercent(l)
        self.a = Color.clampDecimal(a)
    """d
    [CAST] Converts the color to a valid HTML color string in format hsla(h, s, l, a)
    """
    def __str__(self):
        return f"hsl({self.h}, {self.s}%, {self.l}%, {self.a})"  
    
class DrawScheduler:
    __drawBuffer = [lambda pos : 1 + 1]
    
    def registerShape(function):
        DrawScheduler.__drawBuffer.append(function)
        return len(DrawScheduler.__drawBuffer) - 1
    
    def draw(canvas):
        for drawer in DrawScheduler.__drawBuffer:
            drawer(canvas)
            
    def destroyShape(shapeID):
        print(f"Destroying: {shapeID} with length {len(DrawScheduler.__drawBuffer)}")
        DrawScheduler.__drawBuffer[shapeID] = lambda c : 1 + 1

"""d
Contains functions for interacting with the application window and controls.
"""
class App:
    KEY_MAP = simplegui.KEY_MAP
    CHAR_MAP = {v : k.lower() for k, v in simplegui.KEY_MAP.items()}
    
    __guiFrame = None
    __background = 'white'
    defaultFill = 'black'
    
    __downFunction = lambda key : 1 + 1
    __upFunction = lambda key : 1 + 1
    __updateFunction = lambda : 1 + 1
    
    heldKeys = []
    __keyHoldMap = {}
    
    
    def __down(key):
        App.heldKeys.append(key)
        App.__downFunction(key)
    def __up(key):
        App.heldKeys.remove(key)
        App.__upFunction(key)
    def __update(canvas):
        for key in App.heldKeys:
            if key in App.__keyHoldMap.keys():
                App.__keyHoldMap[key]()
        App.__updateFunction()
        DrawScheduler.draw(canvas)
    
    def initialize():
        frame = simplegui.create_frame("Test", 500, 500)
        frame.set_draw_handler(App.__update)
        frame.set_canvas_background(App.__background)
        frame.set_keydown_handler(App.__down)
        frame.set_keyup_handler(App.__up)
        App.__guiFrame = frame
        frame.start()
    
    """d
    Retrieves the window's background color.
    :return The background color of the window :- string
    """
    def getBackground():
        return App.__background
    """d
    Changes the window's background color to the provided color.
    :param color :- The desired background color :- color, string
    """
    def setBackground(color):
        App.__background = str(color)
        App.__guiFrame.set_canvas_background(str(color))
    
    """d
    Binds a function to be called whenever the mouse is clicked.
    :param function :- The function to be executed when the mouse is clicked. Must take in a 2-element tuple for the position in format (x, y) :- function
    """
    def onMouseClick(function):
        App.__guiFrame.set_mouseclick_handler(function)
    """d
    Binds a function to be called whenever a mouse button is held down and the cursor is moved.
    :param function :- The function to be executed when the mouse is dragged. Must take in a 2-element tuple for the position in format (x, y) :- function
    """
    def onMouseDrag(function):
        App.__guiFrame.set_mousedrag_handler(function)

    """d
    Binds a function to be called whenever a key is pressed down.
    :param function :- The function to be called when a key is pressed. Must take in an int for the key that was pressed, to convert between characters and numbers use App.KEY_MAP :- function
    """
    def onKeyDown(function):
        App.__downFunction = function
    """d
    Binds a function to be called whenever a key is released.
    :param function :- The function to be called when a key is released. Must take in an int for the key that was pressed, to convert between characters and numbers use App.KEY_MAP :- function
    """
    def onKeyUp(function):
        App.__upFunction = function
    """d
    Binds a function to be called while a key is held.
    :param key :- The key to bind this function to. This string must be only 1 character long :- string
    :param function :- The function to be called while the provided key is held. This function must accept no arguments :- function
    """
    def whileKeyDown(key, function):
        App.__keyHoldMap.update({simplegui.KEY_MAP[key] : function})

    """d
    Binds a function to be called every time the window is updated. This occurs roughly 60 times a second under ideal conditions.
    :param function :- The function to be called every update. This function must accept no arguments :- function
    """
    def onUpdate(function):
        App.__updateFunction = function
    
    """d
    Calculates the width that a string of text will take up.
    :param text :- The text to find the width of :- string
    :param size :- The font size of the text :- number
    :return The width of the text :- int
    """
    def textSize(text, size):
        return App.__guiFrame.get_canvas_textwidth(text, size)
    
class Rect:
    def __init__(self, startX, startY, width, height, fill=App.defaultFill, border=None, borderWidth=2):
        self.__startX = startX
        self.__startY = startY
        self.__width = width
        self.__height = height
        
        self.__fill = 'rgba(255, 255, 255, 0)' if fill == None else fill
        self.__border = 'rgba(255, 255, 255, 0)' if border == None else border
        self.borderWidth = borderWidth
        
        self.__calculatePoints()
        
        self.visible = True
        
        self.__id = DrawScheduler.registerShape(self.__draw)
    
    def __getStartX(self):
        return self.__startX
    def __setStartX(self, startX):
        self.__startX = startX
        self.__calculatePoints()
    def __getStartY(self):
        return self.__startY
    def __setStartY(self, startY):
        self.__startY = startY
        self.__calculatePoints()
    def __getWidth(self):
        return self.__width
    def __setWidth(self, width):
        self.__width = width
        self.__calculatePoints()
    def __getHeight(self):
        return self.__height
    def __setHeight(self, height):
        self.__height = height
        self.__calculatePoints()
    def __getCenterX(self):
        return self.__startX + (self.__width / 2.0)
    def __setCenterX(self, centerX):
        self.startX = centerX - (self.__width / 2.0)
    def __getCenterY(self):
        return self.__startY + (self.__height / 2.0)
    def __setCenterY(self, centerY):
        self.startY = centerY - (self.__height / 2.0)
    def __getBorder(self):
        return self.__border
    def __setBorder(self, border):
        self.__border = 'rgba(255, 255, 255, 0)' if border == None else border
    def __getFill(self):
        return self.__fill
    def __setFill(self, fill):
        self.__fill = 'rgba(255, 255, 255, 0)' if fill == None else fill
    
    def __draw(self, canvas):
        if not self.visible:
            return
        canvas.draw_polygon(self.__points, self.borderWidth, str(self.border), str(self.fill))

    def contains(self, x, y):
        return x >= self.startX and x <= self.points[1][0] and y >= self.startY and y <= self.points[3][1]
    
    def __calculatePoints(self):
        startX = self.startX
        startY = self.startY
        width = self.width
        height = self.height
        
        self.__points = [(startX, startY), (startX + width, startY), (startX + width, startY + height), (startX, startY + height)]
    
    def __area(self):
        return self.width * self.height
    
    startX = property(__getStartX, __setStartX)
    startY = property(__getStartY, __setStartY)
    width = property(__getWidth, __setWidth)
    height = property(__getHeight, __setHeight)
    centerX = property(__getCenterX, __setCenterX)
    centerY = property(__getCenterY, __setCenterY)
    border = property(__getBorder, __setBorder)
    fill = property(__getFill, __setFill)
    area = property(__area)
    
    
    def __del__(self):
        DrawScheduler.destroyShape(self.__id)
class Circle:
    def __init__(self, centerX, centerY, radius, fill=App.defaultFill, border=None, borderWidth=2):
        self.centerX = centerX
        self.centerY = centerY
        self.radius = radius
        
        self.__fill = 'rgba(255, 255, 255, 0)' if fill == None else fill
        self.__border = 'rgba(255, 255, 255, 0)' if border == None else border
        self.borderWidth = borderWidth
        
        self.visible = True
        
        self.__id = DrawScheduler.registerShape(self.__draw)
    
    def __draw(self, canvas):
        if not self.visible:
            return
        canvas.draw_circle((self.centerX, self.centerY), self.radius, self.borderWidth, str(self.border), str(self.fill))
    
    def contains(self, x, y):
        return math.sqrt(((x - self.centerX) ** 2) + ((y - self.centerY) ** 2)) <= self.radius
    
    def __getBorder(self):
        return self.__border
    def __setBorder(self, border):
        self.__border = 'rgba(255, 255, 255, 0)' if border == None else border
    def __getFill(self):
        return self.__fill
    def __setFill(self, fill):
        self.__fill = 'rgba(255, 255, 255, 0)' if fill == None else fill
    
    def __area(self):
        return math.PI * (self.radius ** 2.0)  

    area = property(__area)
    fill = property(__getFill, __setFill)
    border = property(__getFill, __setFill)
    
    def __del__(self):
        DrawScheduler.destroyShape(self.__id)
class Polygon:
    def __init__(self, *args, fill=App.defaultFill, border=None, borderWidth=2):
        self.points = list(args)
        
        self.__fill = 'rgba(255, 255, 255, 0)' if fill == None else fill
        self.__border = 'rgba(255, 255, 255, 0)' if border == None else border
        self.borderWidth = borderWidth
        
        self.visible = True
        
        self.__id = DrawScheduler.registerShape(self.__draw)
        
    def __draw(self, canvas):
        if not self.visible:
            return
        canvas.draw_polygon(self.points, self.borderWidth, str(self.border), str(self.fill))

    def contains(self, x, y):
        raise NotImplementedError()
       
    def __getBorder(self):
        return self.__border
    def __setBorder(self, border):
        self.__border = 'rgba(255, 255, 255, 0)' if border == None else border
    def __getFill(self):
        return self.__fill
    def __setFill(self, fill):
        self.__fill = 'rgba(255, 255, 255, 0)' if fill == None else fill
    
    border = property(__getBorder, __setBorder)
    fill = property(__getFill, __setFill)
    
    def __del__(self):
        DrawScheduler.destroyShape(self.__id)
class Text:
    def __init__(self, text, centerX, centerY, size, fill=App.defaultFill):
        self.__text = text
        self.__centerX = centerX
        self.__centerY = centerY
        self.__size = size
        
        self.__fill = 'rgba(255, 255, 255, 0)' if fill == None else fill
        
        self.__recalculatePoint()
        
        DrawScheduler.registerShape(self.__draw)
        
    def __draw(self, canvas):
        canvas.draw_text(self.__text, self.__point, self.size, str(self.fill))
    
    def __recalculatePoint(self):
        self.__point = (self.__centerX - (App.textSize(self.__text, self.__size) / 2.0), self.__centerY + (self.__size / 4.0))
    
    def __width(self):
        return App.textSize(self.__text, self.size)
    def __height(self):
        return self.__size / 4
    
    def __getText(self):
        return self.__text
    def __setText(self, text):
        self.__text = str(text)
        self.__recalculatePoint()
    def __getCenterX(self):
        return self.__centerX
    def __setCenterX(self, centerX):
        self.__centerX = centerX
        self.__recalculatePoint()
    def __getCenterY(self):
        return self.__centerY
    def __setCenterY(self, centerY):
        self.__centerY = centerY
        self.__recalculatePoint()
    def __getSize(self):
        return self.__size
    def __setSize(self, size):
        self.__size = size
        self.__recalculatePoint()
    def __getFill(self):
        return self.__fill
    def __setFill(self, fill):
        self.__fill = 'rgba(255, 255, 255, 0)' if fill == None else fill
        
    text = property(__getText, __setText)
    centerX = property(__getCenterX, __setCenterX)
    centerY = property(__getCenterY, __setCenterY)
    size = property(__getSize, __setSize)
    fill = property(__getFill, __setFill)
    width = property(__width)
    height = property(__height)
    
    def contains(self, x, y):
        raise NotImplementedError()
    
    def __del__(self):
        DrawScheduler.destroyShape(self.__id)
class Line:
    def __init__(self, startX, startY, endX, endY, lineWidth, fill=App.defaultFill):
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY
        
        self.lineWidth = lineWidth
        
        self.fill = 'rgba(255, 255, 255, 0)' if fill == None else fill
        
        self.__id = DrawScheduler.registerShape(self.__draw)
        
    def __draw(self, canvas):
        canvas.draw_line((self.startX, self.startY), (self.endX, self.endY), self.lineWidth, self.fill)

    def __del__(self):
        DrawScheduler.destroyShape(self.__id)
        
App.initialize()
import simplegui
import math

class Color:
    def clamp8Bit(value):
        return max(0, min(int(value), 255))
    def clampDecimal(value):
        return max(0.0, min(value, 1.0))
    def clampPercent(value):
        return max(0, min(value, 100))
    def clampDegrees(value):
        return max(0, min(value, 360))
    
class RGB:
    def __init__(self, r, g, b):
        self.r = Color.clamp8Bit(r)
        self.g = Color.clamp8Bit(g)
        self.b = Color.clamp8Bit(b)

    def __str__(self):
        return f"rgb({self.r}, {self.g}, {self.b})"
class RGBA:
    def __init__(self, r, g, b, a):
        self.r = Color.clamp8Bit(r)
        self.g = Color.clamp8Bit(g)
        self.b = Color.clamp8Bit(b)
        self.a = Color.clampDecimal(a)
    
    def __str__(self):
        return f"rgb({self.r}, {self.g}, {self.b}, {self.a})"
class HSL:
    def __init__(self, h, s, l):
        self.h = Color.clampDegrees(h)
        self.s = Color.clampPercent(s)
        self.l = Color.clampPercent(l)
    
    def __str__(self):
        return f"HSL({self.h}, {self.s}%, {self.l}%)"    
class HSLA:
    def __init__(self, h, s, l, a):
        self.h = Color.clampDegrees(h)
        self.s = Color.clampPercent(s)
        self.l = Color.clampPercent(l)
        self.a = Color.clampDecimal(a)
    
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

class App:
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
    
    def getBackground():
        return App.__background
    def setBackground(color):
        App.__background = color
        App.__guiFrame.set_canvas_background(color)
    
    def onMouseClick(function):
        App.guiFrame.set_mouseclick_handler(function)
    def onMouseDrag(function):
        App.guiFrame.set_mousedrag_handler(function)

    def onKeyDown(function):
        App.__downFunction = function
    def onKeyUp(function):
        App.__upFunction = function
    def whileKeyDown(key, function):
        App.__keyHoldMap.update({simplegui.KEY_MAP[key] : function})

    def onUpdate(function):
        App.__updateFunction = function
        
    def textSize(text, size):
        return App.__guiFrame.get_canvas_textwidth(text, size)
    
class Rect:
    def __init__(self, startX, startY, width, height, fill=App.defaultFill, border=None, borderWidth=2):
        self.__startX = startX
        self.__startY = startY
        self.__width = width
        self.__height = height
        
        self.fill = fill
        self.border = 'rgba(255, 255, 255, 0)' if border == None else border
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
        return width * height
    
    startX = property(__getStartX, __setStartX)
    startY = property(__getStartY, __setStartY)
    width = property(__getWidth, __setWidth)
    height = property(__getHeight, __setHeight)
    centerX = property(__getCenterX, __setCenterX)
    centerY = property(__getCenterY, __setCenterY)
    area = property(__area)
    
    def __del__(self):
        DrawScheduler.destroyShape(self.__id)
class Circle:
    def __init__(self, centerX, centerY, radius, fill=App.defaultFill, border=None, borderWidth=2):
        self.centerX = centerX
        self.centerY = centerY
        self.radius = radius
        
        self.fill = fill
        self.border = 'rgba(255, 255, 255, 0)' if border == None else border
        self.borderWidth = borderWidth
        
        self.visible = True
        
        self.__id = DrawScheduler.registerShape(self.__draw)
    
    def __draw(self, canvas):
        if not self.visible:
            return
        canvas.draw_circle((self.centerX, self.centerY), self.radius, self.borderWidth, str(self.border), str(self.fill))
    
    def contains(self, x, y):
        return math.sqrt(((x - self.centerX) ** 2) + ((y - self.centerY) ** 2)) <= self.radius
    
    def __area(self):
        return math.PI * (self.radius ** 2.0)  

    area = property(__area)
    
    def __del__(self):
        DrawScheduler.destroyShape(self.__id)
class Polygon:
    def __init__(self, *args, fill=App.defaultFill, border=None, borderWidth=2):
        self.points = list(args)
        
        self.fill = fill
        self.border = 'rgba(255, 255, 255, 0)' if border == None else border
        self.borderWidth = borderWidth
        
        self.visible = True
        
        self.__id = DrawScheduler.registerShape(self.__draw)
        
    def __draw(self, canvas):
        if not self.visible:
            return
        canvas.draw_polygon(self.points, self.borderWidth, str(self.border), str(self.fill))

    def contains(self, x, y):
        raise NotImplementedError()
        
    def __del__(self):
        DrawScheduler.destroyShape(self.__id)   
class Text:
    def __init__(self, text, centerX, centerY, size, fill=App.defaultFill):
        self.__text = text
        self.__centerX = centerX
        self.__centerY = centerY
        self.__size = size
        
        self.fill = fill
        
        self.__recalculatePoint()
        
        DrawScheduler.registerShape(self.__draw)
        
    def __draw(self, canvas):
        canvas.draw_text(self.__text, self.__point, self.size, str(self.fill))
    
    def __recalculatePoint(self):
        self.__point = (self.__centerX - (App.textSize(self.__text, self.__size) / 2.0), self.__centerY + (self.__size / 4.0))
    
    def __width(self):
        return App.textSize(self.__text, self.size)
    
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
        
    text = property(__getText, __setText)
    centerX = property(__getCenterX, __setCenterX)
    centerY = property(__getCenterY, __setCenterY)
    size = property(__getSize, __setSize)
    width = property(__width)
    
    def contains(self, x, y):
        raise NotImplementedError()
    
    def __del__(self):
        DrawScheduler.destroyShape(self.__id)
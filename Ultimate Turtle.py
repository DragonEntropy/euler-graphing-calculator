import turtle
import math
import tkinter as tk

class Equation:
    def __init__(self, variables, image, calculate, defaults, format_list, template):
        super().__init__()
        self.variables = variables
        self.image = image
        self.calculate = calculate
        self.defaults = defaults
        self.format_list = format_list
        self.template = template
    def output(self, inputs):
        outputs = []
        for var in range(0, self.variables):
            if self.format_list[var] == 0:
                outputs.append(str(inputs[var]))
            elif self.format_list[var] == 1:
                if inputs[var] == 1:
                    outputs.append("")
                elif inputs[var] == -1:
                    outputs.append("-")
                else:
                    outputs.append(str(inputs[var]))
            elif self.format_list[var] == 2:
                if inputs[var] == 0:
                    outputs.append("")
                elif inputs[var] > 0:
                    outputs.append(" + " + str(inputs[var]))
                else:
                    outputs.append(" - " + str(inputs[var])[1:])
            elif self.format_list[var] == 3:
                if inputs[var] == 0:
                    outputs.append("")
                elif inputs[var] < 0:
                    outputs.append(" + " + str(inputs[var])[1:])
                else:
                    outputs.append(" - " + str(inputs[var]))
        return self.template.format(*outputs)

#All formulae for their respective calculations
def constant(eq_list, theta):
    return eq_list[0]
def linear(eq_list, theta):
    return eq_list[0] * (theta - eq_list[1])
def modulo(eq_list, theta):
    return eq_list[0] * ((theta - eq_list[1]) % eq_list[2]) + eq_list[3]
def sinusoidal(eq_list, theta):
    return eq_list[0] * math.cos(math.radians(eq_list[1] * (theta - eq_list[2]))) + eq_list[3]
def polynomial(eq_list, theta):
    return eq_list[0] * math.pow(theta - eq_list[1], eq_list[2]) + eq_list[3]
def exponential(eq_list, theta):
    return math.pow(eq_list[0], eq_list[1] * (theta - eq_list[2])) + eq_list[3]
def logarithmic(eq_list, theta):
    return eq_list[0] * math.log(theta - eq_list[2], eq_list[1]) + eq_list[3]

Constant = Equation(1, "constant.png", constant, [1], [0], "{0}")
Linear = Equation(2, "linear.png", linear, [1, 0], [1, 3], "{0}(theta{1})")
Modulo = Equation(4, "modulo.png", modulo, [0.01, 0, 90, 0], [1, 3, 0, 2], "{0}((theta{1})mod{2}){3}")
Sinusoidal = Equation(4, "sinusoidal.png", sinusoidal, [1, 1, 0, 0], [1, 1, 3, 2], "{0}cos({1}(theta{2})){3}")
Polynomial = Equation(4, "polynomial.png", polynomial, [1, 0, 2, 0], [1, 3, 0, 2], "{0}exp(theta{1}, {2}){3}")
Exponential = Equation(4, "exponential.png", exponential, [10, 1, 0, 0], [0, 1, 3, 2], "exp({0}, {1}(theta{2})){3}")
Logarithmic = Equation(4, "logarithmic.png", logarithmic, [1, 10, -1, 0], [1, 0, 3, 2], "{0}log((theta{2}), {1}){3}")
label_dict = {0: "A", 1: "B", 2: "C", 3: "D"}
equation_list = ["Constant", "Linear", "Modulo", "Sinusoidal", "Polynomial", "Exponential", "Logarithmic"]
equation_dict = {"Constant" : Constant, "Linear" : Linear, "Modulo" : Modulo, "Sinusoidal" : Sinusoidal, "Polynomial" : Polynomial, "Exponential" : Exponential, "Logarithmic" : Logarithmic}

mod_type_list = []
arg_type_list = []
    
def clearEquations():
    global mod_equations, arg_equations, mod_type_list, arg_type_list, equations
    mod_equations = []
    arg_equations = []
    mod_type_list = []
    arg_type_list = []
    equations = 0  

def sketch(plots, theta_factor): #Sketches the graph
    turtle.title("Ultimate Sketch")
    global mod_eq, arg_eq, t, alive
    t = turtle.Turtle()
    t.getscreen().screensize(3000, 3000)
    t.hideturtle()
    t.speed(10)
    t.penup()
    raw_theta = 0
    alive = True
    
    for eq in range(0, equations):
        print("The expression for the modulus of equation {0} is {1}".format(eq + 1, mod_type_list[eq].output(mod_equations[eq])))
        print("The expression for the argument of equation {0} is {1}".format(eq + 1, arg_type_list[eq].output(arg_equations[eq])))
    while raw_theta <= plots and alive == True:
        x = 0
        y = 0
        for eq in range (0, equations):
            mod = 100 * mod_type_list[eq].calculate(mod_equations[eq], raw_theta*theta_factor) #modulus calculation
            arg = math.radians(arg_type_list[eq].calculate(arg_equations[eq], raw_theta*theta_factor)) #argument calculation
            x += mod * math.cos(arg) #x-position calculation
            y += mod * math.sin(arg) #y-position calculation
        t.goto(x, y)
        if raw_theta == 0:
            t.pendown()
        raw_theta += 1
    clearEquations()

def parseEquation(input_dict, equation_dict, type_list, equations, eq): #Processes data from the input fields into an ordered list
    equation = []
    for field in input_dict:
        data = input_dict[field].get()
        if data == "":
            data = 0
        number = float(data)
        equation.append(number)
        #input_dict[field].delete(0, tk.END) #resets the fields
    equation_dict.append(equation)
    type_list.append(eq)

def submit():
    global mod_eq, arg_eq, equations
    equations += 1
    parseEquation(mod_dict, mod_equations, mod_type_list, equations, mod_eq)
    parseEquation(arg_dict, arg_equations, arg_type_list, equations, arg_eq)

def graph():
    global mod_eq, arg_eq, equations
    equations += 1
    parseEquation(mod_dict, mod_equations, mod_type_list, equations, mod_eq)
    parseEquation(arg_dict, arg_equations, arg_type_list, equations, arg_eq)
    plots = int(points.get())
    theta_factor = 360 / plots
    sketch(plots, theta_factor)

def reset():
    global alive
    alive = False
    turtle.Screen().clear()
    clearEquations()

def launchWindow(): #Uses a custom GUI for entering formulae
    clearEquations()
    window = tk.Tk()
    window.title("Ultimate graphing calculator - Alexander Jephtha")
    
    global mod_dict, arg_dict
    mod_dict = {}
    arg_dict = {}
    #window.attributes("-fullscreen", True) #For fullscreen

    def modulusUpdate(equation):
        global mod_formula, mod_variables, mod_eq
        mod_eq = equation_dict.get(equation)
        try:
            mod_formula.pack_forget()
            mod_variables.forget()
        except NameError:
            pass
        
        #Modulus formula image section
        global mod_img
        mod_formula = tk.Canvas(master = mod_frame, width = 700, height = 80)
        mod_img = tk.PhotoImage(file = "mod_" + mod_eq.image)
        mod_formula.create_image(350, 40, image = mod_img)

        #Input fields for modulus variables
        mod_variables = tk.Frame(master = mod_frame)
        for i in range(0, mod_eq.variables):
            frame = tk.Frame(master = mod_variables, borderwidth = 1, padx = 20)
            frame.grid(row = 0, column = i)
            name = tk.Label(master = frame, text = label_dict[i] + ": ")
            input_field = "input"+str(label_dict[i])
            mod_dict[input_field] = tk.Entry(master = frame, width = 5)
            mod_dict[input_field].insert(0, mod_eq.defaults[i])
            name.pack()
            mod_dict[input_field].pack()
            
        mod_formula.pack()
        mod_variables.pack()

    def argumentUpdate(equation):
        global arg_formula, arg_variables, arg_eq
        arg_eq = equation_dict.get(equation)
        try:
            arg_formula.pack_forget()
            arg_variables.forget()
        except NameError:
            pass
        
        #Argument formula image section
        global arg_img
        arg_formula = tk.Canvas(master = arg_frame, width = 800, height = 80)
        arg_img = tk.PhotoImage(file = "arg_" + arg_eq.image)
        arg_formula.create_image(400, 40, image = arg_img)

        #Input fields for argument variables
        arg_variables = tk.Frame(master = arg_frame)
        for i in range(0, arg_eq.variables):
            frame = tk.Frame(master = arg_variables, borderwidth = 0, padx = 20)
            frame.grid(row = 0, column = i)
            name = tk.Label(master = frame, text = label_dict[i] + ": ")
            input_field = "input"+str(label_dict[i])
            arg_dict[input_field] = tk.Entry(master = frame, width = 5)
            arg_dict[input_field].insert(0, arg_eq.defaults[i])
            name.pack()
            arg_dict[input_field].pack()

        arg_formula.pack()
        arg_variables.pack()

    #Title section
    text_list = [
        tk.Label(text = "Ultimate graphing calculator", width = 100, font = ("lucida 20 bold italic", 25)),
        tk.Label(text = "1. Select the type of equation for the modulus and argument", width = 100, font = ("lucida 20 bold italic", 11)),
        tk.Label(text = "2. Enter the variables for your equation below", width = 100, font = ("lucida 20 bold italic", 11)),
        tk.Label(text = "3. Click submit and graph to graph the function", width = 100, font = ("lucida 20 bold italic", 11)),
        tk.Label(text = "4. Alternatively, click submit and add another to sum multiple equations", width = 100, font = ("lucida 20 bold italic", 11))
        ]
    
    #Main frame to split modulus formulae from argument formulae
    main_frame = tk.Frame()
    mod_frame = tk.Frame(master = main_frame, borderwidth = 1, padx = 0)
    arg_frame = tk.Frame(master = main_frame, borderwidth = 1, padx = 0)
    mod_frame.grid(row = 0, column = 0)
    arg_frame.grid(row = 0, column = 1)

    #Modulus formula menu
    mod_selection = tk.Frame(master = mod_frame)
    mod_equation = tk.StringVar(master = mod_selection, value = "Constant")
    mod_dropdown_label = tk.Label(master = mod_selection, text = "Modulus formula: ")
    mod_dropdown_menu = tk.OptionMenu(mod_selection, mod_equation, equation_list[0], *equation_list[1:], command = modulusUpdate)
    mod_dropdown_label.grid(row = 0, column = 0)
    mod_dropdown_menu.grid(row = 0, column = 1)
    mod_selection.pack()
    #Argument formula menu
    arg_selection = tk.Frame(master = arg_frame)
    arg_equation = tk.StringVar(master = arg_selection, value = "Linear")
    arg_dropdown_label = tk.Label(master = arg_selection, text = "Argument formula: ")
    arg_dropdown_menu = tk.OptionMenu(arg_selection, arg_equation, equation_list[0], *equation_list[1:], command = argumentUpdate)
    arg_dropdown_label.grid(row = 0, column = 0)
    arg_dropdown_menu.grid(row = 0, column = 1)
    arg_selection.pack()

    #Default modulus and argument formulae
    modulusUpdate("Constant")
    argumentUpdate("Linear")

    #Points plotted for determining precision section
    sub_variables = tk.Frame(pady = 15)
    points_label = tk.Label(master = sub_variables, text = "Points to plot: ")
    points_label.grid(row = 0, column = 0)
    global points
    points = tk.Entry(master = sub_variables, width = 5)
    points.insert(0, "360")
    points.grid(row = 0, column = 1)

    #Submit and graph buttons section
    bottom = tk.Frame()
    submitButton = tk.Button(master = bottom, text = "Submit and add another", width = 20, height = 1, command = submit)
    submitButton.grid(row = 0, column = 0, padx = 10)
    graphButton = tk.Button(master = bottom, text = "Submit and graph", width = 20, height = 1, command = graph)
    graphButton.grid(row = 0, column = 1, padx = 10)
    resetButton = tk.Button(master = bottom, text = "Clear the graph", width = 20, height = 1, command = reset)
    resetButton.grid(row = 0, column = 2, padx = 10)

    buffer = tk.Frame(height = 15)
    
    for text in text_list:
        text.pack()
    elements = [main_frame, sub_variables, bottom, buffer]
    for part in elements:
        part.pack()

    window.mainloop()

launchWindow()

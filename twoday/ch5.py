#%%
class Student: 
    def __init__(self, name): 
        self.__name = name 
  
s1 = Student("Santhosh") 
s1.__name = "see"
s1.age = 20
print(s1.__name, s1._Student__name, s1.age)

# %%
s1._Student__name

# %%
s2 = Student("Taylor")
s1._Student__name

# %%
# class attributes are shared among all instances
class ML:
    data = {'x': [0, 1, 2, 3, 4],
            'y': [1, 2, 3, 4, 5]}
    
    def __init__(self, method):
        self.method = method

    def run(self):
        # you can access class attribute with self. A better way is to wrap self with type()
        print(f'{self.method}, a={self.data["x"]}, {id(self.data)}')
        
pca = ML('PCA')
pca.run()

# %%
rf = ML('RF')
rf.data['x'][0] = -1
rf.run()

# %%
nn = ML('NN')
nn.run()

# %%
# __call__
class A:
    pass

a = A()

A.__call__

# %%
class A:
    def __call__():
        print("called from A")

a = A()
    
print(A.__call__.__call__.__call__)

# %%
import dis

dis.dis(A.__call__)

# %%
dis.dis(A.__call__.__call__)
# %%

# %%
class Counter():
    count = 0
    
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self):
        self.count += 1
        
# Counter()
# c1 = Counter()
# c2 = Counter()
# print(Counter.count, Counter.count)
# c1()

# print(Counter.count, Counter.count)


# %%
@Counter
def timed_func():
    pass

timed_func()
timed_func()

timed_func.count
# %%

# %%
# class as attribute of an instance
###########################Descriptor#############################
class Weather:
    def __init__(self, temp):
        self.temp = temp
        
w1 = Weather(-300)
print(f"today's temperature is {w1.temp} degrees")

#%%
class Weather:
    def __init__(self):
        ...
    
    def getter(self):
        try:
            return self.z
        except AttributeError:
            print("temperature not set")
    
    def setter(self, y):
        print("entering setter")
        if y > -275:
            self.z = y
        else:
            raise ValueError("too low")
            print('not allowed')
            
    temperature = property(getter, setter)
        
w1 = Weather()
w1.temperature = -300
print(f"today's temperature is {w1.temperature} degrees")
# print(w1.temperature)

#%%
import time

class TimeDesc:
    def __get__(self, obj, objtype=None):
        return time.time()

class UseCase:
    size = TimeDesc()
    def __init__(self):
        pass
# %%
import time
d1 = UseCase()
print(d1.size)
time.sleep(1)
print(UseCase.size)


# %%
class Desc:
    def __get__(self, obj, type=None):
        # is type the function?
        print(f"getting value from {type(obj)}")

class Base:
    attr1 = Desc()
    
inst1 = Base()
print(inst1.attr1)

# %%
class MyDescriptor:
    def __get__(self, instance, owner):
        print(f"self: {self}")           # The descriptor instance
        print(f"instance: {instance}")   # The instance of MyClass (or None if accessed via the class)
        print(f"owner: {owner}")         # The class MyClass (or a subclass)

class MyClass:
    attr = MyDescriptor()

# Access via instance
obj = MyClass()
obj.attr

# Access via class
MyClass.attr


# %%
class TempDesc:
    def __get__(self, instance, owner):
        try:
            return instance.z
        except Exception:
            print("Haven't set temperature.")
            
    def __set__(self, instance, value):
        if value > -273:
            instance.z = value
        else:
            print("not allowed.")
            
class NewTemp:
    temperature = TempDesc()
    
nt1 = NewTemp()
# %%
nt1.temperature = 300
print(nt1.temperature)
# %%
nt1.temperature=-300
print(nt1.temperature)
# %%

import time

class LazyProperty:
    def __init__(self, function):
        self.function = function
        self.name = function.__name__

    def __get__(self, obj, type=None) -> object:
        print("here")
        obj.__dict__[self.name] = self.function(obj)
        return obj.__dict__[self.name]

class DeepThought:
    @LazyProperty
    def meaning_of_life(self):
        time.sleep(1)
        return 42

my_deep_thought_instance = DeepThought()
print(my_deep_thought_instance.__dict__)
# %%


print(my_deep_thought_instance.meaning_of_life)
print(my_deep_thought_instance.__dict__)
# %%

print(my_deep_thought_instance.meaning_of_life)
print(my_deep_thought_instance.meaning_of_life)
# %%
class Student:
    def __init__(self):
        self.score = []
        
    def score_input(self, value):
        self.score.append(value)
        
    @staticmethod
    def grade(value):
        if 0 <= value < 60:
            return "fail"
        elif 60 <= value <90:
            return "pass"
        else:
            return "great"
            

#%%
s1 = Student()
print(s1.grade(90))
print(Student.grade(61))

#%%
class Student:
    def __init__(self):
        self.score = []
        
    def score_input(self, value):
        self.score.append(value)
        
    @staticmethod
    def read(name, score):
        s = Student()
        s.score = score
        return s
    
class FirstYear(Student):
    pass
          

#%%
fys = FirstYear()
type(fys.read("Alice", [60, 70, 90]))

#%%
import time
class Example:
    def __init__(self, ML):
        self.ML = ML
        
    @staticmethod
    def decor(func):
        def wrapper(*args, **kwargs):
            print(f"starting time: {time.time()}")
            func(*args, **kwargs)
            print(f"end execution, {time.time()}")
        return wrapper
        
    @decor
    def run(self):
        print(f'calling {self.ML}')
        time.sleep(1)
        return 0
    
    # want to add some loggin information with a decorator
    

#  %%
e1 = Example("RF")
e1.run()

# %%
from abc import ABC, abstractmethod
import torch.nn as nn

class NeuralNet(ABC, nn.Module):
    @abstractmethod
    def __init__(self):
        super(NeuralNet, self).__init__()

    @abstractmethod
    def forward(self, x):
        pass
    
    def train_model(self, data, labels):
        # Placeholder for a generic training method
        pass

    def evaluate_model(self, data, labels):
        # Placeholder for a generic evaluation method
        pass

# Example of a Deep Neural Network (DNN)
class DNN(NeuralNet):
    def __init__(self, input_size, hidden_size, output_size):
        super(DNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Example of a Convolutional Neural Network (CNN)
class CNN(NeuralNet):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(32 * 13 * 13, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = x.view(-1, 32 * 13 * 13)
        x = self.fc1(x)
        return x

# Example of a Recurrent Neural Network (RNN)
class RNN(NeuralNet):
    def __init__(self, input_size, hidden_size, output_size, num_layers=1):
        super(RNN, self).__init__()
        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(1, x.size(0), self.hidden_size)
        out, _ = self.rnn(x, h0)
        out = self.fc(out[:, -1, :])
        return out
    
    
#%%
from abc import ABC, abstractmethod
class NeuralNet(ABC):
    @abstractmethod
    def __init__(self):
        super().__init__()

    @abstractmethod
    def forward(self, x):
        pass
    
    def train_model(self, data, labels):
        pass
n1 = NeuralNet()

#%%
from abc import ABC, abstractmethod
class MLClass:
    def __init__(self, data):
        self.data = data

class NeuralNet(MLClass):
    def __init__(self, data):
        super().__init__(data)

    def forward(self, x):
        pass

class Predictor(MLClass):
    def __init__(self, data, model=""):
        super().__init__(data)
        self.model = model
        
    def pred(self, x):
        print(f"{self.model} predicts at {x}")
        

# %%
class DNN(NeuralNet, Predictor):
    def __init__(self, data):
        super().__init__(data)


d1 = DNN(1, "model1")
d1.model
# %%

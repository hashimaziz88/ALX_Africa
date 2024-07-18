class A:
    def greet(self):
        return "Hello from Class A"

class B(A):
    def greet(self):
        return "Hello from Class B"

class C(A):
    def greet(self):
        return "Hello from Class C"

class D(B,C):
    pass

obj_a = A()
print(obj_a.greet())
obj_b = B()
print(obj_b.greet())
obj_c = C()
print(obj_c.greet())
obj_d = D()
print(obj_d.greet())
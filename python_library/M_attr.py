import attr


@attr.s
class Person:
    name: str = attr.ib()
    age: int = attr.ib()
    email: str = attr.ib(default="")

p1 = Person("Alice", 25, "alice@example.com")
p2 = Person("Bob", 30)

print(p1)
# output: Person(name='Alice', age=25, email='alice@example.com')

print(p1 == p2)
# output: False

p1_dict = attr.asdict(p1)
print(p1_dict)
import person_pb2

person = person_pb2.Person()
person.id = 1234
person.name = "John Doe"
person.email = "jdoe@example.com"
phone = person.phones.add()
phone.number = "555-4321"
phone.type = person_pb2.Person.HOME

print("person of type:", type(person), person)

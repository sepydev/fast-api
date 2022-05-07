from tasks import add

result = add.delay(3, 3)
result.ready()
result.get()

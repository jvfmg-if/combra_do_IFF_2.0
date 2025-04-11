
def insertes(lista):
  
  for x in lista:
    insert = f"INSERT INTO Ambulatorios VALUES({x})"
    print(f"{insert};\n")

insertes(['1, 1, 30',
	'2, 1, 50',
	'3, 2, 40',
	'4, 2, 25',
	'5, 2, 55'

])
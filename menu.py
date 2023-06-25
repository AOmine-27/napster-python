def printMenu():
  print('\nSelect 1 action (press 1 to 4)')
  print('1. JOIN')
  print('2. SEARCH')
  print('3. DOWNLOAD')

def executeCommand(arg):
  if arg == "1":
    return 'JOIN'
  elif arg == "2":
    return 'SEARCH'
  elif arg == "3":
    return 'DOWNLOAD'
  else: 
    print("Invalid option. Quitting...")
    return 'QUIT' 
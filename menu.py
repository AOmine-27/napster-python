def printMenu():
  print('\nSelect 1 action')
  print('1. JOIN')
  print('2. SEARCH')
  print('3. DOWNLOAD')
  print('Or any key to quit.')

def executeCommand(arg):
  if arg == "1":
    return 'JOIN'
  elif arg == "2":
    return 'SEARCH'
  elif arg == "3":
    return 'DOWNLOAD'
  else: 
    print("Quitting...")
    return 'QUIT' 
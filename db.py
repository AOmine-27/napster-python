import json
FILE_NAME = 'server-data.json'

def appendPeerData(files_array, peer_ip, peer_port):
  with open(FILE_NAME, "r") as file:
    data = json.load(file)
  if (data["lock"] == True):
    print("Failed to update server db, try again later.")
    return
  else:
    data["lock"] = True
    with open(FILE_NAME, "w") as file:
      json.dump(data, file)

    new_data = {
      "peer_ip": peer_ip,
      "peer_port": peer_port,
      "files": files_array
    }
    data["data"].append(new_data)
    data["lock"] = False
    with open(FILE_NAME, "w") as file:
      json.dump(data, file)

def clearDb():
  with open(FILE_NAME, "r") as file:
    data = json.load(file)
  data["lock"] = False
  data["data"] = []
  with open(FILE_NAME, "w") as file:
    json.dump(data, file)
  print("DB cleared")

def searchFile(file_name):
  peers_with_file = []
  with open(FILE_NAME, "r") as file:
    data = json.load(file)
  data["data"]
  for peer in data["data"]:
    if file_name in peer["files"]:
      peers_with_file.append({
        "peer_ip": peer["peer_ip"],
        "peer_port": peer["peer_port"]
      })
  if (len(peers_with_file) > 0):
    return peers_with_file
  else:
    print("Not peers with the file were found")
    return -1
  print(peers_with_file)

def updatePeerData(files_array, peer_ip, peer_port):
  # Check if file is already being used by another process
  with open(FILE_NAME, "r") as file:
      data = json.load(file)
  if (data["lock"] == True):
    print("Failed to update server db, try again later.")
    return
  else:
    # Locks the file so no other process uses it
    data["lock"] = True
    with open(FILE_NAME, "w") as file:
      json.dump(data, file)

    # Search for the peer data to update
    for peer in data["data"]:
      if (peer["peer_ip"] == peer_ip and peer["peer_port"] == peer_port):
        peer["files"] = files_array

    data["lock"] = False
    with open(FILE_NAME, "w") as file:
      json.dump(data, file)

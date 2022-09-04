from benserver import server

def dht(data):
    temperature = data["temperature"]
    humidity = data["humidity"]
    print(f"Temperature: {temperature}")
    print(f"humidity: {humidity}")
    return {"message":"ok"}
server1 = server("0.0.0.0",8585)
server1.add_action_handler("dhtsensor",dht)
server1.start()
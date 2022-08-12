from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y--%H:%M:%S")
print(dt_string)
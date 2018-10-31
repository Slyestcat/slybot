import re
import socket

# --------------------------------------------- Start Settings ----------------------------------------------------
HOST = "irc.twitch.tv"                          # Hostname of the IRC-Server in this case twitch's
PORT = 6667                                     # Default IRC-Port
CHAN = "#slyestcat"                               # Channelname = #{nickname}
NICK = "Slyestbot"                                # Nickname = Twitch username
PASS = "redacted"   						# www.twitchapps.com/tmi/ will help to retrieve the required authkey
# --------------------------------------------- End Settings -------------------------------------------------------


# --------------------------------------------- Start Functions ----------------------------------------------------
def send_pong(msg):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(chan, msg):
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


def send_nick(nick):
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password):
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan):
    con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan):
    con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))
# --------------------------------------------- End Functions ------------------------------------------------------


# --------------------------------------------- Start Helper Functions ---------------------------------------------
def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result


def parse_message(msg):
    if len(msg) >= 1:
        msg = msg.split(' ')
        options = {'!test': command_test,
                   '!twitter': command_twitter,
				   '!youtube': command_youtube,
				   '!prime': command_prime,
				   '!twitchprime': command_prime,
				   '!sub': command_sub,
				   '!subscribe': command_sub,
				   '!discord': command_discord,
				   '!donate': command_donate,
				   '!snapchat': command_snapchat,
				   'hello?': command_hello,
				   'meow': command_meow,
				   'hi': command_hi,
				   'bye': command_bye}
        if msg[0] in options:
            options[msg[0]]()
# --------------------------------------------- End Helper Functions -----------------------------------------------


# --------------------------------------------- Start Command Functions --------------------------------------------
def command_test():
    send_message(CHAN, "testing")

def command_twitter():
    send_message(CHAN, "You can find Sly's Twitter at https://twitter.com/Jarrvd")
	
def command_youtube():
	send_message(CHAN, "You can find Sly's Youtube at https://youtube.com/Slyestcat")

def command_prime():
	send_message(CHAN, "Amazon Prime members get a free Twitch subscription each month. Link Your Account Here: twitch.amazon.com/prime Using: i.imgur.com/NvVFM1B")

def command_sub():
	send_message(CHAN, "Support Sly by subsribing to his channel at https://www.twitch.tv/products/slyestcat")

def command_discord():
	send_message(CHAN, "You can join Sly's Discord channel at https://discord.gg/XkyyCdx")

def command_donate():
	send_message(CHAN, "You can support Sly with donations at https://www.twitchalerts.com/donate/slyestcat") 
	
def command_snapchat():
	send_message(CHAN, "Sly's snap is 'Slyestcat'")

def command_hello():
	send_message(CHAN, "is it me you're looking for? (ditto)")

def command_meow():
	send_message(CHAN, "https://goo.gl/LQEVQz") #TODO make this pull from a database of cat images and display a new imgur link each time

def command_hi():
	send_message(CHAN, "Hi") #TODO make this say "Hi, $user" with the username of who pulled the request

def command_bye():
	send_message(CHAN, "Bye! Thanks for watching!")
# --------------------------------------------- End Command Functions ----------------------------------------------

con = socket.socket()
con.connect((HOST, PORT))

send_pass(PASS)
send_nick(NICK)
join_channel(CHAN)

data = ""

while True:
    try:
        data = data+con.recv(1024).decode('UTF-8')
        data_split = re.split(r"[~\r\n]+", data)
        data = data_split.pop()

        for line in data_split:
            line = str.rstrip(line)
            line = str.split(line)

            if len(line) >= 1:
                if line[0] == 'PING':
                    send_pong(line[1])

                if line[1] == 'PRIVMSG':
                    sender = get_sender(line[0])
                    message = get_message(line)
                    parse_message(message)

                    print(sender + ": " + message)

    except socket.error:
        print("Socket died")

    except socket.timeout:
        print("Socket timeout")

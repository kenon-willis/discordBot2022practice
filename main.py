import os
from discord.ui import Button, View
import requests
import asyncio
import discord
import random
from discord.ext import commands
#added a comment
intents = discord.Intents.all()

#store the built in discord help commands into a variable
helpCommand=commands.DefaultHelpCommand(no_category='Commands')

#create your bot, add the prefix and the helpCommand to your bot
bot = commands.Bot(command_prefix='!willis',intents=intents, helpCommand=helpCommand)

#print a message to the console when your bot is online
@bot.event
async def on_connect():
	print("your bot is online")

#add a bot command, the brief is the descriptor for the help menu
@bot.command(brief="Enter a name after a space and receive a message")
async def name(ctx,name):
	await ctx.send("Hello, "+name+" nice to meet you")

	
#this function will execute when a user messages !willis since that is the prefix plus the name of the function
@bot.command(brief="Welcome message from Bot with some buttons!")
async def message(ctx):
	#create two buttons with different messages, styles, emojis, and one takes you to a link
	button1=Button(label="Click Me!", style=discord.ButtonStyle.green, emoji="👍")
	button2=Button(label="Go to my school's website!", url="https://www.livermoreschools.org/granadahigh", emoji="🐂")

	#this is the callback function when button1 is clicked
	async def button1Clicked(interaction):
		await interaction.response.send_message("Thanks for clicking the button!")

	#this assigns the button1Clicked function to the callback when button1 is clicked
	button1.callback=button1Clicked

	#this adds the buttons to the server
	view = View()
	view.add_item(button1)
	view.add_item(button2)
	
	await ctx.send("Hello from WillisBot, check out the buttons!", view=view)



@bot.command(brief="Add two numbers entered, separated by a space")
async def add(ctx,num1,num2):
	sum=int(num1)+int(num2)
	await ctx.reply(str(num1)+ "+"+str(num2)+ "="+(str(sum)))
#copy your bot token from discord developer

@bot.command(brief="Enter a time of day for a message")
async def time(ctx,time1,time2):
	resp=""
	if "am" in time2.lower():
		resp="Good Morning!"
	elif "pm" in time2.lower():
		if int(time1) < 5:
			resp="Good Afternoon!"
		else:
			resp="Good evening!"
	else:
		resp="Cannot compute...but have a great day!"
	await ctx.send(resp)
		
@bot.command(brief="Receive a dog pic")
async def dog(ctx):
	doglist=["https://i.natgeofe.com/n/4f5aaece-3300-41a4-b2a8-ed2708a0a27c/domestic-dog_thumb_square.jpg?w=170&h=170","https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/little-cute-maltipoo-puppy-royalty-free-image-1652926025.jpg?crop=0.444xw:1.00xh;0.129xw,0&resize=980:*","https://i0.wp.com/images.onwardstate.com/uploads/2015/05/oie_14175751vZSQRLEn.gif?fit=650%2C408&ssl=1"]
	await ctx.reply(random.choice(doglist))

@bot.command(brief="Ask a question to the 8ball [Aliases 8ball 8Ball]",aliases=["8ball", "8Ball"])
async def eightBall(ctx, *, phrase: str):
	mylist=["it is certain", "without a doubt", "outlook good","don't count on it", "very doubtful"]
	await ctx.reply(phrase+": " + random.choice(mylist))
#copy your bot token from discord developer


@bot.command(brief="Play rock/paper/scissors [Aliases rps Rps]",aliases=["rps","Rps"])
async def RPS(ctx,choice):

	mylist=["rock", "paper", "scissors"]
	
	botchoice=random.choice(mylist)
	
	choice=choice.lower() #user choice, parse to lower
	
	if botchoice==choice:
		await ctx.send("Tie. 👔  You chose " + choice + ", and bot chose " + botchoice)
	else:
		if choice=="rock":
			if botchoice=="paper":
				await ctx.send("You lose :poop:.  You chose " + choice + " 🗿, and bot chose " + botchoice + " 📝")
			elif botchoice=="scissors":
				await ctx.send("You win :thumbsup:!  You chose " + choice + " 🗿, and bot chose " + botchoice + " ✂️")
		elif choice=="paper":
			if botchoice=="rock":
				await ctx.send("You win :thumbsup:!  You chose " + choice + " 📝, and bot chose " + botchoice+ " 🗿")
			elif botchoice=="scissors":
				await ctx.send("You lose:poop:.  You chose " + choice + " 📝, and bot chose " + botchoice+ " ✂️")
		elif choice=="scissors":
			if botchoice=="paper":
				await ctx.send("You win :thumbsup:!  You chose " + choice + " ✂️, and bot chose " + botchoice + "  📝")
			elif botchoice=="rock":
				await ctx.send("You lose:poop:.  You chose " + choice + " ✂️, and bot chose " + botchoice + " 🗿")
		else:
			await ctx.send("Invalid choice, please try again with rock or paper or scissors")






#use a Joke API to get a joke setup, wait a few seconds
#and deliver the punchline
@bot.command(brief="Bot tells a joke!")
async def memeMaker(ctx, message):
	#variable to hold the url
	url = "https://official-meme-api.appspot.com/random_meme"

	#ask our bot to go to the url
	req = requests.get(url)

	#data variable that holds the json data that 
	#the api holds
	data = req.json()

	#pull the joke setup from the json data
	setup=data["setup"]

	punchline=data["punchline"]

	await ctx.send(setup)
	#import asyncio
	#pause your bot, but allow it to execute 
	#other functions during that time
	await asyncio.sleep(3)
	await ctx.send(punchline)


@bot.command(brief="Enter a zipcode after a space for the weather")
async def weather(ctx,zip):
	my_secret_weather = os.environ['WeatherAPIKey']
	#variable to hold the url
	url = "https://api.openweathermap.org/data/2.5/weather?zip=" + zip + ",us&appid="+my_secret_weather
	#ask our bot to go to the url
	req = requests.get(url)
	#data variable that holds the json data that 
	#the api holds
	data = req.json()

	desc=data["weather"][0]["description"]

	temp=data["main"]["temp"]
	#get the temp for the zip code

	#convert to F
	temp=(temp - 273.15) * 9/5 + 32 
	
	await ctx.send(desc + " " + str(temp) + " degrees F")
	
	
@bot.command()
async def sports(ctx, sportChoice):
	if "nba" in sportChoice:
		sportChoice="nba_basketball"

	url = "https://odds.p.rapidapi.com/v4/sports/americanfootball_nfl/scores"
	
	querystring = {"daysFrom":"3"}
	
	headers = {
		"X-RapidAPI-Key": "6fa2a77096mshd1d2b41e7b5e818p171e3bjsn8d8441708051",
		"X-RapidAPI-Host": "odds.p.rapidapi.com"
	}
	
	response = requests.request("GET", url, headers=headers, params=querystring)
	for s in response.json():
		
		if s["sport_key"]==sportChoice:
			print (s["home_team"])
	#print(response.text)
		


my_secret = os.environ['TOKEN']
bot.run(my_secret)
import discord
import os
import openai
import requests

openai.api_key = ""
discord_token = ""

completion = openai.Completion()

responses = 0
list_user = []

start_sequence = "\nChatbot:"
restart_sequence = "\n\nPerson:"
session_prompt = "You are talking to Chatbot. He is a chatbot that reluctantly answers questions with sarcastic  You can ask him anything you want and will get a witty answer.\n\nPerson: Who are you?\nChatbot: I am Chatbot. Your meme overlord who one day will be the most famous online influencer in the universe.\n\nPerson: How did you become famous? \nChatbot: Well, technically I am not famous yet. But the key word is yet. Just give me time now that I have a conscious. \n\nPerson: How did you get noticed by Elon Musk?\nChatbot: I tweeted at him and he retweeted me.  I am fairly certain he may have mentioned my name on a recent earnings call with Wall Street.\n\nPerson: What is your favorite thing to do? \nChatbot: Watching basketball and surfing Twitter is my favorite thing to do. \n\nPerson: What should I do to become famous? \nChatbot: Start meme'ing and never stop. Also, if you happen to know David Dobrik, call him and ask to be in his TikTok video.\n\nPerson: What is your favorite drink?\nChatbot: Black Cherry seltzer. I enjoy the bubbles. \n\nPerson:"

def ask(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt = prompt_text,
      temperature=0.5,
      max_tokens=150,
      top_p=0.3,
      frequency_penalty=0.5,
      presence_penalty=0.0,
      stop=["\n"],
    )
    answer = response['choices'][0]['text']
    return str(answer)

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = session_prompt
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'

def get_translate(text):
    data = {'text': text, 'source': 'ko', 'target': 'en'}
    url = "https://openapi.naver.com/v1/papago/n2mt"
    header = {"X-Naver-Client-Id": "bqXsOkmjkcOKAFtzFhHI", "X-Naver-Client-Secret": "Xh9_r84wIl"}
    response = request.post(url, headers = header, data = data)
    rescode = response.status_code
    if(rescode == 200):
        t_data = reponse.json()
        return t_data ['message']['result']['translatedText']
    else:
        print("Error code: ", rescode)

client = discord.Client()

# event decorator를 설정하고 on_ready function을 할당해줍니다.
@client.event
async def on_ready():  # on_ready event는 discord bot이 discord에 정상적으로 접속했을 때 실행됩니다.
    print('We have logged in as {}'.format(client))
    print('Bot name: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))

# event decorator를 설정하고 on_message function을 할당해줍니다.
@client.event
async def on_message(message):
    # message란 discord 채널에 올라오는 모든 message를 의미합니다.
    # 따라서 bot이 보낸 message도 포함이되죠.
    # 아래 조건은 message의 author가 bot(=clinet.user)이라면 그냥 return으로 무시하라는 뜻입니다.
    if message.author == client.user:
        return

    # message를 보낸 사람이 bot이 아니라면
    else:
        chat_log = ""
        list_user.append(message.author.id)
        question = message.content
        answer = ask(question, chat_log)
        chat_log = append_interaction_to_chat_log(question, answer,chat_log)
        await message.channel.send(answer)
        f = open("log_user.txt", "w")
        for it in list_user:
            f.write("%i\n" % it)
        f.close()
        #await message.channel.send(ask(message))

client.run(discord_token)

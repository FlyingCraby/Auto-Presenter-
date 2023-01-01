import speech_recognition as sr
import time
from gtts import gTTS
import serial
import os
import wolframalpha
import openai
import urllib.request

state = 0
trys = 0
name = ""
qanswered = 0
client = wolframalpha.Client('TYPE IN HERE')
openailog = ""
thisdict =  {
  "What is the size of american goldfinch": "The length is 5 inches and the wingspan is 19 to 22 centermeter. ",
  "size": "The length is 5 inches and the wingspan is 19 to 22 centermeter. ",
  "size of": "The length is 5 inches and the wingspan is 19 to 22 centermeter. ",
  "What color do they have with plumage": "Spring males have brilliant yellow and shiny black and a bit of white while females and winter birds are more dull.", 
  "color": "Spring males have brilliant yellow and shiny black and a bit of white while females and winter birds are more dull.", 
  "color of plumage": "Spring males have brilliant yellow and shiny black and a bit of white while females and winter birds are more dull.", 
  "color of feather": "Spring males have brilliant yellow and shiny black and a bit of white while females and winter birds are more dull.", 
  "plumage": "Spring males have brilliant yellow and shiny black and a bit of white while females and winter birds are more dull.", 
  "feather": "Spring males have brilliant yellow and shiny black and a bit of white while females and winter birds are more dull.", 
  "What kind of body parts do they have": "They have conical bill; pointed, notched tail and wingbars.",
  "body parts": "We have conical bill; pointed, notched tail and wingbars.",
  "body": "We have conical bill; pointed, notched tail and wingbars.",
  "Field Marks": "We have conical bill; pointed, notched tail and wingbars.",
  "What do they look like": "We have conical bill; pointed, notched tail and wingbars.",
  "look like": "We have conical bill; pointed, notched tail and wingbars.",
  "What food do they eat": "We eats mostly seeds, but we do eat some insects. We mostly eat seeds from the daisy(composite) family, weeds and grasses, and small seeds from trees such as elm, birch, and alder. We also eat insects to a limited extent in the summer.",
  "food": "We eats mostly seeds, but we do eat some insects. We mostly eat seeds from the daisy(composite) family, weeds and grasses, and small seeds from trees such as elm, birch, and alder. We also eat insects to a limited extent in the summer.",
  "eat": "We eats mostly seeds, but we do eat some insects. We mostly eat seeds from the daisy(composite) family, weeds and grasses, and small seeds from trees such as elm, birch, and alder. We also eat insects to a limited extent in the summer.",
  "How do they find food": "We usually climbs on to plants to reach the seeds for food.",
  "find food": "We usually climbs on to plants to reach the seeds for food.",
  "How to find food": "We usually climbs on to plants to reach the seeds for food.",
  "Where do they build nests": "Females normally build nests in a high shrub where two or three vertical branches connect.",
  "nest": "Females normally build nests in a high shrub where two or three vertical branches connect. The nest is usually made out of plant fiber lined with plants down.",
  "nests": "Females normally build nests in a high shrub where two or three vertical branches connect. The nest is usually made out of plant fiber lined with plants down.",
  "build nests": "Females normally build nests in a high shrub where two or three vertical branches connect. The nest is usually made out of plant fiber lined with plants down.",
  "build": "Females normally build nests in a high shrub where two or three vertical branches connect. The nest is usually made out of plant fiber lined with plants down.",
  "egg": "Number of eggs:2-7 eggs; Size of eggs:The length of the egg is about 0.6-0.7 inch and the width of the egg is about 0.5inch. Color of eggs:The egg is pale bluish white and sometimes there are faint brown spots around the large end. Incubation period:12-14 days",
  "nesting period": "The nestling period for a us is 11- to 17 days",
  "location": "We mostly lives in the United States. Though We also live at southern canada and northern mexico",
  "where do they live": "We mostly lives in the United States. Though We also live at southern canada and northern mexico",
  "live": "We mostly lives in the United States. Though We also live at southern canada and northern mexico",
  "environment": "Our main habitat is weedy fields and floodplains where plants such as thistles and asters grow.  We are also found in roadsides, orchards, and backyards.",
  "habitat": "our main habitat is weedy fields and floodplains where plants such as thistles and asters grow. We are also found in roadsides, orchards, and backyards.",
  "facts": "We is the only bird in the finch family that sheds its feathers twice a year. Female American goldfinches can weave a nest that can hold water.",
  "question": "In what state are We the state bird?How many times does the We molt in a year?Are We endangered?",
  "quiz": "In what state are we the state bird?How many times do we molt?Are We endangered?"
}

openai.api_key = "TYPE IN HERE
r = sr.Recognizer()
try:
    dev = '/dev/ttyACM0'
    ser = serial.Serial(
            port=dev, #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
    )
except:
    dev = '/dev/ttyACM1'
    ser = serial.Serial(
            port=dev, #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
    )
time.sleep(3)
    
def say(outputext):
    print(outputext)
    if outputext != "":
        try:
            voice = gTTS(text = outputext, lang = 'en', slow = False)
            voice.save('voice.mp3')
            os.system('cvlc ~/Desktop/Bird_project/version2/voice.mp3 --play-and-exit')
        except:
            pass
        
def listen(timeouts):
    try:
        with sr.Microphone() as source:
            audio = r.listen(source, timeout = timeouts)
        text = r.recognize_google(audio)
        trys = 0 
        return text
    except sr.WaitTimeoutError:
        return "Err:timeout"
    except sr.UnknownValueError:
        return "Err:UnknownSpeech"

def distance(ser):
    ser.write(b'd\n')
    time.sleep(0.5)
    distance = ser.readline().decode('utf-8').strip()
    if distance != '' and distance != '0':
        distance = int(distance)
    else:
        distance = 10000000
    return distance

while True:
    print('state: ', state)
    if state == 0:
        urllib.request.urlopen("https://Birdproject-v2-server.flyingcrabs.repl.co/writevisits")
        ser.write(b'l g3o3\n')
        ser.write(b's 0')
        name = ""
        qanswered = 0
        openailog = ""
        state = 1
    if state == 1:
        os.system('cvlc ~/Desktop/Bird_project/version2/Birdsong.mp3 --play-and-exit')
        if distance(ser) < 50:
            state = 2
    if state == 2:
        ser.write(b'l g1o1')
        say("Welcome to Jingjing and Dingding's home. My friend Justin goo from 5a brought us here. nice to meet you. What is your name?")
        state = 3
    if state == 3:
        text = listen(5)
        if text == 'Err:timeout':
            trys = 0
            state = 0
        elif text == 'Err:UnknownSpeech':
            trys = trys + 1
            if trys == 3:
                trys = 0
                state = 0
            else:
                say('sorry I can not understand you. please try again')
        else:
            print(text)
            name = text
            state = 4
    if state == 4:
        say("Hello" + name + ". We are small North American birds and we are also part of the finch family.  We mostly live in the US but we also live in Northern Mexico and Southern canada. We are Grainavors which means we eat seeds but we also eat small insects. You can find us yearly around feeders and other areas full of seeds. This one is a female.")
        ser.write(b'l g1o2')
        time.sleep(2)
        say("and this is a male.")
        ser.write(b'l g2o1')
        time.sleep(2)
        state = 5
    if state == 5:
        ser.write(b'l g3o3')
        say("Ask me a question like what do I eat.")
        text = listen(5)
        if text == 'Err:timeout':
            trys = 0
            state = 0
        elif text == 'Err:UnknownSpeech':
            trys = trys + 1
            if trys == 3:
                trys = 0
                state = 0
            else:
                say('sorry I can not understand you. please try again')
        else:
            urllib.request.urlopen("https://Birdproject-v2-server.flyingcrabs.repl.co/questions/" + text)
            print(text)
            words = text.split()
            print(words)
            awnsered = False
            for x in words:
                try:
                    say(thisdict[x.strip()])
                    awnsered = True
                    qanswered = qanswered + 1
                except:
                    pass
            if awnsered == False:
                say("I could not answer your question. Did you say " + text)
            if qanswered == 2:
                say("would you like me to answer off topic questions or should we chat. Please answer this on the screen.")
                ser.write(b's 1')
                while True:
                    if ser.readline().decode('utf-8').strip() == "1":
                        #wolfram
                        state = 6
                        break
                    if ser.readline().decode('utf-8').strip() == "11":
                        #openai
                        state = 7
                        break
    if state == 6:
        response = ""
        say("You can ask any questions you want like who was the first president of the United States.")
        text = listen(5)
        if text == "Err:timeout":
            trys = 0
            state = 0
        elif text == "Err:UnknownSpeech":
            trys = trys + 1
            if trys == 3:
                trys = 0
                state = 0
            else:
                say('I can not understand you. Please try again.')
        else:
            try:
                res = client.query(text)
                response = next(res.results).text
            except:
               response = "Sorry, I can not anwser that"
            say(response)
    if state == 7:
        say("Say something to start the conversation.")
        state = 8
    if state == 8:
        text = listen(5)
        if text == 'Err:timeout':
            trys = 0
            state = 0
        elif text == 'Err:UnknownSpeech':
            trys = trys + 1
            if trys == 3:
                trys = 0
                state = 0
            else:
                say('sorry I can not understand you. please try again')

        else:
            openailog = openailog + '\nYou:' + text
            response = openai.Completion.create(
              model="text-davinci-003",
              prompt=openailog,
              temperature=1,
              max_tokens=300,
              top_p=1.0,
              frequency_penalty=0.5,
              presence_penalty=0.0
            )
            response = dict(response)["choices"][0]["text"].strip()
            say(response)

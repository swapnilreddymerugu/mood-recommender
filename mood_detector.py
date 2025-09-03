from textblob import TextBlob
def get_mood(text):
    analysis=TextBlob(text)
    polarity=analysis.sentiment.polarity
    if polarity>+0.3:
        return "happy"
    elif polarity<-0.3:
        return "sad"
    else:
        return "neutral"
user_input=input("how are you feeling today?")
mood=get_mood(user_input)
print("detected mood:",mood)    
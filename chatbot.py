# chatbot.py
import fake_news_model 

def chatbot():
    print("🤖Fake News Chatbot: Ask me to check news headlines or articles📝. Type 'exit' to quit.\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("🤖 Chatbot: Goodbye! Stay informed and safe.")
            break
        
        # Send input to fake news detector
        prediction, confidence = fake_news_model.predict_fake_news(user_input)
        
        # Chatbot response
        print(f"🤖 Chatbot: This looks **{prediction}** with {confidence*100:.0f}% confidence.\n")

if __name__ == "__main__":
    chatbot()

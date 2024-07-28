
import requests
import re
import os
import asyncio
from surrealdb import Surreal
from openai import OpenAI
from dotenv import load_dotenv

collection_name = "text_embeddings"
text_field_name="text"
embedding_field_name="embedding"
model="text-embedding-3-small"

 
 

async def create_embedding(openai_client, query_string, model=model):
    response = openai_client.embeddings.create(
        input=query_string,
        model=model
    )
    query_embedding = response.data[0].embedding
    return query_embedding

async def save_text_and_embedding(db, text, embedding, collection_name=collection_name, text_field_name=text_field_name, embedding_field_name=embedding_field_name):
    data = {
        text_field_name: text,
        embedding_field_name: embedding,
    }
    await db.create(collection_name, data)

async def db_info(db):
    query = f"INFO FOR DB;"
    try:
        results = await db.query(query)
        print(results)
    except Exception as e:
        print(f"There was a problem creating the index: {e}")

    query = f"INFO FOR TABLE ROOT;"
    try:
        results = await db.query(query)
        print(results)
    except Exception as e:
        print(f"There was a problem creating the index: {e}")

async def upload_text(db, openai_client, chunks, collection_name=collection_name, text_field_name=text_field_name, embedding_field_name=embedding_field_name, model=model):
    print(f"Uploading chunks... (this may take a while)")
    for chunk in chunks:
        try:
            embedding = await create_embedding(openai_client, chunk, model)
            await save_text_and_embedding(db, chunk, embedding, collection_name, text_field_name, embedding_field_name)
            print(f"Uploaded chunk: {chunk[:42]}...")
        except Exception as e:
            print(f"Failed to upload chunk. Error: {e}")
 
async def main():
    load_dotenv()
    url = "https://leasingnews.org/PDF/sell_pen2018.pdf" 

    chunks =  [
    "Best Answer to “Sell Me This Pen” I Have  I personally never thought anyone would actually say, “sell me this pen” in a sales interview. I was wrong. It will happen to you too. And to avoid panic, you should know exactly what to say back.  I am going to give you the right sales framework to respond perfectly every time.  On a quick side note, did you know this sales interview question has been around for millions of years? Its origins date back to the earliest of cavemen. Selling slingshots cavetocave. Except back then, they asked, “sell me this bowl of crushed berries.”  Anyways. The point is, one day it will happen to you and I want you to be prepared.  Because if you start to describe how smooth the pen feels and how shiny the pen looks, just like you saw in the Wolf of Wallstreet … You probably won’t get the job.  Why it matters to sell me this pen  At first, I didn’t realize why it mattered. It just seemed like a silly question. But, you’ll see.  When you become good at answering ",
    " probably won’t get the job.  Why it matters to sell me this pen  At first, I didn’t realize why it mattered. It just seemed like a silly question. But, you’ll see.  When you become good at answering this question, you actually become one hell of a salesperson.  And that’s why people still ask it in interviews. It shows your creative approach and how good you are at actually selling product not just reading your resume.  There are exactly four sales skills the interviewer is looking to see when you answer:  1. how you gather information  2. how you respond to information  3. how you deliver information  4. and how you ask for something closing  Now, since I had a lot of sales interviews lined up at the beginning of last year. I thought, I better practice my response just in case.  The “just wing it” strategy is best for making pancake mix, not for sales interviews.  So let’s go through exactly what you can say to address each sales skill. Because when you do it right, you will blow the",
    "t wing it” strategy is best for making pancake mix, not for sales interviews.  So let’s go through exactly what you can say to address each sales skill. Because when you do it right, you will blow their mind!  Here’s exactly what you can say  Just to back up for a second, I had 26 sales interviews in a period of three months. Someone was bound to ask me. Ok. The Director of Sales stood up and said, “it was great meeting you Ian. Let me go grab the CEO to come in next.” Moments later, the CEO of the 30 person startup walked in the small conference room.  Shortly after initial greetings, the CEO wasted no time to start the interview.  I practiced my answer beforehand. I made sure my answer displayed the four sales skills the CEO needed to hear.  Now you can read it for yourself. And then use it for yourself.  At the bottom, you can see a simple sales framework to memorize that will make this work for you in any situation.  You can memorize the script, but more importantly, memorize the s",
    " it for yourself.  At the bottom, you can see a simple sales framework to memorize that will make this work for you in any situation.  You can memorize the script, but more importantly, memorize the sales framework at the end.  Here you go…  CEO: Do me a favor, sell me this pen. reaches across to hand me the pen  Me: I slowly roll the pen between my index and thumb fingers. When was the last time you used a pen?  CEO: This morning.  Me: Do you remember what kind of pen that was?  CEO: No.  Me: Do you remember why you were using it to write?  CEO: Yes. Signing a few new customer contracts.  Me: Well I’d say that’s the best use for a pen we have a subtle laugh.  Wouldn’t you say signing those new customer contracts is an important event for the business? nods head Then shouldn’t it be treated like one. What I mean by that is, here you are signing new customer contracts, an important and memorable event. All while using a very unmemorable pen.  We grew up, our entire lives, using cheap BI",
    "d like one. What I mean by that is, here you are signing new customer contracts, an important and memorable event. All while using a very unmemorable pen.  We grew up, our entire lives, using cheap BIC pens because they get the job done for grocery lists and directions. But we never gave it much thought to learn what’s best for more important events.  This is the pen for more important events. This is the tool you use to get deals done. Think of it as a symbol for taking your company to the next level. Because when you begin using the right tool, you are in a more productive state of mind, and you begin to sign more new customer contracts.  Actually. You know what? Just this week I shipped ten new boxes of these pens to Elon Musk’s office .Unfortunately, this is my last pen today reach across to hand pen back to CEO. So, I suggest you get this one. Try it out. If you’re not happy with it, I will personally come back next week to pick it up. And it won’t cost you a dime.  What do you sa",
    "oss to hand pen back to CEO. So, I suggest you get this one. Try it out. If you’re not happy with it, I will personally come back next week to pick it up. And it won’t cost you a dime.  What do you say?  CEO: picks jaw up off floor Yes.  See how simple that was. The CEO loved it. Why?  Because all four sales skills were displayed.  Here’s the simple sales framework I used to answer “sell me this pen”. Memorize it for yourself.  1. Find out how they last used a pen gather info  2. Emphasize the importance of the activity they last used a pen respond to info  3. Sell something bigger than a pen, like a state of mind deliver info  4. Ask for the buy closing  Does that make sense? Yes. Ok, good.  Conclusion  Remember, it’s not about actually selling a pen. It’s about showing how well you can sell a product.  Take 15 minutes today to practice the script above. I promise you will benefit.  Plus, would you mind doing me a favor. Share this with ONE person in sales. It could save their career ",
    "ell a product.  Take 15 minutes today to practice the script above. I promise you will benefit.  Plus, would you mind doing me a favor. Share this with ONE person in sales. It could save their career  credit: http://www.dealermarketing.com/sellmethispen  AUTHOR: DARIN GEORGE"
  ]
    
    async with Surreal("wss://surrealdb.lacchinh.com/rpc") as db:
        await db.signin({
            "user": os.getenv("DB_USER", "root"), 
            "pass": os.getenv("DB_PASSWORD", "root")
        })
        await db.use("test", "test")

        openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        upload_task = asyncio.create_task(upload_text(db, openai_client, chunks))

        await upload_task
        await db_info(db)

if __name__ == "__main__":
    asyncio.run(main())
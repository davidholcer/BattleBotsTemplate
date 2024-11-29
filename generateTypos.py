import random
import typo
import math
import re

class TypoGenerator:
    def __init__(self, text, seed=None):
        self.text = text
        self.result = text
        self.seed = seed if seed is not None else random.randint(0, 10**6)
        random.seed(self.seed)  # Set the random seed
        self.myStrErrer = typo.StrErrer(text,seed=self.seed)

    def char_swap(self, preservefirst=False, preservelast=False):
        # Assume implementation exists
        self.result=self.myStrErrer.char_swap().result

    def missing_char(self, preservefirst=False, preservelast=False):
        # Assume implementation exists
        self.result=self.myStrErrer.missing_char().result

    def extra_char(self, preservefirst=False, preservelast=False):
        # Assume implementation exists
        self.result=self.myStrErrer.extra_char().result

    def nearby_char(self, preservefirst=False, preservelast=False):
        # Assume implementation exists
        self.result=self.myStrErrer.nearby_char().result

    def similar_char(self):
        # Assume implementation exists
        self.result=self.myStrErrer.similar_char().result

    def skipped_space(self):
        # Assume implementation exists
        self.result=self.myStrErrer.skipped_space().result

    def random_space(self):
        # Assume implementation exists
        self.result=self.myStrErrer.random_space().result

    def repeated_char(self):
        # Assume implementation exists
        self.result=self.myStrErrer.repeated_char().result

    def unichar(self):
        # Assume implementation exists
        self.result=self.myStrErrer.unichar().result

    def determine_typo_count(self):
        """Determine the number of typos based on the text length."""
        chars_per_100 = len(self.text) / 100
        mean_typos = 0.9
        # std_dev_typos = 0.428571 
        std_dev_typos = .42

        # Sample from normal distribution
        typo_count = max(0, round(random.gauss(mean_typos * chars_per_100, std_dev_typos * chars_per_100)))
        return typo_count

    def apply_typo(self):
        """Applies a random typo based on predefined probabilities."""
        typo_functions = [
            (self.char_swap, 0.15),       # 15% chance
            (self.missing_char, 0.15),   # 15% chance
            (self.extra_char, 0.10),     # 10% chance
            (self.nearby_char, 0.10),    # 10% chance
            (self.similar_char, 0.10),   # 10% chance
            (self.skipped_space, 0.10),  # 10% chance
            (self.random_space, 0.10),   # 10% chance
            (self.repeated_char, 0.10),  # 10% chance
            (self.unichar, 0.10),        # 10% chance
        ]

        # Weighted sampling to select a function
        functions, weights = zip(*typo_functions)
        selected_function = random.choices(functions, weights, k=1)[0]
        # print(selected_function)
        # Apply the selected function
        selected_function()

    def apply_multiple_typos(self):
        """Applies typos to the string based on its length."""
        # Determine the number of typos
        num_typos = self.determine_typo_count()
        # print(num_typos)

        for _ in range(num_typos):
            self.apply_typo()
        return self.result


class TweetAugmenter:
    def __init__(self, seed=None):
        self.seed = seed if seed is not None else random.randint(0, 10**6)
        random.seed(self.seed)

    # def add_emojis(self, text):
    #     """Adds or multiplies emojis in the text based on probabilities, ensuring multiplication happens only once."""
    #     all_emojis = ["😂", "🔥", "😎", "💔", "🌟", "❤️", "😊", "😢", "😡", "🎉", "🤔", "😜", "🙄", "💯", "👍", "👎", "👏"]
    #     emoji_pattern = r"[^\w\s,]"
    #     emojis = re.findall(emoji_pattern, text)  # Find all existing emojis
    #     emoji_multiplier_applied = False  # Ensure multiplication happens only once

    #     if emojis:  # If emojis exist in the text
    #         if random.random() < 0.6 and not emoji_multiplier_applied:  # 60% chance to multiply existing emojis
    #             # Multiply the first emoji found
    #             emoji_to_multiply = emojis[0]
    #             additional_emojis = " ".join(random.choices(all_emojis, k=random.randint(1, 2)))
    #             text = text.replace(emoji_to_multiply, f"{emoji_to_multiply} {additional_emojis}", 1)
    #             emoji_multiplier_applied = True
    #     elif random.random() < 0.5:  # 50% chance to add emojis if none exist
    #         num_emojis = random.randint(1,4)
    #         new_emojis = " ".join(random.choices(all_emojis, k=num_emojis))
    #         text += f" {new_emojis}"

    #     return text

    #expand the emojis to all possible, and don't just add, when you see one add between 1-4 others next to it with 60% chance.

    def add_hashtags(self, text):
        if random.random() < 0.60:  # 20% chance
            words = text.split()
            num_hashtags = random.randint(1, 5)
            hashtagged_words = random.sample(words, k=min(num_hashtags, len(words)))
            for word in hashtagged_words:
                text = text.replace(word, f"#{word}")
        return text

    def double_links(self, text):
        link_pattern = r"https://t.co/twitter_link"
        links = re.findall(link_pattern, text)
        if links and random.random() < 0.30:  # 15% chance
            doubled_links = [f"{link} {link}" for link in links]
            for original, doubled in zip(links, doubled_links):
                text = text.replace(original, doubled, 1)
        return text

    def fix_links(self, text):
        words = text.split()
        updated_words = [
            "https://t.co/twitter_link" if "://" in word else word for word in words
        ]
        return " ".join(updated_words)


    def add_mentions(self, text):
        if random.random() < 0.40:  # 10% chance
            num_mentions = random.randint(1, 3)
            mentions = [f"@mention" for _ in range(num_mentions)]
            text += " " + " ".join(mentions)
        return text

    def exaggerate_words(self, text):
        """Exaggerates punctuation or the ending letters of a word."""
        words = text.split()

        # Choose one word or punctuation to exaggerate (if applicable)
        indices_to_exaggerate = [
            i for i, word in enumerate(words) 
            if word.endswith(("!", "?")) or len(word) > 1
        ]

        if indices_to_exaggerate:
            # Randomly select one word/punctuation to exaggerate
            index = random.choice(indices_to_exaggerate)
            
            # If the word ends with "!" or "?", exaggerate the punctuation
            if words[index].endswith(("!", "?")):
                punctuation = words[index][-1]  # Get the last character (! or ?)
                exaggeration = punctuation * random.randint(1, 5)  # Repeat 1-5 times
                words[index] += exaggeration
            
            # Otherwise, exaggerate the last character of the word
            elif random.random() < 0.05:  # 5% chance
                words[index] += words[index][-1] * random.randint(2, 6)

        return " ".join(words)

    #don't just randomly add an exclamation mark. when you see exclamation or question mark, expand them by adding multiple next to it (with 20% chance). same for extra letters to end of a word.

    def change_case(self, text):
        words = text.split()
        for i in range(len(words)):
            if random.random() < 0.1:  # 5% chance
                if words[i] != "https://t.co/twitter_link":words[i] = words[i].upper()
            elif random.random() < 0.05:  # 1% chance
                if words[i] != "https://t.co/twitter_link":words[i] = ''.join(c.upper() if random.random() < 0.5 else c.lower() for c in words[i])
        return " ".join(words)

    def randomize_sentence_case(self, text):
        if random.random() < 0.8:  # 80% chance
            text = text[0].lower() + text[1:] if text else text
        return text

    

    def process_tweet(self, tweet):
        typo_gen = TypoGenerator(tweet, seed=self.seed)
        tweet = typo_gen.apply_multiple_typos()
        # tweet = self.add_emojis(tweet)
        tweet = self.add_hashtags(tweet)
        tweet = self.double_links(tweet)
        tweet = self.add_mentions(tweet)
        tweet = self.exaggerate_words(tweet)
        tweet = self.change_case(tweet)
        tweet = self.randomize_sentence_case(tweet)
        tweet = self.fix_links(tweet)
        return tweet

    # make sure when adding typos to the tweets that the typos do not apply on words "@mention" or "https://t.co/twitter_link"

    def process_tweets(self, tweets):
        return [self.process_tweet(tweet) for tweet in tweets]


# Example Usage
# tweets = ["Imagine combining the best aspects of today's pop icons into one artist!? Dreams could come true! ✨", 'Spotted Mahomes enjoying time courtside! Such vibes 🔥', "Nominees are in, and OMG—I can't even choose the best one this week! 🎟️", 'Just won a small victory, and it feels good! 💪 https://t.co/twitter_link', 'Definitely excited for what comes next! 🚀', 'Getting super into DIY home decor lately—so many ideas! 🛠️🏡', 'Wrapping up the season rewatch and feeling nostalgic. Some episodes were definitely underrated! 📺 https://t.co/twitter_link', 'The way my team played in the first half had me screaming at the TV. Come on guys! #StayFocused', "Whoa, that angle was wild! My brain can't handle all this creativity! 🌀", 'Tried starting my day productive but ended up napping instead… oops! 💤', "Our team's skating looks sharp these days! 🍃 Bring it on!", "Feeling something special about tonight's game, I just know it’s going to be memorable #LetsGoTeam", "Adrenaline pumping; I'm always ready to face challenges head-on! 💥🫶🏾 https://t.co/twitter_link", "Who's streaming the latest movie releases? Drop your recommendations! 🎬👇", "It's funny how trends come back around—remember when we all wore those baggy jeans? 😂 #Throwback https://t.co/twitter_link", 'Only way to get through this week is to find some cursed lyrics to keep me entertained 😂 https://t.co/twitter_link', 'Gotta share this gem I stumbled upon after finishing a great movie! 💎 @mention', 'Was that play unexpected or what?! The energy was palpable out there! 🏒👀', 'What if we did something completely radical and reinvented everything? Just a thought 💭 https://t.co/twitter_link', "Can't stress enough how epic that last action scene was! 💥🍿 https://t.co/twitter_link", 'That penalty call was absolutely ridiculous 😂 #GameDay', 'Fantasy trade proposition got everyone talking—what are your predictions? 🔮', 'Current mood: spontaneous adventures are the best kind of therapy 🌍✨', 'Ayy, anyone else craving congolese food? Just hit differently! 👌🏿 https://t.co/twitter_link', 'People sleeping on this track owe it another listen—it’s actually fire 🔥 https://t.co/twitter_link', "Rumors swirling about health checks pre-trades—what's going on in Hollywood?", 'Simplifying life is usually the key to happiness 😊 https://t.co/twitter_link']

def augmentTweets(tweets):
    augmenter = TweetAugmenter()
    augmented_tweets = augmenter.process_tweets(tweets)
    return augmented_tweets

# for original, augmented in zip(tweets, augmented_tweets):
    # print(f"Original: {original}")
    # print(f"Augmented: {augmented}")
    # print("-" * 50)


# Example Usage
# typo_gen = TypoGenerator("oh my god who is this dickhead on espn2 complaining about the refs reviewing a temple player getting hit in the face to declare a flagrant foul is ruining the sport")
# output = typo_gen.apply_multiple_typos()
# print(f"Original: oh my god who is this dickhead on espn2 complaining about the refs reviewing a temple player getting hit in the face to declare a flagrant foul is ruining the sport")
# print(f"With Typos: {output}")

#INSTRUCTIONS
#typos:
#using the above class, add typos to the sentence as shown above. however, when seeing a link "https://t.co/twitter_link" don't apply typos to the link.
#INSERT CLASS HERE

#emojis:
#when you see only one emoji, add btwn 1-4 50% of the time.
#INSERT CLASS HERE

#hashstags
# add hashtags by hashtagging btwn 1-4 words 20% of the time.
# only allow 10% of sentences to have only 1 hashtag.
#INSERT CLASS HERE

#links:
# 15% of the time double up links by adding another "https://t.co/twitter_link" after the one that is there.
#INSERT CLASS HERE

# mentions
# assure ~10% of tweets have mentions. 50% of those should have >1 mention (btwn 1-4).
#INSERT CLASS HERE

#special chars:
#when you see
#INSERT CLASS HERE

#sentence structure:
#don't always start the tweets with capital letters.
#INSERT CLASS HERE

#words
#btwn 0.5 and 5% of words can be exagerated by adding many extra chars (btwn 1-10 repetitions) to the end of the word. i.e. hi becomes hiiii
# btwn 0.5 and 5% of words can be ALL UPPERCASE
#btwn 0.5 and 1% of words can be iNtErCHAngEd uPPerCase LIkE thIs
#INSERT CLASS HERE

#bring it all together
#create a function that takes in as input an array of tweets (string sentences), and applies all the above classes to it taking in mind the mentioned probabilities.
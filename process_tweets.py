import os
import re
import nltk

def main():
    print('loading tweets...')
    with open('tweets.txt', encoding='utf-8') as f:
        all_tweets = f.readlines()

    print('Cleaning tweets...')
    editted_tweets = [
        re.sub(r'https://t\.co/.*$|@.+?( |$)|\n|[^\w .!?]|\d', ' ', t)
            .replace(r"\'", "'").lower() for t in set(all_tweets)
    ]



    cachedStopWords = nltk.corpus.stopwords.words("english")
    cachedStopWords.extend([w.replace("'", '') for w in cachedStopWords if "'" in w])

    def remove_stopwords(text):
        return [w for w in text if w not in cachedStopWords]

    tokenizer = nltk.RegexpTokenizer(r"\w+")
    print("Tokenizing tweets...")
    tokenized_tweets = [remove_stopwords(tokenizer.tokenize(t)) for t in editted_tweets]

    stemmer = nltk.stem.porter.PorterStemmer()

    print("Stemming tweets...")
    def word_stemmer(text):
        return [stemmer.stem(w) for w in text]

    stemmed_tweets = [word_stemmer(t) for t in tokenized_tweets]

    print('Saving to processed_tweets.txt...')
    processed_tweets = [' '.join(t) for t in stemmed_tweets if t]
    with open('processed_tweets.txt', 'w+', encoding='utf-8') as f:
        for t in processed_tweets:
            f.write(t+'\n')
    print(f'Finished. Processed {len(processed_tweets)} tweets.')

if __name__ == '__main__':
    main()
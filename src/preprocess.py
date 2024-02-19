import pandas as pd
from hazm import Normalizer, word_tokenize, stopwords_list


# Normalization and tokenization
def preprocess_text(text, normalizer):
    # Normalize the text
    normalized_text = normalizer.normalize(text)

    # Tokenize the text
    tokens = word_tokenize(normalized_text)

    # Remove stopwords
    clean_tokens = [token for token in tokens if token not in stopwords_list()]

    # Join tokens back into a single string
    cleaned_text = ' '.join(clean_tokens)

    return cleaned_text


# Limit the number of words in a text
def limit_text(text, max_words=500):
    try:
        return " ".join(text.split()[:max_words] if text else "")
    except:
        return "-"


# Main function to preprocess dataset
def preprocess_dataset(df, save_file: str = None):
    # Drop rows with NaN text
    df = df.dropna(subset=['text'])

    # Initialize the normalizer
    normalizer = Normalizer()

    # Apply preprocessing to all texts in the dataset
    df['text'] = df['text'].apply(lambda x: preprocess_text(x, normalizer))
    df['text'] = df['text'].apply(limit_text)

    # Shuffle the dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    if save_file:
        df.to_csv(save_file, index=False)
    return df


if __name__ == "__main__":
    # Example usage
    df = pd.read_csv("../datasets/raw/persian_authors.csv")
    processed_df = preprocess_dataset(df)
    print(processed_df.head())

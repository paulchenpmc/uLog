# Requires Python 3
import datetime
import glob
import os
import re
import wordcloud
import matplotlib.pyplot as plt
from textblob import TextBlob

HOME                        = r'C:\test'
DEFAULT_CUSTOM_METRICS_LIST = ['STRESS','FOCUS','ENERGY','MOOD','ALCOHOL','COFFEE','LOCATION','TODO','WEIGHT']

def get_current_datetime():
    current_datetime     = datetime.datetime.now()
    return current_datetime.strftime("%Y-%m-%d")

def get_latest_entry_datetime():
    filtered_entries = get_all_entries_filepath()
    # Sort alphabetically for the latest entry
    filtered_entries.sort(reverse=True)
    # Open that entry and extract the custom metrics
    latest_entry_datetime = filtered_entries[0].replace('.txt', '')
    return latest_entry_datetime

def get_all_entries_filepath():
    entries_list = glob.glob(os.path.join(HOME, '*.txt'))
    # Filter for only journal entry files
    r = re.compile('.*[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].txt')
    filtered_entries = list(filter(r.match, entries_list)) # Python 3 specific implementation, maybe replace with a backwards compatible method someday :')
    return filtered_entries

def get_latest_entry_filepath():
    """
    Gets filepath to most recent journal entry in journal directory
    """
    filtered_entries = get_all_entries_filepath()
    # Sort alphabetically for the latest entry
    filtered_entries.sort(reverse=True)
    # Open that entry and extract the custom metrics
    latest_entry_filepath = filtered_entries[0]
    return latest_entry_filepath

def get_latest_entry_custom_metrics():
    """
    Returns a list of custom tracking metrics to append to a new journal entry format
    """
    # If no previous entries, use default custom metrics for format
    if not get_latest_entry_filepath():
        return ''.join(['{}:\n'.format(a) for a in DEFAULT_CUSTOM_METRICS_LIST]) # TODO: Reconsider whether to force default metrics on first journal entry - Could just allow users to discover the feature

    custom_metrics_list = []
    with open(get_latest_entry_filepath(), 'r') as infile:
        for line in infile:
            match = re.match('([A-Z]+):', line)
            if match:
                custom_metrics_list.append(match.group(1))
    return ''.join(['{}:\n'.format(a) for a in custom_metrics_list])

def get_entry_text(filepath):
    with open(filepath, 'r') as infile:
        text = [line for line in infile.readlines()]
    text = ' '.join(text)
    return text

def create_new_entry():
    """
    Generates new journal entry file with formatting including the current date and custom user metrics
    """
    current_datetime_str = get_current_datetime()
    new_entry_filename   = '{}.txt'.format(current_datetime_str)
    custom_metrics_list  = get_latest_entry_custom_metrics()
    with open(os.path.join(HOME, new_entry_filename), 'w') as new_journal_file:
        new_entry_format = []
        new_entry_format.append(current_datetime_str) # Date at the top
        new_entry_format.append('\n\n\n\n')           # Leave some spacing
        new_entry_format.append(custom_metrics_list)  # Carry over the custom metrics from last journal entry
        new_journal_file.writelines(new_entry_format)

def create_wordcloud(filepath):
    # Create stopword list:
    stopwords = set(wordcloud.STOPWORDS)
    # Generate a word cloud image
    text  = get_entry_text(filepath)
    cloud = wordcloud.WordCloud(stopwords=stopwords).generate(text)
    # Save the image
    cloud.to_file(os.path.join(HOME, get_latest_entry_datetime() + ".png"))

def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def graph_all_entries_sentiment():
    filepath_list  = get_all_entries_filepath()
    sentiment_dict = {}
    for filepath in filepath_list:
        text     = get_entry_text(filepath)
        polarity = get_sentiment(text)
        date     = filepath.split('\\')[-1].replace('.txt', '')
        sentiment_dict[date] = polarity
    plt.bar(range(len(sentiment_dict)), list(sentiment_dict.values()), align='center') # TODO: Fix x axis so it is readable
    plt.xticks(range(len(sentiment_dict)), list(sentiment_dict.keys()))
    plt.savefig(os.path.join(HOME, 'sentiment.png'))

def main():
    print('Running uLog...')
    while True:
        print('Please select an action...\n\
  1) Create new journal entry\n\
  2) Create wordcloud of entries\n\
  3) Graph sentiment of all entries\n\
  Exit) Exit program\n\
  ')
        user_input = input()
        if user_input == '1':
            create_new_entry()
        elif user_input == '2':
            # TODO: Second level of input here to determine date or dates for wordcloud
            create_wordcloud(get_latest_entry_filepath())
        elif user_input == '3':
            graph_all_entries_sentiment()
        elif user_input.lower() == 'exit':
            break
        else:
            print('Invalid input.')
        print()
    print('Exiting...')

if __name__ == '__main__':
    main()
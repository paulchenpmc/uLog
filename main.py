import datetime
import glob
import os

HOME = r'C:\Users\temp'
CUSTOM_METRICS_LIST = ''.join(['{}:\n'.format(a) for a in ['STRESS','FOCUS','ENERGY','MOOD','ALCOHOL','COFFEE','LOCATION','TODO','WEIGHT']])

def get_custom_metrics_from_last_entry():
    entries_list = glob.glob(os.path.join(HOME, '*.txt'))
    print(entries_list)
    # TODO - Extract custom metrics from most recent journal entry to carry over into new entry format instead of hardcoding

def create_new_entry():
    current_datetime     = datetime.datetime.now()
    current_datetime_str = current_datetime.strftime("%Y-%m-%d")
    new_entry_filename   = '{}.txt'.format(current_datetime_str)
    get_custom_metrics_from_last_entry()
    with open(os.path.join(HOME, new_entry_filename), 'w') as new_journal_file:
        new_entry_format = []
        new_entry_format.append(current_datetime_str) # Date at the top
        new_entry_format.append('\n\n\n\n')           # Leave some spacing
        new_entry_format.append(CUSTOM_METRICS_LIST)  # Carry over the custom metrics from last journal entry (Alt idea: keep a format file for new entries?)
        new_journal_file.writelines(new_entry_format)

def main():
    print('Running uLog...')
    create_new_entry()
    print('Exiting...')

if __name__ == '__main__':
    main()
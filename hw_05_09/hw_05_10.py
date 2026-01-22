import os.path
import csv
import re
from datetime import datetime
import pyodbc


published_feeds_file = "published_feeds_file.txt"
feeds_to_publish_file = "feeds_to_publish.txt"
count_words_file = "count_words.csv"
count_letters_file = "count_letters.csv"


class FeedTool:

    def __init__(self):
        self.records = []

    def publish_feeds_from_file(self):
        user_input = input("Enter file path with feeds to publish or press Enter to use default folder:")
        default_path = feeds_to_publish_file
        feeds_file = user_input.strip() if user_input else default_path

        if os.path.exists(feeds_file):
            if os.path.isfile(feeds_file):
                self.process_feeds_from_file(feeds_file)
                self.publish(published_feeds_file)
                self.calculate_words(published_feeds_file, count_words_file)
                self.calculate_letters(published_feeds_file, count_letters_file)
                # os.remove(feeds_file)
        else:
            print("File to retrieve feeds info doesn't exist")

    def publish_feeds_via_console(self):
        feed_type = input("Enter feed type: news, ad, event (or press Enter to exit):")
        if feed_type == "news":
            text_entered = False
            text_input = ""
            city_input = ""
            while True:
                if not text_entered:
                    text_input = input("Enter text or press 'q' to exit: ")
                    if text_input.lower() == 'q':
                        exit()
                    elif not text_input:
                        print("Text should be entered.")
                        continue
                    else:
                        text_entered = True
                city_input = input("Enter city: ")
                if city_input == 'q':
                    exit()
                if not city_input:
                    print("City should be entered.")
                    continue
                break
            publication_feed = NewsFeed("News", text_input, city_input)
            publication_feed.publish(published_feeds_file)
            self.calculate_words(published_feeds_file, count_words_file)
            self.calculate_letters(published_feeds_file, count_letters_file)

        elif feed_type == "ad":
            text_entered = False
            text_input = ""
            expiration_date_input = ""
            while True:
                if not text_entered:
                    text_input = input("Enter text or press 'q' to exit: ")
                    if text_input.lower() == 'q':
                        exit()
                    elif not text_input:
                        print("Text should be entered.")
                        continue
                    else:
                        text_entered = True

                expiration_date_input = input("Enter expiration date (format: YYYY-MM-DD): ")
                if expiration_date_input == 'q':
                    exit()
                if not expiration_date_input:
                    print("Expiration date should be provided.")
                    continue
                break
            publication_feed = PrivateAd("PrivateAd", text_input, expiration_date_input)
            publication_feed.publish(published_feeds_file)
            self.calculate_words(published_feeds_file, count_words_file)
            self.calculate_letters(published_feeds_file, count_letters_file)

        elif feed_type == "event":
            event_description = ""
            event_speaker = ""
            event_date = ""
            description_entered = False
            speaker_entered = False
            while True:
                if not description_entered:
                    event_description = input("Enter event description: ")
                    if event_description.lower() == 'q':
                        exit()
                    elif not event_description:
                        print("Text should be entered.")
                        continue
                    else:
                        description_entered = True

                if not speaker_entered:
                    event_speaker = input("Enter Speaker name: ")
                    if event_speaker.lower() == 'q':
                        exit()
                    elif not event_speaker:
                        print("Event speaker should be entered.")
                        continue
                    else:
                        speaker_entered = True

                event_date = input("Enter Event Date: ")

                if event_date.lower() == 'q':
                    exit()
                elif not event_date:
                    print("Event date should be entered.")
                    continue
                else:
                    pattern = r'^\d{4}-\d{2}-\d{2}$'
                    if not re.match(pattern, event_date):
                        print("Incorrect event date format is entered. Should be: YYYY-MM-DD.")
                        continue
                break

            publication_feed = CommunityEvent("Event", event_description, event_speaker, event_date)
            publication_feed.publish(published_feeds_file)
            self.calculate_words(published_feeds_file, count_words_file)
            self.calculate_letters(published_feeds_file, count_letters_file)
        else:
            print("Not existing feed type entered")

    def publish(self, file_name):
        for record in self.records:
            record.publish(file_name)

    def process_feeds_from_file(self, file_path):

        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                record_type, data = line.strip().split(":")
                if record_type == "news":
                    text, city = data.split(";")
                    new = NewsFeed("News", text, city)
                    self.records.append(new)
                elif record_type == "ad":
                    text, expiration_date = data.split(";")
                    ad = PrivateAd("PrivateAd", text, expiration_date)
                    self.records.append(ad)
                elif record_type == "event":
                    text, speaker, date = data.split(";")
                    ad = CommunityEvent("Event", text, speaker, date)
                    self.records.append(ad)

    @staticmethod
    def calculate_words(feeds_file_path, csw_file_path):
        try:
            with open(feeds_file_path, 'r') as file:
                words_count = {}
                for line in file:
                    words = re.findall(r'\b\w+\b', line.lower())
                    for word in words:
                        if word.isalpha():
                            words_count[word] = words_count.get(word, 0) + 1
                with open(csw_file_path, 'w', newline='') as csw_file:
                    writer = csv.writer(csw_file, delimiter='-')
                    for word, count in sorted(words_count.items()):
                        writer.writerow([word.ljust(10), str(count).rjust(5)])
                return "Results were updated in csw file"
        except FileNotFoundError:
            return "File is not found"

    @staticmethod
    def calculate_letters(feeds_file_path, csw_file_path):
        try:
            with open(feeds_file_path, 'r') as file:
                all_letters_count = 0
                letter_count = {}
                uppercase_occurrences = {}
                for line in file:
                    for char in line:
                        if char.isalpha():
                            all_letters_count += 1
                            char_lower = char.lower()
                            letter_count[char_lower] = letter_count.get(char_lower, 0) + 1
                            if char.isupper():
                                uppercase_occurrences[char_lower] = uppercase_occurrences.get(char_lower, 0) + 1
                for letter, count in letter_count.items():
                    uppercase_count = uppercase_occurrences.get(letter, 0)
                    letter_count[letter] = (count, uppercase_count)
                # Create csv file and add results
                with open(csw_file_path, 'w', newline='') as csw_file:
                    writer = csv.writer(csw_file, delimiter=',')
                    writer.writerow(['letter'.ljust(20), 'count_all'.ljust(20), 'count_uppercase'.ljust(20),
                                     'percentage %'.ljust(20)])
                    for letter, counts in sorted(letter_count.items()):
                        total_count, uppercase_count = counts
                        percentage = round(total_count / all_letters_count * 100, 2)
                        writer.writerow([letter.ljust(20), str(total_count).ljust(20), str(uppercase_count).ljust(20),
                                         str(percentage).ljust(20)])
                return "Results were updated in csw file"
        except FileNotFoundError:
            print("Letters File not found")

    @staticmethod
    def check_for_duplicates():
        connection = pyodbc.connect('DRIVER={SQLite3 ODBC Driver};'
                                    'Direct=True;'
                                    'Database=test_10.db;'
                                    'String Types= Unicode')
        cursor = connection.cursor()
        all_duplicates = []

        try:
            duplicates_check_query = ["SELECT * FROM News GROUP BY text, city HAVING COUNT(*) > 1",
                                      "SELECT * FROM PrivateAd GROUP BY text, expiration_date HAVING COUNT(*) > 1",
                                      "SELECT * FROM Event GROUP BY text, speaker, event_date  HAVING COUNT(*) > 1"]
            for query in duplicates_check_query:
                cursor.execute(query)
                duplicates = cursor.fetchall()
                all_duplicates.extend(duplicates)
        except pyodbc.Error as e:
            print(f'Error with processing query: {e}')

        # Print duplicates if found
        if all_duplicates:
            print("Duplicates found:")
            for row in all_duplicates:
                print(row)
        else:
            print("No duplicates")
        cursor.close()
        connection.close()


class Publication:
    def __init__(self, name, text):
        self.name = name
        self.text = text
        self.type = "Publication"
        self.records = []

    def publish_format(self):
        return (f'\n{self.name}:{"-"*38}\n'
                f'\n{self.text}\n'
                f'\n{"-"*50}\n')

    def insert_feed_queries(self):
        create_table_query = f'''
                CREATE TABLE IF NOT EXISTS {self.type} (
                text text)
                '''
        data_to_insert = self.text
        insert_query = f'''
                INSERT INTO {self.type} (text, city, publish_date) VALUES (?)'''
        return create_table_query, data_to_insert, insert_query

    def publish(self, file_name):
        with open(file_name, "a") as file:
            fixed_length = 50
            lines = self.publish_format().splitlines()
            for line in lines:
                parts = [line[i:i+fixed_length] for i in range(0, len(line), fixed_length)]
                for part in parts:
                    file.write(part + "\n")

        create_table_query, data_to_insert, insert_query = self.insert_feed_queries()
        connection = pyodbc.connect('DRIVER={SQLite3 ODBC Driver};'
                                    'Direct=True;'
                                    'Database=test_10.db;'
                                    'String Types= Unicode')
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        cursor.execute(insert_query, data_to_insert)
        connection.commit()
        cursor.close()
        connection.close()


class NewsFeed(Publication):
    def __init__(self, name="News", text="Default text", city="Default city"):
        Publication.__init__(self, name=name, text=text)
        self.city = city
        self.type = "News"

    def publish_date(self):
        return self.__calculate_publish_date()

    def __calculate_publish_date(self):
        current_date = datetime.now()
        formatted_date = current_date.strftime('%Y-%m-%d %H:%M-%S')
        return formatted_date

    def publish_format(self):
        return (f'\n{self.name}:{"-"*45}\n'
                f'\n{self.text}\n'
                f'\nCity: {self.city}, {self.publish_date()}\n'
                f'{"-"*50}\n')

    def insert_feed_queries(self):

        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {self.type} (
        text text,
        city varchar,
        publish_date date)
        '''
        data_to_insert = (self.text, self.city, str(self.publish_date()))
        insert_query = f'''
        INSERT INTO {self.type} (text, city, publish_date) VALUES (?, ?, ?)'''
        return create_table_query, data_to_insert, insert_query


class PrivateAd(Publication):
    def __init__(self, name, text, expiration_date):
        Publication.__init__(self, name=name, text=text)
        self.type = "PrivateAd"
        self.expiration_date = expiration_date

    def days_left(self):
        current_date = datetime.now().date()
        expiration_date_format = datetime.strptime(self.expiration_date, "%Y-%m-%d").date()
        delta = expiration_date_format - current_date
        return delta.days

    def publish_format(self):
        return (f'\n{self.name}:{"-"*40}\n'
                f'\n{self.text}\n'
                f'\nActual until: {self.expiration_date}, {self.days_left()} day(s) left\n'
                f'{"-"*50}')

    def insert_feed_queries(self):

        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {self.type} (
        text text,
        expiration_date date,
        days_left int)
        '''
        data_to_insert = (self.text, self.expiration_date, self.days_left())
        insert_query = f'''
        INSERT INTO {self.type} (text, expiration_date, days_left) VALUES (?, ?, ?)'''
        return create_table_query, data_to_insert, insert_query


class CommunityEvent(Publication):
    def __init__(self, name, text, speaker, date):
        Publication.__init__(self, name=name, text=text)
        self.type = "Event"
        self.speaker = speaker
        self.date = date

    def get_date(self):
        return self.__format_date()

    def __format_date(self):
        converted_date = datetime.strptime(self.date, '%Y-%m-%d').date()
        return converted_date

    def publish_format(self):
        return (f'\n{self.name}:{"-"*44}\n'
                f'\n{self.text.ljust(10)}\n'
                f'\nEvent date: {self.date}, Speaker: {self.speaker}\n'
                f'{"-"*50}\n')

    def insert_feed_queries(self):

        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {self.type} (
        text text,
        speaker varchar,
        event_date date)
        '''
        data_to_insert = (self.text, self.speaker, self.get_date())
        insert_query = f'''
        INSERT INTO {self.type} (text, speaker, event_date) VALUES (?, ?, ?)'''
        return create_table_query, data_to_insert, insert_query


if __name__ == '__main__':

    ft = FeedTool()
    ft.publish_feeds_from_file()
    ft.check_for_duplicates()

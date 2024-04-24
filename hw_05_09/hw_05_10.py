import os.path
import csv
import re
from datetime import datetime
import pyodbc


class FeedTool:
    def __init__(self):
        self.records = []

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


class Publication:
    def __init__(self, name, text):
        self.name = name
        self.text = text
        self.type = "Publication"
        self.records = []

    def publish_format(self):
        return (f'\n{self.name}:------------------------------------------\n'
                f'\n{self.text}\n'
                f'\n-----------------------------------------------\n')

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
            file.write(self.publish_format())

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
        self.records = []
        self.type = "News"

    def publish_date(self):
        return self.__calculate_publish_date()

    def __calculate_publish_date(self):
        current_date = datetime.now()
        formatted_date = current_date.strftime('%Y-%m-%d %H:%M-%S')
        return formatted_date

    def publish_format(self):
        return (f'\n{self.name}:------------------------------------------\n'
                f'{self.text}\n'
                f'City: {self.city}, {self.publish_date()}\n'
                f'\n-----------------------------------------------\n')

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
        return (f'\n{self.name}:------------------------------------\n'
                f'{self.text}\n'
                f'Actual until: {self.expiration_date}, {self.days_left()} day(s) left\n'
                f'\n-----------------------------------------------\n')

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
        return (f'\n{self.name}:-----------------------------------------\n'
                f'{self.text}\n'
                f'Speaker: {self.speaker}\n'
                f'Event date: {self.date}\n'
                f'\n-----------------------------------------------\n')

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
        print("File not found")


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


if __name__ == '__main__':

    user_input = input("Enter file path with feeds to publish or press Enter to use default folder:")
    default_path = "feeds_to_publish.txt"
    feeds_published = "feeds_file.txt"
    feeds_to_publish_file = user_input.strip() if user_input else default_path

    if os.path.exists(feeds_to_publish_file):
        if os.path.isfile(feeds_to_publish_file):
            feed = FeedTool()
            feed.process_feeds_from_file(feeds_to_publish_file)
            feed.publish(feeds_published)
            os.remove(feeds_to_publish_file)
            count_words_file = "count_words.csw"
            count_letters_file = "count_letters.csw"
            count_words_result = calculate_words(feeds_published, count_words_file)
            count_letters_result = calculate_letters(feeds_published, count_letters_file)

    else:
        print("File doesn't exist")
    check_for_duplicates()

import os.path
from datetime import datetime


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
                    ad = PrivateAd("Private Ad", text, expiration_date)
                    self.records.append(ad)
                elif record_type == "event":
                    text, speaker, date = data.split(";")
                    ad = CommunityEvent("Event", text, speaker, date)
                    self.records.append(ad)


class Publication:
    def __init__(self, name, text):
        self.name = name
        self.text = text
        self.records = []

    def publish_format(self):
        return (f'\n{self.name}:------------------------------------------\n'
                f'\n{self.text}\n'
                f'\n-----------------------------------------------\n')

    def publish(self, file_name):
        with open(file_name, "a") as file:
            file.write(self.publish_format())


class NewsFeed(Publication):
    def __init__(self, name="News", text="Default text", city="Default city"):
        Publication.__init__(self, name=name, text=text)
        self.city = city
        self.records = []

    def add_news(self, text, city):
        self.records.append({"type": "news", "text": text, "city": city})

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


class PrivateAd(Publication):
    def __init__(self, name, text, expiration_date):
        Publication.__init__(self, name=name, text=text)
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


class CommunityEvent(Publication):
    def __init__(self, name, text, speaker, date):
        Publication.__init__(self, name=name, text=text)
        self.speaker = speaker
        self.date = date

    def get_date(self):
        return self.__format_date()

    def __format_date(self):
        return self.date.strftime('%Y-%m-%d %H:%M-%S')

    def publish_format(self):
        return (f'\n{self.name}:-----------------------------------------\n'
                f'{self.text}\n'
                f'Speaker: {self.speaker}\n'
                f'Event date: {self.date}\n'
                f'\n-----------------------------------------------\n')


if __name__ == '__main__':

    user_input = input("Enter file path with feeds to publish or press Enter to use default folder:")
    default_path = "feeds_to_publish.txt"

    file_path = user_input.strip() if user_input else default_path

    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            feed = FeedTool()
            feed.process_feeds_from_file(file_path)
            feed.publish("published_feeds_file.txt")
            os.remove(file_path)
    else:
        print("File doesn't exist")

from datetime import datetime


class PublicationTool:
    def __init__(self, publication_type):
        self.publication_type = publication_type
        self.feed_data = []

    def add_record(self, feed):
        self.feed_data.append(feed)

    def publish(self, file_name):
        with open(file_name, "a") as file:
            for feed in self.feed_data:
                file.write(feed.publish_format())


class Publication:
    def __init__(self, name, text):
        self.name = name
        self.text = text


class NewsFeed(Publication):
    def __init__(self, name, text, city):
        Publication.__init__(self, name=name, text=text)
        self.city = city

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
                f'-----------------------------------------------')

    def publish(self, file_name):
        with open(file_name, "a") as file:
            file.write(self.publish_format())


class PrivateAd(Publication):
    def __init__(self, name, text, expiration_date):
        Publication.__init__(self, name=name, text=text)
        self.expiration_date = expiration_date

    def days_left(self):
        current_date = datetime.now().date()
        if self.expiration_date < current_date:
            expired_string = "expired 0"
            return expired_string
        else:
            delta = self.expiration_date - current_date
            return delta.days

    def publish_format(self):
        return (f'\n{self.name}:------------------------------------------\n'
                f'{self.text}\n'
                f'Actual until: {self.expiration_date}, {self.days_left()} day(s) left\n'
                f'-----------------------------------------------')

    def publish(self, file_name):
        with open(file_name, "a") as file:
            file.write(self.publish_format())


while True:
    feed_type = input("Enter feed type: news, ad (or press any key to exit):")
    if feed_type == "news":
        text_input = input("Enter text: ")
        city_input = input("Enter city: ")
        publication_feed = NewsFeed("News", text_input, city_input)
        publication_feed.publish("feeds_file.txt")
    if feed_type == "ad":
        text_input = input("Enter text: ")
        expiration_date_input = input("Enter expiration date (format: YYYY-MM-DD): ")
        try:
            date_object = datetime.strptime(expiration_date_input, "%Y-%m-%d").date()
            publication_feed = PrivateAd("Add", text_input, date_object)
            publication_feed.publish("feeds_file.txt")
        except ValueError:
            print("Wrong date format was entered. Please try again with date format: YYYY-MM-DD.")
    else:
        print("Not existing feed type entered")
        break

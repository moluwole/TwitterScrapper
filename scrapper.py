import argparse
import json
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')


def get_driver(username):
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get('https://twitter.com/{0}'.format(username))
        return driver
    except WebDriverException:
        return None


def get_tweets(username):
    driver = get_driver(username)
    if driver is None:
        print("Unable to instantiate Chrome Web driver")
    else:
        all_tweets = []
        tweets_div = driver.find_elements_by_css_selector('.stream ol li')
        for element in tweets_div:
            try:
                img_element = element.find_element_by_css_selector(".content").find_element_by_css_selector('a') \
                    .find_element_by_css_selector('img')

                name_element = element.find_element_by_css_selector('.content .stream-item-header strong')
                username_element = element.find_element_by_css_selector('.content .username b')
                tweet_body = element.find_element_by_css_selector('.content p')

                single_tweet = {
                    'imgSource': img_element.get_attribute('src'),
                    'username': "@{0}".format(username_element.text),
                    'name': name_element.text,
                    'tweetBody': tweet_body.text
                }
                all_tweets.append(single_tweet)
            except NoSuchElementException:
                continue

        filename = save_to_file(username, all_tweets)
        print("Tweets saved to : {0}".format(filename))


def save_to_file(username, tweets):
    data = {'tweets': tweets}
    filename = username + "_tweets.json"
    with open(filename, 'w') as tweet_file:
        tweet_file.write(json.dumps(data))

    return filename


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pull tweets from a twitter account")
    parser.add_argument('-u', '--username', help="Twitter's account username", required=True)

    args = parser.parse_args()
    get_tweets(args.username)


# LT_bot (Listening Tweeter)

This simple script only implements the transfer of tweets from user accounts that are in the public domain (in simple words).

The idea is that a message with a user's tweet arrives in Telegram faster than a push notification is triggered
(with minimal server costs: 2 cores, 2 GB of RAM, 10 GB of hard disk - the speed will vary from 0 to 3 maximum).

That is, the program performs streaming parsing of the user's first tweet and compares the previous and new tweets by a unique link to the tweet,
 after identifying a discrepancy, the program sends a message to Telegram with the contents of the tweet (except for emoticons and emojis).

The parsing itself is mainly implemented on the Selenium framework
(it was Selenium that was used as the basis due to the fact that the Tweeter API allows you to send a request to the server only with a delay of 10s,
which does not meet my requirements from the program), the Tweepy library in the main script implements the receipt of media images in the form of links,
 no more, because getting the text from a tweet using this library carried some kind of bugs with it and sometimes the text was simply not received when requested

REQUIREMENTS
To fully use the program, you will need
Twitter API (https://developer.twitter.com/en), Telegram API (https://t.me/BotFather) and Telegram ID (https://t.me/getmyid_bot)
of the user to whom messages will be sent to the bot , chromedriver (which will run in stationary mode). Server or PC with system requirements 2 cores,
2GB RAM, 10GB hard drive for optimal performance.

If you're having trouble getting media from your tweets, try using the tweeter API documentation or raising the level of access for your tweeter dev project.

When installing the project on the hardware on which you will use it, do not forget to grant superuser rights to the chromedriver (The installation of which will already be if necessary). This is done with the command:

sudo chmod 775 chromedriver
or
sudo chmod +x chromedriver

Then you can safely run the script with the command:
sudo python3 main.py

Script main.py is oriented to restart the main parsing script after 1 minute break.
This was done with the aim of long-term ability to listen to a particular user without interruption,
because the program constantly reloads the page and this often leads to the tweeter server limiting communication with the server from which too many requests come.
So that the script does not hang forever until the server cache is clogged, the main script waits 30 until the element is loaded,
otherwise it gives an error and the main script goes to reload in 1 minute, after which the main script starts the parsing script again

One way or another, the source code is in the public domain, so it is completely open to your ideas and improvements.

I will be grateful for constructive criticism

Good luck


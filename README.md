# VEX Forum Alert Bot
A bot that scrapes the VEX Forum RSS feed and posts to Discord

Feel free to look around in the scripts to see how it works. 
Whenever it sees a new post, it saves it in a SQL database, then posts it on discord like this:

https://imgur.com/a/kHyLXtZ

Whenever the most recent post is edited, it can also see that, and post what it sees like this: 

https://imgur.com/a/69W5ouE

Whenever the most recent post is deleted, it will show this:

https://imgur.com/a/MZeI0WB

Still working out the details, but every so often the bot will search the database and the last 100 forum posts, and find anything that was deleted or removed. 

The scrape.py script checks the forum every so often, and posts new things it finds on discord every so often. 

The commands.py script accepts commands from discord. These are the possible commands as of now:

.add - adds the current channel to the list of channels to send posts to. It also logs the username of the user who calls it, along with their discord user ID.

.remove - same as .add, but it removes the list of channels instead.

.refresh - if the bot stops responding properly, you can run this and it will refresh the connection to the database

.SELECT - this can run SQL queries into the database. I have put protections in place to prevent a SQL injection attack. No, Bobby Tables does not have a VEX Forum account, so no need to search for their posts. This command takes 3 arguments. The first one will be what column to read. This can be `link`, `content`, `author`, `time` `imglink` (user pfp), and `topic`. There are a few other columns, but nothing will give you anything interesting. These are also the only possible values for the second argument. The third argument will be what the second one is equal to. For example, you could say `.SELECT content link "83498/12"` and it would look for the content of the post where the link is equal to `83498/12`. The link is in the topicnum/postnum format. Running this command would give you `Thanks, I guess I didn’t see that last night.`  

.report - This will find for you all the recent deleted or removed posts. Be careful running this, though, it will post in every channel signed up to receive updates. 

.check - Only I can run this command, but it will send a test message in all channels signed up to receive updates. 

Lastly, this is just a personal project, and if an admin from the VEX Forum asks me to stop this bot, I will happily do so. 

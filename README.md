# Twitch reader [CZ](./README_CZ.md)
**Twitch reader** is a program, which is reading Twitch chat in selected channel and then write it in the text file. It can run in CMD or GUI interface, but GUI interface has more functions.

## Functions
It have only one function now, and that's message sorting according to which hashtag is included in the message. ***Hashtags must be separated by space, otherwise the program will not catch that message.*** You are deciding, which hashtags will be catched by your list of hashtags in the settings.

## Setup
Setup is pretty easy. You need to fill only a few data. For this purpose is GUI program `config.exe`. If the program exit immediately, most likely you haven't entered your parameters correctly.

### Filling the data
- main
    - nick
    - token (which you can get [here](https://twitchapps.com/tmi/) (You need Twitch account for this.))
    - channel
- minor
    - CMD
        - raw output (from Twitch API)
        - output (formatted nick and message)
    - GUI
        - refresh rate (interval in ms, when the text will update)
        - commands
    - gui (check for mod with GUI)

	
***You have to fill minor data, without that the program will not work.***

## Modifications
There's notes in the code, which can help you. For your code is reserved a block, which is highlighted with comments. GUI doesn't have any exceptions and it has been written in Tkinter.
![](https://media.giphy.com/media/5b5CuS5enNTxhwAkSD/giphy.gif)


# PodcastArchiver
Do you want to save a podcast to your local machine? Maybe you are canceling your podcast service subscription but you don't want to permanently loose all your episodes. Maybe a podcast is getting canceled and you want to save the content. Or maybe you just want to archive a show for the future!

This program will download the RSS feed, cover art, and all the episode audio files. It will then make a simple website from the titles and descriptions of the show itself and the episodes. The website has simple relative links to it can be used on a machine with no web server. Just open an .html file in the browser. The program also compresses everything in a nice tar ball for achieving.

##  Requirements

 - Git
 - Linux, MacOS or Windows 10 with WSL
 - Python 3+

## Install

    git clone https://github.com/mr-rigden/PodcastArchiver.git
    cd PodcastArchiver
    python3 python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Usage

    positional arguments:
      url            Podcast RSS URL
    
    optional arguments:
      -h, --help     show this help message and exit
      -v, --verbose  increase output verbosity

## Credit

 - [Jason Rigden](https://twitter.com/mr_rigden)
## License

**MIT License**

Copyright 2019 Jason Rigden

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# Based on code from "Programming Collective Intelligence" p. 31 generatefeedvector.py,
# by Toby Segaran, published by O'Reilly Media
# http://shop.oreilly.com/product/9780596529321.do


import feedparser
import re
import ssl

MULTIFEED_PREVALENCE_LOWER_BOUND = 0.03
MULTIFEED_PREVALENCE_UPPER_BOUND = 1.0
DATAFILE_PATH = "../"
FEED_OUTPUT_FILE_PREFIX = "feed_output_"


# return title & dictionary foR word ocunts for RSS feed
def get_feed_summaries_with_word_count(feed):
    # parse the feed

    wc = {} # words and their counts from titles & summaries in feed entries
    summaries = [] # list of summaries for each entry

    # Loop over all entries
    for e in feed.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description
        summaries.append("**************summary*************\n" \
                         + summary + "\n")
        # extract a list of words
        words = getwords(e.title + ' ' + summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1
    return summaries, wc


def getwords(html):
    # Remove all html tags
    txt = re.compile(r'<[^>]+>').sub('', html)

    # split words by all non-alpha characters
    words = re.compile(r'[^A-Z^a-z+]').split(txt)

    # convert to lowercase
    return [word.lower() for word in words if word != '']


def get_basic_feed_data(feed):
    data = "The title is:  " + feed.feed.title \
        + "\n\nThe Language is:  " + feed.feed.language \
        + "\n\nThe updated information is: " + feed.feed.updated \
        + "\n\nThe link is:  " + feed.feed.link
    return data


def main():
    apcount = {}
    wordcounts = {}
    file_length = 0
    summaries = []

    # 'hacky' solution for ssl verification failure error from https://stackoverflow.com/questions/28282797/feedparser-parse-ssl-certificate-verify-failed/28296087
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

    # loop over each url in the input file & process each one
    with open((DATAFILE_PATH + 'feedlist.txt'), 'r') as feedlist:
        for line in feedlist:

            # parse feed & set variables
            file_length += 1
            d = feedparser.parse(line)
            basicdata = get_basic_feed_data(d)
            summaries, wc = get_feed_summaries_with_word_count(d)

            # write this feeds information to file
            filename = DATAFILE_PATH + FEED_OUTPUT_FILE_PREFIX + d.feed.title + ".txt"
            outfile = open(filename, 'w+')
            outfile.write(basicdata + "\n\n")
            for i in summaries:
                outfile.write(i + "\n")
            outfile.write("\n*************Words count************\n")
            for word, count in wc.items():
                outfile.write("\n" + word + " " + str(count))
            outfile.close()

            # add the wordcounts dict from this feed, to the dictionary of wordcounts
            wordcounts[d.feed.title] = wc

            # count number of blogs each word appears in
            for word, count in wc.items():
                apcount.setdefault(word, 0)
                if count > 1:
                    apcount[word] += 1
            if 'str' in line:
                break

    # Decide which words to include based on multiple feed usage
    wordlist = []
    for w, bc in apcount.items():
        frac = float(bc)/file_length
        if MULTIFEED_PREVALENCE_LOWER_BOUND <= frac <= MULTIFEED_PREVALENCE_UPPER_BOUND:
            wordlist.append(w)

    # print common words to file
    out = open((DATAFILE_PATH + 'commonwords.txt'), 'w+')
    out.write("*************Words in common***********\n\n")
    for word in wordlist:
        out.write(word + "\n")
    out.close()

main()

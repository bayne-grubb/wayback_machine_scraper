import string

import pandas as pd

df = pd.read_csv('./data/bigboi.csv', parse_dates=["Date"], index_col=0)


def remove_weird_header(text):
    removed = text.replace(
        " Please click here to read an important security message.  ", "")
    return removed


def remove_bois(text, string):
    removed = text.replace(string, "")
    return removed


string_to_remove = "If you submit more than that we will block Save Page Now requests from your IP number for 5 minutes.Please feel free to write to us at info@archive.org if you have questions about this. Please include your IP address and any URLs in the email so we can provide you with better service., "
df["Text"] = df["Text"].apply(lambda x: remove_weird_header(x))
df["Text"] = df["Text"].apply(lambda x: x.strip())
df["Text"] = df["Text"].apply(lambda x: remove_bois(x, string_to_remove))

df.to_csv("./data/bigboi.csv")

for tweet in alltweets:
                t = tweet.split()
                for i in t:
                        if 'http' in i:
                                r = requests.get(i)
                                if 'x-twitter-response-tags' not in r.headers.keys():
                                        links.append(i)
                                        c.execute("INSERT INTO links (link) values(?)", (i, ))
                                        conn.commit()

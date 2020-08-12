import Web_Scrapper


def read_data(user_address, location_address):
    """

    :param user_address: file containing user's data to sign in
    :param location_address: file containing city and states where doctors are located
    :return: data structures containing user data and location data in a tuple
    """
    user_data = open(user_address)
    access_data = [w[:-1] for w in user_data.readlines()]  # cleaning up new line char
    user_data.close()
    location_data = open(location_address)
    states_cities = [loc[:-1] for loc in location_data.readlines() if bool(loc[:-1])]
    location_data.close()
    locations = {}
    state = ''
    for i in states_cities:
        if i.isupper() and i not in locations:
            state = i
            locations.setdefault(state, [])
        else:
            locations[state].append(i)
    return access_data, locations  # may wanna add a pop to pop empty keys


def feed_scrapper(scrapper, signin_info, locations):
    """

    :param scrapper: scrapper class from the imported file to download data
    :param signin_info: iterable containing user's data to sign in
    :param locations: dictionary containing city and states where doctors are located
    :return: None, runs class to download data
    """
    for state, city in locations.items():
        for c in city:
            asn = scrapper(signin_info, c, state)
            asn.login_link()
            asn.username()
            asn.password()
            asn.member_data()


def get_df(parser, download_dir):
    """

    :param parser: parser class from the imported file to parse and clean data
    :param download_dir: path where files were downloaded in feed_scrapper
    :return: pandas data frame containing clean data
    """
    data = parser(download_dir)
    data.data_parser()
    return data.df


def clean_df(df):
    """

    :param df: dataframe to be further cleaned 
    :return: newly mutated dataframe based on the company's needs
    """
    cleanRegex = re.compile(r"(\)+)|(\(+)|('+)")
    df = df.drop(["Title"], axis=1)
    for h in df.head(0):
        df[h] = df[h].str.strip('[]\"\'():Address<>\t ')
    for e, v in enumerate(df["Phone"]):
        if cleanRegex.findall(v):
            df.at[e, "Phone"] = cleanRegex.sub('', v)
        elif "," in v and len(v) == 1:
            df.at[e, "Phone"] = ''

    return df
    
files = read_data("./Selenium Drivers/account_data.txt", "./Selenium Drivers/locations.txt")
feed_scrapper(Web_Scrapper.FarmaconScrapper, files[0], files[1])

asn_df = clean_df(get_df(Web_Scrapper.VCardParser, "../../Downloads/passed/"))
asn_df.to_csv('asn_data.csv', index=False)

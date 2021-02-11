from nltk.corpus import stopwords
import string
# list of unwanted words commonly found in job titles that I am not currently looking for
languages = ['ios','php','unity','javascript','typescript','java']
jobTitles = ['senior','frontend','lead','manager','lead','intermediate','web']
unwantedWordsSet = set(languages + jobTitles)

def nltkPreprocess(text):
    """
    description:
    Very simple preprocessor that lower, clean, remove stopwords(filler) and then compares it to a set of unwanted keywords
    input: 
        - string
    outputs:
        - ['wanted', 'unwanted'] flag

    """
    languages = ['ios','php','unity','javascript','typescript','java']
    jobTitles = ['senior','frontend','lead','manager','lead','intermediate','web','principal']
    unwantedWordsSet = set(languages + jobTitles)

    # lower
    words = text.lower().split()
    # remove punctiuation
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in words]
    #remove stopwords
    stop_words = set(stopwords.words('english'))
    clean = [w for w in stripped if not w in stop_words if w!='' and w.isnumeric()==False and len(w) >2] #len >3 to filter garbage
    if set(clean) & unwantedWordsSet:
        return 'unwanted'
    # if you return clean (the object) you get the list of word cleaned words         
    return 'wanted'
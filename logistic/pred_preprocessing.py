
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pickle

mms_pos = pickle.load(open('./savedModels/mms/mms_pos', 'rb'))
mms_neu = pickle.load(open('./savedModels/mms/mms_neu', 'rb'))
mms_neg = pickle.load(open('./savedModels/mms/mms_neg', 'rb'))
mms_compound = pickle.load(open('./savedModels/mms/mms_compound', 'rb'))
mms_fb1 = pickle.load(open('./savedModels/mms/mms_fb1', 'rb'))
mms_fb2 = pickle.load(open('./savedModels/mms/mms_fb2', 'rb'))
mms_fb3 = pickle.load(open('./savedModels/mms/mms_fb3', 'rb'))
mms_fb4 = pickle.load(open('./savedModels/mms/mms_fb4', 'rb'))
mms_fb5 = pickle.load(open('./savedModels/mms/mms_fb5', 'rb'))
mms_fb6 = pickle.load(open('./savedModels/mms/mms_fb6', 'rb'))
mms_fb7 = pickle.load(open('./savedModels/mms/mms_fb7', 'rb'))

tfidf_essay = pickle.load(open('./savedModels/tfidf_vectoriser_15000', 'rb'))
ohe_ss = pickle.load(open('./savedModels/mms/ohe_ss', 'rb'))
ohe_tp = pickle.load(open('./savedModels/mms/ohe_tp', 'rb'))
ohe_pgc = pickle.load(open('./savedModels/mms/ohe_pgc','rb'))
mlb_cc = pickle.load(open('./savedModels/mms/mlb_cc', 'rb'))
mlb_csc = pickle.load(open('./savedModels/mms/mlb_csc', 'rb'))
mms_price = pickle.load(open('./savedModels/mms/mms_price', 'rb'))
mms_ppp = pickle.load(open('./savedModels/mms/mms_ppp', 'rb'))

# Essay Preprocessing
def essayPreProcess(input_essay):
    import contractions
    import inflect
    import re
    p=inflect.engine()
    
    # Inner function
    def is_float(string):
        pattern = r"^[-+]?[0-9]*\.?[0-9]+$"
        match = re.match(pattern, string)
        return bool(match)

    sentence1 = ''
    for word in input_essay.split(' '):
        if(word.isnumeric()):
            a = int(word)
            a = p.number_to_words(a) # type: ignore
            sentence1 = sentence1 + ' ' + str(a)
        elif(is_float(word)):
            a = float(word)
            a = p.number_to_words(a) # type: ignore
            sentence1 = sentence1 + ' ' + str(a)
        else:
            sentence1 = sentence1 + ' ' + word

    return sentence1


# Creating new features & Normalising them #
def newFeatures(var_essay, price, ppp, cc, csc):
    sid = SentimentIntensityAnalyzer()
    sentiment_score = sid.polarity_scores(var_essay)
    neg = sentiment_score['neg']
    pos = sentiment_score['neu']
    neu = sentiment_score['pos']
    compound = sentiment_score['compound']
    if ppp==0:
        fb1 =  price    
    else:
        fb1 = price/ppp
    fb2 = len(cc.split(' ')) #number of clean categories
    fb3 = len(csc.split(' ')) #number of clean sub categories
    fb4 = fb2/fb3
    fb5 = len(var_essay.split(' ')) #number of words in essay
    fb6 = fb5/fb2
    fb7 = fb5/fb3

    res_dict_newfeat = {
        'res_pos' : mms_pos.transform([[pos]]) ,
        'res_neu' : mms_neu.transform([[neu]]) ,
        'res_neg' : mms_neg.transform([[neg]]) ,
        'res_compound' : mms_compound.transform([[compound]]) ,
        'res_fb1' : mms_fb1.transform([[fb1]]) ,
        'res_fb2' : mms_fb2.transform([[fb2]]) ,
        'res_fb3' : mms_fb3.transform([[fb3]]) ,
        'res_fb4' : mms_fb4.transform([[fb4]]) ,
        'res_fb5' : mms_fb5.transform([[fb5]]) ,
        'res_fb6' : mms_fb6.transform([[fb6]]) ,
        'res_fb7' : mms_fb7.transform([[fb7]]) 
    }

    return res_dict_newfeat


# Preprocessing/Normalising given inputs #
def preprocessInputs(var_essay, ss, tp, pgc, cc, csc, price, ppp):

    res_dict_ppInputs = {
        'res_essay' : tfidf_essay.transform([var_essay]) ,
        'res_ss' : ohe_ss.transform([[ss]]) ,
        'res_tp' : ohe_tp.transform([[tp]]) ,
        'res_pgc' : ohe_pgc.transform([[pgc]]) ,
        'res_cc' : mlb_cc.transform([[cc]]) ,
        'res_csc' : mlb_csc.transform([[csc]]) ,
        'res_price' : mms_price.transform([[price]]) ,
        'res_ppp' : mms_ppp.transform([[ppp]]) 
    }
    
    return res_dict_ppInputs
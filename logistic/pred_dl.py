import pickle
import numpy as np
import tensorflow
from sklearn.metrics import roc_auc_score


Tokenizer = pickle.load(open('./savedModels/DL/token_essay_dl', 'rb'))
ohe_ss = pickle.load(open('./savedModels/DL/ohe_ss_dl', 'rb'))
ohe_tp = pickle.load(open('./savedModels/DL/ohe_tp_dl', 'rb'))
ohe_pgc = pickle.load(open('./savedModels/DL/ohe_pgc_dl','rb'))
mlb_cc = pickle.load(open('./savedModels/DL/ohe_cc_dl', 'rb'))
mlb_csc = pickle.load(open('./savedModels/DL/ohe_csc_dl', 'rb'))
mms_price = pickle.load(open('./savedModels/DL/sc_price_dl', 'rb'))

def auroc(y_true, y_pred):
    return tensorflow.numpy_function(roc_auc_score, (y_true, y_pred), tensorflow.double)

dlmodel = tensorflow.keras.models.load_model("./savedModels/DL/weights-03-0.7438.hdf5", compile=False,custom_objects={"auroc": auroc})
dlmodel.compile(loss = tensorflow.keras.losses.categorical_crossentropy, optimizer = tensorflow.keras.optimizers.Adam(), metrics=[auroc])

def mainPredict(dict_inputs):
    varEssay = essayPreProcess(dict_inputs['essay'])

    
    dict_Inputs = preprocessInputs(varEssay, dict_inputs['ss'], dict_inputs['tp'], dict_inputs['pgc'],
                                      dict_inputs['cc'], dict_inputs['csc'], dict_inputs['price'], dict_inputs['tpp'])    

    predDL= dlPredictor(dict_Inputs)
    return predDL

def dlPredictor(dict_Inputs):
   
    input_stack = np.hstack((dict_Inputs['res_ss'], dict_Inputs['res_pgc'], dict_Inputs['res_tp'], dict_Inputs['res_cc'], dict_Inputs['res_csc'], dict_Inputs['res_price'], dict_Inputs['res_ppp']))
    input_stack = np.expand_dims(input_stack,axis=2)

    input_to_model = [dict_Inputs['res_paddedessay'], input_stack]
    
    dlResult = dlmodel.predict(input_to_model)
    return dlResult


# Essay Preprocessing
def essayPreProcess(input_essay):
    
    encoded_essay = Tokenizer.texts_to_sequences([input_essay])
    padded_essay = tensorflow.keras.preprocessing.sequence.pad_sequences(encoded_essay, maxlen=300, padding='post')
    
    return padded_essay




# Preprocessing/Normalising given inputs #
def preprocessInputs(padded_essay, ss, tp, pgc, cc, csc, price, ppp):

    res_dict_Inputs = {
        'res_paddedessay' : padded_essay , 
        'res_ss' : ohe_ss.transform([[ss]]) ,
        'res_tp' : ohe_tp.transform([[tp]]) ,
        'res_pgc' : ohe_pgc.transform([[pgc]]) ,
        'res_cc' : mlb_cc.transform([[cc]]) ,
        'res_csc' : mlb_csc.transform([[csc]]) ,
        'res_price' : mms_price.transform([[price]]) ,
        'res_ppp' : mms_price.transform([[ppp]]) 
    }
    
    return res_dict_Inputs
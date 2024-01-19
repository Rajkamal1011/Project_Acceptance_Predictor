import pickle
from scipy.sparse import hstack

from . import pred_preprocessing

# Pickle Model Calling
lrmodel = pickle.load(open('./savedModels/lr/set2_mms_lr_model', 'rb'))


def mainPredict(dict_inputs):

    varEssay = pred_preprocessing.essayPreProcess(dict_inputs['essay'])

    dict_newFeatures = pred_preprocessing.newFeatures(varEssay, dict_inputs['price'], dict_inputs['tpp'], dict_inputs['cc'],
                                    dict_inputs['csc'])
    
    dict_ppInputs = pred_preprocessing.preprocessInputs(varEssay, dict_inputs['ss'], dict_inputs['tp'], dict_inputs['pgc'],
                                      dict_inputs['cc'], dict_inputs['csc'], dict_inputs['price'], dict_inputs['tpp'])    

    predLR = lrPredictor(dict_newFeatures, dict_ppInputs)
    return predLR


# Prediction Function
def lrPredictor(dict_newFeatures, dict_ppInputs):
    input_to_model = hstack((dict_ppInputs['res_essay'], dict_ppInputs['res_ss'], 
                             dict_ppInputs['res_tp'], dict_ppInputs['res_pgc'], 
                             dict_ppInputs['res_cc'], dict_ppInputs['res_csc'], 
                             dict_ppInputs['res_price'], dict_ppInputs['res_ppp'], 
                             dict_newFeatures['res_neg'], dict_newFeatures['res_pos'], 
                             dict_newFeatures['res_neu'], dict_newFeatures['res_compound'], 
                             dict_newFeatures['res_fb1'], dict_newFeatures['res_fb2'], 
                             dict_newFeatures['res_fb3'], dict_newFeatures['res_fb4'], 
                             dict_newFeatures['res_fb5'], dict_newFeatures['res_fb6'], 
                             dict_newFeatures['res_fb7'])).tocsr()
    
    lrResult = lrmodel.predict_proba(input_to_model)
    return lrResult


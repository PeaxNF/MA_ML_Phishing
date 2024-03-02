import pandas as pd
from sklearn.feature_selection import mutual_info_classif,chi2,f_classif,SelectKBest
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt

def plot_scores(features,label,clf):
    filter_func=[f_classif,chi2,mutual_info_classif]#,'chi2','mutual_info_classif']
    df=pd.DataFrame()
    #filter_name=['Annova_accuracy','Annova_recall','chi2_accuracy','chi2_recall','mi_accuracy','mi_recall']
    filter_name=['Annova','chi2','mi']
    
    #scores=[]
    # count_ac=0
    # count_re=1
    count=0
    X_train, X_test, y_train, y_test = train_test_split(features, label, test_size=0.3,random_state=42)
    for j in filter_func:
        scores_ac=[]
        scores_re=[]
        score=[]
        number_features=[]
        for i in range(10,100,10):
            fil=SelectKBest(score_func=j, k=i)
            fil.fit(X_train,y_train)
            X_train_selected=X_train.loc[:, fil.get_support()]
            X_test_selected=X_test.loc[:, fil.get_support()]
            clf.fit(X_train_selected, y_train)
            y_pred = clf.predict(X_test_selected)
            # scores_ac.append(metrics.accuracy_score(y_test, y_pred)*100)
            # scores_re.append(metrics.recall_score(y_test, y_pred)*100)
            number_features.append(i)
            score.append((metrics.accuracy_score(y_test, y_pred)*100+metrics.recall_score(y_test, y_pred)*100)/2)
            print(score)
            # print(str(j)+"Accuracy:",metrics.accuracy_score(y_test, y_pred))
            # print(str(j)+"Recall:",metrics.recall_score(y_test, y_pred))
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)  
        # scores_ac.append(metrics.accuracy_score(y_test, y_pred)*100)
        # scores_re.append(metrics.recall_score(y_test, y_pred)*100)
        number_features.append(len(X_train.columns))
        score.append((metrics.accuracy_score(y_test, y_pred)*100+metrics.recall_score(y_test, y_pred)*100)/2)
        #df['features_number']= pd.Series(features_number)
        df[filter_name[count]] = pd.Series(score)
        count=count+1
        # df[filter_name[count_ac]] = pd.Series(scores_ac)
        # df[filter_name[count_re]] = pd.Series(scores_re)
        # count_ac=count_ac+2
        # count_re=count_re+2
    df['number_features']= pd.Series(number_features)
    df.set_index('number_features',inplace=True)
    # scores=[]      
    # clf.fit(X_train, y_train)
    # y_pred = clf.predict(X_test)
    # df[len(X_train.columns)] = pd.Series(scores)


    return df
    #     df1 = pd.DataFrame({'Filter': [ ],
    #                              i: scores }).set_index('Filters')
    #     dn.append(df1)    
    # dn = pd.concat(dn, axis=1)
    # return dn


def plot_max(df_scores,savepath):
    df_scores.plot(xticks=df_scores.index, marker='o',figsize=(20, 10),grid=True)
    plt.annotate("Max " + str(round(df_scores.max().max(),2)), (df_scores[df_scores.max().idxmax()].idxmax()+1, df_scores.max().max()),color='red')
    
    plt.savefig(savepath,dpi=300, bbox_inches = "tight")
    plt.show()

import pandas as pd
from sklearn.feature_selection import mutual_info_classif,chi2,f_classif,SelectKBest
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import keras
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf
import numpy as np
#import keras.tensflow 


def plot_scores(features,label,clf):
    filter_func=[f_classif,chi2,mutual_info_classif]
    df=pd.DataFrame()
    filter_name=['Annova','chi2','mi']
    count=0
    X_train, X_test, y_train, y_test = train_test_split(features, label, test_size=0.3,random_state=42)
    for j in filter_func:
        score=[]
        number_features=[]
        for i in range(10,100,10):
            fil=SelectKBest(score_func=j, k=i)
            fil.fit(X_train,y_train)
            X_train_selected=X_train.loc[:, fil.get_support()]
            X_test_selected=X_test.loc[:, fil.get_support()]
            clf.fit(X_train_selected, y_train)
            y_pred = clf.predict(X_test_selected)
            number_features.append(i)
            score.append((metrics.accuracy_score(y_test, y_pred)*100+metrics.recall_score(y_test, y_pred)*100)/2)
            print(score)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)  
        number_features.append(len(X_train.columns))
        score.append((metrics.accuracy_score(y_test, y_pred)*100+metrics.recall_score(y_test, y_pred)*100)/2)
        df[filter_name[count]] = pd.Series(score)
        count=count+1
    df['number_features']= pd.Series(number_features)
    df.set_index('number_features',inplace=True)

    return df


def plot_scores_nnn(features,label):
    filter_func=[f_classif,chi2,mutual_info_classif]#,'chi2','mutual_info_classif']
    df=pd.DataFrame()
    filter_name=['Annova','chi2','mi']
    count=0
    X_train, X_test, y_train, y_test = train_test_split(features, label, test_size=0.3,random_state=42)
    scaler = MinMaxScaler()
    scaler.fit(X_train)
    X_train_normalized = scaler.transform(X_train)
    X_test_normalized = scaler.transform(X_test)
    #scores=[]
    # count_ac=0
    # count_re=1
    for j in filter_func:
        score=[]
        number_features=[]
        # scores_ac=[]
        # scores_re=[]
        for i in range(10,100,10):
            
            fil=SelectKBest(score_func=j, k=i)
            fil.fit(X_train_normalized,y_train)
            X_train_normalized_selected=fil.transform(X_train_normalized)
            X_test_normalized_selected=fil.transform(X_test_normalized)
            #X_train_normalized_selected=X_train_normalized.loc[:, fil.get_support()]
            #X_test_normalized_selected=X_test_normalized.loc[:, fil.get_support()]
            # clf.fit(X_train, y_train)
            # y_pred = clf.predict(X_test)

            # Neural network
            keras.backend.clear_session()

            #tf.random.set_seed(0)
            model = Sequential()
            model.add(Dense(16, input_dim=X_train_normalized_selected.shape[1], activation='relu'))
            #model.add(Dense(12, activation='relu'))
            model.add(Dense(1, activation='sigmoid'))
            model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
            history = model.fit(X_train_normalized_selected, y_train, epochs=100, batch_size=64)
            y_pred = model.predict(X_test_normalized_selected)
            y_pred = tf.squeeze(y_pred)
            y_pred = np.array([1 if x >= 0.5 else 0 for x in y_pred])
            number_features.append(i)
            score.append((metrics.accuracy_score(y_test, y_pred)*100+metrics.recall_score(y_test, y_pred)*100)/2)
            print(score)
        model = Sequential()
        model.add(Dense(16, input_dim=X_train.shape[1], activation='relu'))
        #model.add(Dense(12, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        history = model.fit(X_train, y_train, epochs=100, batch_size=64)    
        y_pred = model.predict(X_test)
        y_pred = tf.squeeze(y_pred)
        y_pred = np.array([1 if x >= 0.5 else 0 for x in y_pred])
        number_features.append(len(X_train.columns))
        score.append((metrics.accuracy_score(y_test, y_pred)*100+metrics.recall_score(y_test, y_pred)*100)/2) 
        df[filter_name[count]] = pd.Series(score)
        count=count+1
        print(number_features)
    df['number_features']= pd.Series(number_features)
    df.set_index('number_features',inplace=True)   
        #     scores_ac.append(metrics.accuracy_score(test, pred)*100)
        #     scores_re.append(metrics.recall_score(test, pred)*100)
        #     #print(scores)
        #     print(str(j)+"Accuracy:",metrics.accuracy_score(test, pred))
        #     print(str(j)+"Recall:",metrics.recall_score(test, pred))
        # # clf.fit(X_train, y_train)
        # # y_pred = clf.predict(X_test)  
        # # scores_ac.append(metrics.accuracy_score(y_test, y_pred)*100)
        # # scores_re.append(metrics.recall_score(y_test, y_pred)*100)      
        # df[filter_name[count_ac]] = pd.Series(scores_ac)
        # df[filter_name[count_re]] = pd.Series(scores_re)
        # count_ac=count_ac+2
        # count_re=count_re+2
    
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


def plot_max(df_scores,title,savepath):#
    ax=df_scores.plot(xticks=df_scores.index, marker='o',figsize=(20, 10),grid=True)
    ax.set_title(title)
    ax.set_xlabel("Number of features")
    ax.set_ylabel("Performance Score [%]")
    plt.annotate("Max " + str(round(df_scores.max().max(),2)), (df_scores[df_scores.max().idxmax()].idxmax()+1, df_scores.max().max()),color='red')
    plt.savefig(savepath,dpi=300, bbox_inches = "tight")
    plt.show()

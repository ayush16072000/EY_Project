import numpy as np
from flask import Flask, request, jsonify, render_template
#import pickle
import os
import pandas as pd
from datewise import helperdate
#from dataframe_cov import helperfunc

app = Flask(__name__)
#model = pickle.load(open('model.pkl', 'rb'))
 #path =
print(os.getcwd())
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''

    int_features = [str(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    print("things are printing->", final_features[0])

    urljson = "https://api.covid19india.org/v4/data-" + final_features[0][0] + ".json"

    print("url_printing: ", urljson)


    path = os.getcwd()

    try:
        dfs = os.listdir(path + '/cache')
        #print("list of df: ", dfs)
        fileName = "df_" + str(final_features[0][0]) + ".csv"
        print("searching filename: ", fileName)
        for df in dfs:
            if(df == fileName):
                print("File found")
                dff = pd.read_csv(r'cache/'+str(fileName))
                dff = dff.sort_values(by = ['priority_score'], axis = 0)
                rank = [i for i in range(1,641)]
                dff['rank'] = rank
                #dff.set_index("District name")
                #print(dff)
                print("yes")
                try:
                    output = dff[dff["District name"] == final_features[0][1]]
                    active = output['active']
                    death = output['deceased']
                    recovered = output['recovered']
                    priority_score = output['priority_score']
                    rank = 641 - int(output['rank'])
                    if (final_features[0][2]):
                        #print("age", abs(int(final_features[0][2])-15))
                        age = int(final_features[0][2])
                        agerank = (641 - rank)/640*((abs(int(final_features[0][2])-15)+1)/100)*10
                        print(agerank)
                        return render_template('index.html', activec = '{}'.format(int(active)), deathc = '{}'.format(int(death)), recoveredc = '{}'.format(int(recovered)), rankc = '{}'.format(int(rank)), prediction_text='The overall Priority score is {} and out of 640 districts the rank is {} . Higher the score and lower the rank, severe is the situation for the district and it needs to be prioritized for vaccination.'.format(int(priority_score), rank), agedata = "The agewise priority is based on a 1-10 scale, and so the priority as per the given age of {} is {}".format(age, round(agerank, 2)))
                    else:
                        return render_template('index.html', activec = '{}'.format(int(active)), deathc = '{}'.format(int(death)), recoveredc = '{}'.format(int(recovered)), rankc = '{}'.format(int(rank)), prediction_text='The overall Priority score is {} and out of 640 districts the rank is {} . Higher the score and lower the rank, severe is the situation for the district and it needs to be prioritized for vaccination.'.format(int(priority_score), rank))
                except:
                    return render_template('index.html', activec = '0', deathc = '0', recoveredc = '0', rankc = '0', prediction_text='Either the {} is not listed or please check the correct spelling for the corresponding district.'.format(final_features[0][1]))

    except:
        print("It may take time")

    df = helperdate(urljson, final_features[0][1], final_features[0][0])
    df = df.reset_index()
    #print(df)
    df = df.sort_values(by = ["priority_score"], axis = 0)
    rank = [i for i in range(1,641)]
    df['rank'] = rank
    #print(df)
    output = df[df['District name'] == final_features[0][1]]
    active = output['active']
    death = output['deceased']
    recovered = output['recovered']
    priority_score = output['priority_score']
    rank = 641 - int(output['rank'])
    return render_template('index.html', activec = '{}'.format(int(active)), deathc = '{}'.format(int(death)), recoveredc = '{}'.format(int(recovered)), rankc = '{}'.format(int(rank)), prediction_text='The overall Priority score is {} and out of 640 districts the rank is {} . Higher the score and lower the rank, severe is the situation for the district and it needs to be prioritized for vaccination.'.format(int(priority_score), rank))

    #return render_template('index.html', prediction_text='Employee Salary should be $ {}'.format(output))

if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == "__main__":
#     app.run(host ='0.0.0.0', port = 5001, debug = True)

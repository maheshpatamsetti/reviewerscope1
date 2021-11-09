#!flask/bin/python
from flask import Flask, send_from_directory, request
import os, json, zipfile, csv, collections, ast

SOURCE_DIRECTORY = '../tosend/'
app = Flask(__name__)
@app.route('/')
def send():
    print("zipping and sending results")
    # userpath = os.path.abspath("../users/"+str(request.args.get('user')))
    userpath = request.args.get('user')
    print("user path: ",str(request.args.get('user')))
    logfile = userpath+"/tosend/logs"

  ########################### zipping output files ##########################
    # zipf = zipfile.ZipFile('../tosend/out.zip','w', zipfile.ZIP_DEFLATED)
    # for _,_, files in os.walk('../tosend/'):
    #     for file in files:
    #         if ".zip" not in file: 
    #             zipf.write("../tosend/"+file)
    # zipf.close()
    # return send_from_directory(SOURCE_DIRECTORY, "out.zip", as_attachment=True)
    # return json.dumps({'success':True, 'top': names, 'recommended': fa}), 200, {'ContentType':'application/json'}
    recommended = None
    with open(userpath+"/tosend/topreviewers.json") as json_file:
        recommended = json.loads(json_file.read())
    for key, value in recommended.items():
        recommended[key] = ast.literal_eval(value)
    assignments = collections.defaultdict(list)
    try:
        with open(userpath+"/tosend/finalassignments") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                assignments[row[0]].append(row)
    except:
        with open(logfile, "w") as f:
            f.write("Send Service: Finalassignment not found")
        f.close()
            
    relevantpapers = []
    with open(userpath+"/tosend/mostrelevantreviewerpaper.json") as json_file:
        relevantpapers = json.loads(json_file.read())
        
    json_data=open(userpath+"/submissions.json").read()
    submission_list = json.loads(json_data)

    # read missing reviewers into missing_reviewers_list[]
    missing_reviewers_list = []
    try:
        with open(userpath+"/tosend/missingreviewers.txt") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                    missing_reviewers_list.append(row)
    except:
        with open(logfile, "w") as f:
            f.write("Send Service: missing reviewers not found")
        f.close()

    ##### sending top reviewer scores ######
    toprscores = None
    with open(userpath+"/tosend/topreviewerscores.json") as json_file:
        toprscores = json.loads(json_file.read())
    
    ##### sending top reviewer scores ######
    coinames = None
    with open(userpath + "/tosend/coinames.json") as json_file:
        coinames = json.loads(json_file.read())

    ##### sending sources of conflict ######
    sourcesofconflict = None
    with open(userpath + "/tosend/sourcesofconflicts.json") as json_file:
        sourcesofconflict = json.loads(json_file.read())

    ##### testing additional files ######
    finaldictionary = None
    ini_string = {'nikhil': 1, 'akash' : 5, 
              'manjeet' : 10, 'akshat' : 15}  
    ini_string = json.dumps(ini_string)
    finaldictionary = json.loads(ini_string)
        
    return json.dumps({'success':True, 'assignment': assignments, 'recommended': recommended, \
        'submissions': submission_list, 'missingreviewers': missing_reviewers_list, \
        'relevantpapers': relevantpapers, 'toprscores': toprscores, 'coinames': coinames, \
        'finaldictionary': finaldictionary, 'sourcesofconflict': sourcesofconflict}), \
        200, {'ContentType':'application/json'}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 9095))
    app.run(host='0.0.0.0', port=port)
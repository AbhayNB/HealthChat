from flask import Flask, render_template, request, redirect
import os
import openai
data=[('Select The Health Condition ','And Severity of Condition to continue')]
app=Flask(__name__)
hel=None
sev=None
api=os.environ.get('OPENAI_API_KEY')
def formq(a,d):
    query=""
    for i,j in d:
        query+=f"\nMe: {i}\nChatBot:{j}"
    query+=f"\nMe: {a}\nChatBot:"
    return query
def ans(q):
    openai.api_key = api
    start_sequence = "\nAdua:"
    restart_sequence = "\nYou: "
    query= q
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=query,
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" You:", " Adua:"]
    )
    return response.choices[0].text
@app.route('/cat',methods=['GET','POST'])
def category():
    global data
    global hel
    global sev
    if request.method=='POST':
        h= request.form['health']
        hel=h
        c= request.form['severity']
        sev=c
        data=[(f"I have this {h} with severity {c}, give details about this",ans(f'I have this {h} with severity {c}, give details about this'))]
        return redirect('/#{}'.format(len(data)-1))
    return redirect('/#{}'.format(len(data)-1))
@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        openai.api_key = api
        start_sequence = "\nAdua:"
        restart_sequence = "\nYou: "
        query= request.form['book']
        q=formq(query,data)
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=q,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" You:", " Adua:"]
        )
        data.append((query,response.choices[0].text ))
        return redirect('/#{}'.format(len(data)-1))
    return render_template('chat.html',data=data,h=hel,s=sev)
@app.route('/next')
def nextpage():
    return """This is next page <br>
Abhi kuch ni h isme <br>
<a href="/">back</a>"""
if __name__=='__main__':
    app.run(debug=True)
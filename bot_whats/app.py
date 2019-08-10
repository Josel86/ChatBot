from flask import Flask, render_template, request, jsonify 
from pusher import Pusher
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import random
import pickle
import json
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from twilio.twiml.messaging_response import MessagingResponse
import requests
from twilio.rest import Client

app = Flask(__name__)
pusher = Pusher(app_id=u'835900', key=u'e3412dad9232d73e7e37', secret=u'637a314baf4cd55a5499', cluster=u'mt1')
API_KEY = 'c196af53f56d479184268d74c3d967c7'
ENDPOINT = 'https://southcentralus.api.cognitive.microsoft.com/text/analytics/v2.1/sentiment'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/eTicket.db"
db = SQLAlchemy(app)

class Comanda(db.Model):
    __tablename__ = 'Comanda'
    id = db.Column(db.Integer, primary_key=True)
    noTicket = db.Column(db.Integer)
    status = db.Column(db.Integer)
    descripcion = db.Column(db.String)
    nombreCliente = db.Column(db.String)
    articulos = db.Column(db.String)
    comentarios = db.Column(db.String)
    def __repr__(self):
        return '<Comanda %r>' % (self.id)

class ventas_db(db.Model):
    __tablename__ = 'ventas_db'

    Id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.String)
    BillNumber = db.Column(db.String)
    Description = db.Column(db.String)
    Time1 = db.Column(db.String)
    Time = db.Column(db.String)
    Day = db.Column(db.String)
    TimeBucket = db.Column(db.String)
    Category2 = db.Column(db.String)
    Rate = db.Column(db.Integer)
    Total = db.Column(db.Float)
    Cost = db.Column(db.Float)
    Profits = db.Column(db.Float)

    def __repr__(self):
        return '<ventas_db %r>' % (self.Id)
    
class Comentarios(db.Model):
    __tablename__ = 'Comentarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    comentario = db.Column(db.String)
    clasificacion = db.Column(db.String)
    telefono = db.Column(db.String)

    def __repr__(self):
        return '<ventas_db %r>' % (self.Id)
    

stemmer = LancasterStemmer()
app.secret_key = 'AWSEATD'
# import our chat-bot intents file
data = pickle.load( open( "training_data", "rb" ) )
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

# import our chat-bot intents file
with open('intents.json') as json_data:
    intents = json.load(json_data)
# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)
# load our saved model
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
model.load('./model.tflearn')

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))

def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# create a data structure to hold user context
context = {}

ERROR_THRESHOLD = 0.25
def classify(sentence):
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list

def response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents['intents']:
                # find a tag matching the first result
                if i['tag'] == results[0][0]:
                    # set context for this intent if necessary
                    if 'context_set' in i:
                        if show_details: print ('context:', i['context_set'])
                        context[userID] = i['context_set']

                    # check if this intent is contextual and applies to this user's conversation
                    if not 'context_filter' in i or \
                        (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details: print ('tag:', i['tag'])
                        # a random response from the intent
                        return random.choice(i['responses'])

            results.pop(0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/ventas')
def ventas():
    # Query all passengers
    description = request.values.get('Description')
    print(description)
    search = "%{}%".format(description)
    posts = ventas_db.query.filter(ventas_db.Description.like(search)).first()
    db.session.commit()

    if posts is None:
        posts = ''
    else:
        posts = {
            posts.Description : posts.Total 
          }
    return jsonify(posts)


@app.route('/sendWhats')
def sendWhats():
    print('send whats')
    
    if "1" in request.values.get("name"):
        url = 'https://bit.ly/whatsapp-image-example'
    elif "2" in request.values.get("name"):
        url = 'https://bit.ly/whatsapp-image-example'
    else:
        url = 'https://bit.ly/whatsapp-image-example'
    # Query all passengers
    account_sid = 'AC05d2b6ca63a79b7246ef86c173e11983'
    auth_token = '8f0d28a4c59b1a131d74b5f2c18c84ba'
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
                                  body= 'Recomendation 🌮' + '' + url,
                                  from_='whatsapp:+14155238886',
                                  to='whatsapp:+5215539936847',
                              )
    print(message.sid)
    return 'El whats app se envio correctamente'
    

@app.route('/selMessage')
def select_comment():
    # Query all passengers
    results = db.session.query(Comentarios.id, Comentarios.nombre, Comentarios.comentario, Comentarios.clasificacion, Comentarios.telefono).all()
    db.session.commit()
    return jsonify(results)

def get_articulo(description):
    # Query all passengers
    print(description)
    search = "%{}%".format(description)
    posts = ventas_db.query.filter(ventas_db.Description.like(search)).first()
    db.session.commit()

    if posts is None:
        return None, None
    else:
        return posts.Description, posts.Total 
#        posts = {
  #          posts.Description : posts.Total 
 #         }

def insert_comment(nombre, description, phone):
    # Query all passengers
    score = analysis_text(description)
    if(score <= 0.33):
        clasificacion = 'Bad'
    elif (score <= 0.66):
        clasificacion = 'Neutral'
    else:
        clasificacion = 'Good'
    comments = Comentarios(nombre = nombre, comentario = description, clasificacion=clasificacion, telefono=phone)
    
    db.session.add(comments)
    db.session.commit()
    
    pusher.trigger(u'message', u'send', {
        u'name': nombre,
        u'message': description,
        u'clasificacion': clasificacion,
        u'telefono': phone
        })

    
    return 'Ok'
    
def analysis_text(text):
    print('Processing: ' + text)
    headers  = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': API_KEY
    }
    params   = {
        'showStats': True,
    }
    body = {
      "documents": [     
            {
            "language": "en",
            "id": "1",
            "text": text
            }
        ]
    }
    response = requests.post(ENDPOINT, headers=headers, params=params, data=str(body))
    results = json.loads(response.content)
    return float(results['documents'][0]['score'])

@app.route('/ventasall')
def ventasall():
    # Query all passengers
    posts = db.session.query(ventas_db.Description, ventas_db.Total).all()
    db.session.commit()
    return jsonify(posts)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    media_files = []
    num_media = int(request.values.get("NumMedia"))
    resp = MessagingResponse()
    
    if not num_media:
        question = request.values.get('Body')
        cellphone = request.values.get('From')
        
        grupo = classify(question)[0][0]
        respuesta = response(question)
        if('name' in grupo):
            # Query all passengers
            results = db.session.query(Comanda.id, Comanda.noTicket, Comanda.status, Comanda.descripcion,
            Comanda.nombreCliente, Comanda.articulos, Comanda.comentarios).all()
     
            if len(results) == 0:
                # Insert
                comanda = Comanda(nombreCliente = question.split()[-1])
                db.session.add(comanda)
                db.session.commit()
                respuesta = "Hi, " + question.split()[-1] + ". What do you want to eat?"
            else:
                name = [result[4] for result in results][0]
                respuesta = "Sorry, I think you are " + name + ". What do you want to eat?"
            resp.message(get_description('Smart Rest ' + '\U0001F31F' , respuesta, ""))
            return str(resp)

        if('buy' in grupo):
            descArt = question
            number = [int(s) for s in descArt.split() if s.isdigit()]
            if len(number) > 0:
                descArt = descArt.rstrip('s')
                indice = descArt.index(str(number[0])) + len(str(number[0])) + 1
                descArt = descArt[indice::]
                cantidad = number[0]
                descArt, importe = get_articulo(descArt)
                #importe = articulos.get(descArt)
            else: 
                cantidad = 1
                descArt = descArt.split()[-1]
                descArt, importe = get_articulo(descArt)
#                importe = articulos.get(descArt)            
            if importe is None:
                respuesta = "I'm so sorry, We don't have this food. I'll send you my recommendation"
                resp.message(get_description('Smart Rest 😭' , respuesta, "http://www.restaurantedondecarol.com/noticias.php"))
                return str(resp)
            else:
                # Query all passengers
                result = db.session.query(Comanda.id, Comanda.noTicket, Comanda.status, Comanda.descripcion,
                    Comanda.nombreCliente, Comanda.articulos, Comanda.comentarios).first()

                comandas = []
                articulo = {
                    "cantidad": cantidad,
                    "name": descArt,
                    "importe": importe
                }

                if result is None:
                    comandas.append(articulo)
                    comanda = Comanda(articulos = json.dumps(comandas))
                    db.session.add(comanda)
                    db.session.commit()
                else:
                    if result.articulos is None:
                        comandas.append(articulo)
                        Comanda.query.filter_by(id=result.id).update(dict(articulos=json.dumps(comandas)))
                    else:
                        data = json.loads(result.articulos)
                        data.append(articulo)
                        Comanda.query.filter_by(id=result.id).update(dict(articulos=json.dumps(data)))
                                
                    db.session.commit()
                respuesta = "Mmm, It's delicious, Do you want anything else?"
            resp.message(get_description('Smart Rest 🌮' , respuesta, ""))
            return str(resp)

        if('comment' in grupo):
            # Query all passengers
            result = db.session.query(Comanda.id, Comanda.noTicket, Comanda.status, Comanda.descripcion,
                    Comanda.nombreCliente, Comanda.articulos, Comanda.comentarios).first()

            if result is None:
                respuesta = "I'. sorry, can you tell me. What's your name"
            else:
                Total = 0.00
                insert_comment(result.nombreCliente, question, cellphone)
                dataItems = json.loads(result.articulos)
                for d in dataItems:
                    importe = float(d['importe'])
                    Total += importe
                    pusher.trigger(u'order', u'details', {
                        u'noTicket': result.id,
                        u'cantidad': d['cantidad'],
                        u'descripcion': d['name'],
                        u'importe': d['importe'],
                        u'cliente': result.nombreCliente,
                        u'fuente': 'w'
                    })
                pusher.trigger(u'order', u'place', {
                    u'units': str(Total)
                    })
                Comanda.query.filter_by(id=result.id).delete()
                db.session.commit()
            resp.message(get_description('Smart Rest 📖' , respuesta,""))
            return str(resp)
    
        if('cost' in grupo):
            # Query all passengers
            result = db.session.query(Comanda.id, Comanda.noTicket, Comanda.status, Comanda.descripcion,
                    Comanda.nombreCliente, Comanda.articulos, Comanda.comentarios).first()

            if result is None:
                respuesta = "Do you want to buy something?"
            else:
                if result.articulos is None:
                    respuesta = "Do you want to buy something?"
                else:
                    Total = 0.00
                    respuesta = ''
                    data = json.loads(result.articulos)
                    for d in data:
                        importe = float(d['importe'])
                        cantidad = float(d['cantidad'])
                        respuesta += str(d['cantidad']) + ' ' +  d['name'] + ' - ' + str(cantidad * importe) + '\n'
                        Total += cantidad * importe
                    respuesta += '\rIt costs $ ' + str(Total) + '. Do you have some comment?'
            resp.message(get_description('Smart Rest Order ☝' , respuesta,""))
            return str(resp)
        resp.message(get_description('Smart Rest ' + '\U0001F604' , respuesta,""))
        return str(resp)
    else:
        for idx in range(num_media):
            media_url = request.values.get(f'MediaUrl{idx}')
            mime_type = request.values.get(f'MediaContentType{idx}')
            media_files.append((media_url, mime_type))
            req = requests.get(media_url)
            file_extension = mimetypes.guess_extension(mime_type)
            media_sid = os.path.basename(urlparse(media_url).path)

            with open(f"app_data/{media_sid}{file_extension}", 'wb') as f:
                f.write(req.content)
           
            print(media_url)
        
        msg = resp.message("Tengo hambre.")
    #        msg.media(GOOD_BOY_URL)

    return resp.message(str(resp))
# Helper function to get an emoji's description
def get_description(title,description,url):
    # And template it
    return render_template(
        'response.txt',
        title=title,
        description=description,
        url= url)

if __name__ == '__main__':
	app.run(debug=True)
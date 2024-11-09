from flask import Flask, request, jsonify
import smtplib
import email.message

app = Flask(__name__)

def enviar_email(destinatario, assunto, corpo):
    msg = email.message.Message()
    msg['Subject'] = assunto
    msg['From'] = 'lucastftoliveira@gmail.com'
    msg['To'] = destinatario
    password = 'rorn ymwa npwo divm'  # Substitua pela senha do app do Gmail
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls()
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Email enviado com sucesso')
        return "Email enviado com sucesso", 200
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return f"Erro ao enviar email: {e}", 500

# Rota para enviar e-mail via API
@app.route('/enviar_email', methods=['POST'])
def api_enviar_email():
    data = request.get_json()
    
    destinatario = data.get('destinatario')
    assunto = data.get('assunto')
    corpo = data.get('corpo')
    
    if not destinatario or not assunto or not corpo:
        return jsonify({"error": "Todos os campos (destinatario, assunto, corpo) são obrigatórios."}), 400
    
    status, code = enviar_email(destinatario, assunto, corpo)
    return jsonify({"status": status}), code

if __name__ == '__main__':
    app.run(port=5000)

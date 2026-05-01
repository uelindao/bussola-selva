import streamlit as st
import time
import smtplib
from email.message import EmailMessage
import ssl

# ── configuração da página e estilo ───────────────────────────────────────────
st.set_page_config(page_title="bússola selva", page_icon="🌿", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600&family=Inter:wght@300;400;500&display=swap');
*,*::before,*::after{box-sizing:border-box;}
html,body,.stApp{background:#161615!important;color:#EAE8E3!important;font-family:'Inter',sans-serif!important;}
.stApp::before{display:none!important;}

.arch-header{text-align:center;padding:2rem 1rem 1rem;}
.arch-header h1{font-family:'Montserrat',sans-serif;font-size:2.5rem;font-weight:500;letter-spacing:-0.05em;
color:#EAE8E3!important;line-height:1.1;margin-bottom:0.4rem;text-transform:lowercase;}
.arch-header p{color:#8C8881;font-size:0.9rem;font-family:'Inter',sans-serif;letter-spacing:0.02em;text-transform:lowercase;}

.question-box {background:#1C1B1A; padding: 2rem; border: 1px solid #2A2928; margin-top: 2rem;}
.question-title {font-family:'Montserrat',sans-serif; font-size:1.2rem; color:#EAE8E3; margin-bottom: 1.5rem; text-transform:lowercase;}

.stRadio > label {display:none;} /* esconde o label padrão do radio */
.stRadio > div {display: flex; flex-direction: column; gap: 1rem;}
.stRadio > div > label {
    background:#121211!important; border:1px solid #2A2928!important; padding: 1rem!important; 
    border-radius: 0px!important; color:#8C8881!important; font-family:'Inter',sans-serif!important;
    text-transform:lowercase; cursor:pointer; transition: all 0.2s ease;
}
.stRadio > div > label:hover {border-color: #C49A6C!important; color: #EAE8E3!important;}

.stButton>button {background:#213326!important; color:#EAE8E3!important; border:none!important; border-radius:0px!important;
font-family:'Inter',sans-serif!important; font-weight:400!important; font-size:0.9rem!important;
text-transform:lowercase!important; padding: 0.8rem 2rem!important; margin-top: 2rem; width: 100%; transition:all 0.2s ease-in-out!important;}
.stButton>button:hover {background:#1A291E!important;}

.stTextInput>div>div>input {background:#121211!important; border:1px solid #2A2928!important; border-radius:0px!important;
color:#EAE8E3!important; font-family:'Inter',sans-serif!important; padding: 0.8rem!important;}
.stTextInput>label {font-family:'Inter',sans-serif!important; font-size:0.8rem!important; color:#8C8881!important; text-transform:lowercase!important;}

.dossier-box {background:#121211; border: 1px solid #C49A6C; padding: 2rem; margin-top: 1rem;}
.dossier-title {font-family:'Montserrat',sans-serif; font-size:1.1rem; color:#C49A6C; text-transform:lowercase; letter-spacing:0.1em; margin-bottom:1rem;}
.dossier-text {font-family:'Inter',sans-serif; font-size:0.9rem; color:#EAE8E3; line-height:1.6; text-transform:lowercase;}
</style>
""", unsafe_allow_html=True)

# ── gerenciamento de estado (passos do wizard) ───────────────────────────────
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

def next_step():
    st.session_state.step += 1

def reset_app():
    st.session_state.step = 0
    st.session_state.answers = {}

# ── cabeçalho global ─────────────────────────────────────────────────────────
st.markdown("""
<div class="arch-header">
    <h1>bússola selva</h1>
    <p>onde você habita, define como você vive.</p>
</div>
""", unsafe_allow_html=True)

# ── passo 0: introdução ──────────────────────────────────────────────────────
if st.session_state.step == 0:
    st.markdown("""
    <div style="text-align:center; color:#8C8881; font-family:'Inter',sans-serif; font-size:1rem; line-height:1.6; max-width: 600px; margin: 0 auto 2rem; text-transform:lowercase;">
        descubra a essência da sua futura casa em uma experiência sensorial de 2 minutos. 
        ao final, nossa inteligência artificial irá traçar o seu perfil arquitetônico e revelar o ecossistema ideal para o seu modo de viver.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("iniciar jornada"):
            next_step()
            st.rerun()

# ── passo 1: a manhã ideal (biofilia vs tech) ────────────────────────────────
elif st.session_state.step == 1:
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">1. como é a sua manhã ideal na nova casa?</div>', unsafe_allow_html=True)
    
    q1 = st.radio("escolha:", [
        "acordar com a luz do sol filtrada por um jardim denso e tomar café sentindo a brisa",
        "acordar com a automação abrindo as persianas e ajustando a climatização silenciosamente"
    ], key="q1")
    
    if st.button("próximo", key="btn1"):
        st.session_state.answers['manha'] = q1
        next_step()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── passo 2: conexão social ──────────────────────────────────────────────────
elif st.session_state.step == 2:
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">2. quando recebem amigos, onde a magia acontece?</div>', unsafe_allow_html=True)
    
    q2 = st.radio("escolha:", [
        "em uma cozinha gourmet espaçosa, integrando quem cozinha e quem conversa",
        "na área externa, ao redor de um fogo de chão ou de uma piscina natural integrada"
    ], key="q2")
    
    if st.button("próximo", key="btn2"):
        st.session_state.answers['social'] = q2
        next_step()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── passo 3: objeção silenciosa (valor vs preço) ─────────────────────────────
elif st.session_state.step == 3:
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">3. ao pensar no investimento, o que faz mais sentido para vocês?</div>', unsafe_allow_html=True)
    
    q3 = st.radio("escolha:", [
        "sustentabilidade inteligente que gera economia futura (solar, cisterna), mesmo exigindo maior investimento inicial",
        "reduzir o custo imediato da obra ao máximo, priorizando a estética antes da eficiência térmica e energética"
    ], key="q3")
    
    if st.button("próximo", key="btn3"):
        st.session_state.answers['investimento'] = q3
        next_step()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── passo 4: medos reais ─────────────────────────────────────────────────────
elif st.session_state.step == 4:
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">4. qual é a sua maior preocupação ao pensar em construir?</div>', unsafe_allow_html=True)
    
    q4 = st.radio("escolha:", [
        "a obra virar um caos, com imprevisibilidade, retrabalhos e atrasos",
        "estourar o orçamento sem controle prévio ou aviso",
        "a casa ficar parecendo 'de catálogo', genérica e sem a nossa identidade"
    ], key="q4")
    
    if st.button("próximo", key="btn4"):
        st.session_state.answers['medo'] = q4
        next_step()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── passo 5: captação do lead (o gate) ───────────────────────────────────────
elif st.session_state.step == 5:
    st.markdown("""
    <div style="text-align:center; color:#EAE8E3; font-family:'Montserrat',sans-serif; font-size:1.2rem; margin-bottom:1rem; text-transform:lowercase;">
        sua essência foi mapeada.
    </div>
    <div style="text-align:center; color:#8C8881; font-family:'Inter',sans-serif; font-size:0.9rem; margin-bottom:2rem; text-transform:lowercase;">
        nossa inteligência está pronta para gerar o seu dossiê técnico e de viabilidade. para onde devemos enviar o seu resultado?
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        nome = st.text_input("como devemos chamar vocês?")
        email = st.text_input("qual o seu melhor e-mail?")
        whatsapp = st.text_input("whatsapp com ddd")
        
        if st.button("revelar minha casa ideal", key="btn5"):
            if nome and email and whatsapp:
                st.session_state.answers['lead'] = {'nome': nome, 'email': email, 'whatsapp': whatsapp}
                next_step()
                st.rerun()
            else:
                st.warning("por favor, preencha todos os campos para continuarmos.")

# ── passo 6: processamento e resultado ───────────────────────────────────────
elif st.session_state.step == 6:
    nome_casal = st.session_state.answers['lead']['nome']
    
    # Efeito de loading falso para dar peso à "análise da IA"
    with st.spinner("cruzando dados sensoriais com arquitetura de alto desempenho..."):
        time.sleep(3)
        
    st.markdown(f"""
    <div style="text-align:center; color:#EAE8E3; font-family:'Montserrat',sans-serif; font-size:1.5rem; margin-bottom:2rem; text-transform:lowercase;">
        olá, {nome_casal}. bem-vindos ao futuro de vocês.
    </div>
    """, unsafe_allow_html=True)
    
    # Lógica simples baseada nas respostas para personalizar o dossiê
    bio_vs_tech = "uma forte conexão com a natureza e design biofílico" if "jardim" in st.session_state.answers['manha'] else "integração tecnológica e conforto invisível"
    foco_social = "a cozinha gourmet será o coração pulsante da casa" if "cozinha" in st.session_state.answers['social'] else "a área externa será o refúgio perfeito para encontros"
    medo = st.session_state.answers['medo'].split(',')[0]
    
    # Dossiê
    st.markdown(f"""
    <div class="dossier-box">
        <div class="dossier-title">✦ dossiê de viabilidade selva</div>
        <div class="dossier-text">
            analisamos o perfil de vocês e o resultado é claro: o projeto ideal exige {bio_vs_tech}, onde {foco_social}.<br><br>
            notamos que a maior preocupação de vocês é {medo}. por isso, o sistema construtivo perfeito para o seu perfil (como o woodframe ou steel frame) atrelado a um projeto executivo milimetricamente detalhado será essencial. isso blinda o investimento de vocês contra surpresas.<br><br>
            vocês valorizam um ecossistema completo — não apenas a planta, mas uma habitação de alto desempenho que respeite a história e a rotina da família.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # CTA Final focado na segurança emocional
    st.markdown("""
    <div style="text-align:center; color:#8C8881; font-family:'Inter',sans-serif; font-size:0.9rem; margin-bottom:1rem; text-transform:lowercase;">
        todo grande projeto começa com uma conversa honesta. vamos entender como materializar essa essência no seu terreno?
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("agendar reunião de alinhamento com a selva"):
            with st.spinner("enviando seus dados para a selva..."):
                try:
                    # Configurando a estrutura do e-mail
                    msg = EmailMessage()
                    msg['Subject'] = f"✦ Novo Lead Qualificado: {nome_casal}"
                    msg['From'] = st.secrets["email"]["sender"]
                    msg['To'] = st.secrets["email"]["receiver"]
                    
                    # Corpo do e-mail com todas as respostas
                    body = f"""
                    NOVO LEAD CAPTADO PELA BÚSSOLA SELVA
                    
                    DADOS DE CONTATO:
                    Nome: {st.session_state.answers['lead']['nome']}
                    E-mail: {st.session_state.answers['lead']['email']}
                    WhatsApp: {st.session_state.answers['lead']['whatsapp']}
                    
                    RESPOSTAS DO DIAGNÓSTICO:
                    1. Manhã Ideal (Biofilia x Tech):
                    {st.session_state.answers['manha']}
                    
                    2. Conexão Social (Layout):
                    {st.session_state.answers['social']}
                    
                    3. Investimento (Sustentabilidade x Custo):
                    {st.session_state.answers['investimento']}
                    
                    4. Maior Preocupação (Dores):
                    {st.session_state.answers['medo']}
                    
                    ---
                    Este e-mail foi gerado automaticamente pelo aplicativo Bússola Selva.
                    """
                    msg.set_content(body)
                    
                    # Conectando ao servidor do Google e enviando
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                        server.login(st.secrets["email"]["sender"], st.secrets["email"]["password"])
                        server.send_message(msg)
                        
                    st.success("recebemos seus dados! nossa equipe entrará em contato pelo whatsapp em breve.")
                
                except Exception as e:
                    st.error("Ops! Tivemos um pequeno erro ao enviar os dados. Por favor, chame a gente direto no Instagram!")
                    print(f"Erro no envio de email: {e}")

        if st.button("refazer jornada"):
            reset_app()
            st.rerun()
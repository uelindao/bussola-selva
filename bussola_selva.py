import streamlit as st
import time
import smtplib
from email.message import EmailMessage
import ssl
import html 

# ── configuração da página e estilo ───────────────────────────────────────────
st.set_page_config(page_title="bússola selva", page_icon="🌿", layout="centered")

# injeção do fontawesome para os ícones e estilos css (sem linhas em branco para evitar quebra no streamlit)
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600&family=Inter:wght@300;400;500&display=swap');
*,*::before,*::after{box-sizing:border-box;}
html,body,.stApp{background:#161615!important;color:#EAE8E3!important;font-family:'Inter',sans-serif!important;}
.stApp::before{display:none!important;}
.arch-header{text-align:center;padding:2.5rem 1.5rem;background-color:#1A291E;border:1px solid #2E4534;border-radius:8px;margin-bottom:2rem;margin-top:1rem;}
.arch-header h1{font-family:'Montserrat',sans-serif;font-size:2.5rem;font-weight:600;letter-spacing:-0.05em;color:#EAE8E3!important;line-height:1.1;margin-bottom:0.6rem;text-transform:lowercase;}
.arch-header p{color:#8C8881;font-size:1rem;font-family:'Inter',sans-serif;letter-spacing:0.02em;text-transform:lowercase;margin:0;}
.question-title{font-family:'Montserrat',sans-serif;font-size:1.2rem;color:#EAE8E3;margin-bottom:1.5rem;text-transform:lowercase;font-weight:500;}
.stRadio>div{display:flex;flex-direction:column;gap:1rem;}
.stRadio>div>label{background:#121211!important;border:1px solid #2A2928!important;padding:1rem!important;border-radius:4px!important;color:#8C8881!important;font-family:'Inter',sans-serif!important;text-transform:lowercase;cursor:pointer;transition:all 0.2s ease;}
.stRadio>div>label:hover{border-color:#C49A6C!important;color:#EAE8E3!important;}
.stButton>button{background:#2E4534!important;color:#EAE8E3!important;border:none!important;border-radius:4px!important;font-family:'Inter',sans-serif!important;font-weight:500!important;font-size:1rem!important;text-transform:lowercase!important;padding:0.8rem 2rem!important;margin-top:2rem;width:100%;transition:all 0.2s ease-in-out!important;}
.stButton>button:hover{background:#1A291E!important;color:#C49A6C!important;}
.stTextInput>div>div>input{background:#121211!important;border:1px solid #2A2928!important;border-radius:4px!important;color:#EAE8E3!important;font-family:'Inter',sans-serif!important;padding:0.8rem!important;}
.stTextInput>label{font-family:'Inter',sans-serif!important;font-size:0.85rem!important;color:#8C8881!important;text-transform:lowercase!important;}
div[data-testid="stVerticalBlock"] div[data-testid="stTextInput"]:nth-of-type(4){display:none !important;}
.dossier-box{background:#121211;border:1px solid #C49A6C;padding:2rem;margin-top:1rem;border-radius:4px;}
.dossier-title{font-family:'Montserrat',sans-serif;font-size:1.1rem;color:#C49A6C;text-transform:lowercase;letter-spacing:0.1em;margin-bottom:1rem;font-weight:600;}
.dossier-text{font-family:'Inter',sans-serif;font-size:0.95rem;color:#EAE8E3;line-height:1.7;text-transform:lowercase;}
.footer-container{display:flex;justify-content:space-between;margin-top:5rem;padding-top:3rem;border-top:1px solid #2A2928;color:#8C8881;font-family:'Inter',sans-serif;font-size:0.85rem;text-transform:lowercase;}
.footer-col{display:flex;flex-direction:column;gap:2rem;}
.footer-col-right{text-align:right;}
.footer-title{font-family:'Montserrat',sans-serif;font-size:1.1rem;color:#EAE8E3;margin-bottom:0.8rem;font-weight:400;letter-spacing:0.15em;text-transform:lowercase;}
.footer-text{margin:0.3rem 0;line-height:1.5;}
.footer-socials{display:flex;gap:1.2rem;font-size:1.5rem;margin-top:0.5rem;}
.footer-col-right .footer-socials{justify-content:flex-end;}
.footer-socials a{color:#EAE8E3;transition:color 0.2s ease;text-decoration:none;}
.footer-socials a:hover{color:#C49A6C;}
.footer-copy{text-align:right;margin-top:3rem;margin-bottom:2rem;font-size:0.75rem;color:#8C8881;text-transform:lowercase;}
@media(max-width:768px){.footer-container{flex-direction:column;gap:2.5rem;}.footer-col-right{text-align:left;}.footer-col-right .footer-socials{justify-content:flex-start;}.footer-copy{text-align:center;}}
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
    
    # ajuste das colunas para centralizar o botão perfeitamente
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("iniciar jornada"):
            next_step()
            st.rerun()

# ── passo 1: a manhã ideal (biofilia vs tech) ────────────────────────────────
elif st.session_state.step == 1:
    st.markdown('<div class="question-title" style="margin-top: 2rem;">1. como é a sua manhã ideal na nova casa?</div>', unsafe_allow_html=True)
    
    q1 = st.radio("escolha:", [
        "acordar com a luz do sol filtrada por um jardim denso e tomar café sentindo a brisa",
        "acordar com a automação abrindo as persianas e ajustando a climatização silenciosamente"
    ], key="q1", label_visibility="collapsed")
    
    if st.button("próximo", key="btn1"):
        st.session_state.answers['manha'] = q1
        next_step()
        st.rerun()

# ── passo 2: conexão social ──────────────────────────────────────────────────
elif st.session_state.step == 2:
    st.markdown('<div class="question-title" style="margin-top: 2rem;">2. quando recebem amigos, onde a magia acontece?</div>', unsafe_allow_html=True)
    
    q2 = st.radio("escolha:", [
        "em uma cozinha gourmet espaçosa, integrando quem cozinha e quem conversa",
        "na área externa, ao redor de um fogo de chão ou de uma piscina natural integrada"
    ], key="q2", label_visibility="collapsed")
    
    if st.button("próximo", key="btn2"):
        st.session_state.answers['social'] = q2
        next_step()
        st.rerun()

# ── passo 3: objeção silenciosa (valor vs preço) ─────────────────────────────
elif st.session_state.step == 3:
    st.markdown('<div class="question-title" style="margin-top: 2rem;">3. ao pensar no investimento, o que faz mais sentido para vocês?</div>', unsafe_allow_html=True)
    
    q3 = st.radio("escolha:", [
        "sustentabilidade inteligente que gera economia futura (solar, cisterna), mesmo exigindo maior investimento inicial",
        "reduzir o custo imediato da obra ao máximo, priorizando a estética antes da eficiência térmica e energética"
    ], key="q3", label_visibility="collapsed")
    
    if st.button("próximo", key="btn3"):
        st.session_state.answers['investimento'] = q3
        next_step()
        st.rerun()

# ── passo 4: medos reais ─────────────────────────────────────────────────────
elif st.session_state.step == 4:
    st.markdown('<div class="question-title" style="margin-top: 2rem;">4. qual é a sua maior preocupação ao pensar em construir?</div>', unsafe_allow_html=True)
    
    q4 = st.radio("escolha:", [
        "a obra virar um caos, com imprevisibilidade, retrabalhos e atrasos",
        "estourar o orçamento sem controle prévio ou aviso",
        "a casa ficar parecendo 'de catálogo', genérica e sem a nossa identidade"
    ], key="q4", label_visibility="collapsed")
    
    if st.button("próximo", key="btn4"):
        st.session_state.answers['medo'] = q4
        next_step()
        st.rerun()

# ── passo 5: captação do lead e envio seguro de e-mail ───────────────────────
elif st.session_state.step == 5:
    st.markdown("""
    <div style="text-align:center; color:#EAE8E3; font-family:'Montserrat',sans-serif; font-size:1.2rem; margin-bottom:1rem; text-transform:lowercase; font-weight:600;">
        sua essência foi mapeada.
    </div>
    <div style="text-align:center; color:#8C8881; font-family:'Inter',sans-serif; font-size:0.95rem; margin-bottom:2rem; text-transform:lowercase;">
        nossa inteligência está pronta para gerar o seu dossiê técnico e de viabilidade. para onde devemos enviar o seu resultado?
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        nome_bruto = st.text_input("como devemos chamar vocês?")
        email_bruto = st.text_input("qual o seu melhor e-mail?")
        whatsapp_bruto = st.text_input("whatsapp com ddd")
        
        # honeypot: campo oculto via css (robôs preenchem, humanos não veem)
        honeypot = st.text_input("campo de segurança", key="hp_campo", label_visibility="collapsed")
        
        if st.button("revelar minha casa ideal", key="btn5"):
            if nome_bruto and email_bruto and whatsapp_bruto:
                
                # 1. blindagem contra xss
                nome = html.escape(nome_bruto.strip())
                email = html.escape(email_bruto.strip())
                whatsapp = html.escape(whatsapp_bruto.strip())
                
                st.session_state.answers['lead'] = {'nome': nome, 'email': email, 'whatsapp': whatsapp}
                
                # envia o e-mail silenciosamente
                with st.spinner("cruzando dados sensoriais com arquitetura de alto desempenho..."):
                    
                    # 2. blindagem contra spam
                    if not honeypot: 
                        try:
                            msg = EmailMessage()
                            titulo_seguro = nome.replace('\n', '').replace('\r', '')
                            msg['Subject'] = f"✦ novo lead qualificado: {titulo_seguro}"
                            msg['From'] = st.secrets["email"]["sender"]
                            msg['To'] = st.secrets["email"]["receiver"]
                            
                            body = f"novo lead captado pela bússola selva\n\ndados de contato:\nnome: {nome}\ne-mail: {email}\nwhatsapp: {whatsapp}\n\nrespostas do diagnóstico:\n1. manhã ideal: {st.session_state.answers['manha']}\n2. conexão social: {st.session_state.answers['social']}\n3. investimento: {st.session_state.answers['investimento']}\n4. maior preocupação: {st.session_state.answers['medo']}"
                            
                            msg.set_content(body)
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                                server.login(st.secrets["email"]["sender"], st.secrets["email"]["password"])
                                server.send_message(msg)
                        except Exception as e:
                            print(f"erro no envio de email: {e}")
                    
                    time.sleep(2.5)
                    next_step()
                    st.rerun()
            else:
                st.warning("por favor, preencha todos os campos para continuarmos.")

# ── passo 6: dossiê final ────────────────────────────────────────────────────
elif st.session_state.step == 6:
    nome_casal = st.session_state.answers['lead']['nome']
        
    st.markdown(f"""
    <div style="text-align:center; color:#EAE8E3; font-family:'Montserrat',sans-serif; font-size:1.5rem; margin-bottom:2rem; text-transform:lowercase; font-weight:600;">
        olá, {nome_casal}. bem-vindos ao futuro de vocês.
    </div>
    """, unsafe_allow_html=True)
    
    if "jardim" in st.session_state.answers['manha']:
        atmosfera = "uma forte conexão com a natureza, utilizando design biofílico, jardins internos e luz natural abundante"
    else:
        atmosfera = "uma integração tecnológica total, com automação discreta e conforto invisível ditando o ritmo da rotina"

    if "cozinha" in st.session_state.answers['social']:
        coracao = "onde uma cozinha gourmet ampla e integrada será o coração pulsante da casa"
    else:
        coracao = "onde as áreas externas, com fogo de chão ou piscina natural, se tornam o refúgio perfeito para encontros"

    if "sustentabilidade" in st.session_state.answers['investimento']:
        sistema = "como vocês valorizam economia de longo prazo, recomendamos fortemente sistemas construtivos modernos e sustentáveis, como o wood frame ou steel frame. eles oferecem conforto térmico superior e facilitam a integração com painéis solares e cisternas, zerando suas preocupações futuras."
    else:
        sistema = "como o foco de vocês está no melhor balanço do custo imediato, nossa estratégia será focar em um projeto executivo extremamente detalhado. isso permite otimizar o uso de materiais construtivos e alcançar uma estética de alto padrão sem desperdícios na execução."

    if "caos" in st.session_state.answers['medo']:
        solucao_dor = "sabemos que a imprevisibilidade da obra tira o sono de vocês. para garantir um cronograma cravado e uma obra limpa, a industrialização da construção aliada ao nosso detalhamento rigoroso de projeto será a chave para blindar a saúde mental de vocês."
    elif "orçamento" in st.session_state.answers['medo']:
        solucao_dor = "notamos que estourar o orçamento é o maior receio de vocês. o antídoto para isso é a tecnologia que utilizamos em nosso escritório: nós construímos a sua casa virtualmente antes do primeiro tijolo, garantindo quantitativos exatos e blindando o seu bolso contra surpresas."
    else:
        solucao_dor = "percebemos que o pavor de vocês é acabar com uma 'casa de catálogo'. nosso compromisso será desenhar uma arquitetura com identidade profunda, fugindo de tendências genéricas e criando detalhes únicos que reflitam exclusivamente a história do casal."

    st.markdown(f"""
    <div class="dossier-box">
        <div class="dossier-title">✦ dossiê de viabilidade selva</div>
        <div class="dossier-text">
            analisamos o perfil de vocês e a visão está clara: o projeto ideal exige {atmosfera}, {coracao}.<br><br>
            {sistema}<br><br>
            além disso, {solucao_dor}<br><br>
            vocês não precisam de apenas uma planta. vocês precisam de um ecossistema completo e pensado para a vida de vocês.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align:center; color:#8C8881; font-family:'Inter',sans-serif; font-size:0.95rem; margin-bottom:1rem; text-transform:lowercase;">
        nossa equipe de arquitetura já recebeu o seu dossiê e entrará em contato pelo whatsapp muito em breve para darmos o próximo passo.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("refazer jornada"):
            reset_app()
            st.rerun()

# ── rodapé fixo (renderizado em todas as telas) ──────────────────────────────
st.markdown("""
<div class="footer-container">
    <div class="footer-col">
        <div>
            <div class="footer-title">contato</div>
            <div class="footer-text">selvaurbanaprojetos@gmail.com</div>
            <div class="footer-text">55 51 99251-4815</div>
            <div class="footer-text">55 51 98088-6131</div>
        </div>
        <div>
            <div class="footer-title">redes sociais</div>
            <div class="footer-socials">
                <a href="https://wa.me/5551992514815" target="_blank" title="whatsapp"><i class="fab fa-whatsapp"></i></a>
                <a href="https://br.pinterest.com/selvaurbana_/" target="_blank" title="pinterest"><i class="fab fa-pinterest"></i></a>
                <a href="https://instagram.com/selva.urb" target="_blank" title="instagram"><i class="fab fa-instagram"></i></a>
                <a href="https://facebook.com/selvaurbanaprojetos" target="_blank" title="facebook"><i class="fab fa-facebook"></i></a>
                <a href="https://linkedin.com/company/selvaurbanaprojetos" target="_blank" title="linkedin"><i class="fab fa-linkedin"></i></a>
            </div>
        </div>
    </div>
    <div class="footer-col footer-col-right">
        <div>
            <div class="footer-title">localização</div>
            <div class="footer-text">av. benjamin constant, 1194</div>
            <div class="footer-text">ed. diamond center, sala 702</div>
            <div class="footer-text">cep 95900-056, lajeado/rs</div>
        </div>
    </div>
</div>
<div class="footer-copy">© 2026 selva urbana ltda. todos os direitos reservados.</div>
""", unsafe_allow_html=True)
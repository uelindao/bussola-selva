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
.btn-cta:hover{background:#1A291E!important;color:#C49A6C!important;}
@media(max-width:768px){.footer-container{flex-direction:column;gap:2.5rem;}.footer-col-right{text-align:left;}.footer-col-right .footer-socials{justify-content:flex-start;}.footer-copy{text-align:center;}}
</style>
""", unsafe_allow_html=True)

# ── gerenciamento de estado (passos do wizard e score) ───────────────────────
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'score' not in st.session_state:
    st.session_state.score = {'classico': 0, 'minimalista': 0, 'industrial': 0}

def next_step():
    st.session_state.step += 1

def reset_app():
    st.session_state.step = 0
    st.session_state.answers = {}
    st.session_state.score = {'classico': 0, 'minimalista': 0, 'industrial': 0}

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
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("iniciar jornada"):
            next_step()
            st.rerun()

# ── passo 1: pergunta sobre fachada ──────────────────────────────────────────
elif st.session_state.step == 1:
    st.markdown('<div class="question-title" style="margin-top: 2rem;">1. ao andar pela rua e olhar para uma casa, o que te para?</div>', unsafe_allow_html=True)
    
    opcoes = {
        "um telhado de madeira aparente, formas equilibradas e tons neutros que convidam a entrar": "classico",
        "linhas horizontais puras, grandes vidros e brises que enquadram a paisagem lá de fora": "minimalista",
        "concreto bruto, esquadrias metálicas escuras e uma vegetação que parece querer engolir a construção": "industrial"
    }
    
    q1 = st.radio("escolha:", list(opcoes.keys()), key="q1", label_visibility="collapsed")
    
    if st.button("próximo", key="btn1"):
        st.session_state.answers['fachada'] = q1
        st.session_state.score[opcoes[q1]] += 1
        next_step()
        st.rerun()

# ── passo 2: pergunta sobre o coração da casa ────────────────────────────────
elif st.session_state.step == 2:
    st.markdown('<div class="question-title" style="margin-top: 2rem;">2. se você pudesse viver em apenas um ambiente da casa, qual seria?</div>', unsafe_allow_html=True)
    
    opcoes = {
        "uma sala de estar com luz natural suave, sofá de linho e madeira clara ao redor": "classico",
        "um living sem paredes, integrado à cozinha gourmet e ao deck com vista para a natureza": "minimalista",
        "um espaço com jardim de inverno interno, pedra natural e concreto aparente no teto": "industrial"
    }
    
    q2 = st.radio("escolha:", list(opcoes.keys()), key="q2", label_visibility="collapsed")
    
    if st.button("próximo", key="btn2"):
        st.session_state.answers['coracao'] = q2
        st.session_state.score[opcoes[q2]] += 1
        next_step()
        st.rerun()

# ── passo 3: pergunta sobre sensação ─────────────────────────────────────────
elif st.session_state.step == 3:
    st.markdown('<div class="question-title" style="margin-top: 2rem;">3. qual palavra define o que você quer sentir ao abrir a porta da sua casa?</div>', unsafe_allow_html=True)
    
    opcoes = {
        "serenidade — uma casa que acalma e acolhe ao mesmo tempo": "classico",
        "liberdade — espaços abertos, sem barreiras, integrados com o mundo lá fora": "minimalista",
        "força — uma casa com personalidade própria, que não se parece com nenhuma outra": "industrial"
    }
    
    q3 = st.radio("escolha:", list(opcoes.keys()), key="q3", label_visibility="collapsed")
    
    if st.button("próximo", key="btn3"):
        st.session_state.answers['sensacao'] = q3
        st.session_state.score[opcoes[q3]] += 1
        next_step()
        st.rerun()

# ── passo 4: pergunta sobre investimento ─────────────────────────────────────
elif st.session_state.step == 4:
    st.markdown('<div class="question-title" style="margin-top: 2rem;">4. ao pensar no investimento, o que faz mais sentido para vocês?</div>', unsafe_allow_html=True)
    
    opcoes = {
        "materiais de qualidade e acabamentos atemporais que valorizem o imóvel a cada ano": "classico",
        "autossuficiência: painéis solares, sistemas modernos e uma obra enxuta sem desperdício": "minimalista",
        "impacto visual e originalidade — mesmo que exija materiais especiais e soluções únicas": "industrial"
    }
    
    q4 = st.radio("escolha:", list(opcoes.keys()), key="q4", label_visibility="collapsed")
    
    if st.button("próximo", key="btn4"):
        st.session_state.answers['investimento'] = q4
        st.session_state.score[opcoes[q4]] += 1
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
                
                # blindagem contra xss
                nome = html.escape(nome_bruto.strip())
                email = html.escape(email_bruto.strip())
                whatsapp = html.escape(whatsapp_bruto.strip())
                
                st.session_state.answers['lead'] = {'nome': nome, 'email': email, 'whatsapp': whatsapp}
                
                # lógica de desempate: industrial > minimalista > clássico
                score = st.session_state.score
                vencedor = "classico"
                max_pts = score["classico"]
                
                if score["minimalista"] >= max_pts:
                    vencedor = "minimalista"
                    max_pts = score["minimalista"]
                    
                if score["industrial"] >= max_pts:
                    vencedor = "industrial"
                    max_pts = score["industrial"]
                
                st.session_state.answers['estilo'] = vencedor
                
                nomes_estilos = {
                    "classico": "clássico atemporal",
                    "minimalista": "minimalismo sustentável",
                    "industrial": "industrial biofílico"
                }
                nome_estilo_vencedor = nomes_estilos[vencedor]
                
                # envia o e-mail silenciosamente
                with st.spinner("cruzando dados sensoriais com arquitetura de alto desempenho..."):
                    
                    if not honeypot: 
                        try:
                            msg = EmailMessage()
                            titulo_seguro = nome.replace('\n', '').replace('\r', '')
                            msg['Subject'] = f"✦ novo lead qualificado: {titulo_seguro}"
                            msg['From'] = st.secrets["email"]["sender"]
                            msg['To'] = st.secrets["email"]["receiver"]
                            
                            body = f"""novo lead captado pela bússola selva

dados de contato:
nome: {nome}
e-mail: {email}
whatsapp: {whatsapp}

respostas do diagnóstico:
1. fachada: {st.session_state.answers['fachada']}
2. coração da casa: {st.session_state.answers['coracao']}
3. sensação: {st.session_state.answers['sensacao']}
4. investimento: {st.session_state.answers['investimento']}

estilo identificado: {nome_estilo_vencedor}
pontuação: clássico atemporal: {score['classico']} | minimalismo sustentável: {score['minimalista']} | industrial biofílico: {score['industrial']}"""
                            
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
    estilo_vencedor = st.session_state.answers['estilo']
    
    dados_projetos = {
        "classico": {
            "texto": "o perfil de vocês aponta para uma arquitetura de elegância atemporal. não é sobre tendência — é sobre permanência. nossa proposta será criar uma casa com volumetria equilibrada, telhado amadeirado, formas orgânicas e uma paleta neutra que aquece sem pesar. cada detalhe será pensado para que a luz natural percorra os ambientes de maneira suave, criando uma atmosfera de serenidade absoluta. o mobiliário seguirá linhas fluidas — linho, bouclé, madeira clara — em harmonia perfeita com o que existe do lado de fora. uma casa que envelhece com elegância, como vocês.",
            "img": "https://static.wixstatic.com/media/4067bd_09c81922336348faab4bcd1304079e96~mv2.png/v1/fill/w_1920,h_734,q_90,enc_avif,quality_auto/4067bd_09c81922336348faab4bcd1304079e96~mv2.png",
            "url": "https://www.selvaurbanaprojetos.com.br/projetos/casa-k%26a",
            "cta": "ver projeto: casa k&a",
            "legenda": "casa k&a — porto alegre, rs"
        },
        "minimalista": {
            "texto": "vocês pertencem à arquitetura que recusa o supérfluo. linhas horizontais puras, planta completamente livre e grandes panos de vidro que enquadram a paisagem como se ela fosse parte do projeto — porque ela é. nossa proposta será uma residência em steel frame, leve e autossuficiente: painéis fotovoltaicos integrados à cobertura, brises articulados que dominam a luminosidade, e um deck que dissolve a fronteira entre o dentro e o fora. o conforto aqui não é decorativo, é estrutural. uma casa que trabalha por vocês, silenciosamente.",
            "img": "https://static.wixstatic.com/media/4067bd_dcc4e7c998e04a768e0df45b6931560e~mv2.png/v1/fit/w_960,h_353,q_90,enc_avif,quality_auto/4067bd_dcc4e7c998e04a768e0df45b6931560e~mv2.png",
            "url": "https://www.selvaurbanaprojetos.com.br/projetos/casa-b%26j",
            "cta": "ver projeto: casa b&j",
            "legenda": "casa b&j — arroio do meio, rs"
        },
        "industrial": {
            "texto": "o perfil de vocês é o mais potente que existe: quem não tem medo de materiais brutos. concreto aparente, esquadrias metálicas pretas, painéis de madeira ripada — e então, quebrando tudo isso, uma vegetação que abraça a construção por dentro e por fora. nossa proposta será criar uma casa com presença e identidade própria, onde a rigidez dos materiais industriais é permanentemente subvertida pela vida que pulsa nos jardins verticais e aberturas estratégicas. uma casa que não imita nada. uma casa que só poderia ser de vocês.",
            "img": "https://static.wixstatic.com/media/4067bd_2cb29b55883746f0abfd36292493f016~mv2.webp/v1/fit/w_1920,h_702,q_90,enc_avif,quality_auto/4067bd_2cb29b55883746f0abfd36292493f016~mv2.webp",
            "url": "https://www.selvaurbanaprojetos.com.br/projetos/casa-d%26a",
            "cta": "ver projeto: casa d&a",
            "legenda": "casa d&a — arroio do meio, rs"
        }
    }
    
    projeto = dados_projetos[estilo_vencedor]

    st.markdown(f"""
    <div style="text-align:center; color:#EAE8E3; font-family:'Montserrat',sans-serif; font-size:1.5rem; margin-bottom:2rem; text-transform:lowercase; font-weight:600;">
        olá, {nome_casal}. bem-vindos ao futuro de vocês.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="dossier-box">
        <div class="dossier-title">✦ dossiê de viabilidade selva</div>
        <div class="dossier-text">
            {projeto['texto']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    st.image(projeto['img'], use_container_width=True)
    st.markdown(f"<div style='text-align:center; color:#8C8881; font-size:0.85rem; font-family:\"Inter\",sans-serif; text-transform:lowercase; margin-top:0.5rem;'>{projeto['legenda']}</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="text-align:center; margin-top:2.5rem; margin-bottom:2.5rem;">
        <a href="{projeto['url']}" class="btn-cta" target="_blank" style="
            display:inline-block;
            background:#2E4534;
            color:#EAE8E3;
            font-family:'Inter',sans-serif;
            font-size:1rem;
            font-weight:500;
            text-transform:lowercase;
            text-decoration:none;
            padding:0.8rem 2rem;
            border-radius:4px;
            transition:all 0.2s ease;
        ">{projeto['cta']} →</a>
    </div>
    """, unsafe_allow_html=True)
    
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
import json
import os
import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="Trilha da Roça - Gerenciador", page_icon="🤠", layout="wide"
)

# Estilização CSS personalizada (incluindo o layout compacto de avatares)
st.markdown(
    """
    <style>
    .main {
        background-color: #121817;
        color: #f4e8d1;
    }
    .status-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
        background: #DB8645;
        color: #fff;
    }
    .status-badge.no-jogo {
        background: #00ad9d;
        color: #121817;
    }
    .marco-selo {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(0, 173, 157, 0.15);
        border: 1px solid #00ad9d;
        color: #00ad9d;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
    }
    .link-btn {
        display: inline-block;
        margin-top: 6px;
        font-size: 11px;
        color: #00ad9d;
        text-decoration: none;
        border: 1px solid #00ad9d;
        padding: 2px 6px;
        border-radius: 4px;
    }
    .link-btn:hover {
        background: #00ad9d;
        color: #121817;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Arquivos JSON locais para persistência
ARQUIVO_DADOS = "dados_trilha.json"


def carregar_dados(arquivo, padrao):
  if os.path.exists(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
      return json.load(f)
  return padrao


def salvar_dados(arquivo, dados):
  with open(arquivo, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=4)


# Configurações padrão iniciais caso os arquivos não existam
status_padrao = ["No Jogo", "Eliminado", "Finalista", "Expulso", "Desistente"]
funcoes_padrao = [
    "Chapéu do Fazendeiro",
    "Trato dos Bichos",
    "Limpeza",
    "Horta",
    "Na Roça",
]
total_semanas_padrao = 14

# Inicializa estados
if "participantes" not in st.session_state:
  st.session_state["participantes"] = carregar_dados(ARQUIVO_DADOS, [])
if "config_status" not in st.session_state:
  st.session_state["config_status"] = carregar_dados(
      "config_status.json", status_padrao
  )
if "config_funcoes" not in st.session_state:
  st.session_state["config_funcoes"] = carregar_dados(
      "config_funcoes.json", funcoes_padrao
  )
if "config_total_semanas" not in st.session_state:
  cfg_geral = carregar_dados(
      "config_geral.json", {"total_semanas": total_semanas_padrao}
  )
  st.session_state["config_total_semanas"] = cfg_geral.get(
      "total_semanas", total_semanas_padrao
  )

# Controle de qual participante está selecionado para gerenciamento na aba de Elenco
if "peao_selecionado" not in st.session_state:
  st.session_state["peao_selecionado"] = None

# Título do App
st.title("🤠 Trilha da Roça - A Fazenda")
st.markdown("Painel de gerenciamento, configuração e linha do tempo dos peões.")

# --- PAINEL LATERAL (CONTROLES) ---
st.sidebar.header("⚙️ Painel de Controle")
aba = st.sidebar.radio(
    "Navegação",
    ["Visualizar Trilha", "👥 Gerenciar Elenco & Jornada", "⚙️ Configurações"],
)

# 1. ABA DE CONFIGURAÇÕES (ADMIN)
if aba == "⚙️ Configurações":
  st.subheader("⚙️ Configurações Gerais da Temporada")

  # --- CONFIGURAÇÃO DE TOTAL DE SEMANAS ---
  st.markdown("### 📅 Duração da Temporada")
  col_sem_1, col_sem_2 = st.columns([2, 1])
  with col_sem_1:
    novo_total_semanas = st.number_input(
        "Total de Semanas da Edição",
        min_value=1,
        max_value=30,
        value=int(st.session_state["config_total_semanas"]),
        step=1,
        help=(
            "Define o limite máximo de semanas exibidas nos seletores de"
            " marcos e na linha do tempo."
        ),
    )
  with col_sem_2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 Salvar Semanas"):
      st.session_state["config_total_semanas"] = int(novo_total_semanas)
      salvar_dados(
          "config_geral.json",
          {"total_semanas": st.session_state["config_total_semanas"]},
      )
      st.success("Duração atualizada com sucesso!")
      st.rerun()

  st.markdown("---")

  col_cfg1, col_cfg2 = st.columns(2)

  # --- GERENCIAR STATUS ---
  with col_cfg1:
    st.markdown("### 📊 Status Permitidos")
    novo_status = st.text_input("Novo Status", key="input_novo_status")
    if st.button("Adicionar Status"):
      if (
          novo_status
          and novo_status not in st.session_state["config_status"]
      ):
        st.session_state["config_status"].append(novo_status)
        salvar_dados("config_status.json", st.session_state["config_status"])
        st.success(f"Status '{novo_status}' adicionado!")
        st.rerun()

    st.markdown("---")
    st.write("Editar ou remover status existentes:")

    for i, s_atual in enumerate(st.session_state["config_status"]):
      c1, c2, c3 = st.columns([3, 1, 1])
      with c1:
        edit_status = st.text_input(
            f"Editar Status {i}",
            value=s_atual,
            key=f"edit_status_{i}",
            label_visibility="collapsed",
        )
      with c2:
        is_changed_status = edit_status.strip() != s_atual
        if st.button(
            "💾 Salvar",
            key=f"save_status_{i}",
            disabled=not is_changed_status,
        ):
          if edit_status:
            st.session_state["config_status"][i] = edit_status.strip()
            salvar_dados(
                "config_status.json", st.session_state["config_status"]
            )
            st.success("Atualizado!")
            st.rerun()
      with c3:
        if st.button("🗑️ Excluir", key=f"del_status_{i}"):
          if len(st.session_state["config_status"]) > 1:
            st.session_state["config_status"].pop(i)
            salvar_dados(
                "config_status.json", st.session_state["config_status"]
            )
            st.warning("Removido!")
            st.rerun()
          else:
            st.error("Mínimo de 1 status exigido.")

  # --- GERENCIAR FUNÇÕES / SELOS ---
  with col_cfg2:
    st.markdown("### 🏷️ Funções / Selos")
    nova_funcao = st.text_input("Nova Função", key="input_nova_funcao")
    if st.button("Adicionar Função"):
      if (
          nova_funcao
          and nova_funcao not in st.session_state["config_funcoes"]
      ):
        st.session_state["config_funcoes"].append(nova_funcao)
        salvar_dados("config_funcoes.json", st.session_state["config_funcoes"])
        st.success(f"Função '{nova_funcao}' adicionada!")
        st.rerun()

    st.markdown("---")
    st.write("Editar ou remover funções existentes:")

    for j, f_atual in enumerate(st.session_state["config_funcoes"]):
      cf1, cf2, cf3 = st.columns([3, 1, 1])
      with cf1:
        edit_funcao = st.text_input(
            f"Editar Função {j}",
            value=f_atual,
            key=f"edit_funcao_{j}",
            label_visibility="collapsed",
        )
      with cf2:
        is_changed_funcao = edit_funcao.strip() != f_atual
        if st.button(
            "💾 Salvar",
            key=f"save_funcao_{j}",
            disabled=not is_changed_funcao,
        ):
          if edit_funcao:
            st.session_state["config_funcoes"][j] = edit_funcao.strip()
            salvar_dados(
                "config_funcoes.json", st.session_state["config_funcoes"]
            )
            st.success("Atualizado!")
            st.rerun()
      with cf3:
        if st.button("🗑️ Excluir", key=f"del_funcao_{j}"):
          if len(st.session_state["config_funcoes"]) > 1:
            st.session_state["config_funcoes"].pop(j)
            salvar_dados(
                "config_funcoes.json", st.session_state["config_funcoes"]
            )
            st.warning("Removido!")
            st.rerun()
          else:
            st.error("Mínimo de 1 função exigida.")

# 2. ABA DE GERENCIAR ELENCO E INCLUSÃO DE JORNADA
elif aba == "👥 Gerenciar Elenco & Jornada":
  st.subheader("👥 Seleção de Participante para Gestão de Marcos")
  st.markdown(
      "Clique na foto redonda do participante abaixo para abrir o painel de"
      " lançamento da jornada."
  )

  # Formulário de Cadastro Rápido na Barra Lateral (envolve form para limpar os inputs nativamente)
  st.sidebar.subheader("➕ Novo Participante")
  with st.sidebar.form("form_elenco_novo", clear_on_submit=True):
    nome_peao = st.text_input("Nome do Participante")
    status_peao = st.selectbox(
        "Status Inicial", st.session_state["config_status"]
    )
    foto_peao = st.text_input(
        "URL da Foto", placeholder="https://exemplo.com/foto.jpg"
    )

    cadastrar_peao = st.form_submit_button("Cadastrar no Elenco")

    if cadastrar_peao:
      if nome_peao:
        lista = st.session_state["participantes"]
        existe = any(p["nome"].lower() == nome_peao.lower() for p in lista)

        if not existe:
          novo_p = {
              "nome": nome_peao,
              "status": status_peao,
              "foto": (
                  foto_peao
                  if foto_peao
                  else "https://via.placeholder.com/150"
              ),
              "semanas": {},
          }
          lista.append(novo_p)
          salvar_dados(ARQUIVO_DADOS, lista)
          st.sidebar.success(
              f"Participante '{nome_peao}' cadastrado com sucesso!"
          )
          st.rerun()
        else:
          st.sidebar.error("Já existe um participante com esse nome.")
      else:
        st.sidebar.warning("O nome do participante é obrigatório.")

  participantes = st.session_state["participantes"]

  if not participantes:
    st.info(
        "Nenhum participante cadastrado ainda. Use a barra lateral para"
        " adicionar."
    )
  else:
    # --- CONTROLE DE ORDENAÇÃO ---
    col_ord1, col_ord2, _ = st.columns([2, 3, 5])
    with col_ord1:
      criterio_ordenacao = st.selectbox(
          "Ordenar Elenco por:",
          ["Ordem de Cadastro", "Nome (A-Z)", "Status"],
          label_visibility="collapsed",
      )

    # Aplica ordenação temporária na exibição conforme escolha
    if criterio_ordenacao == "Nome (A-Z)":
      participantes_exibicao = sorted(participantes, key=lambda x: x["nome"].lower())
    elif criterio_ordenacao == "Status":
      participantes_exibicao = sorted(participantes, key=lambda x: x["status"])
    else:
      participantes_exibicao = participantes

    st.markdown("<br>", unsafe_allow_html=True)

    # Renderização em grade compacta de avatares
    num_cols = min(len(participantes_exibicao), 10)
    cols_elenco = st.columns(num_cols)

    for idx, p in enumerate(participantes_exibicao):
      with cols_elenco[idx % num_cols]:
        is_selecionado = (
            st.session_state["peao_selecionado"] == p["nome"]
        )
        borda_cor = "#DB8645" if is_selecionado else "#00ad9d"
        espessura = "4px" if is_selecionado else "2px"

        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 5px;" title="{p['nome']} ({p['status']})">
                <img src="{p.get('foto', '')}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover; border: {espessura} solid {borda_cor}; cursor: pointer;">
                <div style="font-size: 10px; color: {'#DB8645' if is_selecionado else '#ffffff'}; font-weight: bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 60px; margin: 0 auto;">{p['nome'].split()[0]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Selecionar" if not is_selecionado else "Ativo",
            key=f"btn_sel_{idx}",
            use_container_width=True,
        ):
          st.session_state["peao_selecionado"] = p["nome"]
          st.rerun()

    # --- SEÇÃO INSERIDA LOGO ABAIXO QUANDO UM PEÃO É SELECIONADO ---
    if st.session_state["peao_selecionado"]:
      peao_ativo = next(
          (
              p
              for p in participantes
              if p["nome"] == st.session_state["peao_selecionado"]
          ),
          None,
      )

      if peao_ativo:
        st.markdown("---")
        st.markdown(
            f"### ✏️ Gerenciando Jornada de: **{peao_ativo['nome']}**"
        )

        col_form, col_historico = st.columns([1, 1])

        with col_form:
          st.markdown("#### Adicionar Novo Marco / Status")
          # clear_on_submit=True garante que os campos de texto/url limpam após o clique em Salvar
          with st.form("form_marco_direto", clear_on_submit=True):
            atualizar_status = st.checkbox(
                "Atualizar status geral do peão?", value=False
            )
            novo_status_peao = st.selectbox(
                "Novo Status Geral", st.session_state["config_status"]
            )

            st.markdown("---")
            total_sem = int(st.session_state["config_total_semanas"])
            lista_semanas_opcoes = [
                f"Semana {i}" for i in range(1, total_sem + 1)
            ]

            semana_selecionada_str = st.selectbox(
                "Selecione a Semana", lista_semanas_opcoes
            )
            semana = int(semana_selecionada_str.replace("Semana ", ""))

            funcao = st.selectbox(
                "Função / Tarefa (Selo)", st.session_state["config_funcoes"]
            )
            descricao = st.text_area("Descrição do Acontecimento")
            url_link = st.text_input(
                "URL de Referência (Vídeo / Matéria)",
                placeholder="https://R7.com/...",
            )

            salvar_marco = st.form_submit_button("Salvar Marco na Semana")

            if salvar_marco:
              if atualizar_status:
                peao_ativo["status"] = novo_status_peao

              if "semanas" not in peao_ativo:
                peao_ativo["semanas"] = {}

              s_str = str(semana)
              if s_str not in peao_ativo["semanas"]:
                peao_ativo["semanas"][s_str] = []

              peao_ativo["semanas"][s_str].append([funcao, descricao, url_link])

              salvar_dados(ARQUIVO_DADOS, participantes)
              st.success(
                  f"Marco adicionado à Semana {semana} para"
                  f" {peao_ativo['nome']}!"
              )
              st.rerun()

        with col_historico:
          st.markdown("#### Histórico Cadastrado")
          semanas = peao_ativo.get("semanas", {})
          if semanas:
            for s_num, lista_marcos in sorted(
                semanas.items(), key=lambda x: int(x[0])
            ):
              st.markdown(f"**Semana {s_num}**")
              for m_idx, m_dados in enumerate(lista_marcos):
                f_nome = m_dados[0]
                desc = m_dados[1]
                link = m_dados[2] if len(m_dados) > 2 else ""

                st.markdown(
                    f"""
                    <div style="background: #1a2322; border: 1px solid #283735; padding: 8px; border-radius: 6px; margin-bottom: 6px; font-size: 12px;">
                        <span style="color: #00ad9d; font-weight: bold;">[{f_nome}]</span> {desc}
                        {f'<br><a href="{link}" target="_blank" style="color: #DB8645; font-size: 11px;">🔗 Link externo</a>' if link else ''}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
          else:
            st.info("Nenhum marco cadastrado para este participante ainda.")

# 3. ABA DE VISUALIZAÇÃO
else:
  st.subheader("📋 Linha do Tempo Ativa")

  participantes = st.session_state["participantes"]

  if not participantes:
    st.info(
        "Nenhum participante cadastrado ainda. Use a aba de gerenciamento para"
        " começar."
    )


  def get_icone(texto_funcao):
    t = texto_funcao.lower()
    if "fazendeiro" in t or "chapéu" in t:
      return "🤠"
    elif any(
        x in t
        for x in [
            "bichos",
            "animal",
            "vaca",
            "cavalo",
            "ave",
            "porco",
            "trato",
        ]
    ):
      return "🐄"
    elif "limpeza" in t or "limpar" in t or "lixo" in t:
      return "🧹"
    elif "horta" in t or "planta" in t or "cultivo" in t:
      return "🌱"
    elif "roça" in t or "indicação" in t or "votação" in t:
      return "🔥"
    elif "festa" in t or "vip" in t:
      return "🎉"
    return "⭐"


  for p in participantes:
    status_texto = p.get("status", "No Jogo")
    is_no_jogo = any(
        s in status_texto.lower() for s in ["no jogo", "campeão", "finalista"]
    )
    badge_class = "status-badge no-jogo" if is_no_jogo else "status-badge"

    st.markdown(
        f"""
      <div style="background: #1a2322; border: 2px solid #283735; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
          <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px; border-bottom: 2px dashed #283735; padding-bottom: 12px;">
              <img src="{p.get('foto', '')}" style="width: 70px; height: 70px; border-radius: 50%; object-fit: cover; border: 3px solid #00ad9d;">
              <div>
                  <h3 style="margin: 0 0 5px 0; color: #ffffff;">{p['nome']}</h3>
                  <span class="{badge_class}">{status_texto}</span>
              </div>
          </div>
      </div>
      """,
        unsafe_allow_html=True,
    )

    semanas = p.get("semanas", {})
    if semanas:
      cols = st.columns(min(len(semanas), 4))
      idx = 0
      for semana_num, lista_marcos in sorted(
          semanas.items(), key=lambda x: int(x[0])
      ):
        with cols[idx % len(cols)]:
          st.markdown(
              f"""
              <div style="background: #212e2c; border: 1px solid #283735; padding: 10px; border-radius: 6px; margin-bottom: 10px;">
                  <div style="font-size: 10px; font-weight: bold; color: #DB8645; text-transform: uppercase; margin-bottom: 6px;">Semana {semana_num}</div>
              """,
              unsafe_allow_html=True,
          )

          for dados_semana in lista_marcos:
            func_nome = dados_semana[0]
            desc = dados_semana[1]
            url_link = dados_semana[2] if len(dados_semana) > 2 else ""
            icone = get_icone(func_nome)

            link_html = (
                f'<a href="{url_link}" target="_blank" class="link-btn">🔗 Ver'
                " Detalhes</a>"
                if url_link
                else ""
            )

            st.markdown(
                f"""
                <div style="margin-bottom: 8px; border-bottom: 1px dotted rgba(255,255,255,0.1); padding-bottom: 6px;">
                    <span class="marco-selo">{icone} {func_nome}</span>
                    <div style="font-size: 12px; color: #d1c2a5; margin-top: 4px;">{desc}</div>
                    {link_html}
                </div>
                """,
                unsafe_allow_html=True,
            )

          st.markdown("</div>", unsafe_allow_html=True)
        idx += 1
    else:
      st.markdown(
          "<p style='color: #bfa888; font-size: 12px;'>Nenhum marco cadastrado"
          " para este participante.</p>",
          unsafe_allow_html=True,
      )

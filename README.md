# 🧹 Google Workspace User Cleanup & Auditor

Uma ferramenta Python simples e ágil para administradores do Google Workspace que precisam sincronizar a base de usuários do Google com a lista de funcionários ativos (RH) sem a necessidade de ferramentas complexas (como GAM ou APIs avançadas).

**O problema:** Comparar planilhas manualmente para saber quem saiu da empresa e ainda tem acesso ao e-mail é trabalhoso e propenso a erros.
**A solução:** Este script automatiza o cruzamento de dados, ignora erros de digitação comuns e gera um arquivo pronto para atualização em massa no Google Admin.

## 🚀 Principais Vantagens

* **Sem Dependência de GAM/API:** Funciona puramente com manipulação de CSVs, ideal para auditorias rápidas.
* **Smart Matching (Nome + Sobrenome):** Utiliza uma lógica de normalização que compara apenas o Primeiro e o Último nome. Isso resolve problemas onde o RH cadastra "João Silva" e o e-mail é "João da Silva".
* **Preparado para o Google Admin:** O arquivo de saída já vem formatado com a coluna `New Status` = `Suspended`, pronto para upload na ferramenta de atualização em massa do Google.
* **Resiliente:** Lida automaticamente com diferentes codificações de arquivo (UTF-8 ou Latin1) e remove acentos/espaços extras.

## 🛠️ Pré-requisitos

* Python 3.x instalado.
* Biblioteca `pandas`.

``bash
`pip install pandas`  

## ⚙️ Configuração Rápida
Antes de rodar, abra o script .py e faça dois pequenos ajustes para o seu cenário:

* **Defina seu Domínio:** Procure a linha que contém @emece.com.br e altere para o domínio da sua empresa (ex: @suaempresa.com.br).

* **Verifique a Coluna de Nomes:** O script assume que o Nome Completo na sua lista de ativos (RH) está na segunda coluna (índice 1). Se estiver em outra, ajuste a variável col_nome_ativos.

## 📂 Como Usar
* **1. Obtenha os Arquivos**
* **Coloque os dois arquivos abaixo na mesma pasta do script:**

* **users_google.csv:** Exporte a lista de usuários diretamente do Google Admin Console (Usuários > Fazer o download dos usuários).

* **lista_ativos.csv:** A planilha atualizada do seu RH/DP contendo quem está ativo na empresa.

* **2. Execute o Script*
``Bash
  `python audit_users.py`

* **3. Analise o Resultado**
O script gerará o arquivo `usuarios_para_suspender_smart_match.csv`.

* **Este arquivo contém:**

Os e-mails que estão no Google mas não foram encontrados na lista de ativos.

A data do último login (a logica está adiocionada no condigo, porém o google ainda não fornece essa informação via CSV).

A "Chave de Conferência" usada (para você entender por que o script sugeriu a suspensão).

* **4. Atualização em Massa**
Após validar visualmente o CSV gerado:

Vá ao Google Admin Console.

Acesse Usuários > Atualizar usuários em massa.

Faça o upload do arquivo gerado pelo script para suspender as contas automaticamente.

## 🧠 Lógica de Comparação ("Por que é seguro?")
O script não faz uma comparação exata de strings (que falha facilmente). Ele:

Remove acentos e coloca tudo em minúsculo.

Extrai apenas o Primeiro e o Último nome de ambas as listas.

Compara as chaves resultantes.

Exemplo: Se no Google está Ana de Souza Maria e no RH está Ana Maria, o script entende que são a mesma pessoa (Chave: ana maria) e não sugere a suspensão.

## ⚠️ Isenção de Responsabilidade
* **Sempre revise o arquivo de saída usuarios_para_suspender_smart_match.csv antes de fazer o upload no Google. Nomes homônimos ou apelidos muito diferentes podem exigir verificação manual.**

## ☕ Contribuição
* **Sinta-se à vontade para sugerir melhorias ou adaptar o código para a realidade da sua organização!**

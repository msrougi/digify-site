# -*- coding: utf-8 -*-
"""
Digify — portfólio.

IMPORTANTE: o campo "escopo" descreve o que foi construído — isso eu sei dos
projetos. O campo "resultado" está VAZIO de propósito: número de cliente é
afirmação séria e eu não invento. Preencha com o que você puder comprovar, ou
deixe vazio (o card omite o bloco sozinho).

IMAGEM: coloque a captura em assets/cases/<slug>.jpg (1600x1000 aprox.).
Se o arquivo não existir, o card usa um bloco tipográfico. Nada quebra.
No Firefox: botão direito na página → "Fazer captura de tela" → "Salvar página inteira".
"""

CASES = [
{
 "slug": "serlaw", "c": "ultra", "featured": True,
 "name": "SERLaw", "client": "Srougé & Reis Advogados",
 "sector": "Advocacia", "year": "2026",
 "url": "https://www.serlaw.com.br",
 "tagline": "Um site que precisa transmitir confiança antes da primeira palavra.",
 "problem": "Escritório de advocacia vende credibilidade. O site precisava parecer sólido em três segundos, carregar rápido e ser encontrado por quem procura advogado societário, tributário ou cível em São Paulo.",
 "escopo": [
   "Site institucional estático, sem WordPress, para performance e segurança máximas",
   "Identidade em navy e dourado, com Cormorant Garamond e Jost",
   "Ilustração vetorial autoral em SVG, sem banco de imagem",
   "Schema.org, Open Graph e estrutura de títulos para busca local",
   "Formulário de contato sem servidor, via FormSubmit",
 ],
 "stack": ["HTML", "CSS", "SVG", "Schema.org", "FormSubmit"],
},
{
 "slug": "voe-vento-norte", "c": "jade", "featured": True,
 "name": "Vento Norte Paraglider", "client": "Escola de parapente · Curitiba",
 "sector": "Esporte e turismo", "year": "2026",
 "url": "https://voeventonorte.com.br",
 "tagline": "Loja virtual para um esporte que se vende pela emoção.",
 "problem": "Vender voo duplo e equipamento exige duas coisas ao mesmo tempo: imagem que emociona e checkout que não atrapalha. E precisava ser achado por quem busca parapente em Curitiba, um termo local e disputado.",
 "escopo": [
   "Loja WooCommerce completa, com catálogo de voos e equipamentos",
   "Tema Astra com Elementor, customizado para a identidade da escola",
   "Página de arquivo replicando o hero da home para consistência visual",
   "Seleção e configuração dos widgets de exibição de produto",
   "Meios de pagamento e regras de frete configurados",
 ],
 "stack": ["WordPress", "WooCommerce", "Elementor", "Astra"],
},
{
 "slug": "sindico-fmf", "c": "flame", "featured": True,
 "name": "Síndico FMF", "client": "Fernando Marrey Ferreira",
 "sector": "Gestão condominial e advocacia", "year": "2025",
 "url": "https://sindicofmf.com.br",
 "tagline": "Síndico profissional que também é advogado — dois públicos, um site.",
 "problem": "O desafio era comunicar duas competências sem confundir: gestão condominial para o condomínio e formação jurídica como diferencial, sem parecer escritório de advocacia.",
 "escopo": [
   "Site institucional em WordPress com Elementor",
   "Grade de certificações destacando a formação e os registros profissionais",
   "Página de contato com caminho direto para orçamento",
   "CSS customizado e correções de responsividade em todos os breakpoints",
 ],
 "stack": ["WordPress", "Elementor", "CSS"],
},
{
 "slug": "reforma-expressa", "c": "violet", "featured": False,
 "name": "Reforma Expressa", "client": "Eng. Ana Paula Liebscher",
 "sector": "Engenharia e reformas", "year": "2025",
 "url": "https://reformaexpressa.com",
 "tagline": "Engenharia de reformas com orçamento claro desde a primeira visita.",
 "problem": "O setor de reformas sofre de desconfiança crônica. O site precisava passar previsibilidade — prazo, escopo e processo visíveis antes do contato.",
 "escopo": [
   "Site multipágina em WordPress com Elementor e Pro Elements",
   "Instalador em pacote único, para deploy replicável",
   "Estrutura de serviços com caminho direto ao orçamento",
   "Hospedagem e configuração na Hostinger",
 ],
 "stack": ["WordPress", "Elementor", "Hostinger"],
},
{
 "slug": "digify-scraper", "c": "cyan", "featured": False,
 "name": "Digify Scraper", "client": "Produto próprio",
 "sector": "Ferramenta web", "year": "2025",
 "url": "https://imagescraper.digify.live",
 "tagline": "Ferramenta interna que virou produto público.",
 "problem": "Baixar imagens em lote de uma página inteira era tarefa manual e repetitiva na produção dos sites. Virou aplicação — e depois virou ativo de SEO por atrair busca própria.",
 "escopo": [
   "Aplicação em Flask e Python para download de imagens em lote",
   "Sistema de jobs com polling, para não travar em página grande",
   "Landing indexável com FAQ e dados estruturados, atacando busca própria",
   "Espaços de anúncio integrados, transformando a ferramenta em ativo",
   "Deploy e monitoramento no Render",
 ],
 "stack": ["Python", "Flask", "Render"],
},
{
 "slug": "plugins-digify", "c": "pink", "featured": False,
 "name": "Digify Plugins", "client": "Produto próprio",
 "sector": "Software para WordPress", "year": "2026",
 "url": "https://plugins.digify.live",
 "tagline": "Plugins WordPress comerciais, com licenciamento próprio.",
 "problem": "Resolver internamente problemas que apareciam em todo projeto de cliente, e transformar a solução em produto com atualização e suporte próprios.",
 "escopo": [
   "Catálogo de plugins com documentação e suporte",
   "Sistema de licenciamento offline com assinatura Ed25519",
   "Servidor de atualização automática hospedado na Netlify",
   "Gerador de licenças com criptografia AES-256-GCM",
 ],
 "stack": ["PHP", "WordPress", "Ed25519", "Netlify"],
},
]

PORTFOLIO = {
 "slug": "portfolio/",
 "title": "Portfólio | Sites, Lojas e Sistemas Entregues | Digify",
 "desc": "Projetos entregues pela Digify: sites institucionais, lojas virtuais, sistemas e ferramentas. Escopo, tecnologia e o que foi resolvido em cada um.",
 "eyebrow": "Portfólio",
 "h1": "Os últimos projetos que saíram daqui.",
 "lede": "Mais de 300 projetos em 10 anos. Estes seis são os mais recentes e mostram bem a variedade — de site institucional que precisa transmitir confiança a ferramenta em Python que virou produto.",
}

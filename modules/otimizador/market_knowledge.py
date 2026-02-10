"""
Base de Conhecimento de Mercado - Headhunter Elite

Contém mapeamento de 22+ áreas profissionais com:
- Keywords essenciais (10-15 por área)
- Métricas/KPIs específicos (5-8 por área)
- Verbos fortes recomendados (5-8 por área)
- Ferramentas/tecnologias comuns
"""

# Base de conhecimento com 22+ áreas profissionais
MARKET_KNOWLEDGE = {
    'Software Engineer': {
        'keywords': [
            'desenvolvimento', 'código', 'API', 'backend', 'frontend', 
            'arquitetura', 'refatoração', 'debugging', 'deploy', 'CI/CD',
            'microserviços', 'cloud', 'testes automatizados', 'code review', 'git'
        ],
        'metrics': [
            'tempo de resposta da API', 'cobertura de testes (%)', 
            'bugs resolvidos', 'deploys por semana', 'linhas de código refatoradas',
            'tempo de build reduzido', 'uptime (%)', 'performance (ms)'
        ],
        'verbos_fortes': [
            'Desenvolvi', 'Implementei', 'Arquitetei', 'Otimizei', 'Refatorei',
            'Automatizei', 'Escalei', 'Integrei'
        ],
        'ferramentas': [
            'Python', 'Java', 'JavaScript', 'TypeScript', 'Node.js', 'React',
            'Docker', 'Kubernetes', 'AWS', 'Git', 'Jenkins', 'PostgreSQL'
        ]
    },
    
    'Data Scientist': {
        'keywords': [
            'machine learning', 'análise de dados', 'modelagem preditiva', 
            'estatística', 'big data', 'ETL', 'visualização de dados',
            'algoritmos', 'feature engineering', 'pipeline de dados', 'deep learning',
            'processamento de dados', 'data mining', 'regressão', 'classificação'
        ],
        'metrics': [
            'acurácia do modelo (%)', 'F1-score', 'ROC-AUC', 'RMSE',
            'dados processados (GB/TB)', 'tempo de treinamento reduzido',
            'modelos em produção', 'datasets analisados'
        ],
        'verbos_fortes': [
            'Modelei', 'Analisei', 'Treinei', 'Implementei', 'Otimizei',
            'Visualizei', 'Previ', 'Extraí'
        ],
        'ferramentas': [
            'Python', 'R', 'SQL', 'Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow',
            'PyTorch', 'Jupyter', 'Tableau', 'Power BI', 'Spark', 'Hadoop'
        ]
    },
    
    'Product Manager': {
        'keywords': [
            'roadmap', 'backlog', 'discovery', 'user story', 'MVP', 'product vision',
            'stakeholders', 'priorização', 'OKRs', 'métricas de produto', 'go-to-market',
            'feature launch', 'user research', 'A/B testing', 'product strategy'
        ],
        'metrics': [
            'NPS', 'CSAT', 'retenção (%)', 'churn (%)', 'MAU/DAU', 'time-to-market',
            'features lançadas', 'adoption rate (%)', 'revenue impactado (R$/US$)'
        ],
        'verbos_fortes': [
            'Priorizei', 'Defini', 'Lancei', 'Coordenei', 'Conduzi',
            'Validei', 'Estruturei', 'Alavancei'
        ],
        'ferramentas': [
            'Jira', 'Confluence', 'Miro', 'Figma', 'Amplitude', 'Mixpanel',
            'Google Analytics', 'ProductBoard', 'Notion', 'Slack'
        ]
    },
    
    'Sales Manager': {
        'keywords': [
            'pipeline', 'forecast', 'quota', 'fechamento', 'prospecção', 'cold call',
            'discovery call', 'negociação', 'gestão de contas', 'upsell', 'cross-sell',
            'ciclo de vendas', 'território', 'inside sales', 'field sales'
        ],
        'metrics': [
            'faturamento (R$/US$)', 'quota atingida (%)', 'pipeline gerado (R$/US$)',
            'taxa de conversão (%)', 'ticket médio (R$/US$)', 'deals fechados',
            'ciclo de vendas (dias)', 'CAC', 'LTV'
        ],
        'verbos_fortes': [
            'Fechei', 'Negociei', 'Prospectei', 'Gerei', 'Expandi',
            'Conquistei', 'Atingi', 'Superei'
        ],
        'ferramentas': [
            'Salesforce', 'HubSpot', 'Pipedrive', 'Outreach', 'Salesloft',
            'ZoomInfo', 'Apollo', 'LinkedIn Sales Navigator', 'Gong', 'Excel'
        ]
    },
    
    'Marketing Manager': {
        'keywords': [
            'branding', 'campanha', 'leads', 'funil', 'SEO', 'SEM', 'content marketing',
            'inbound', 'outbound', 'automação', 'mídia paga', 'redes sociais',
            'brand awareness', 'persona', 'jornada do cliente'
        ],
        'metrics': [
            'MQL gerados', 'SQL convertidos', 'CAC', 'ROAS', 'CTR (%)', 'CPC',
            'leads qualificados', 'taxa de conversão (%)', 'ROI de campanha (%)',
            'impressões', 'engajamento (%)'
        ],
        'verbos_fortes': [
            'Gerei', 'Planejei', 'Executei', 'Otimizei', 'Aumentei',
            'Converti', 'Posicionei', 'Lancei'
        ],
        'ferramentas': [
            'Google Ads', 'Facebook Ads', 'HubSpot', 'RD Station', 'SEMrush',
            'Google Analytics', 'Mailchimp', 'Hootsuite', 'Canva', 'WordPress'
        ]
    },
    
    'HR Manager': {
        'keywords': [
            'recrutamento', 'seleção', 'onboarding', 'offboarding', 'cultura organizacional',
            'employer branding', 'desenvolvimento de pessoas', 'avaliação de desempenho',
            'plano de carreira', 'treinamento', 'engajamento', 'retenção', 'DHO'
        ],
        'metrics': [
            'time-to-hire (dias)', 'custo por contratação (R$)', 'taxa de retenção (%)',
            'turnover (%)', 'eNPS', 'vagas preenchidas', 'taxa de aprovação no período de experiência (%)',
            'ROI de treinamento'
        ],
        'verbos_fortes': [
            'Recrutei', 'Estruturei', 'Implementei', 'Conduzi', 'Desenvolvi',
            'Retive', 'Capacitei', 'Integrei'
        ],
        'ferramentas': [
            'Gupy', 'Kenoby', 'LinkedIn Recruiter', 'Workday', 'SAP SuccessFactors',
            'ADP', 'BambooHR', 'Culture Amp', 'Survey Monkey', 'Excel'
        ]
    },
    
    'Financial Analyst': {
        'keywords': [
            'análise financeira', 'budget', 'forecast', 'P&L', 'DRE', 'fluxo de caixa',
            'valuation', 'FP&A', 'CAPEX', 'OPEX', 'EBITDA', 'margem', 'ROI',
            'controladoria', 'conciliação bancária'
        ],
        'metrics': [
            'budget gerenciado (R$/US$)', 'forecast accuracy (%)', 'margem EBITDA (%)',
            'variance (R$/%)', 'saving (R$/US$)', 'ROI (%)', 'DFC projetado',
            'redução de custos (R$/%)'
        ],
        'verbos_fortes': [
            'Analisei', 'Projetei', 'Otimizei', 'Reduzi', 'Consolidei',
            'Modelei', 'Auditorei', 'Avaliei'
        ],
        'ferramentas': [
            'Excel', 'SAP', 'Oracle', 'Power BI', 'Tableau', 'Totvs',
            'Bloomberg', 'Capital IQ', 'Python', 'SQL'
        ]
    },
    
    'Supply Chain Manager': {
        'keywords': [
            'logística', 'inventário', 'S&OP', 'procurement', 'fornecedores', 'lead time',
            'estoque', 'distribuição', 'armazenagem', 'transporte', 'WMS', 'TMS',
            'demanda', 'planejamento de produção', 'cadeia de suprimentos'
        ],
        'metrics': [
            'redução de lead time (%/dias)', 'giro de estoque', 'fill rate (%)',
            'OTIF (%)', 'custo logístico reduzido (R$/%)', 'acuracidade de inventário (%)',
            'saving de procurement (R$/US$)', 'SKUs gerenciados'
        ],
        'verbos_fortes': [
            'Otimizei', 'Negociei', 'Reduzi', 'Gerenciei', 'Estruturei',
            'Implementei', 'Coordenei', 'Consolidei'
        ],
        'ferramentas': [
            'SAP', 'Oracle', 'WMS', 'TMS', 'Excel', 'Power BI', 'Tableau',
            'Blue Yonder', 'Manhattan', 'Kinaxis'
        ]
    },
    
    'Legal Operations': {
        'keywords': [
            'contratos', 'compliance', 'gestão de risco', 'due diligence', 'contencioso',
            'LGPD', 'GDPR', 'governança corporativa', 'litigation', 'regulatory',
            'auditoria jurídica', 'M&A', 'propriedade intelectual', 'legal tech'
        ],
        'metrics': [
            'contratos revisados', 'tempo médio de análise (dias)', 'saving legal (R$/US$)',
            'litígios reduzidos (%)', 'compliance score (%)', 'SLA de resposta (horas)',
            'processos automatizados', 'risco mitigado (R$)'
        ],
        'verbos_fortes': [
            'Negociei', 'Estruturei', 'Revisei', 'Implementei', 'Mitigando',
            'Assessorei', 'Conduzi', 'Validei'
        ],
        'ferramentas': [
            'DocuSign', 'Contract Logix', 'Ironclad', 'LegalZoom', 'Clio',
            'NetDocuments', 'Excel', 'PowerPoint', 'Salesforce'
        ]
    },
    
    'DevOps Engineer': {
        'keywords': [
            'CI/CD', 'infraestrutura como código', 'automação', 'containers', 'orquestração',
            'monitoramento', 'observability', 'deploy', 'pipeline', 'cloud', 'SRE',
            'kubernetes', 'terraform', 'ansible', 'GitOps'
        ],
        'metrics': [
            'deploy frequency (por dia/semana)', 'lead time (horas)', 'MTTR (minutos)',
            'uptime (%)', 'disponibilidade (%)', 'tempo de build reduzido (%)',
            'incidentes reduzidos (%)', 'infraestrutura provisionada (nodes/VMs)'
        ],
        'verbos_fortes': [
            'Automatizei', 'Implementei', 'Otimizei', 'Monitorei', 'Escalei',
            'Configurei', 'Migrei', 'Provisionei'
        ],
        'ferramentas': [
            'Kubernetes', 'Docker', 'Terraform', 'Ansible', 'Jenkins', 'GitLab CI',
            'AWS', 'Azure', 'GCP', 'Prometheus', 'Grafana', 'ELK Stack', 'Datadog'
        ]
    },
    
    'UX Designer': {
        'keywords': [
            'design system', 'wireframe', 'protótipo', 'user research', 'usabilidade',
            'teste de usabilidade', 'jornada do usuário', 'persona', 'interface',
            'design thinking', 'UI/UX', 'acessibilidade', 'design responsivo', 'sketch'
        ],
        'metrics': [
            'SUS score', 'task success rate (%)', 'time on task (segundos)',
            'error rate (%)', 'NPS', 'telas desenhadas', 'protótipos validados',
            'usuários testados', 'adoption rate (%)'
        ],
        'verbos_fortes': [
            'Desenhei', 'Prototipei', 'Conduzi', 'Testei', 'Validei',
            'Implementei', 'Estruturei', 'Refinei'
        ],
        'ferramentas': [
            'Figma', 'Sketch', 'Adobe XD', 'InVision', 'Miro', 'Maze',
            'UserTesting', 'Hotjar', 'Optimal Workshop', 'Zeplin'
        ]
    },
    
    'Project Manager': {
        'keywords': [
            'cronograma', 'escopo', 'stakeholders', 'risco', 'orçamento', 'Agile',
            'Scrum', 'Kanban', 'PMI', 'roadmap', 'sprint', 'milestone', 'deliverable',
            'resource allocation', 'gestão de mudanças'
        ],
        'metrics': [
            'projetos entregues', 'on-time delivery (%)', 'budget adherence (%)',
            'stakeholders gerenciados', 'economia de budget (R$/US$)', 'time-to-market (dias)',
            'risco mitigado', 'SLA cumprido (%)'
        ],
        'verbos_fortes': [
            'Coordenei', 'Planejei', 'Entreguei', 'Gerenciei', 'Mitigando',
            'Implementei', 'Conduzi', 'Otimizei'
        ],
        'ferramentas': [
            'Jira', 'Asana', 'MS Project', 'Monday.com', 'Trello', 'Confluence',
            'Smartsheet', 'Wrike', 'Excel', 'PowerPoint'
        ]
    },
    
    'Customer Success Manager': {
        'keywords': [
            'retenção', 'churn', 'onboarding', 'adoção', 'upsell', 'cross-sell',
            'health score', 'QBR', 'advocacy', 'NPS', 'renewal', 'expansion',
            'customer journey', 'playbook', 'customer lifecycle'
        ],
        'metrics': [
            'NRR (%)', 'GRR (%)', 'churn reduzido (%)', 'NPS', 'CSAT',
            'upsell (R$/US$)', 'expansion revenue (R$/US$)', 'onboarding time (dias)',
            'adoption rate (%)', 'contas gerenciadas'
        ],
        'verbos_fortes': [
            'Retive', 'Expandi', 'Implementei', 'Reduzi', 'Atingi',
            'Conduzi', 'Estruturei', 'Cultivei'
        ],
        'ferramentas': [
            'Salesforce', 'Gainsight', 'ChurnZero', 'Totango', 'Zendesk',
            'Intercom', 'HubSpot', 'Tableau', 'Excel', 'Looker'
        ]
    },
    
    'Business Analyst': {
        'keywords': [
            'requisitos', 'análise de processos', 'mapeamento', 'documentação', 'user story',
            'gap analysis', 'stakeholders', 'dados', 'SQL', 'business intelligence',
            'KPI', 'dashboard', 'modelagem', 'improvement', 'UAT'
        ],
        'metrics': [
            'processos mapeados', 'requisitos levantados', 'projetos analisados',
            'economia (R$/US$)', 'eficiência aumentada (%)', 'tempo de processo reduzido (%)',
            'relatórios criados', 'stakeholders atendidos'
        ],
        'verbos_fortes': [
            'Analisei', 'Mapeie', 'Documentei', 'Levantei', 'Implementei',
            'Otimizei', 'Estruturei', 'Validei'
        ],
        'ferramentas': [
            'SQL', 'Excel', 'Power BI', 'Tableau', 'Jira', 'Confluence',
            'Visio', 'Lucidchart', 'Bizagi', 'Python'
        ]
    },
    
    'Operations Manager': {
        'keywords': [
            'processos', 'eficiência operacional', 'KPI', 'SLA', 'continuous improvement',
            'lean', 'Six Sigma', 'otimização', 'gestão de equipe', 'escalabilidade',
            'automação', 'produtividade', 'qualidade', 'padronização', 'workflow'
        ],
        'metrics': [
            'eficiência aumentada (%)', 'custo operacional reduzido (R$/%)',
            'SLA cumprido (%)', 'produtividade aumentada (%)', 'tempo de processo reduzido (%)',
            'economia (R$/US$)', 'throughput', 'erro reduzido (%)'
        ],
        'verbos_fortes': [
            'Otimizei', 'Implementei', 'Reduzi', 'Aumentei', 'Estruturei',
            'Automatizei', 'Escalei', 'Gerenciei'
        ],
        'ferramentas': [
            'Excel', 'Power BI', 'Tableau', 'SAP', 'Oracle', 'Jira',
            'Asana', 'Monday.com', 'SQL', 'Python'
        ]
    },
    
    'Content Manager': {
        'keywords': [
            'conteúdo', 'editorial', 'SEO', 'copywriting', 'blog', 'e-book', 'social media',
            'calendário editorial', 'engajamento', 'branded content', 'storytelling',
            'content strategy', 'content marketing', 'produção de conteúdo', 'curadoria'
        ],
        'metrics': [
            'conteúdos publicados', 'pageviews', 'engajamento (%)', 'leads gerados',
            'CTR (%)', 'tempo médio na página (min)', 'conversão (%)', 'SEO ranking',
            'shares', 'downloads'
        ],
        'verbos_fortes': [
            'Produzi', 'Gerenciei', 'Criei', 'Otimizei', 'Planejei',
            'Distribuí', 'Aumentei', 'Posicionei'
        ],
        'ferramentas': [
            'WordPress', 'HubSpot', 'SEMrush', 'Google Analytics', 'Canva',
            'Adobe Creative Suite', 'Hootsuite', 'Buffer', 'Trello', 'Ahrefs'
        ]
    },
    
    'Growth Hacker': {
        'keywords': [
            'growth', 'experimentos', 'A/B testing', 'funil', 'aquisição', 'ativação',
            'retenção', 'revenue', 'referral', 'viral loop', 'product-led growth',
            'metrics', 'analytics', 'conversion', 'pirate metrics'
        ],
        'metrics': [
            'crescimento (%)', 'CAC reduzido (%/R$)', 'LTV aumentado (R$/US$)',
            'conversion rate (%)', 'retention rate (%)', 'viral coefficient',
            'experiments rodados', 'winners identificados', 'uplift (%)'
        ],
        'verbos_fortes': [
            'Escalei', 'Experimentei', 'Otimizei', 'Aumentei', 'Desbloqueei',
            'Ativei', 'Converti', 'Alavancuei'
        ],
        'ferramentas': [
            'Amplitude', 'Mixpanel', 'Google Analytics', 'Optimizely', 'VWO',
            'Hotjar', 'SQL', 'Python', 'Segment', 'Heap', 'Looker'
        ]
    },
    
    'Cybersecurity Analyst': {
        'keywords': [
            'segurança da informação', 'vulnerabilidades', 'penetration testing', 'SIEM',
            'firewall', 'IDS/IPS', 'incident response', 'compliance', 'ISO 27001',
            'threat intelligence', 'SOC', 'forensics', 'security audit', 'risk assessment'
        ],
        'metrics': [
            'vulnerabilidades corrigidas', 'incidentes respondidos', 'tempo de resposta (horas)',
            'ataques mitigados', 'compliance score (%)', 'security score', 'patches aplicados',
            'scans realizados', 'risco reduzido (%)'
        ],
        'verbos_fortes': [
            'Protegi', 'Identifiquei', 'Mitigando', 'Implementei', 'Respondi',
            'Auditei', 'Configurei', 'Remediando'
        ],
        'ferramentas': [
            'Splunk', 'QRadar', 'Fortinet', 'Palo Alto', 'CrowdStrike', 'Nessus',
            'Burp Suite', 'Metasploit', 'Wireshark', 'Snort', 'OSSEC'
        ]
    },
    
    'Cloud Architect': {
        'keywords': [
            'arquitetura cloud', 'AWS', 'Azure', 'GCP', 'multi-cloud', 'hybrid cloud',
            'serverless', 'IaC', 'escalabilidade', 'resiliência', 'custo', 'segurança',
            'migração cloud', 'cloud native', 'well-architected'
        ],
        'metrics': [
            'custo cloud reduzido (R$/%)', 'disponibilidade (%)', 'latência (ms)',
            'recursos provisionados', 'economia (R$/US$)', 'workloads migrados',
            'arquiteturas desenhadas', 'SLA atingido (%)'
        ],
        'verbos_fortes': [
            'Arquitetei', 'Migrei', 'Otimizei', 'Implementei', 'Desenhei',
            'Automatizei', 'Escalei', 'Configurei'
        ],
        'ferramentas': [
            'AWS', 'Azure', 'GCP', 'Terraform', 'CloudFormation', 'Kubernetes',
            'Docker', 'Ansible', 'Jenkins', 'Prometheus', 'Grafana'
        ]
    },
    
    'Mobile Developer': {
        'keywords': [
            'iOS', 'Android', 'React Native', 'Flutter', 'mobile development',
            'app store', 'play store', 'push notifications', 'offline mode',
            'performance', 'UI/UX mobile', 'native', 'cross-platform', 'SDK'
        ],
        'metrics': [
            'downloads', 'rating (estrelas)', 'crash-free rate (%)', 'MAU/DAU',
            'session duration (min)', 'retention rate (%)', 'app size (MB)',
            'performance (FPS)', 'features lançadas'
        ],
        'verbos_fortes': [
            'Desenvolvi', 'Implementei', 'Otimizei', 'Publiquei', 'Refatorei',
            'Integrei', 'Corrigi', 'Escalei'
        ],
        'ferramentas': [
            'Swift', 'Kotlin', 'React Native', 'Flutter', 'Xcode', 'Android Studio',
            'Firebase', 'TestFlight', 'Fastlane', 'Git', 'Jira'
        ]
    },
    
    'Backend Developer': {
        'keywords': [
            'API REST', 'GraphQL', 'microserviços', 'database', 'SQL', 'NoSQL',
            'arquitetura', 'escalabilidade', 'performance', 'security', 'cache',
            'message queue', 'authentication', 'server-side', 'cloud'
        ],
        'metrics': [
            'tempo de resposta (ms)', 'throughput (req/s)', 'uptime (%)',
            'APIs desenvolvidas', 'endpoints criados', 'bugs corrigidos',
            'cobertura de testes (%)', 'database queries otimizadas'
        ],
        'verbos_fortes': [
            'Desenvolvi', 'Implementei', 'Arquitetei', 'Otimizei', 'Escalei',
            'Integrei', 'Refatorei', 'Automatizei'
        ],
        'ferramentas': [
            'Node.js', 'Python', 'Java', 'Go', 'PostgreSQL', 'MongoDB', 'Redis',
            'Docker', 'Kubernetes', 'AWS', 'Kafka', 'RabbitMQ', 'Git'
        ]
    },
    
    'Frontend Developer': {
        'keywords': [
            'HTML', 'CSS', 'JavaScript', 'React', 'Vue', 'Angular', 'TypeScript',
            'responsivo', 'UI', 'componentes', 'performance', 'acessibilidade',
            'SPA', 'webpack', 'styled-components', 'state management'
        ],
        'metrics': [
            'lighthouse score', 'page load time (ms)', 'FCP (ms)', 'LCP (ms)',
            'componentes criados', 'páginas desenvolvidas', 'browser compatibility (%)',
            'bundle size (KB)', 'accessibility score (%)'
        ],
        'verbos_fortes': [
            'Desenvolvi', 'Implementei', 'Otimizei', 'Criei', 'Refatorei',
            'Integrei', 'Desenhei', 'Configurei'
        ],
        'ferramentas': [
            'React', 'Vue', 'Angular', 'TypeScript', 'JavaScript', 'Sass', 'Webpack',
            'Vite', 'Figma', 'Git', 'Chrome DevTools', 'Storybook'
        ]
    }
}


def detectar_area_por_cargo(cargo: str) -> str:
    """
    Detecta área profissional baseada no cargo usando matching de keywords.
    
    Args:
        cargo: String com o cargo-alvo (ex: "Gerente de Vendas")
        
    Returns:
        str: Nome da área profissional identificada, ou 'Generalista' se não encontrar
    """
    if not cargo:
        return 'Generalista'
    
    cargo_lower = cargo.lower()
    
    # Mapeamento direto de palavras-chave no cargo para áreas
    mapeamento_direto = {
        'software': 'Software Engineer',
        'desenvolvedor': 'Software Engineer',
        'developer': 'Software Engineer',
        'programador': 'Software Engineer',
        'data scientist': 'Data Scientist',
        'cientista de dados': 'Data Scientist',
        'analista de dados': 'Data Scientist',
        'product manager': 'Product Manager',
        'gerente de produto': 'Product Manager',
        'product owner': 'Product Manager',
        'sales': 'Sales Manager',
        'vendas': 'Sales Manager',
        'comercial': 'Sales Manager',
        'marketing': 'Marketing Manager',
        'rh': 'HR Manager',
        'recursos humanos': 'HR Manager',
        'gente e gestão': 'HR Manager',
        'people': 'HR Manager',
        'financial': 'Financial Analyst',
        'financeiro': 'Financial Analyst',
        'finanças': 'Financial Analyst',
        'controller': 'Financial Analyst',
        'supply chain': 'Supply Chain Manager',
        'logística': 'Supply Chain Manager',
        'logistics': 'Supply Chain Manager',
        'legal': 'Legal Operations',
        'jurídico': 'Legal Operations',
        'compliance': 'Legal Operations',
        'devops': 'DevOps Engineer',
        'sre': 'DevOps Engineer',
        'ux': 'UX Designer',
        'designer': 'UX Designer',
        'ui/ux': 'UX Designer',
        'project manager': 'Project Manager',
        'gerente de projetos': 'Project Manager',
        'pmo': 'Project Manager',
        'customer success': 'Customer Success Manager',
        'cs manager': 'Customer Success Manager',
        'sucesso do cliente': 'Customer Success Manager',
        'business analyst': 'Business Analyst',
        'analista de negócios': 'Business Analyst',
        'operations': 'Operations Manager',
        'operações': 'Operations Manager',
        'content': 'Content Manager',
        'conteúdo': 'Content Manager',
        'growth': 'Growth Hacker',
        'cybersecurity': 'Cybersecurity Analyst',
        'segurança': 'Cybersecurity Analyst',
        'infosec': 'Cybersecurity Analyst',
        'cloud architect': 'Cloud Architect',
        'arquiteto': 'Cloud Architect',
        'mobile': 'Mobile Developer',
        'ios': 'Mobile Developer',
        'android': 'Mobile Developer',
        'backend': 'Backend Developer',
        'back-end': 'Backend Developer',
        'frontend': 'Frontend Developer',
        'front-end': 'Frontend Developer',
    }
    
    # Tentar matching direto primeiro
    for keyword, area in mapeamento_direto.items():
        if keyword in cargo_lower:
            return area
    
    # Se não encontrou match direto, retornar generalista
    return 'Generalista'


def obter_conhecimento_mercado(area: str) -> dict:
    """
    Retorna keywords, metrics, verbos fortes e ferramentas para a área.
    
    Args:
        area: Nome da área profissional
        
    Returns:
        dict: Dicionário com conhecimento de mercado da área, ou dados genéricos se não encontrar
    """
    # Retornar conhecimento específico da área
    if area in MARKET_KNOWLEDGE:
        return MARKET_KNOWLEDGE[area]
    
    # Se for 'Generalista' ou área não mapeada, retornar conjunto genérico
    return {
        'keywords': [
            'gestão', 'liderança', 'projeto', 'análise', 'planejamento',
            'implementação', 'desenvolvimento', 'estratégia', 'otimização', 'melhoria'
        ],
        'metrics': [
            'resultado atingido', 'economia (R$)', 'eficiência (%)',
            'prazo cumprido', 'qualidade', 'produtividade (%)'
        ],
        'verbos_fortes': [
            'Gerenciei', 'Implementei', 'Desenvolvi', 'Coordenei', 'Otimizei',
            'Analisei', 'Estruturei', 'Planejei'
        ],
        'ferramentas': [
            'Excel', 'PowerPoint', 'Word', 'Outlook', 'Teams', 'Slack'
        ]
    }

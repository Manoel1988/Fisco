# 📚 Guia de Uso - Página de Legislações

## Visão Geral

A nova funcionalidade de **Legislações Tributárias** permite consultar, filtrar e categorizar toda a base legal do sistema Fisco de forma organizada e intuitiva.

## Funcionalidades Principais

### 🔍 **Filtros Avançados**
- **Busca por texto**: Busque por título, ementa, palavras-chave ou número
- **Filtro por Esfera**: Federal, Estadual, Municipal
- **Filtro por Tipo**: Lei, Decreto, Instrução Normativa, etc.
- **Filtro por Área**: Tributário, Fiscal, Trabalhista, etc.
- **Filtro por Órgão**: Receita Federal, Congresso Nacional, etc.
- **Filtro por Relevância**: Essencial, Crítica, Alta, Média, Baixa
- **Ordenação**: Data, relevância, título (A-Z ou Z-A)

### 📊 **Estatísticas em Tempo Real**
- Contador total de legislações
- Distribuição por esfera (Federal, Estadual, Municipal)
- Estatísticas por categoria
- Indicadores visuais com cores distintas

### 🎯 **Categorização Visual**
- **Badges coloridos** para identificar rapidamente:
  - 🔵 **Federal**: Azul
  - 🟢 **Estadual**: Verde
  - 🟡 **Municipal**: Amarelo
  - ⭐ **Relevância**: Cores de acordo com a importância

### 📄 **Visualização Detalhada**
- **Página de detalhes** para cada legislação
- **Texto completo** quando disponível
- **Legislações relacionadas** e similares
- **Palavras-chave** organizadas
- **Links para texto oficial**
- **Filtros rápidos** por categoria

## Como Usar

### 1. **Acesso à Página**
- Na página inicial, clique no botão **"📚 Consultar Legislações"**
- Ou acesse diretamente: `http://localhost:8000/legislacoes/`

### 2. **Aplicar Filtros**
- Use a **barra lateral esquerda** para aplicar filtros
- Os filtros são aplicados automaticamente ao selecionar
- Use o campo de **busca** para encontrar legislações específicas

### 3. **Explorar Resultados**
- **Cards informativos** mostram resumo de cada legislação
- **Badges coloridos** indicam esfera e relevância
- **Paginação** para navegar entre resultados
- **Links diretos** para texto oficial

### 4. **Ver Detalhes**
- Clique em **"Ver Detalhes"** para informações completas
- Explore **legislações relacionadas** e similares
- Use **filtros rápidos** para encontrar legislações similares

## Exemplos de Uso

### 🔍 **Buscar ICMS**
1. Digite "ICMS" no campo de busca
2. Filtre por "Esfera: Estadual"
3. Ordene por "Relevância (Maior)"

### 📊 **Legislações Municipais**
1. Selecione "Esfera: Municipal"
2. Filtre por "Área: Tributário"
3. Veja estatísticas atualizadas

### ⭐ **Legislações Essenciais**
1. Selecione "Relevância: Essencial"
2. Ordene por "Data (Mais Recente)"
3. Explore as mais importantes

## Estrutura dos Dados

### **Campos Principais**
- **Título**: Nome completo da legislação
- **Número/Ano**: Identificação oficial
- **Tipo**: Lei, Decreto, Instrução Normativa, etc.
- **Esfera**: Federal, Estadual, Municipal
- **Órgão**: Emissor da legislação
- **Área**: Tributário, Fiscal, etc.
- **Relevância**: 1-5 (Baixa a Essencial)

### **Conteúdo**
- **Ementa**: Resumo oficial
- **Resumo Executivo**: Explicação detalhada
- **Texto Completo**: Conteúdo integral
- **Palavras-chave**: Tags para busca
- **URL Oficial**: Link para fonte oficial

## Benefícios

### 🎯 **Para Auditores**
- Acesso rápido à base legal
- Filtros específicos por área de interesse
- Identificação de oportunidades de recuperação fiscal

### 📈 **Para Gestores**
- Visão geral do arcabouço legal
- Estatísticas de cobertura por esfera
- Priorização por relevância

### 🔍 **Para Pesquisadores**
- Busca avançada por texto
- Legislações relacionadas
- Navegação intuitiva

## Tecnologia

### **Frontend**
- **Bootstrap 5**: Interface responsiva
- **Font Awesome**: Ícones profissionais
- **JavaScript**: Filtros automáticos
- **CSS customizado**: Identidade visual

### **Backend**
- **Django Views**: Lógica de filtros
- **Paginação**: Performance otimizada
- **Queries otimizadas**: Busca eficiente
- **Estatísticas em tempo real**: Contadores dinâmicos

## Próximos Passos

### 🚀 **Funcionalidades Futuras**
- **Favoritos**: Marcar legislações importantes
- **Histórico**: Consultas recentes
- **Exportação**: PDF, Excel, etc.
- **Alertas**: Notificações de atualizações
- **API**: Integração com outros sistemas

### 📊 **Melhorias Planejadas**
- **Gráficos**: Visualização de estatísticas
- **Comparação**: Lado a lado de legislações
- **Anotações**: Comentários pessoais
- **Compartilhamento**: Links diretos

## Suporte

Para dúvidas ou sugestões sobre a funcionalidade de legislações:
- Acesse o painel administrativo Django
- Consulte a documentação técnica
- Entre em contato com a equipe de desenvolvimento

---

**Sistema Fisco** - Auditoria Fiscal Inteligente
*Versão com Legislações Categorizadas* 
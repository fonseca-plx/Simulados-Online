# Template de Criação de Simulados

## Funcionalidades Implementadas

### 1. Formulário Principal
- **Campo Tema**: Validação em tempo real (5-30 caracteres)
- **Seleção de Questões**: Interface visual com cards interativos
- **Definição de Pesos**: Inputs numéricos para cada questão selecionada (1-10)
- **Contador Dinâmico**: Mostra quantas questões foram selecionadas
- **Progress Bar**: Indica progresso até o mínimo de 10 questões

### 2. Validações Cliente (JavaScript)
- Mínimo de 10 questões obrigatório
- Pesos entre 1 e 10 para todas as questões selecionadas
- Tema com tamanho correto
- Feedback visual em tempo real

### 3. Validações Servidor (Django)
- Implementadas na função `criar_simulado` do service
- Validação de existência das questões
- Validação de pesos fornecidos
- Uso de transações para consistência

### 4. Interface do Usuário
- **Design Responsivo**: Funciona em desktop e mobile
- **Cards Interativos**: Visual muda quando questão é selecionada
- **Botão de Criação de Questões**: Link direto para cadastro de novas questões
- **Status Visual**: Mostra quando está pronto para criar o simulado
- **Acessibilidade**: Navegação por teclado e foco visível

### 5. Integração com a View
- **GET**: Carrega questões disponíveis e renderiza o formulário
- **POST**: Processa dados e chama o service para criar o simulado
- **Tratamento de Erros**: Exibe mensagens de validação
- **Redirecionamento**: Vai para página de detalhes do simulado criado

## Como Funciona

1. **Carregamento**: A view busca todas as questões disponíveis e passa para o template
2. **Seleção**: Usuário seleciona questões clicando nos checkboxes
3. **Pesos**: Quando uma questão é selecionada, o input de peso é habilitado
4. **Validação**: JavaScript valida em tempo real se requisitos foram atendidos
5. **Submit**: Formulário envia dados para a view que chama o service
6. **Criação**: Service valida e cria o simulado com as questões e pesos
7. **Resultado**: Usuário é redirecionado para ver o simulado criado

## Estrutura de Dados Enviada

```python
POST = {
    'tema': 'Nome do Simulado',
    'questoes': ['1', '2', '3', ...],  # IDs das questões selecionadas
    'peso_questao_1': '5',             # Peso da questão ID 1
    'peso_questao_2': '8',             # Peso da questão ID 2
    'peso_questao_3': '3',             # Peso da questão ID 3
    # ... etc
}
```

## Arquivos Relacionados
- **Template**: `simulado/templates/simulado/sim/form.html`
- **JavaScript**: `simulado/static/js/criar_simulado.js`
- **CSS**: `simulado/static/css/criar_simulado.css`
- **View**: `simulado/views/simulados.py` - `CriarSimuladoView`
- **Service**: `simulado/services/casousosimulado.py` - `criar_simulado`

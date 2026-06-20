/* ==================== VARIÁVEIS GLOBAIS ==================== */
let activityChart = null;
let intentChart = null;
let messageCount = 0;

/* ==================== INICIALIZAÇÃO ==================== */
document.addEventListener('DOMContentLoaded', function() {
    initializeMenuListeners();
    loadDashboardData();
    initializeCharts();
    setInterval(refreshDashboard, 5000); // Atualiza a cada 5 segundos
});

/* ==================== MENU NAVIGATION ==================== */
function initializeMenuListeners() {
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active de todos
            menuItems.forEach(m => m.classList.remove('active'));
            document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
            
            // Adiciona active ao clicado
            this.classList.add('active');
            const sectionName = this.getAttribute('data-section');
            document.getElementById(sectionName).classList.add('active');
            
            // Atualiza título
            const titles = {
                'dashboard': 'Dashboard',
                'chat': 'Chat com JARVIS',
                'tasks': 'Gerenciador de Tarefas',
                'apis': 'APIs Disponíveis',
                'memory': 'Sistema de Memória'
            };
            document.getElementById('section-title').textContent = titles[sectionName];
            
            // Carrega dados específicos
            if (sectionName === 'tasks') loadTasks();
            if (sectionName === 'apis') loadApis();
            if (sectionName === 'memory') loadMemory();
        });
    });
}

/* ==================== DASHBOARD ==================== */
async function loadDashboardData() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        document.getElementById('status-name').textContent = data.name || 'JARVIS';
        document.getElementById('status-version').textContent = data.version || '1.0.0';
        document.getElementById('status-conversations').textContent = data.conversation_count || 0;
        document.getElementById('status-memory').textContent = (data.memory_interactions || 0) + ' interações';
        
        // Atualiza estatísticas
        document.getElementById('stat-tasks').textContent = '4'; // Backup, Report, Cleanup, Monitor
        document.getElementById('stat-apis').textContent = '3'; // Weather, News, GitHub
        document.getElementById('stat-patterns').textContent = '0';
        
    } catch (error) {
        console.error('Erro ao carregar status:', error);
    }
}

/* ==================== CHAT ==================== */
async function sendMessage(event) {
    event.preventDefault();
    
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Adiciona mensagem do usuário
    addMessage(message, 'user-message');
    input.value = '';
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessage(data.jarvis_response, 'jarvis-message');
        } else {
            addMessage('Erro: ' + (data.error || 'Erro desconhecido'), 'jarvis-message');
        }
    } catch (error) {
        console.error('Erro ao enviar mensagem:', error);
        addMessage('Erro de conexão com o servidor', 'jarvis-message');
    }
}

function addMessage(text, className) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll para o final
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    messageCount++;
}

/* ==================== TAREFAS ==================== */
async function loadTasks() {
    try {
        const response = await fetch('/api/tasks');
        const data = await response.json();
        
        const tasksList = document.getElementById('available-tasks');
        tasksList.innerHTML = '';
        
        if (data.available_tasks && Array.isArray(data.available_tasks)) {
            data.available_tasks.forEach(task => {
                const taskEl = document.createElement('div');
                taskEl.className = 'task-item';
                taskEl.innerHTML = `
                    <div>
                        <div class="task-item-name">📌 ${capitalize(task)}</div>
                        <div class="task-item-desc">Tarefa: ${task}</div>
                    </div>
                    <button class="btn-task" onclick="executeTask('${task}')">Executar</button>
                `;
                tasksList.appendChild(taskEl);
            });
        }
        
        // Histórico de execução
        const historyList = document.getElementById('execution-history');
        historyList.innerHTML = '';
        
        if (data.execution_history && Array.isArray(data.execution_history)) {
            data.execution_history.slice(-5).forEach(execution => {
                const historyEl = document.createElement('div');
                historyEl.className = 'execution-item';
                historyEl.innerHTML = `
                    <div class="execution-item-title">✅ ${capitalize(execution.task)}</div>
                    <div class="execution-item-time">${new Date(execution.timestamp).toLocaleString('pt-BR')}</div>
                `;
                historyList.appendChild(historyEl);
            });
        }
        
    } catch (error) {
        console.error('Erro ao carregar tarefas:', error);
    }
}

async function executeTask(taskName) {
    try {
        const response = await fetch('/api/tasks/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ task_name: taskName })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(`✅ Tarefa '${taskName}' enfileirada para execução!`);
            loadTasks();
            loadDashboardData();
        } else {
            alert(`❌ Erro: ${data.error}`);
        }
    } catch (error) {
        console.error('Erro ao executar tarefa:', error);
        alert('Erro ao executar tarefa');
    }
}

/* ==================== APIs ==================== */
async function loadApis() {
    try {
        const response = await fetch('/api/apis');
        const data = await response.json();
        
        const apisList = document.getElementById('available-apis');
        apisList.innerHTML = '';
        
        if (data.available_apis && Array.isArray(data.available_apis)) {
            data.available_apis.forEach(api => {
                const apiEl = document.createElement('div');
                apiEl.className = 'api-item';
                apiEl.innerHTML = `
                    <div>
                        <div class="task-item-name">🔌 ${capitalize(api)}</div>
                        <div class="task-item-desc">Endpoint: /api/${api}</div>
                    </div>
                `;
                apisList.appendChild(apiEl);
            });
        }
        
    } catch (error) {
        console.error('Erro ao carregar APIs:', error);
    }
}

/* ==================== MEMÓRIA ==================== */
async function loadMemory() {
    try {
        const response = await fetch('/api/memory');
        const data = await response.json();
        
        // Interações recentes
        const interactionsList = document.getElementById('recent-interactions');
        interactionsList.innerHTML = '';
        
        if (data.recent_interactions && Array.isArray(data.recent_interactions)) {
            data.recent_interactions.slice(-5).forEach(interaction => {
                const interactionEl = document.createElement('div');
                interactionEl.className = 'interaction-item';
                interactionEl.innerHTML = `
                    <div class="task-item-name">💭 ${interaction.intent || 'unknown'}</div>
                    <div class="task-item-desc">"${interaction.user_input.substring(0, 50)}..."</div>
                `;
                interactionsList.appendChild(interactionEl);
            });
        }
        
        // Padrões aprendidos
        const patternsList = document.getElementById('learned-patterns');
        patternsList.innerHTML = '';
        
        if (data.learned_patterns && Array.isArray(data.learned_patterns)) {
            if (data.learned_patterns.length === 0) {
                patternsList.innerHTML = '<div class="pattern-item">Nenhum padrão aprendido ainda</div>';
            } else {
                data.learned_patterns.forEach(pattern => {
                    const patternEl = document.createElement('div');
                    patternEl.className = 'pattern-item';
                    patternEl.innerHTML = `
                        <div class="task-item-name">🎓 ${pattern.name}</div>
                        <div class="task-item-desc">${pattern.description}</div>
                    `;
                    patternsList.appendChild(patternEl);
                });
            }
        }
        
    } catch (error) {
        console.error('Erro ao carregar memória:', error);
    }
}

/* ==================== GRÁFICOS ==================== */
function initializeCharts() {
    // Gráfico de Atividade
    const activityCtx = document.getElementById('activityChart');
    if (activityCtx) {
        activityChart = new Chart(activityCtx, {
            type: 'line',
            data: {
                labels: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom'],
                datasets: [{
                    label: 'Mensagens',
                    data: [12, 19, 3, 5, 2, 3, 8],
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#6366f1',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 20
                    }
                }
            }
        });
    }
    
    // Gráfico de Intenções
    const intentCtx = document.getElementById('intentChart');
    if (intentCtx) {
        intentChart = new Chart(intentCtx, {
            type: 'doughnut',
            data: {
                labels: ['Tarefas', 'Saudações', 'APIs', 'Aprendizado', 'Outros'],
                datasets: [{
                    data: [35, 25, 20, 15, 5],
                    backgroundColor: [
                        '#6366f1',
                        '#ec4899',
                        '#10b981',
                        '#f59e0b',
                        '#ef4444'
                    ],
                    borderColor: '#fff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
}

/* ==================== ATUALIZAÇÃO AUTOMÁTICA ==================== */
function refreshDashboard() {
    loadDashboardData();
}

/* ==================== UTILITÁRIOS ==================== */
function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

/* ==================== EVENTOS DE TECLADO ==================== */
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + K para focar no chat
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        document.getElementById('chat-input').focus();
    }
});

/* ==================== MENU MOBILE (FUTURO) ==================== */
function toggleSidebarMobile() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('active');
}

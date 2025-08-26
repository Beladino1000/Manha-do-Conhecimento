// Função para obter o valor atual do localStorage
function getCurrentValue() {
    const storedValue = localStorage.getItem(parse'contadorValor');
    return storedValue ? parseInt(storedValue) : 0;
}

// Função para atualizar o valor exibido e salvar no localStorage
function updateDisplay(value) {
    document.getElementById('valor').textContent = value;
    localStorage.setItem('contadorValor', value);
}

// Função para adicionar 1
function add1() {
    const currentValue = getCurrentValue();
    updateDisplay(currentValue + 1);
}

// Função para subtrair 1
function subtract1() {
    const currentValue = getCurrentValue();
    updateDisplay(currentValue - 1);
}

// Função para resetar o contador
function reset() {
    updateDisplay(0);
}

// Função para adicionar valor personalizado
function addcv() {
    const input = document.getElementById('customInput');
    const value = parseInt(input.value) || 0;
    const currentValue = getCurrentValue();
    updateDisplay(currentValue + value);
    input.value = ''; // Limpa o campo após a operação
}

// Função para subtrair valor personalizado
function subtractcv() {
    const input = document.getElementById('customInput');
    const value = parseInt(input.value) || 0;
    const currentValue = getCurrentValue();
    updateDisplay(currentValue - value);
    input.value = ''; // Limpa o campo após a operação
}

// Inicializa o contador com o valor salvo quando a página carrega
document.addEventListener('DOMContentLoaded', function() {
    const initialValue = getCurrentValue();
    updateDisplay(initialValue);
});
//Função para lipar o localStorage
function resetar() {
    localStorage.clear(); // Limpa o localStorage

}




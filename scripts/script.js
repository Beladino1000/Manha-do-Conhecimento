document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const valorElement = document.getElementById('valor');
    const incrementButton = document.getElementById('increment');
    const decrementButton = document.getElementById('decrement');
    const resetButton = document.getElementById('reset');
    const addCustomButton = document.getElementById('addCustom');
    const subtractCustomButton = document.getElementById('subtractCustom');
    const customInput = document.getElementById('customInput');

    // Recuperar valor do localStorage ou iniciar com 0
    let count = localStorage.getItem('contador') ? parseInt(localStorage.getItem('contador')) : 0;
    valorElement.textContent = count;

    // Função para atualizar o contador e salvar no localStorage
    function updateCount(value) {
        count = value;
        valorElement.textContent = count;
        localStorage.setItem('contador', count);
    }

    // Event Listeners
    incrementButton.addEventListener('click', function() {
        updateCount(count + 1);
    });

    decrementButton.addEventListener('click', function() {
        updateCount(count - 1);
    });

    resetButton.addEventListener('click', function() {
        updateCount(0);
    });

    addCustomButton.addEventListener('click', function() {
        const customValue = parseInt(customInput.value);
        if (!isNaN(customValue)) {
            updateCount(count + customValue);
        }
        customInput.value = '';
    });

    subtractCustomButton.addEventListener('click', function() {
        const customValue = parseInt(customInput.value);
        if (!isNaN(customValue)) {
            updateCount(count - customValue);
        }
        customInput.value = '';
    });
});
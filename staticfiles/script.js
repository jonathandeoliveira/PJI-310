// Tamanho de fonte padrão
let defaultFontSize = 16;

// Função para ajustar o tamanho da fonte
function adjustFontSize(change) {
  const body = document.body;
  const currentSize = parseFloat(window.getComputedStyle(body).fontSize);
  body.style.fontSize = `${currentSize + change}px`;
}

// Função para resetar o tamanho da fonte para o padrão
function resetFontSize() {
  document.body.style.fontSize = `${defaultFontSize}px`;
}

// Script para aplicar clases CSS de Tailwind a los formularios de Django
document.addEventListener('DOMContentLoaded', function() {
  // Aplicar clase a todos los inputs
  const inputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"], input[type="number"], textarea, select');
  inputs.forEach(input => {
    input.classList.add('form-input');
  });

  // Establecer atributos requeridos donde sea necesario
  const requiredInputs = document.querySelectorAll('[required]');
  requiredInputs.forEach(input => {
    if (input.id) {
      const label = document.querySelector(`label[for="${input.id}"]`);
      if (label && !label.querySelector('.required-asterisk')) {
        const asterisk = document.createElement('span');
        asterisk.className = 'required-asterisk text-red-500 ml-1';
        asterisk.textContent = '*';
        label.appendChild(asterisk);
      }
    }
  });
});

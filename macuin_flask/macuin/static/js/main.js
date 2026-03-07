// ─── Toggle contraseña ────────────────────────────────────
function togglePassword(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  const isPass = input.type === 'password';
  input.type = isPass ? 'text' : 'password';
  btn.style.opacity = isPass ? '1' : '0.4';
}

// ─── Precio range live update ─────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const range = document.querySelector('input[name="precio_max"]');
  const label = document.getElementById('max-val');
  if (range && label) {
    range.addEventListener('input', () => {
      label.textContent = '$' + Number(range.value).toLocaleString();
    });
  }
});

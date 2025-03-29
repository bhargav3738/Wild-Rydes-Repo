document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.querySelector(".register-form");
  const registerButton = document.querySelector(".register-button");

  registerForm.addEventListener("submit", (e) => {
    e.preventDefault();
    registerButton.textContent = "Registering...";
    registerButton.disabled = true;

    // Simulate API call
    setTimeout(() => {
      registerForm.submit();
    }, 1000);
  });

  // Add smooth hover effect to form inputs
  const inputs = document.querySelectorAll(
    'input[type="text"], input[type="email"], input[type="password"]'
  );
  inputs.forEach((input) => {
    input.addEventListener("focus", () => {
      input.style.transform = "scale(1.02)";
    });
    input.addEventListener("blur", () => {
      input.style.transform = "scale(1)";
    });
  });

  // Password strength indicator
  const passwordInput = document.querySelector('input[name="password1"]');
  const strengthIndicator = document.createElement("div");
  strengthIndicator.className = "password-strength";
  passwordInput.parentNode.insertBefore(
    strengthIndicator,
    passwordInput.nextSibling
  );

  passwordInput.addEventListener("input", () => {
    const strength = calculatePasswordStrength(passwordInput.value);
    updateStrengthIndicator(strength);
  });

  function calculatePasswordStrength(password) {
    // This is a simple example. In a real-world scenario, you'd want a more robust check.
    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength++;
    if (password.match(/\d/)) strength++;
    if (password.match(/[^a-zA-Z\d]/)) strength++;
    return strength;
  }

  function updateStrengthIndicator(strength) {
    const colors = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71"];
    const labels = ["Weak", "Fair", "Good", "Strong"];
    strengthIndicator.style.backgroundColor = colors[strength];
    strengthIndicator.textContent = labels[strength];
  }
});

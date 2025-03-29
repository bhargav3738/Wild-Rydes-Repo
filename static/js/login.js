document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.querySelector(".login-form");
  const loginButton = document.querySelector(".login-button");

  loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    loginButton.textContent = "Logging in...";
    loginButton.disabled = true;

    // Simulate API call
    setTimeout(() => {
      loginForm.submit();
    }, 1000);
  });

  // Add smooth hover effect to form inputs
  const inputs = document.querySelectorAll(
    'input[type="text"], input[type="password"]'
  );
  inputs.forEach((input) => {
    input.addEventListener("focus", () => {
      input.style.transform = "scale(1.02)";
    });
    input.addEventListener("blur", () => {
      input.style.transform = "scale(1)";
    });
  });
});

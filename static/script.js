document.addEventListener("DOMContentLoaded", () => {
 
  const textRadio = document.getElementById("textRadio");
  const fileRadio = document.getElementById("fileRadio");
  const textInputArea = document.getElementById("textInputArea");
  const fileInputArea = document.getElementById("fileInputArea");

  if (textRadio && fileRadio && textInputArea && fileInputArea) {
    function toggleInput() {
      if (textRadio.checked) {
        textInputArea.classList.remove("hidden");
        fileInputArea.classList.add("hidden");
      } else {
        fileInputArea.classList.remove("hidden");
        textInputArea.classList.add("hidden");
      }
    }

    textRadio.addEventListener("change", toggleInput);
    fileRadio.addEventListener("change", toggleInput);
    toggleInput(); 
  }

  
  const tabButtons = document.querySelectorAll(".tab-button");
  const tabContents = document.querySelectorAll(".tab-content");

  tabButtons.forEach(button => {
    button.addEventListener("click", () => {
      const tabId = button.getAttribute("data-tab");

      tabButtons.forEach(btn => btn.classList.remove("active"));
      tabContents.forEach(tab => tab.classList.remove("active"));

      document.getElementById(tabId).classList.add("active");
      button.classList.add("active");
    });
  });
});
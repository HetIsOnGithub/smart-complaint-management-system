document.addEventListener("DOMContentLoaded", () => {
  const alerts = document.querySelectorAll(".alert");

  alerts.forEach((alert) => {
    setTimeout(() => {
      if (bootstrap.Alert.getOrCreateInstance) {
        bootstrap.Alert.getOrCreateInstance(alert).close();
      }
    }, 4000);
  });

  const imageInput = document.querySelector('input[type="file"]');

  if (imageInput) {
    imageInput.addEventListener("change", function () {
      const file = this.files[0];

      if (!file) {
        return;
      }

      let preview = document.getElementById("image-preview");

      if (!preview) {
        preview = document.createElement("img");
        preview.id = "image-preview";
        preview.className = "img-fluid rounded border mt-3";
        this.parentNode.appendChild(preview);
      }

      const reader = new FileReader();

      reader.onload = function (event) {
        preview.src = event.target.result;
      };

      reader.readAsDataURL(file);
    });
  }
});

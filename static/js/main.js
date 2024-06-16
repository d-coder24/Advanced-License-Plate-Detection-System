function updateFileName(input) {
  const fileName = input.files[0].name;
  document.getElementById("file-name").textContent = fileName;
}

document.getElementById("upload-form").onsubmit = async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const response = await fetch("/process", {
    method: "POST",
    body: formData,
  });
  const result = await response.json();
  document.getElementById("recognized_text").textContent = result.result;
  document.getElementById("output_image").src = result.image_url;
};

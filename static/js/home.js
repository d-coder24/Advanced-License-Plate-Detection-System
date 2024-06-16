document.getElementById("search-button").addEventListener("click", function () {
  const query = document.getElementById("google-search").value;
  window.location.href = `https://www.google.com/search?q=${query}`;
});

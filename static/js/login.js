document
  .getElementById("login-form")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the form from submitting

    // Get the username and password
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // Check if the password is at least 8 characters long
    if (password.length < 8) {
      alert("Password must be at least 8 characters long.");
      return;
    }

    // // Check if the password is alphanumeric and contains special symbols
    // var passwordRegex = /^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[\W_]).+$/;
    // if (!passwordRegex.test(password)) {
    //   alert("Password must be alphanumeric and contain at least one special symbol.");
    //   return;
    // }

    // Check if the username and password are correct
    if (username === "darshan24" && password === "Darshan@123") {
      // Redirect to a dashboard or home page
      window.open("/main", "_self");
    } else {
      // Display an error message
      alert("Invalid username or password. Please try again.");
    }
  });

// Add keydown event listener to the username input field
document
  .getElementById("username")
  .addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      document.getElementById("password").focus();
    }
  });

const btn = document.getElementById("customer_button");

customer_button.addEventListener("click", (e) => {
    e.preventDefault()
  const form = document.getElementById("form");

  if (form.style.visibility === "hidden") {
    form.style.visibility = "visible";
  } else {
    form.style.visibility = "hidden";
  }
});

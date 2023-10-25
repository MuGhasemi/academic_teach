const inputValue = document.querySelector("#priceToUp");
const toShow = document.querySelector("#priceUp");
const nowCredit = document.querySelector("#nowCredit");
const priceAfterUp = document.querySelector("#priceAfterUp");

inputValue.addEventListener("input", (e) => {
  toShow.innerText = e.target.value;
  priceAfterUp.innerText = +e.target.value + +nowCredit.innerText;
});

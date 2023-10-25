const navProfile = document.querySelector(".nav__profile");
const profileDropdown = document.querySelector(".profile__drop-down");

navProfile.addEventListener("mouseenter", () => {
  profileDropdown.style.display = "block";
});
navProfile.addEventListener("mouseleave", () => {
  profileDropdown.style.display = "none";
});
profileDropdown.addEventListener("mouseenter", () => {
  profileDropdown.style.display = "block";
});
profileDropdown.addEventListener("mouseleave", () => {
  profileDropdown.style.display = "none";
});
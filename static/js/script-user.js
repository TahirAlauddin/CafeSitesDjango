const color_panel = document.querySelector(".color-panel");
let color_selector = document.getElementById("color-selector");
const delete_btn = document.getElementById("delete");
const tables = document.querySelectorAll(".element");
let available_color;
HideColors();
container.addEventListener("dblclick", function (e) {
  if (e.target.classList.contains("element")) {
    
    if (e.target == current_selected) {
      RemoveBorder();
      HideColors();
      color_selector.style.display = "none";
      current_selected = null;
    } else {
      current_selected = e.target;
      color_selector.style.display = "flex";
      RemoveBorder();
      ShowColors();
      color_panel.addEventListener("click", function (color) {

        if (color.target.classList.contains(colors[0])) {
            current_selected.style.backgroundColor = colors[0];
          }
        for (let i=1; i < colors.length; i++) {
          available_color = colors[i];
          if (color.target.classList.contains(available_color)) {
            current_selected.style.backgroundColor = available_color;
          }
        }
      });


      delete_btn.addEventListener('click', (e) => {
        current_selected.classList = "element table_title unselected-color"

      })
      e.target.style.setProperty('border', "2px solid black", "important");
    }
  }
});

//Remove Borders
const RemoveBorder = function () {
  tables.forEach((table) => {
    table.style.border = "none";
  });
};

//Show Color Panel
function ShowColors() {
  color_panel.classList.remove("hidden");
};

// Hide Color Panel
function HideColors() {
  color_panel.classList.add("hidden");
}


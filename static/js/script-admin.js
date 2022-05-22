//Creating Eleemnt at run time
const btn = document.querySelector(".btn");
const savebtn = document.querySelector(".savebtn");
const table_title = document.querySelector(".table_title");
const table_name = document.querySelector("#table_name");
const deleteBtn = document.querySelector("#delete");
const renameBtn = document.querySelector("#rename");
const container = document.querySelector(".container");
let modal = document.getElementById("myModal");
let span = document.getElementsByClassName("close")[0];
let add_title = document.querySelector("#add_title");
let current_selected;

let id
let label = 0;

function createUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
     var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
     return v.toString(16);
  });
}

btn.addEventListener("click", () => {
  id = createUUID();
  label += 1;
  let html = `
        <div class="element table_title unselected-color" id="${id}" name="box${id}" data-index=${id}>T${label}</div>
        `;
  container.insertAdjacentHTML("beforeend", html);
  move();
});
//Moving Effect
let ChooseElement;
const move = function () {
  const elements = document.querySelectorAll(".element");
  elements.forEach((elem) => {
    elem.addEventListener("mousedown", () => {
      elem.style.position = "absolute";
      ChooseElement = elem;

      //adding mousemoeve event to document
      document.onmousemove = (e) => {
        let x = e.pageX;
        let y = e.pageY;
        try {
          ChooseElement.style.left = x - 50 + "px";
          ChooseElement.style.top = y - 50 + "px";
        } catch (error) {
          
        }
      };
    });
  });

  document.onmouseup = (e) => {
    ChooseElement = null;
  };
};
container.addEventListener("dblclick", function (e) {
  if (document.querySelectorAll(".element")) {
    let elements = document.querySelectorAll(".element");
    elements.forEach((elem) => {
      elem.style.border = "none";
    });
  }
  
  if (e.target.classList.contains("element")) {
    console.log(1)
    if (e.target == current_selected) {
      console.log(2)
      e.target.style.border = "none";
      current_selected = null;
    } else if (e.target != current_selected) {
      console.log(3)
      e.target.style.setProperty('border', "2px solid black", "important");
      current_selected = e.target;
    }
  }
});
//Deleting The Table
deleteBtn.addEventListener("click", function () {
  if (current_selected != null) {
    const delelem = current_selected;
    delelem.parentNode.removeChild(delelem);
  }
});

//Renaming The Table
renameBtn.addEventListener("click", function () {
  if (current_selected != null) {
    ShowModal();
    add_title.addEventListener("click", function () {
      let label = table_name.value;
      current_selected.innerText = label;
      HideModal();
    });
  }
});

//Handling Save Button click
let mar_top = [];
let mar_left = [];
let labels = [];
let table_ids = [];


$("#savebtn").click(function () {
  {
    let divs = document.getElementById('container').children;
    Array.from(divs).forEach((div) => {
      mar_top.push(div.offsetTop);
      mar_left.push(div.offsetLeft);
      labels.push(div.innerHTML);
      table_ids.push(div.id);
    });
    //Sending TO Server

    fetch(url, {
      method: "POST",
      headers: {
        "Accept": "application.json",
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({
        table_ids: table_ids,
        array_distance_top: mar_top,
        array_distance_left: mar_left,
        cafe_name: document.getElementById("cafe_name").value,
        array_labels: labels
      }),
      Cache: "default",
    })
      .then((response) => {
        //handle response
        document.getElementById("bgimg-form").submit();
      })
      .then((data) => {
        //handle data
        console.log(data);
      })
      .catch((error) => {
        //handle error
        console.log(error);
      });
  }
});

//Adding Image to background
const image_input = document.querySelector("#bgimg");
image_input.addEventListener("change", function () {
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    const uploaded_image = reader.result;
    document.getElementById('background-image').style.background = `url(${uploaded_image}) no-repeat`;
  });
  reader.readAsDataURL(this.files[0]);
});

// When the user clicks on <span> (x), close the modal
span.onclick = HideModal();
function ShowModal() {
  modal.style.display = "block";
}
function HideModal() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
  if (event.target == modal) {
    HideModal();
  }
};


// responsive navbar
const navbar = document.querySelector(".left__side")
const show = document.querySelector("#show")

show.addEventListener("click", () => {
  navbar.classList.toggle('active')
})
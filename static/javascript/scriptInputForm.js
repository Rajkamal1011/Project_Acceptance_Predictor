var form_1 = document.querySelector(".form_1");
var form_2 = document.querySelector(".form_2");

var form_1_btns = document.querySelector(".form_1_btns");
var form_2_btns = document.querySelector(".form_2_btns");

var form_1_next_btn = document.querySelector(".form_1_btns .btn_next");
var form_2_back_btn = document.querySelector(".form_2_btns .btn_back");

var form_2_progessbar = document.querySelector(".form_2_progessbar");

var btn_submit = document.querySelector(".btn_submit");
var modal_wrapper = document.querySelector(".modal_wrapper");
var shadow = document.querySelector(".shadow");

form_1_next_btn.addEventListener("click", function () {
  form_1.style.display = "none";
  form_2.style.display = "block";

  form_1_btns.style.display = "none";
  form_2_btns.style.display = "flex";

  form_2_progessbar.classList.add("active");
});

form_2_back_btn.addEventListener("click", function () {
  form_1.style.display = "block";
  form_2.style.display = "none";

  form_2_btns.style.display = "none";
  form_1_btns.style.display = "flex";

  form_2_progessbar.classList.remove("active");
});


// SUBMIT Form
btn_submit.addEventListener('click', (event) => {
  event.preventDefault();
  
  document.getElementById("pgcInputId").value = document.getElementById("projectgradeselector").value;
  document.getElementById("tpInputId").value = document.getElementById("teacherprefixselector").value;
  document.getElementById("ssInputId").value = document.getElementById("schoolstateselector").value;

  document.getElementById("essayform1").value = document.getElementById("projectessayWindow").value;
  document.getElementById("inputform1").submit();
  // document.getElementById("inputform2").submit();
})





//  Teacher Prefix Selector CODE
let selectedTP = document.getElementById("teacherprefixselector");
selectedTP.onchange = (event) => {
  var resultTP = document.getElementById("tpInputId");
  resultTP.value = selectedTP.value;
};

//   School State Selector CODE
let selectedSS = document.getElementById("schoolstateselector");
selectedSS.onchange = (event) => {
  var resultSS = document.getElementById("ssInputId");
  resultSS.value = selectedSS.value;
};

//   Project (Clean) Categories CODE
let projCategories = [];

function fetchCCData(arr) {
  document.getElementById("projCategories").innerHTML = "";

  arr.map((projCat) => {
    let projDiv = document.createElement("div");
    projDiv.className = "projCat";

    let node = `<p>${projCat.label}</p>`;

    node += `<div onclick="deleteProjCategories('${projCat.value}')">x</div>`;
    projDiv.innerHTML = node;
    document.getElementById("projCategories").appendChild(projDiv);
  });
}

function selectProjCategories(event) {
  var sleTex = event.options[event.selectedIndex].innerHTML;
  var selVal = event.value;
  if (
    !selVal ||
    projCategories.find((p) => p.value.toString() === selVal.toString())
  ) {
    return console.log("Already selected or empty");
  }

  projCategories.push({
    label: sleTex,
    value: selVal,
  });
  console.log(...projCategories);
  fetchCCData(projCategories);
  fetchSelectedCC(projCategories);
}

fetchCCData(projCategories);

function deleteProjCategories(val) {
  console.log(val);
  console.log(projCategories);
  projCategories = [...projCategories].filter(
    (p) => p.value.toString() !== val.toString()
  );
  fetchCCData(projCategories);
  fetchSelectedCC(projCategories);
}

function fetchSelectedCC(projCategories) {
  let cleanCategories = "";
  for (let i = 0; i < projCategories.length; i++) {
    cleanCategories += projCategories[i].label + " ";
  }
  var resultCC = document.getElementById("ccInputId");
  resultCC.value = cleanCategories;
}

// Project (Clean) Sub Categories CODE
let projSubCategories = [];

function fetchCSCData(arr) {
  document.getElementById("projSubCategories").innerHTML = "";

  arr.map((projSubCat) => {
    let projSubDiv = document.createElement("div");
    projSubDiv.className = "projSubCat";

    let node = `<p>${projSubCat.label}</p>`;

    node += `<div onclick="deleteProjSubCategories('${projSubCat.value}')">x</div>`;
    projSubDiv.innerHTML = node;
    document.getElementById("projSubCategories").appendChild(projSubDiv);
  });
}


function selectProjSubCategories(event) {
  var sleTex = event.options[event.selectedIndex].innerHTML;
  var selVal = event.value;
  if (
    !selVal ||
    projSubCategories.find((p) => p.value.toString() === selVal.toString())
  ) {
    return console.log("Already selected or empty");
  }

  projSubCategories.push({
    label: sleTex,
    value: selVal,
  });
  fetchCSCData(projSubCategories);
  fetchSelectedCSC(projSubCategories);
}

fetchCSCData(projSubCategories);

function deleteProjSubCategories(val) {
  console.log(val);
  console.log(projSubCategories);
  projSubCategories = [...projSubCategories].filter(
    (p) => p.value.toString() !== val.toString()
  );
  fetchCSCData(projSubCategories);
  fetchSelectedCSC(projSubCategories);
}

function fetchSelectedCSC(projSubCategories) {
  let cleanSubCategories = "";
  for (let i = 0; i < projSubCategories.length; i++) {
    cleanSubCategories += projSubCategories[i].label + " ";
  }
  var resultCSC = document.getElementById("cscInputId");
  resultCSC.value = cleanSubCategories;
}

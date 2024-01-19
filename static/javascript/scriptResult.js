let circularProgress1 = document.querySelector(".circular-progress");
let circularProgress2 = document.querySelector(".circular-progress2");
let circularProgress3 = document.querySelector(".circular-progress3");

let progressValue1 = document.querySelector(".progress-value");
let progressValue2 = document.querySelector(".progress-value2");
let progressValue3 = document.querySelector(".progress-value3");



let speed = 75;

let progressStartValue1 = 0;
let progressEndValue1 = document.getElementById("id_result_lr").value;

let progressStartValue2 = 0;
let progressEndValue2 = document.getElementById("id_result_xgb").value;

let progressStartValue3 = 0;  
let progressEndValue3 = document.getElementById("id_result_dl").value;

let progressDoneFlag1 = false;
let progressDoneFlag2 = false;
let progressDoneFlag3 = false;


let progress = setInterval(() => {
  
  if (progressDoneFlag1 == false) {
    progressStartValue1++;
  }
  if (progressDoneFlag2 == false) {
    progressStartValue2++;
  }
  if (progressDoneFlag3 == false) {
    progressStartValue3++;
  }

  progressValue1.textContent = `${progressStartValue1}%`
  progressValue2.textContent = `${progressStartValue2}%`
  progressValue3.textContent = `${progressStartValue3}%`

  circularProgress1.style.background = `conic-gradient(#7d2ae8 ${progressStartValue1 * 3.6}deg, #ededed 0deg)`
  circularProgress2.style.background = `conic-gradient(#7d2ae8 ${progressStartValue2 * 3.6}deg, #ededed 0deg)`
  circularProgress3.style.background = `conic-gradient(#7d2ae8 ${progressStartValue3 * 3.6}deg, #ededed 0deg)`

  if(progressStartValue1 == progressEndValue1){
    progressDoneFlag1 = true;
  }
  if(progressStartValue2 == progressEndValue2){
    progressDoneFlag2 = true;
  }
  if(progressStartValue3 == progressEndValue3){
    progressDoneFlag3 = true;
  }

  if(progressDoneFlag1 && progressDoneFlag2 && progressDoneFlag3){
    clearInterval(progress);
  }
}, speed);

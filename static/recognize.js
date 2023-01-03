// const { Stream } = require("@mui/icons-material")
URL = window.location.href

let canvas = document.querySelector("#canvas")
let connect = canvas.getContext("2d")
let video = document.querySelector('#video')

//if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia){
//    navigator.mediaDevices.getUserMedia({video: true}).then(stream=>{
//        video.srcObject = stream;
//        video.play();
//    })
//}

const camera_button = document.querySelector("#capturecam")
const recognize = document.querySelector("#recognize")
let resp = document.querySelector("#respData")
let name = document.querySelector("#name")
let email = document.querySelector("#email")
let phone = document.querySelector("#phone")
let idproof = document.querySelector("#idproof")


recognize.addEventListener("click", () => {
  sendData()
})

camera_button.addEventListener("click", async function () {
  let stream = await navigator.mediaDevices.getUserMedia({
    video: true,
    audio: false,
  });
  video.srcObject = stream;
  setInterval(showOutput, 100);
});

var showOutput = () => {
  canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
  canvas.ariaHidden = 100;
  // temp latencey fix: please remove it during production :)
  // if (currentCount != prevCount) return
  image_data_url = canvas.toDataURL("image/jpeg");
  // sendMessage()
  // currentCount ++;
}


var sendData = () => {
  data = {
    "image_text": image_data_url.split(",")[1]
  }
  var options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: JSON.stringify(data)
  }
  console.log("otpions: ", options)
  fetch(`/recognize`, options).then((resp) => resp.json()).then((respData) => {
    // alert(`registerd user successfully data: ${respData.status}`)
    console.log("data: ", respData)
    if (respData.found == false) { sendData() }
    else if (respData.found && respData.is_data) {
      // resp.setAttribute("id", "respData") = respData;
      // console.log(respData)
      name.innerHTML = `Name: ${respData.name}`
      email.innerHTML = `Email: ${respData.email}`
      phone.innerHTML = `Phone Number: ${respData.phone_number}`
      idproof.innerHTML = `Govt. ID Number: ${respData.govt_id_number}`
    } else {
      alert(respData)
    }
  })
}
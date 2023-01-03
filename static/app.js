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

const registerButton = document.querySelector("#register")
const fullname = document.querySelector("#name")
const govtID = document.querySelector("#idno")
const email = document.querySelector("#email")
const phone = document.querySelector("#phone")
const camera_button = document.querySelector("#capture")


registerButton.addEventListener("click", () => {
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
    "name": fullname.value,
    "email": email.value,
    "phone_number": phone.value,
    "govt_id_number": govtID.value,
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
  fetch(`/register`, options).then((resp) => resp.json()).then((respData) => {
    alert(`registerd user successfully data: ${respData.status}`)
    console.log("data: ",)
  })
}
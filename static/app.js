// const { Stream } = require("@mui/icons-material")

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


registerButton.addEventListener("click", () => {
    data = {
        "name": fullname.data,
        "email": email.data,
        "phone_number": phone.data,
        "govt_id_number": govtID.data
    }
    console.log(data)
})
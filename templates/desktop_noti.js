function showNotification() {
    const notification = new Notification("Posture Check", {

        icon: "https://www.pngmart.com/image/613344/png/613343",
        body: "FIX YOUR POSTURE!"
        
    })

    notification.oncall = (event) => {
        window.location.href = "FIX YOUR POSTURE" //what you wish to do
    }
}


if(Notification.permission === "granted") { //if granted allow notis

    showNotification();
} else if(Notification.permission !== "denied"){
    Notification.requestPermission().then(permission=>{
        if(permission === "granted") {
            showNotification();
        }
    })
}
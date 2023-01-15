function showNotification() {
    const notification = new Notification("Posture Check", {

        icon: "https://www.pngmart.com/files/22/Mad-Emoji-PNG-Pic.png",
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
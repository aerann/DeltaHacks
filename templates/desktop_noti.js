function showNotification() {
    const notification = new Notification("New Desktop Notification", {
        body: "Frontend stuff"
    })

    notification.onclick = (event) => {
        window.location.href = "youtube.com" //what you wish to do
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
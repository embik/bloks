function hideNotification(element) {
    element.classList.add('hidden');
}

function hideAllNotifications() {
    var notifications = document.querySelectorAll('#notifications>li');
    for (i = 0; i < notifications.length; i++) {
        hideNotification(notifications[i]);
    }
}

(function() {
    var notifications = document.querySelectorAll('#notifications>li');
    for (i = 0; i < notifications.length; i++) {
        notifications[i].onclick = function() { hideNotification(this); };
    }
    setTimeout(hideAllNotifications, 5000);
}());
